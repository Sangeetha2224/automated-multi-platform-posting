# Automated Multi-Platform Posting System

A Python FastAPI application that accepts a message through a REST API and publishes it across multiple platforms. Each platform is handled independently, so a failure on one platform does not stop the remaining platforms.

## 1. Project Overview

This project provides a single API endpoint to distribute a message across multiple platforms.

The application validates the input message, selects the configured platforms internally, attempts to publish the message, and returns the result for each platform.

### Technologies Used

- Python 3
- FastAPI
- Pydantic
- HTTPX
- Uvicorn
- Python-dotenv
- REST APIs

### Integrated Platforms

1. Bluesky
2. Mastodon
3. Discord
4. DEV.to
5. GitHub

## 2. Features

- REST API built with FastAPI.
- Accepts messages up to 200 characters.
- Validates that the message contains exactly one URL.
- Validates the URL format.
- Selects platforms internally; the client does not need to specify platforms.
- Attempts to publish to all configured platforms.
- Handles platform failures independently.
- Continues processing even if one platform fails.
- Returns individual platform status and error details.
- Keeps API credentials in environment variables.

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
│   │   ├── github.py
│   │   ├── reddit.py
│   │   └── telegram.py
│   │
│   └── services/
│       ├── __init__.py
│       └── posting_service.py
│
├── tests/
│   └── test_posting.py
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── discord_service.py
├── test_bluesky.py
└── test_mastodon.py
```

## 4. Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- API credentials for the platforms you want to configure

### Step 1: Clone the Repository

```bash
git clone https://github.com/Sangeetha2224/automated-multi-platform-posting.git
cd automated-multi-platform-posting
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

**Command Prompt:**
```bash
venv\Scripts\activate
```

**Git Bash:**
```bash
source venv/Scripts/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root directory.

Use `.env.example` as a reference and add your own API credentials:

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

Replace the empty values with your own credentials.

**Important:** Never upload your `.env` file or API credentials to GitHub.

## 5. Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 4000 --reload
```

The application will run at:

```text
http://127.0.0.1:4000
```

### API Documentation

Open the following URL in your browser to access the interactive Swagger documentation:

```text
http://127.0.0.1:4000/docs
```

## 6. API Endpoint

### POST /posting

Accepts a message and attempts to publish it to the configured platforms.

**Request URL:**

```text
http://127.0.0.1:4000/posting
```

**Method:** `POST`

**Request Body:**

```json
{
  "message": "Check out our latest update: https://example.com"
}
```

### Validation Rules

- Message must not be empty.
- Message must contain no more than 200 characters.
- Message must contain exactly one URL.
- URL must use HTTP or HTTPS.
- Invalid requests are rejected before platform publishing begins.

## 7. Response Format

The API returns an overall result and individual results for each configured platform.

### Example Response

The following is an illustrative response showing the response structure. Actual status, URL, date, time, and error values depend on the platform API responses.

```json
{
  "success": true,
  "results": [
    {
      "platform": "Bluesky",
      "status": "success",
      "posted_url": "https://bsky.app/profile/example/post/example-id",
      "public_access": true,
      "date": "2026-11-18",
      "time": "10:30:00",
      "error": null
    },
    {
      "platform": "Mastodon",
      "status": "success",
      "posted_url": "https://mastodon.social/@example/example-id",
      "public_access": true,
      "date": "2026-11-18",
      "time": "10:30:01",
      "error": null
    },
    {
      "platform": "Discord",
      "status": "success",
      "posted_url": null,
      "public_access": false,
      "date": "2026-11-18",
      "time": "10:30:02",
      "error": null
    },
    {
      "platform": "DEV.to",
      "status": "success",
      "posted_url": "https://dev.to/example/example-article",
      "public_access": false,
      "date": "2026-11-18",
      "time": "10:30:03",
      "error": null
    },
    {
      "platform": "GitHub",
      "status": "success",
      "posted_url": "https://github.com/example/repository/issues/1",
      "public_access": true,
      "date": "2026-11-18",
      "time": "10:30:04",
      "error": null
    }
  ]
}
```

**Note:** The response above is only an example. The actual implementation determines the returned values. Discord link and public-access values should reflect what the implementation can verify. DEV.to is currently configured to create an unpublished draft, so it is not publicly published.

### Response Fields

| Field | Description |
|---|---|
| success | Overall success indicator |
| results | List of platform results |
| platform | Platform name |
| status | Publishing status: success or failed |
| posted_url | URL of the created post, when available |
| public_access | Whether public access is confirmed |
| date | Date of the operation |
| time | Time of the operation |
| error | Error details, if an operation fails |

## 8. Error Handling

Each platform is processed independently.

If a platform API returns an error or a request fails:

- The error is captured for that platform.
- Its status is returned as `failed`.
- The remaining platforms are still processed.
- The API returns the individual results.

This prevents one platform failure from stopping the entire posting operation.

## 9. Platform Integration Details

| Platform | Integration | Operation |
|---|---|---|
| Bluesky | AT Protocol API | Creates a post |
| Mastodon | Mastodon REST API | Creates a status |
| Discord | Discord Webhook API | Sends a channel message |
| DEV.to | DEV.to API | Creates an unpublished article draft |
| GitHub | GitHub REST API | Creates an issue in the configured repository |

**Important implementation detail:** The DEV.to integration currently creates an unpublished draft rather than publishing a public article.

## 10. Security

- API credentials are stored in environment variables.
- The `.env` file is excluded from Git using `.gitignore`.
- `.env.example` contains variable names without actual secrets.
- Access tokens and webhook URLs should never be committed to the repository.

## 11. Running Tests

Run the test suite using:

```bash
pytest
```

## 12. API References

- [Bluesky AT Protocol Documentation](https://docs.bsky.app/)
- [Mastodon API Documentation](https://docs.joinmastodon.org/api/)
- [Discord Webhook Documentation](https://discord.com/developers/docs/resources/webhook)
- [DEV.to API Documentation](https://developers.forem.com/api)
- [GitHub REST API – Issues](https://docs.github.com/en/rest/issues/issues)

## 13. Author

**Sangeetha M**

- GitHub: https://github.com/Sangeetha2224/
- LinkedIn: https://www.linkedin.com/in/sangeetha-m29/

---

**Project:** Automated Multi-Platform Posting System  
**Framework:** FastAPI  
**Language:** Python