from .base import _Message


class _QuickReply(_Message):

    def _quick_reply(self, text_message, quick_replies, **kwargs):
        """
        Inputs:
            text_message: str.
            quick_replies: [{
                "content_type": "text",
                "title": "text",
                "payload": "text",
                "image_url": must be a valid url,
            }]
        """

        return {
            "message": {
                "text": text_message,
                "quick_replies": quick_replies,
            },
        }

    def __custom_quick_reply(self, content_type, text_message,
                             quick_replies=[]):
        """
        Input:
            content_type: user_email, user_phone_number
            text_message: str.
            quick_replies: [{
                "content_type": "text",
                "title": "text",
                "payload": "text",
            }]
        """
        result = {
            "message": {
                "text": text_message,
            },
        }
        result["message"]["quick_replies"] = [{
            "content_type": content_type,
        }, *quick_replies]
        return result

    def _email(self, text_message, quick_replies=[], **kwargs):
        return self.__custom_quick_reply(
            "user_email", text_message, quick_replies,
        )

    def _phone_number(self, text_message, quick_replies=[], **kwargs):
        return self.__custom_quick_reply(
            "user_phone_number", text_message, quick_replies,
        )


class QuickReply(_QuickReply):

    def quick_reply(self, *args, **kwargs):
        return self.send_api(
            self._quick_reply(*args, **kwargs),
            **kwargs
        )

    def email(self, *args, **kwargs):
        return self.send_api(
            self._email(*args, **kwargs),
            **kwargs
        )

    def phone_number(self, *args, **kwargs):
        return self.send_api(
            self._phone_number(*args, **kwargs),
            **kwargs
        )
