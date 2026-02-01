from rest_framework import serializers
from .models import Device


class PushKeysSerializer(serializers.Serializer):
    p256dh = serializers.CharField()
    auth = serializers.CharField()


class SubscribeRequestSerializer(serializers.Serializer):
    device_id = serializers.CharField()
    endpoint = serializers.CharField()
    keys = PushKeysSerializer()
    user_agent = serializers.CharField(required=False, allow_null=True)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            "id",
            "device_id",
            "endpoint",
            "user_agent",
            "created_at",
        ]


class NotifyAllRequestSerializer(serializers.Serializer):
    title = serializers.CharField()
    message = serializers.CharField()
    data = serializers.DictField(required=False)
