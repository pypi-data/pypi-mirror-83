import time

from django.http import HttpResponse, HttpRequest
from django.db import connections

from .worker import push_evet
from .models import Request, SQLQuery


def django_live_dashboard_asgi_middleware(app):
    from django_live_dashboard.lifespan import lifespan_handler
    from django_live_dashboard.websocket import websocket_handler

    async def wrap(scope, receive, send):
        if scope["type"] == "lifespan":
            return await lifespan_handler(scope, receive, send, app)
        if scope["type"] == "websocket":
            return await websocket_handler(scope, receive, send, app)
        else:
            await app(scope, receive, send)

    return wrap


def get_queries_data(_request):
    queries = []
    for conn in connections.all():
        for query in conn.queries:
            item_data = {
                "duration": float(query.get("time", 0)),
                "sql": query.get("sql", ""),
                "db": conn.alias,
            }
            queries.append(SQLQuery(**item_data))
    return queries


def get_request_event(now, duration, request: HttpRequest, response: HttpResponse):
    data = {
        "time": now,
        "duration": duration,
        "status_code": response.status_code,
        "path": request.build_absolute_uri(),
        "queries": get_queries_data(request),
        "request_headers": {k.lower(): v for k, v in request.headers.items()},
        "response_headers": {k.lower(): v for k, v in response.items()},
    }
    return Request(**data)


def sync_middleware(get_response, request):
    now = time.time()
    response = get_response(request)
    duration = time.time() - now
    request.duration = duration
    event = get_request_event(now, duration, request, response)
    push_evet(event)
    return response


def django_live_dashboard_middleware(get_response):
    def middleware(request):
        return sync_middleware(get_response, request)

    return middleware
