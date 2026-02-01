from django.urls import path
from .views import (
    SubscribeDeviceView,
    ListDevicesView,
    NotifyAllDevicesView,
)

urlpatterns = [
    path("subscribe/", SubscribeDeviceView.as_view()),
    path("devices/", ListDevicesView.as_view()),
    path("all/", NotifyAllDevicesView.as_view()),
]
