
import asyncio

from app.platforms.mastodon import MastodonPlatform


async def main():

    mastodon = MastodonPlatform()

    message = (
        "Testing Mastodon API integration "
        "https://example.com"
    )

    result = await mastodon.post(message)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
