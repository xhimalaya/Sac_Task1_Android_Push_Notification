import json
from pywebpush import webpush

from core.config import (
    VAPID_PRIVATE_KEY,
    VAPID_EMAIL
)


def send_push(device, payload: dict):
    """
    Send a push notification to a single device.
    """
    print(">>>>>>>>>   recived connection ", payload)
    webpush(
        subscription_info={
            "endpoint": device.endpoint,
            "keys": {
                "p256dh": device.p256dh,
                "auth": device.auth
            }
        },
        data=json.dumps(payload),
        vapid_private_key=VAPID_PRIVATE_KEY,
        vapid_claims={
            "sub": VAPID_EMAIL
        }
    )
