from django.apps import AppConfig


class DjangoLiveDashboardConfig(AppConfig):
    name = "django_live_dashboard"
    verbose_name = "Django Live Dashboard"
    asgi_started = False
    asgi_shutdown = False
    redis = None
