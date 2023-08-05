from msn.core import Base


class User(Base):
    """
    Input:
        page_access_token
        recipient_id
    """

    FIELDS = [
        "first_name",
        "last_name",
        "profile_pic",
        "locale",
        "timezone",
        "gender",
    ]

    def __init__(self, page_access_token, psid):
        # Generates endpoint.
        self.access_token = page_access_token
        self.psid = psid 
        self.endpoint = f"/{self.psid}"
        self.set_auth_params()

    def get_profile(self, fields=FIELDS):
        # Get user profile.
        return self.send(params={
            "fields": ",".join(fields),
        })
