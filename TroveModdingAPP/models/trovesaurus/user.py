from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(alias="user_id")
    name: str = Field(alias="username")
    icon: str
    image: str = Field(alias="custom_profile_image")

    @property
    def icon_url(self):
        return f"https://trovesaurus.com/data/catalog/{self.icon}"

    @property
    def image_url(self):
        return ("https://" + self.image) if self.image else None

    @property
    def display_image_url(self):
        return self.image_url or self.icon_url
