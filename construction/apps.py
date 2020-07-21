from django.apps import AppConfig


class ProjectConfig(AppConfig):
    name = 'construction'
    def ready(self):
        import construction.signals