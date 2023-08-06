from httpx import Request
from typing import Any

from .base import BaseHTTP


class AwaitingHTTP(BaseHTTP):
    async def __handle(self,  request: Request, read_json: bool = False,
                       *args, **kwargs) -> Any:
        """Handles async request.

        Parameters
        ----------
        request : Request
        read_json : bool, optional
            by default False

        Returns
        -------
        Any
        """

        return self._handle(
            await request(*args, **kwargs),
            read_json
        )

    async def _get(self, *args, **kwargs) -> dict:
        return await self.__handle(
            self._client.get,
            read_json=True,
            *args, **kwargs
        )

    async def _post(self, *args, **kwargs) -> None:
        return await self.__handle(
            self._client.post,
            *args, **kwargs
        )

    async def _delete(self, *args, **kwargs) -> None:
        return await self.__handle(
            self._client.delete,
            *args, **kwargs
        )

    async def _put(self, *args, **kwargs) -> None:
        return await self.__handle(
            self._client.put,
            *args, **kwargs
        )
