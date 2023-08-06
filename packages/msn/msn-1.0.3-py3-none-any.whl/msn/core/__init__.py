import json
import requests

from msn.utils import logger, URL


class Base:

    endpoint = ""
    header_auth_key = "access_token"
    default_method = "GET"
    _auth_params = {}

    def get_url(self, endpoint=""):
        """
        Input:
            endpoint: must start with "/". Must be set before call this method.
        Output:
            String with well formed url
        """

        return "".join([URL.FACEBOOK, endpoint])

    def set_auth_params(self, **kwargs):
        """Set auth params to use in the requests.
        Input:
            access_token: Must be set before call this method.
            header_auth_key: Will be used to pass the access_token.
            kwargs: Aditional elements.
        Output:
            Dict object with credentials.
        """

        if not self.access_token:
            self._auth_params = {}
            return
        self._auth_params = {
            self.header_auth_key: self.access_token,
            **kwargs
        }

    def send(self, **kwargs):
        """
        Input:
            url: Set the endpoint before and the url will be generated.
            method: post, put, patch and get by default.
            params: Querystring params.
            data: Payload.
        Output:
            Http response.
        """

        # Builds the body.
        kwargs["url"] = self.get_url(endpoint=self.endpoint)
        kwargs["method"] = kwargs.get("method", self.default_method).upper()
        kwargs["headers"] = {
            "Content-Type": "application/json",
        }

        # Sets params.
        params = kwargs.get("params") or {}
        params.update(self._auth_params)
        kwargs["params"] = params

        # Sets payload.
        if kwargs.get("data"):
            kwargs["data"] = json.dumps(kwargs.get("data"))

        # Sends the request.
        response = requests.request(**kwargs)
        if response.status_code != 200:
            logger.error(response.json(), exc_info=True)
        return response
