
import httpx
from datetime import datetime, timezone

from app.config import settings
from app.platforms.base import BasePlatform

class BlueskyPlatform(BasePlatform):

    BASE_URL = "https://bsky.social"

    async def post(self, message: str) -> dict:

        now = datetime.now(timezone.utc)

        result = {
            "platform": "Bluesky",
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": None
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:

                # 1. Authenticate with Bluesky

                auth_response = await client.post(
                    f"{self.BASE_URL}/xrpc/com.atproto.server.createSession",
                    json={
                        "identifier": settings.BLUESKY_HANDLE,
                        "password": settings.BLUESKY_PASSWORD
                    }
                )

                auth_response.raise_for_status()

                session = auth_response.json()

                access_token = session["accessJwt"]
                account_did = session["did"]

                # 2. Create post

                created_at = datetime.now(
                    timezone.utc
                ).isoformat().replace("+00:00", "Z")

                post_response = await client.post(
                    f"{self.BASE_URL}/xrpc/com.atproto.repo.createRecord",
                    headers={
                        "Authorization": f"Bearer {access_token}"
                    },
                    json={
                        "repo": account_did,
                        "collection": "app.bsky.feed.post",
                        "record": {
                            "text": message,
                            "createdAt": created_at
                        }
                    }
                )

                post_response.raise_for_status()

                post_data = post_response.json()

                post_uri = post_data["uri"]
                record_key = post_uri.rsplit("/", 1)[-1]

                # 3. Verify public accessibility

                public_response = await client.get(
                    "https://public.api.bsky.app/xrpc/app.bsky.feed.getPosts",
                    params={"uris": post_uri}
                )

                public_access = False

                if public_response.is_success:
                    public_access = bool(
                        public_response.json().get("posts")
                    )

                # 4. Return actual posting result

                result.update({
                    "status": "success",
                    "posted_url": (
                        f"https://bsky.app/profile/"
                        f"{settings.BLUESKY_HANDLE}/post/{record_key}"
                    ),
                    "public_access": public_access,
                    "date": now.strftime("%Y-%m-%d"),
                    "time": now.strftime("%H:%M:%S")
                })

        except httpx.HTTPStatusError as exc:

            try:
                error_data = exc.response.json()
                error_message = error_data.get(
                    "message",
                    error_data.get("error", exc.response.text)
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