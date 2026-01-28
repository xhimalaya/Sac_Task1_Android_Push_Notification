from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pywebpush import WebPushException

from db.session import get_db
from models.device import Device
from schemas.notification import NotifyAllRequest
from services.push_sender import send_push

router = APIRouter()


@router.post("/notify/all", tags=["Push"])
def notify_all_devices(
    payload: NotifyAllRequest,
    db: Session = Depends(get_db)
):
    """
    Send push notification to all registered devices.
    """

    devices = db.query(Device).all()
    print("-----------devices-------->", devices)

    sent = 0
    failed = 0

    for device in devices:
        try:
            send_push(
                device=device,
                payload={
                    "title": payload.title,
                    "message": payload.message,
                    "data": payload.data
                }
            )
            sent += 1

        except WebPushException:
            failed += 1
            # Optional: remove invalid subscriptions here

    return {
        "sent": sent,
        "failed": failed
    }
