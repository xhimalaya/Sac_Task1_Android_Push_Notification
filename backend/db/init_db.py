from sqlalchemy.orm import Session
from db.session import engine
from models.base import Base

# Import ALL models here
from models.device import Device  # noqa


def init_db():
    Base.metadata.create_all(bind=engine)
