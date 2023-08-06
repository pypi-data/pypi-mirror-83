from msn.core import Base


class _Profile(Base):
    endpoint = "/me/messenger_profile"

    def __init__(self, page_access_token):
        self.access_token = page_access_token
        self.set_auth_params()


class Profile(_Profile):
    """
    Input:
        page_access_token
    """

    @property
    def greeting(self):
        return Greeting(self.access_token)

    @property
    def get_started(self):
        return GetStarted(self.access_token)

    @property
    def whitelisted_domains(self):
        return WhitelistedDomains(self.access_token)

    @property
    def persistent_menu(self):
        return PersistentMenu(self.access_token)

    # To retrieve or set multiple properties.
    def get(self, fields):
        """
        Input:
            fields: list of messenger profile properties to retrieve.
        """
        self.default_method = "GET"
        return self.send(params={
            "fields": ",".join(fields)
        })

    def set(self, data):
        """
        Input:
            data: dict with messenger profile properties to set. 
        """
        self.default_method = "POST"
        return self.send(data=data)

    def delete(self, fields):
        """
        Input:
            fields: list of messenger profile properties to delete.
        """
        self.default_method = "DELETE"
        return self.send(data={
            "fields": fields,
        })


class Greeting(_Profile):

    def get(self):
        self.default_method = "GET"
        return self.send(params={"fields": "greeting"})

    def set(self, greeting):
        """
        Input:
            greeting: str or list.
        """
        self.default_method = "POST"
        if isinstance(greeting, str):
            data = {
                "greeting": [{
                    "locale": "default",
                    "text": greeting,
                }],
            }
        if isinstance(greeting, list):
            data = {"greeting": greeting}
        return self.send(data=data)

    def delete(self):
        self.default_method = "DELETE"
        return self.send(data={
            "fields": ["greeting"],
        })


class GetStarted(_Profile):

    def get(self):
        self.default_method = "GET"
        return self.send(params={"fields": "get_started"})

    def set(self, payload="GET_STARTED_PAYLOAD"):
        """
        Input:
            payload: str.
        """
        self.default_method = "POST"
        return self.send(data={
            "get_started": {
                "payload": payload,
            },
        })

    def delete(self):
        self.default_method = "DELETE"
        # Get started and persistent menu are binded.
        return self.send(data={
            "fields": ["get_started", "persistent_menu"],
        })


class WhitelistedDomains(_Profile):

    def get(self):
        self.default_method = "GET"
        return self.send(params={"fields": "whitelisted_domains"})

    def set(self, domains):
        """
        Input:
            domains: list of valid urls.
        """
        self.default_method = "POST"
        return self.send(data={
            "whitelisted_domains": domains,
        })

    def delete(self):
        self.default_method = "DELETE"
        return self.send(data={
            "fields": ["whitelisted_domains"],
        })


class PersistentMenu(_Profile):

    def get(self):
        self.default_method = "GET"
        return self.send(params={"fields": "persistent_menu"})

    def set(self, menu):
        """
        Input:
            menu: list.
        """
        self.default_method = "POST"
        return self.send(data={
            "persistent_menu": menu,
        })

    def delete(self):
        self.default_method = "DELETE"
        return self.send(data={
            "fields": ["persistent_menu"],
        })
