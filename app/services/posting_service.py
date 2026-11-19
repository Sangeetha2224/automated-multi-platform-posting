
from app.platforms.bluesky import BlueskyPlatform
from app.platforms.mastodon import MastodonPlatform
from app.platforms.discord import DiscordPlatform
from app.platforms.devto import DevtoPlatform
from app.platforms.github import GitHubPlatform


async def publish_message(message: str):

    platforms = [
        BlueskyPlatform(),
        MastodonPlatform(),
        DiscordPlatform(),
        DevtoPlatform(),
        GitHubPlatform()
    ]

    results = []

    for platform in platforms:
        try:
            result = await platform.post(message)
            results.append(result)

        except Exception as exc:
            results.append({
                "platform": platform.__class__.__name__,
                "status": "failed",
                "posted_url": None,
                "public_access": False,
                "date": None,
                "time": None,
                "error": str(exc)
            })

    successful_count = sum(
        1 for result in results
        if result["status"] == "success"
    )

    return {
        "success": successful_count > 0,
        "results": results
    }
