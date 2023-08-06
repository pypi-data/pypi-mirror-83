from .actions import Action
from .quick_replies import QuickReply
from .raw import RawMessage
from .templates import Template


class Message(Action, RawMessage, QuickReply, Template):
    """
    Input:
        page_access_token
        psid
    """

    def __init__(self, page_access_token, psid):
        self.access_token = page_access_token
        self.psid = psid 
        self.set_auth_params()
