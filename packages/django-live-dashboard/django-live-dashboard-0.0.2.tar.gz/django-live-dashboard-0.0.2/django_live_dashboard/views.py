from django.shortcuts import render


def index(request):
    return render(request, "django_live_dashboard/base.html")