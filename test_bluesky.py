import asyncio

from app.platforms.bluesky import BlueskyPlatform


async def main():

    bluesky = BlueskyPlatform()

    message = (
        "Testing automated posting "
        "https://example.com"
    )

    result = await bluesky.post(message)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())