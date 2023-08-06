from msn.core import Base


class _Page(Base):

    def __init__(self, page_id, page_access_token):
        self.access_token = page_access_token
        self.page_id = page_id 
        self.set_auth_params()


class Page(_Page):
    """
    Input:
        page_id 
        page_access_token
    """

    @property
    def subscribed_apps(self):
        return SubscribedApps(self.page_id, self.access_token)


class SubscribedApps(_Page):

    def set(self, fields):
        """
        Input:
            fields: list.
        """
        self.endpoint = f"/{self.page_id}/subscribed_apps"
        self.default_method = "POST"
        return self.send(params={
            "subscribed_fields": ",".join(fields)
        })

    def delete(self):
        self.endpoint = f"/{self.page_id}/subscribed_apps"
        self.default_method = "DELETE"
        return self.send()
