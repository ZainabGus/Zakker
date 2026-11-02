from django.apps import AppConfig


class ZakksConfig(AppConfig):
    name = "zakks"

    def ready(self):
        import zakks.signals

