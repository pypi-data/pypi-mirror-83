from django.urls import path
from .views import index

urlpatterns = [
    path("", index, name="django_live_dashboard_index"),
    path("requests", index),
]
