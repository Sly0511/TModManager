from datetime import datetime

from beanie import Document, Indexed, Link
from pydantic import Field

from .profile import Profile


class User(Document):
    user_token: Indexed(str, unique=True)
    profiles: list[Link[Profile]] = []
    subscribed_profiles: list[Link[Profile]] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
