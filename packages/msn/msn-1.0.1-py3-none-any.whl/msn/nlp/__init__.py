from msn.core import Base


class NLP(Base):
    """
    Input:
        page_access_token
    """

    endpoint = "/me/nlp_configs"
    default_method = "POST"

    def __init__(self, page_access_token):
        self.access_token = page_access_token
        self.set_auth_params()

    def add(self, nlp_enabled=True, custom_token=None):
        """
        Input:
            custom_token: WIT token.
            nlp_enabled: bool.
        """
        return self.send(
            data=self._auth_params,
            params={
                "custom_token": custom_token,
                "nlp_enabled": nlp_enabled,
            },
        )
