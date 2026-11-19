# Automated Multi-Platform Posting System

A Python-based REST API built using **FastAPI** that automatically publishes a user-provided message across multiple third-party platforms through their APIs.

## 1. Project Overview

The Automated Multi-Platform Posting System allows users to submit a short message containing exactly one call-to-action (CTA) URL through a single REST API endpoint.

The application validates the input and sends the message to five integrated platforms.

### Integrated Platforms

| Platform | Integration Method | Posting Type |
|---|---|---|
| Bluesky | Official AT Protocol API | Public post |
| Mastodon | Mastodon REST API | Public status |
| Discord | Discord Webhook API | Channel message |
| DEV.to | DEV.to Articles API | Unpublished article draft |
| GitHub | GitHub REST API | Repository issue |

**Note:** DEV.to currently creates an unpublished article draft. It does not automatically publish a public article.

## 2. Technologies Used

- Python 3.x
- FastAPI
- Uvicorn
- Pydantic
- HTTPX
- Pydantic Settings
- Python dotenv
- REST APIs
- JSON

## 3. Project Structure

```text
automated-posting/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── config.py
│   │
│   ├── platforms/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── bluesky.py
│   │   ├── mastodon.py
│   │   ├── discord.py
│   │   ├── devto.py
│   │   └── github.py
│   │
│   └── services/
│       ├── __init__.py
│       └── posting_service.py
│
├── tests/
│   └── test_posting.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 4. Features

- Single REST API endpoint for multi-platform posting.
- Message length validation (maximum 200 characters).
- Exactly one CTA URL validation.
- URL format validation.
- Automatic posting to five integrated platforms.
- Independent platform error handling.
- Continues processing even if an individual platform fails.
- Structured JSON response for each platform.
- Environment variables for API credentials.
- Asynchronous HTTP requests using HTTPX.

## 5. Installation and Setup

### Prerequisites

- Python 3.x
- Git
- API credentials for the supported platforms.

### Step 1: Clone the Repository

Clone the project from GitHub:

```bash
git clone https://github.com/Sangeetha2224/automated-multi-platform-posting.git
```

Navigate to the project directory:

```bash
cd automated-multi-platform-posting
```

Replace the placeholder with your actual repository URL.

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root.

Add the following variables with your own credentials:

```env
BLUESKY_HANDLE=
BLUESKY_PASSWORD=

MASTODON_BASE_URL=
MASTODON_ACCESS_TOKEN=

DISCORD_WEBHOOK_URL=

DEVTO_API_KEY=

GITHUB_TOKEN=
GITHUB_OWNER=
GITHUB_REPO=
```

**Security:** Never upload your `.env` file or expose API tokens, passwords, or webhook URLs in a public repository.

### Step 5: Run the Application

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 4000 --reload
```

The API will run at:

```text
http://127.0.0.1:4000
```

## 6. API Documentation

FastAPI provides interactive API documentation through Swagger UI.

Open:

```text
http://127.0.0.1:4000/docs
```

### API Endpoint

**Method:** POST

**Endpoint:**

```text
/posting
```

**Full URL:**

```text
http://127.0.0.1:4000/posting
```

### Request Body

```json
{
  "message": "Check out our latest business platform: https://example.com"
}
```

### Input Validation

- Message must not exceed 200 characters.
- Exactly one CTA URL must be included.
- The URL must use HTTP or HTTPS and contain a valid hostname.
- Platform selection is handled internally.

## 7. Response Format

The API returns the posting status separately for every integrated platform.

### Example Response

```json
{
  "success": true,
  "results": [
    {
      "platform": "Bluesky",
      "status": "success",
      "posted_url": "https://example.com/post/123",
      "public_access": true,
      "date": "2026-11-18",
      "time": "04:41:08",
      "error": null
    }
  ]
}
```

The above is an illustrative response. Actual URLs, timestamps, and platform statuses are returned by the integrations.

### Response Fields

| Field | Description |
|---|---|
| platform | Name of the integrated platform |
| status | Success or failed |
| posted_url | Created content URL, when available |
| public_access | Whether the content is publicly accessible |
| date | Posting date |
| time | Posting time |
| error | Error details, if any |

## 8. Error Handling

Each platform is processed independently.

If one platform fails, the application continues processing the remaining platforms.

The overall response indicates success if at least one platform succeeds.

## 9. Platform API Documentation

The application uses the following official API documentation:

- [Bluesky AT Protocol](https://docs.bsky.app/)
- [Mastodon API](https://docs.joinmastodon.org/api/)
- [Discord Webhook Documentation](https://discord.com/developers/docs/resources/webhook)
- [DEV.to API](https://developers.forem.com/api)
- [GitHub REST API – Issues](https://docs.github.com/en/rest/issues/issues)

## 10. Security

- API credentials are stored in environment variables.
- `.env` is excluded from Git using `.gitignore`.
- `.env.example` contains variable names without actual credentials.
- Access tokens and passwords should never be committed to the repository.

## 11. Future Improvements

- Publish DEV.to articles publicly after adding the required publishing workflow.
- Add retry handling for temporary API failures.
- Add automated unit and integration tests.
- Improve platform-specific public URL verification.
- Add structured logging.
- Deploy the FastAPI application to a cloud platform.

## 12. Author

**Sangeetha M.**

GitHub: https://github.com/Sangeetha2224/

LinkedIn: https://www.linkedin.com/in/sangeetha-m29/

---

**Project:** Automated Multi-Platform Posting System  
**Technology:** Python, FastAPI, HTTPX  
**Purpose:** Automated message publishing through multiple third-party APIs.
