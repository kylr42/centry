import asyncio
import json
import logging
from typing import Union

from websocket import create_connection, WebSocket, WebSocketConnectionClosedException


logger = logging.getLogger('centrifuge')
# websocket.enableTrace(True)


class CentrifugeBase:

    def __init__(self, host, port, path='connection/websocket'):
        self.ws: Union[WebSocket, None] = None

        self.host = host
        self.port = port
        self.path = path

        self._conn()

    def _conn(self):
        try:
            self.ws = create_connection(f"ws://{self.host}:{self.port}/{self.path}")
        except ConnectionRefusedError:
            logger.error("Er.: Connection Refused! Maybe settings not correct!")
            exit(42)

    def _send_cmd(self, id, method, params):
        self.ws.send(
            json.dumps(
                {
                    "id": id,
                    "method": method,
                    "params": params
                }
            )
        )
        return self.ws.recv

    async def _loop(self, func):
        while True:
            logger.info("Receiving...")
            result = self.ws.recv()
            logger.debug(f"Received {result}")
            func.__call__()
            await asyncio.sleep(1)


class Centrifuge(CentrifugeBase):

    def connect(self, token, data=None):
        if data is None:
            data = {}

        try:
            params = {
                "token": token,
                "data": data
            }
            return self._send_cmd(id=1, method=0, params=params)

        except WebSocketConnectionClosedException:
            logger.error("Err.: Token or data invalid!")
            exit(42)

    def subscribe(self, channel):
        try:
            params = {
                "channel": channel,
            }
            return self._send_cmd(id=2, method=1, params=params)

        except WebSocketConnectionClosedException:
            logger.error("Err.: Channel not found!")
            exit(42)

    def parse_data(self, data):
        print(f"parse: {data}")

    def loop(self):
        asyncio.create_task(self._loop(self.parse_data))

