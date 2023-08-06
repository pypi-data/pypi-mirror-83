import json
from typing import Callable, Any

from aiohttp_sse_client import client as sse_client
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientPayloadError
import asyncio

from .auth import AuthService
from ..domain import ClientConfig


class ReceiverService(object):
    def __init__(self, billing_id: str, client_id: str, client_secret: str, config: ClientConfig):
        self._logger = config.get_logger(__name__)

        self.auth_service = AuthService(
            purpose=self.__class__.__name__,
            billing_id=billing_id,
            client_id=client_id,
            client_secret=client_secret,
            config=config
        )

        self._config = config
        self._client = None
        self._running = False
        self.session = None

    async def start_timer(self):
        await self.auth_service.start()

    async def start(self, as_json: bool, consumer: Callable[[Any], Any]):
        self._running = True
        await self.auth_service.start()
        while self._running:
            uri = self._config.egress_uri + ("?asJson=true" if as_json else "")
            try:
                async with sse_client.EventSource(uri, headers = {
                        'Authorization': f'Bearer {self.auth_service.get_access_token()}',
                        'Strm-Driver-Version': self._config.version.brief_string(),
                        'Strm-Driver-Build': self._config.version.release_string()
                    }) as event_source:
                    async for event in event_source:
                        await consumer(event.data)
            except ConnectionError as e:
                self._logger.debug("%s", e)
            except ClientPayloadError as e:
                self._logger.debug("%s", e)

    def close(self):
        self._running = False

