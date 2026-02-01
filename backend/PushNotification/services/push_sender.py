import json
from pywebpush import webpush
from django.conf import settings


def send_push(device, payload: dict):
    """
    Send a push notification to a single device.
    """

    webpush(
        subscription_info={
            "endpoint": device.endpoint,
            "keys": {
                "p256dh": device.p256dh,
                "auth": device.auth,
            },
        },
        data=json.dumps(payload),
        vapid_private_key=settings.VAPID_PRIVATE_KEY,
        vapid_claims={
            "sub": settings.VAPID_EMAIL
        },
    )
