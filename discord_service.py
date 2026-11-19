import os
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def post_to_discord(message: str):
    if not DISCORD_WEBHOOK_URL:
        return {
            "platform": "Discord",
            "status": "failed",
            "error": "Webhook URL not configured"
        }

    try:
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json={"content": message},
            timeout=15
        )

        response.raise_for_status()

        return {
            "platform": "Discord",
            "status": "success",
            "error": None
        }

    except requests.RequestException as error:
        return {
            "platform": "Discord",
            "status": "failed",
            "error": str(error)
        }