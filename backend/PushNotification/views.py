from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from pywebpush import WebPushException

from .models import Device
from .serializers import (
    SubscribeRequestSerializer,
    DeviceSerializer,
    NotifyAllRequestSerializer,
)
from .services.push_sender import send_push


class SubscribeDeviceView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SubscribeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        if Device.objects.filter(endpoint=data["endpoint"]).exists():
            return Response({"status": "already_registered"})

        Device.objects.create(
            device_id=data["device_id"],
            endpoint=data["endpoint"],
            p256dh=data["keys"]["p256dh"],
            auth=data["keys"]["auth"],
            user_agent=data.get("user_agent"),
        )

        return Response({"status": "subscribed"}, status=status.HTTP_201_CREATED)


class ListDevicesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)


class NotifyAllDevicesView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = NotifyAllRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = serializer.validated_data
        devices = Device.objects.all()

        sent = 0
        failed = 0

        for device in devices:
            try:
                send_push(
                    device=device,
                    payload={
                        "title": payload["title"],
                        "message": payload["message"],
                        "data": payload.get("data"),
                    },
                )
                sent += 1
            except WebPushException:
                failed += 1

        return Response({
            "sent": sent,
            "failed": failed
        })
