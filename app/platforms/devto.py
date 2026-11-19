
import httpx
from datetime import datetime, timezone

from app.config import settings
from app.platforms.base import BasePlatform


class DevtoPlatform(BasePlatform):

    async def post(self, message: str) -> dict:

        now = datetime.now(timezone.utc)

        try:
            api_key = settings.DEVTO_API_KEY

            if not api_key:
                raise ValueError("DEV.to API key is missing")

            headers = {
                "api-key": api_key,
                "Accept": "application/vnd.forem.api-v1+json",
                "Content-Type": "application/json"
            }

            article_data = {
                "article": {
                    "title": "Automated Update from FastAPI",
                    "body_markdown": message,
                    "published": False
                }
            }

            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    "https://dev.to/api/articles",
                    headers=headers,
                    json=article_data
                )

                response.raise_for_status()
                data = response.json()

                return {
                    "platform": "DEV.to",
                    "status": "success",
                    "posted_url": data.get("url"),
                    "public_access": False,
                    "date": now.strftime("%Y-%m-%d"),
                    "time": now.strftime("%H:%M:%S"),
                    "error": None
                }

        except Exception as exc:
            return {
                "platform": "DEV.to",
                "status": "failed",
                "posted_url": None,
                "public_access": False,
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M:%S"),
                "error": str(exc)
            }
