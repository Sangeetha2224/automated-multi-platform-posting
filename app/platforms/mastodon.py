
import httpx
from datetime import datetime

from app.config import settings
from app.platforms.base import BasePlatform


class MastodonPlatform(BasePlatform):

    async def post(self, message: str) -> dict:

        base_url = settings.MASTODON_BASE_URL.rstrip("/")

        result = {
            "platform": "Mastodon",
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": None
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:

                # 1. Publish status

                response = await client.post(
                    f"{base_url}/api/v1/statuses",
                    headers={
                        "Authorization": (
                            f"Bearer {settings.MASTODON_ACCESS_TOKEN}"
                        )
                    },
                    data={
                        "status": message,
                        "visibility": "public"
                    }
                )

                response.raise_for_status()

                post_data = response.json()

                # 2. Get post details

                post_id = post_data["id"]
                post_url = post_data.get("url")
                created_at = post_data["created_at"]

                post_datetime = datetime.fromisoformat(
                    created_at.replace("Z", "+00:00")
                )

                # 3. Check public accessibility

                public_access = False

                if post_url:
                    verify_response = await client.get(
                        f"{base_url}/api/v1/statuses/{post_id}"
                    )

                    if verify_response.is_success:
                        verified_post = verify_response.json()

                        public_access = (
                            verified_post.get("visibility") == "public"
                            and verified_post.get("id") == post_id
                        )

                # 4. Return actual result

                result.update({
                    "status": "success",
                    "posted_url": post_url,
                    "public_access": public_access,
                    "date": post_datetime.strftime("%Y-%m-%d"),
                    "time": post_datetime.strftime("%H:%M:%S")
                })

        except httpx.HTTPStatusError as exc:

            try:
                error_data = exc.response.json()
                error_message = error_data.get(
                    "error",
                    exc.response.text
                )
            except ValueError:
                error_message = exc.response.text

            result["error"] = (
                f"HTTP {exc.response.status_code}: {error_message}"
            )

        except httpx.RequestError as exc:
            result["error"] = f"Network error: {str(exc)}"

        except Exception as exc:
            result["error"] = str(exc)

        return result
