from typing import Optional, List, Dict
import logging
import time
import asyncio
import websockets
import json
from dataclasses import asdict
from aiohttp import web
from rpc_gateway import messages, errors
from rpc_gateway.websocket_connection import WebsocketConnection, next_message_id
from rpc_gateway.utils import await_sync

logger = logging.getLogger(__name__)


class GatewayConnection:
    def __init__(self, gateway: 'Gateway', connection: websockets.WebSocketServerProtocol):
        self.gateway = gateway
        self.connection = connection
        self.message_pump = WebsocketConnection(connection, lambda message: gateway.handle_request(self, message))
        self.instances: List[str] = []

    async def start(self):
        await self.message_pump.start()

    async def stop(self):
        await self.message_pump.stop()

    def register_instances(self, instances):
        self.instances = list(set(*self.instances, *instances))


class Gateway:
    SERVER_MESSAGES = (messages.Method.GET, messages.Method.SET, messages.Method.CALL, messages.Method.LOCK,
                       messages.Method.UNLOCK, messages.Method.METADATA)

    def __init__(self, host: str = 'localhost', port: int = 8888, http_port: int = 8887):
        self.host = host
        self.port = port
        self.http_port = http_port
        self.logger = logger.getChild(self.__class__.__name__)
        self.websocket_connections: List[WebsocketConnection] = []
        self.websocket: Optional[websockets.WebSocketServer] = None
        self.event_loop = asyncio.get_event_loop()
        self.instances: Dict[str, WebsocketConnection] = {}
        self.instance_groups: Dict[str, List[str]] = {}
        self.websocket_instances: Dict[WebsocketConnection, List[str]] = {}

        self.http_server: Optional[web.Server] = None
        self.http_runner: Optional[web.ServerRunner] = None
        self.http_site: Optional[web.TCPSite] = None

    def start(self, wait = True):
        await_sync(self._start(wait), self.event_loop)

    async def _start(self, wait = True):
        self.logger.info(f'Starting on ws://{self.host}:{self.port}')
        self.websocket = await websockets.serve(self.on_connection, self.host, self.port)

        self.logger.info(f'Starting HTTP server on http://{self.host}:{self.http_port}')
        self.http_server = web.Server(self.handle_http_request)
        self.http_runner = web.ServerRunner(self.http_server)
        await self.http_runner.setup()
        self.http_site = web.TCPSite(self.http_runner, self.host, self.http_port)
        await self.http_site.start()

        if wait:
            await self._wait()

    def wait(self):
        await_sync(self._wait(), self.event_loop)

    async def _wait(self):
        if self.websocket is not None:
            await self.websocket.wait_closed()

        self.logger.info(f'Done')

    def stop(self):
        await_sync(self._stop(), self.event_loop)

    async def _stop(self):
        await self.http_site.stop()
        try:
            await asyncio.gather(*[websocket_connection.stop() for websocket_connection in self.websocket_connections])
        except asyncio.exceptions.CancelledError:
            pass
        self.websocket.close()

    async def on_connection(self, connection: websockets.WebSocketServerProtocol, path: str):
        self.logger.info(f'New connection from {connection.remote_address} path: {path}')
        websocket_connection = WebsocketConnection(connection, request_handler=self.handle_request, close_handler=self.handle_close)
        self.websocket_connections.append(websocket_connection)
        self.websocket_instances[websocket_connection] = []

        await websocket_connection.start()

        if websocket_connection in self.websocket_instances:
            for instance in self.websocket_instances[websocket_connection]:
                self.instances.pop(instance)
        self.websocket_connections.remove(websocket_connection)

        self.logger.info(f'Connection from {connection.remote_address} closed')

    async def _unlock_instance(self, instance_name: str):
        server = self.instances[instance_name]
        return await server.request(messages.Request(method=messages.Method.UNLOCK, data=instance_name), raise_error=False)

    #
    # Request Handlers
    #

    async def handle_forward_request(self, request: messages.Request) -> messages.Response:
        self.logger.info(f'Forwarding request to server: {request}')
        instance = request.data['instance']

        if instance not in self.instances:
            return messages.Response(status=messages.Status.ERROR, data=errors.InstanceNotFoundError(f'Instance not found: {instance}'))

        server = self.instances[request.data['instance']]

        response = await server.request(request, raise_error=False)
        self.logger.info(f'Forwarding response to client: {response}')

        return response

    async def handle_available_request(self, request: messages.Request) -> messages.Response:
        if request.data['instance'] not in self.instances:
            return messages.Response(status=messages.Status.NOT_FOUND)

        server = self.instances[request.data['instance']]
        return await server.request(request)

    async def handle_list_request(self, request: messages.Request) -> messages.Response:
        if 'group' not in request.data or request.data['group'] is None:
            instances = self.instances.keys()
        else:
            group = request.data['group']

            if group not in self.instance_groups:
                return messages.Response(status=messages.Status.ERROR, data=errors.GroupNotFoundError(f'Group not found: {group}'))

            instances = self.instance_groups[group]

        return messages.Response(data=list(instances))

    async def handle_register_request(self, websocket_connection: WebsocketConnection, request: messages.Request) -> messages.Response:
        self.logger.info(f'Registering instances: {request.data}')
        self.websocket_instances[websocket_connection] += request.data

        for instance_name, instance_group in request.data:
            if instance_group not in self.instance_groups:
                self.instance_groups[instance_group] = []

            self.instance_groups[instance_group].append(instance_name)
            self.instances[instance_name] = websocket_connection

        return messages.Response()

    # this is called by the GatewayConnection MessagePump when a new request is received
    async def handle_request(self, websocket_connection: WebsocketConnection, request: messages.Request) -> messages.Response:
        if request.method in self.SERVER_MESSAGES:
            return await self.handle_forward_request(request)

        if request.method == messages.Method.AVAILABLE:
            return await self.handle_available_request(request)

        if request.method == messages.Method.REGISTER:
            return await self.handle_register_request(websocket_connection, request)

        if request.method == messages.Method.LIST:
            return await self.handle_list_request(request)

        return messages.Response(status=messages.Status.ERROR, data=errors.InvalidMethodError(f'Invalid method: {request.method}'))

    async def handle_close(self, websocket_connection: WebsocketConnection):
        if websocket_connection in self.websocket_instances:
            instances = self.websocket_instances[websocket_connection]

            # unlock registered instances
            await asyncio.gather(*[self._unlock_instance(instance_name) for instance_name in instances])

            # remove registered instances
            for instance_name in instances:
                self.instances.pop(instance_name)

                for group, group_instances in self.instance_groups.items():
                    group_instances.remove(instance_name)

            self.websocket_instances.pop(websocket_connection)

        # send an error response for any in-progress requests
        for request_id, response_queue in websocket_connection.receive_queues.items():
            await response_queue.put(messages.Response(status=messages.Status.ERROR, data=errors.ServerConnectionLostError(f'Server connection lost')))

    async def handle_http_request(self, request: web.BaseRequest) -> web.StreamResponse:
        if request.method != 'POST':
            return web.HTTPMethodNotAllowed(request.method, ['POST'])

        message_raw = await request.read()

        try:
            self.logger.info(f'Handling request: {message_raw}')
            message = json.loads(message_raw)
            request = messages.Request(id=next_message_id(), method=message['method'], data=message['data'])

            if request.method in self.SERVER_MESSAGES:
                response = await self.handle_forward_request(request)
            elif request.method == messages.Method.AVAILABLE:
                response = await self.handle_available_request(request)
            elif request.method == messages.Method.LIST:
                response = await self.handle_list_request(request)
            else:
                response = messages.Response(status=messages.Status.ERROR, data=errors.InvalidMethodError(f'Invalid method: {request.method}'))

        except (KeyError, json.decoder.JSONDecodeError):
            response = messages.Response(status=messages.Status.ERROR, data=errors.InvalidMessageError(f'Invalid message: {message_raw}'))

        if response.status == messages.Status.ERROR:
            response.data = repr(response.data)

        response_dict = asdict(response)
        response_dict.pop('id')
        response_dict.pop('encoding')

        return web.json_response(response_dict)


class GatewayClient:
    def __init__(self, gateway_url: str = 'ws://localhost:8888'):
        self.logger = logger.getChild(self.__class__.__name__)
        self.gateway_url = gateway_url
        self.websocket_connection = WebsocketConnection(request_handler=self._log_and_handle_request, close_handler=self._handle_close)
        self.event_loop = asyncio.get_event_loop()
        self.connect_retry_timeout = 2.0

    @property
    def connected(self) -> bool:
        return self.websocket_connection.connection is not None

    async def _connect(self):
        while True:
            try:
                self.logger.info(f'Connecting to {self.gateway_url}')
                self.connection = await websockets.connect(self.gateway_url)
                return
            except OSError:
                self.logger.warning(f'Error connecting to {self.gateway_url}, retrying in {self.connect_retry_timeout} seconds')
                time.sleep(self.connect_retry_timeout)

    def start(self, wait=True):
        await_sync(self._start(wait), self.event_loop)

    async def _start(self, wait=True):
        await self._connect()
        await self.websocket_connection.start(wait=False, connection=self.connection)
        await self._on_start()

        if wait:
            await self._wait()

    def wait(self):
        await_sync(self._wait(), self.event_loop)

    async def _wait(self):
        await self.websocket_connection.wait()

    async def _on_start(self):
        pass

    def stop(self):
        await_sync(self._stop(), self.event_loop)

    async def _stop(self):
        await self.websocket_connection.stop()

    async def _log_and_handle_request(self, websocket_connection: WebsocketConnection, request: messages.Request) -> messages.Response:
        self.logger.debug(f'Request from {websocket_connection}: {request}')
        response = await self._handle_request(websocket_connection, request)
        self.logger.debug(f'Response to {websocket_connection}: {response}')

        return response

    async def _handle_request(self, websocket_connection: WebsocketConnection, request: messages.Request) -> messages.Response:
        pass

    async def _handle_close(self, websocket_connection: WebsocketConnection):
        await self._connect()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    gateway = Gateway()
    gateway.start()