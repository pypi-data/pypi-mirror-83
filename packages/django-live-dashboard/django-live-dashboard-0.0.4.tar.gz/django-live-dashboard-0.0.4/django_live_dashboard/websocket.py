import asyncio
from django.conf import settings
from django.urls import reverse
from .default_settings import ALLOW_ACCESS_CALLBACK, REDIS_KEY_NAMESPACE


async def websocket_handler(scope, receive, send, inner_app):
    ws_path = reverse("django_live_dashboard_index")
    if scope.get("path") != ws_path:
        return await inner_app(scope, receive, send)
    init_message = await receive()
    assert init_message["type"] == "websocket.connect"
    allow_access_cb = settings.DJANGO_LIVE_DASHBOARD.get(
        "ALLOW_ACCESS_CALLBACk", ALLOW_ACCESS_CALLBACK
    )
    if allow_access_cb:
        if await allow_access_cb(scope) is not True:
            return await send({"type": "websocket.close"})
    await send({"type": "websocket.accept"})

    ws_disconnected = False

    async def task_listen_redis_events():
        from django.apps import apps

        app_config = apps.get_app_config("django_live_dashboard")
        redis = app_config.redis
        pubsub = redis.pubsub(ignore_subscribe_messages=True)
        await pubsub.subscribe(
            settings.DJANGO_LIVE_DASHBOARD.get(
                "REDIS_KEY_NAMESPACE", REDIS_KEY_NAMESPACE
            )
            + ":pubsub",
        )
        while True:
            # aredis swallows all exceptions here :( and returns None.
            # So check if disconnected after getting None
            message = await pubsub.get_message()
            if message is None:
                continue
            if not ws_disconnected:
                await send({"type": "websocket.send", "text": message["data"].decode()})
            else:
                break

    async def task_handle_received_message():
        while True:
            message = await receive()
            if message["type"] == "websocket.disconnect":
                break

    tasks = []
    redis_task = asyncio.create_task(task_listen_redis_events())
    tasks.append(redis_task)
    tasks.append(asyncio.create_task(task_handle_received_message()))
    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    ws_disconnected = True
    for t in tasks:
        t.cancel()
