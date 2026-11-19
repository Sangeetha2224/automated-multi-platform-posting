
from pydantic import BaseModel, Field, HttpUrl, field_validator
from urllib.parse import urlsplit
import re


class PostingRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=200
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value):

        urls = re.findall(
            r"https?://[^\s]+",
            value
        )

        if len(urls) != 1:
            raise ValueError(
                "Exactly one CTA link is required"
            )

        url = urls[0].rstrip(".,!?;:)")

        try:
            parsed = urlsplit(url)

            if (
                parsed.scheme not in ["http", "https"]
                or not parsed.hostname
                or "." not in parsed.hostname
                or any(char.isspace() for char in url)
            ):
                raise ValueError()

            HttpUrl(url)

        except Exception:
            raise ValueError("Invalid URL")

        return value
