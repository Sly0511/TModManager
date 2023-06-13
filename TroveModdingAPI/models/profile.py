from random import sample
from string import ascii_letters, digits

from beanie import Document, Indexed
from pydantic import Field


def random_id(k=8):
    return "".join(sample(ascii_letters + digits, k=k))


class Profile(Document):
    share_id: Indexed(str, unique=True) = Field(default_factory=random_id)

