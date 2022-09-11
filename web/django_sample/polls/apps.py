from django.apps import AppConfig


class PollsConfig(AppConfig):
    name = 'polls'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app_object_bla: str = ''
