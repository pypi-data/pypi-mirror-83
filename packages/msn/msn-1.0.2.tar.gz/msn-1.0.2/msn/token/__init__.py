from msn.core import Base


class Token(Base):
    """
    Input:
        app_id
        app_secret
        user_id 
        user_access_token
    """

    def __init__(self, app_id, app_secret, 
                 user_id, user_access_token):
        self.app_id = app_id
        self.app_secret = app_secret 
        self.user_id = user_id
        self.access_token = user_access_token
        self.set_auth_params()

    def generate_long_lived_user_access_token(self):
        """Generates long lived USER access token."""
        self.header_auth_key = "fb_exchange_token"
        self.set_auth_params(
            grant_type="fb_exchange_token",
            client_id=self.app_id,
            client_secret=self.app_secret,
        )
        self.endpoint = "/oauth/access_token"
        # Make the request. 
        response = self.send()
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            return None

    def generate_long_lived_page_access_token(self):
        """Generates long lived PAGE access token."""
        self.header_auth_key = "access_token"
        self.set_auth_params(
            fields="access_token",
        )
        self.endpoint = f"/{self.user_id}/accounts" 
        # Make the request. 
        response = self.send()
        if response.status_code == 200:
            return response.json().get("data")[0].get("access_token")
        return None


    def generate(self):
        self.access_token = self.generate_long_lived_user_access_token()
        return self.generate_long_lived_page_access_token()
