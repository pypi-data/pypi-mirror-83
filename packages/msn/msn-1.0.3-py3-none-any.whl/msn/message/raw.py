from msn.message.enums import MessagingType

from .base import _Message


class _RawMessage(_Message):

    def _raw(self, message, attachment_type="text", is_reusable=True,
             quick_replies=None, **kwargs):
        """
        Input:
            message: str
            attachment_type: audio, video, image, file, text
            is_reusable: bool
            quick_replies: [{
                "content_type": "text",
                "title": "text",
                "payload": "text",
                "image_url": must be a valid url,
            }]
        """

        if attachment_type != "text":
            if str(message).isdigit():
                result = self._attachment_by_id(message, attachment_type)
            else:
                result = self._attachment_by_url(
                    message, attachment_type, is_reusable
                )
        else:
            result = self._text_message(message)

        if quick_replies:
            result["message"]["quick_replies"] = quick_replies

        return result

    def _text_message(self, text_message, **kwargs):
        """
        Input:
            text_message: string to be sent.
        """

        return {
            "message": {
                "text": text_message,
            },
        }

    def _attachment_by_url(self, url, attachment_type="file",
                           is_reusable=True, **kwargs):
        """
        Input:
            attachment_type: audio, video, image, file
        """

        return {
            "message": {
                "attachment": {
                    "type": attachment_type,
                    "payload": {
                        "url": url,
                        "is_reusable": is_reusable,
                    },
                },
            },
        }

    def _attachment_by_id(self, attachment_id, attachment_type="file",
                          **kwargs):
        """
        Input:
            attachment_type: audio, video, image, file
        """

        return {
            "message": {
                "attachment": {
                    "type": attachment_type,
                    "payload": {
                        "attachment_id": attachment_id,
                    },
                },
            },
        }


class RawMessage(_RawMessage):

    def upload_attachment(self, *args, **kwargs):
        """Upload attachment by url.
        Input:
            message: url with the resource
            attachment_type: audio, video, image, file
        Output:
            String with attachment_id.
        """

        # Sets conditions before send the request.
        _endpoint = self.endpoint  # "/me/messages"
        self.endpoint = "/me/message_attachments"
        # Uploads the attachment.
        response = self.send_api(
            self._raw(is_reusable=True, *args, **kwargs),
            **kwargs
        )
        # Set conditions as before in order to reuse the client.
        self.endpoint = _endpoint
        # Returns the attachment_id.
        if response.status_code != 200:
            return response
        return response.json().get("attachment_id")

    def raw(self, *args, **kwargs):
        return self.send_api(
            self._raw(*args, **kwargs),
            **kwargs
        )

    def text_message(self, *args, **kwargs):
        return self.send_api(
            self._text_message(*args, **kwargs),
            **kwargs
        )

    def attachment_by_url(self, *args, **kwargs):
        return self.send_api(
            self._attachment_by_url(*args, **kwargs),
            **kwargs
        )

    def attachment_by_id(self, *args, **kwargs):
        return self.send_api(
            self._attachment_by_id(*args, **kwargs),
            **kwargs
        )
