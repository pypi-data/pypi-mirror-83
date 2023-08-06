from .base import _Message


class _Action(_Message):

    def _mark_seen(self):
        return {"sender_action": "mark_seen"}

    def _typing_on(self):
        return {"sender_action": "typing_on"}

    def _typing_off(self):
        return {"sender_action": "typing_off"}


class Action(_Action):

    def mark_seen(self, *args, **kwargs):
        return self.send_api(
            self._mark_seen(*args, **kwargs),
            **kwargs
        )

    def typing_on(self, *args, **kwargs):
        return self.send_api(
            self._typing_on(*args, **kwargs),
            **kwargs
        )

    def typing_off(self, *args, **kwargs):
        return self.send_api(
            self._typing_off(*args, **kwargs),
            **kwargs
        )
