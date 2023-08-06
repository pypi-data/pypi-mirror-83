from msn.core import Base
from msn.message.enums import MessagingType, NotificationType


class _Message(Base):
    """
    Input:
        page_access_token
        psid 
    """

    endpoint = "/me/messages"

    def enrich_payload(self, data, *args, **kwargs):
        """Adds message_type, tag and PSID to payload."""

        # Adds the PSID.
        payload = {
            "recipient": {
                "id": self.psid,
            },
            **data,
        }
        # Injects the messaging type.
        payload["messaging_type"] = kwargs.get(
            "messaging_type",
            MessagingType.RESPONSE.name
        )
        # Injects the notification type.
        payload["notification_type"] = kwargs.get(
            "notification_type",
            NotificationType.REGULAR.name
        )
        # Injects the tag.
        tag = kwargs.get("tag")
        if tag:
            payload["tag"] = tag
        return payload

    def send_api(self, payload, *args, **kwargs):
        """Builds up the request.
        Input:
            payload: What we really want to send.
            messaging_type: MessagingType.RESPONSE by default.
            tag: not required
        """

        data = self.enrich_payload(payload, *args, **kwargs)
        response = self.send(
            method="POST",
            data=data,
        )
        return response
