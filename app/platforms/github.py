
import httpx
from datetime import datetime, timezone

from app.config import settings
from app.platforms.base import BasePlatform


class GitHubPlatform(BasePlatform):

    async def post(self, message: str) -> dict:

        now = datetime.now(timezone.utc)

        try:
            token = settings.GITHUB_TOKEN
            owner = settings.GITHUB_OWNER
            repo = settings.GITHUB_REPO

            if not token or not owner or not repo:
                raise ValueError("GitHub credentials are missing")

            url = f"https://api.github.com/repos/{owner}/{repo}/issues"

            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            }

            payload = {
                "title": "Automated Posting Update",
                "body": message
            }

            async with httpx.AsyncClient(timeout=30) as client:

                response = await client.post(
                    url,
                    headers=headers,
                    json=payload
                )

                if response.status_code != 201:
                   raise Exception(
                    f"GitHub API Error {response.status_code}: {response.text}"
                )

                data = response.json()

                return {
                    "platform": "GitHub",
                    "status": "success",
                    "posted_url": data.get("html_url"),
                    "public_access": True,
                    "date": now.strftime("%Y-%m-%d"),
                    "time": now.strftime("%H:%M:%S"),
                    "error": None
                }

        except Exception as exc:

            return {
                "platform": "GitHub",
                "status": "failed",
                "posted_url": None,
                "public_access": False,
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M:%S"),
                "error": str(exc)
            }
