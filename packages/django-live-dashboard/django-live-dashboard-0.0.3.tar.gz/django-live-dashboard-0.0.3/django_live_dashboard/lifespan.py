from aredis import StrictRedis
from django.conf import settings
from .default_settings import REDIS_URI, REDIS_KEY_NAMESPACE


async def lifespan_handler(scope, receive, send, inner_app):
    from django.apps import apps

    app_config = apps.get_app_config("django_live_dashboard")

    async def wrapped_send(message):
        if message["type"] == "lifespan.startup.complete":
            app_config.asgi_started = True
        if message["type"] == "lifespan.shutdown.complete":
            app_config.asgi_shutdown = True
        await send(message)

    redis = StrictRedis.from_url(settings.DJANGO_LIVE_DASHBOARD.get("REDIS_URI", REDIS_URI))
    while True:
        message = await receive()
        if message["type"] == "lifespan.startup":
            app_config.redis = redis
            redis.hset(settings.DJANGO_LIVE_DASHBOARD.get("REDIS_KEY_NAMESPACE", REDIS_KEY_NAMESPACE) + ":nodes", )
            try:
                await inner_app(scope, receive, wrapped_send)
            except ValueError:
                pass
            if not app_config.asgi_started:
                await send({"type": "lifespan.startup.complete"})
        elif message["type"] == "lifespan.shutdown":
            try:
                await inner_app(scope, receive, wrapped_send)
            except ValueError:
                pass
            if not app_config.asgi_shutdown:
                await send({"type": "lifespan.shutdown.complete"})
