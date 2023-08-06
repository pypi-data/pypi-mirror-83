import queue
import threading

from django.conf import settings
from pydantic import BaseModel
from redis import Redis

from .default_settings import REDIS_KEY_NAMESPACE, REDIS_URI
from .serializer import serialize

events_queue = queue.Queue()


def event_worker():
    redis = Redis.from_url(settings.DJANGO_LIVE_DASHBOARD.get("REDIS_URI", REDIS_URI))
    while True:
        item = events_queue.get()
        redis.publish(
            settings.DJANGO_LIVE_DASHBOARD.get(
                "REDIS_KEY_NAMESPACE", REDIS_KEY_NAMESPACE
            )
            + ":pubsub",
            item,
        )


def push_evet(event):
    if isinstance(event, BaseModel):
        events_queue.put(serialize(event.dict()))
        return
    events_queue.put(serialize(event))


event_worker_thread = threading.Thread(target=event_worker, daemon=True)


async def system_info_worker():
    pass
