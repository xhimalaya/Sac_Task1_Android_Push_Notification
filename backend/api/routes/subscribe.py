from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from models.device import Device
from schemas.device import SubscribeRequest

router = APIRouter()


@router.post("/subscribe", tags=["Push"])
def subscribe_device(
    payload: SubscribeRequest,
    db: Session = Depends(get_db)
):
    """
    Register a device push subscription.
    This API is idempotent.
    """

    existing = db.query(Device).filter(
        Device.endpoint == payload.endpoint
    ).first()

    if existing:
        return {
            "status": "already_registered"
        }

    device = Device(
        device_id=payload.device_id,
        endpoint=payload.endpoint,
        p256dh=payload.keys.p256dh,
        auth=payload.keys.auth,
        user_agent=payload.user_agent
    )

    db.add(device)
    db.commit()
    db.refresh(device)

    return {
        "status": "subscribed"
    }


@router.get("/devices", tags=["Push"])
def list_subscribed_devices(
    db: Session = Depends(get_db)
):
    """
    Get all subscribed devices.
    """

    devices = db.query(Device).all()

    return [
        {
            "id": d.id,
            "device_id": d.device_id,
            "endpoint": d.endpoint,
            "user_agent": d.user_agent,
            "created_at": d.created_at,
        }
        for d in devices
    ]
