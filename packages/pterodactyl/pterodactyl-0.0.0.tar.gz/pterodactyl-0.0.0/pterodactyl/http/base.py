from httpx import Response


class BaseHTTP:
    def _handle(self, response: Response, json: bool = False) -> dict:
        """Used to handing httpx responses.

        Parameters
        ----------
        response : Response
        json : bool, optional
            If response should be processed as json, by default False

        Returns
        -------
        dict
        """

        response.raise_for_status()

        if json:
            return response.json()
