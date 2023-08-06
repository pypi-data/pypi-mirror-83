from .middleware import (
    django_live_dashboard_asgi_middleware,
    django_live_dashboard_middleware,
)

__all__ = ["django_live_dashboard_asgi_middleware", "django_live_dashboard_middleware"]

default_app_config = "django_live_dashboard.apps.DjangoLiveDashboardConfig"
