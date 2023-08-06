from msn import token, profile, user, nlp, message, page


class Messenger:
    """
    Input:
        app_id
        app_secret
        page_access_token
        user_access_token
    """

    def __init__(self, app_id=None, app_secret=None,
                 page_id=None, user_id=None, psid=None,
                 page_access_token=None, user_access_token=None):
        self.app_id = app_id
        self.app_secret = app_secret 
        self.page_id = page_id 
        self.user_id = user_id
        self.psid = psid 
        self.page_access_token = page_access_token
        self.user_access_token = user_access_token

    @property
    def page(self):
        return page.Page(
            page_id=self.page_id,
            page_access_token=self.page_access_token,
        )

    @property
    def token(self):
        return token.Token(
            app_id=self.app_id,
            app_secret=self.app_secret,
            user_id=self.user_id,
            user_access_token=self.user_access_token,
        )

    @property
    def profile(self):
        return profile.Profile(
            page_access_token=self.page_access_token,
        )

    @property
    def user(self):
        return user.User(
            page_access_token=self.page_access_token,
            psid=self.psid,
        )

    @property
    def message(self):
        return message.Message(
            page_access_token=self.page_access_token,
            psid=self.psid,
        )

    @property
    def nlp(self):
        return nlp.NLP(
            page_access_token=self.page_access_token,
        )
