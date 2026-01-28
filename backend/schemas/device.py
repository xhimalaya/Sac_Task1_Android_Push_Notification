from pydantic import BaseModel


class PushKeys(BaseModel):
    p256dh: str
    auth: str


class SubscribeRequest(BaseModel):
    device_id: str
    endpoint: str
    keys: PushKeys
    user_agent: str | None = None
