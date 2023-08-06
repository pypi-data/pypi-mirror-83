from .base import _Message


class _Template(_Message):

    def _button(self, text, buttons):
        return {
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": buttons,
                    },
                },
            },
        }

    def _generic_template(self, elements, image_aspect_ratio="horizontal",
                          sharable=False):
        return {
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements,
                        "image_aspect_ratio": image_aspect_ratio,
                        "sharable": sharable,
                    },
                },
            },
        }

    def _receipt_template(self, elements, address, summary,
                          adjustments=None, sharable=False, **order):
        return {
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "receipt",
                        "elements": elements,
                        "address": address,
                        "summary": summary,
                        "adjustments": adjustments,
                        "sharable": sharable,
                        **order,
                    },
                },
            },
        }


class Template(_Template):

    def button(self, *args, **kwargs):
        return self.send_api(
            self._button(*args, **kwargs),
            **kwargs
        )

    def generic_template(self, *args, **kwargs):
        return self.send_api(
            self._generic_template(*args, **kwargs),
            **kwargs
        )

    def receipt_template(self, *args, **kwargs):
        return self.send_api(
            self._receipt_template(*args, **kwargs),
            **kwargs
        )
