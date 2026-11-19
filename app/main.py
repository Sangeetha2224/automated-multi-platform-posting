
from fastapi import FastAPI
from app.schemas import PostingRequest
from app.services.posting_service import publish_message

app = FastAPI(
    title="Automated Multi-Platform Posting API",
    version="1.0.0"
)


@app.get("/")
async def home():
    return {
        "message": "Automated Posting API is running"
    }


@app.post("/posting")
async def create_post(request: PostingRequest):

    result = await publish_message(request.message)

    return result
