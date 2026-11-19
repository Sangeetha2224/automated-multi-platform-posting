
import httpx
from datetime import datetime, timezone

from app.config import settings
from app.platforms.base import BasePlatform


class DiscordPlatform(BasePlatform):

    async def post(self, message: str) -> dict:

        now = datetime.now(timezone.utc)

        try:
            webhook_url = settings.DISCORD_WEBHOOK_URL

            if not webhook_url:
                raise ValueError("Discord webhook URL is missing")

            async with httpx.AsyncClient(timeout=20) as client:

                response = await client.post(
                    webhook_url,
                    json={"content": message},
                    params={"wait": "true"}
                )

                response.raise_for_status()
                data = response.json()

                message_id = data.get("id")
                channel_id = data.get("channel_id")

                posted_url = (
                    f"https://discord.com/channels/@me/{channel_id}/{message_id}"
                    if message_id and channel_id
                    else None
                )

                return {
                    "platform": "Discord",
                    "status": "success",
                    "posted_url": posted_url,
                    "public_access": True,
                    "date": now.strftime("%Y-%m-%d"),
                    "time": now.strftime("%H:%M:%S"),
                    "error": None
                }

        except Exception as exc:
            return {
                "platform": "Discord",
                "status": "failed",
                "posted_url": None,
                "public_access": False,
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M:%S"),
                "error": str(exc)
            }
