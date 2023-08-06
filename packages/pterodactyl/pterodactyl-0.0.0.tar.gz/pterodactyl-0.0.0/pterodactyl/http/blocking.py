from httpx import Request
from typing import Any

from .base import BaseHTTP


class BlockingHTTP(BaseHTTP):
    def __handle(self,  request: Request, read_json: bool = False,
                 *args, **kwargs) -> Any:
        """Handles sync request.

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
            request(*args, **kwargs),
            read_json
        )

    def _get(self, *args, **kwargs) -> dict:
        return self.__handle(
            self._client.get,
            read_json=True,
            *args, **kwargs
        )

    def _post(self, *args, **kwargs) -> None:
        return self.__handle(
            self._client.post,
            *args, **kwargs
        )

    def _delete(self, *args, **kwargs) -> None:
        return self.__handle(
            self._client.delete,
            *args, **kwargs
        )

    def _put(self, *args, **kwargs) -> None:
        return self.__handle(
            self._client.put,
            *args, **kwargs
        )
