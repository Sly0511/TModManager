from beanie import Document, Indexed, Link
from .profile import Profile


class User(Document):
    user_token: Indexed(str, unique=True)
    profiles: list[Link[Profile]] = []
