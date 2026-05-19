# Opal Airtable Campaign Tool

A FastAPI-based [Opal](https://www.optimizely.com/ai/) tool that creates campaign records in an Airtable base. Built using the [Opal Tools SDK](https://pypi.org/project/optimizely-opal.opal-tools-sdk/), this server exposes a single tool, `create_airtable_record`, which can be called by Opal to log marketing campaign details directly into Airtable.

## Features

- **FastAPI server** with a health-check root endpoint
- **Opal Tools SDK integration** — registers as a callable Opal tool
- **Airtable API integration** — creates a new record in your `Campaigns` table
- **Environment-based configuration** via `.env`
- **Structured input validation** with Pydantic

## Tool Overview

### `create_airtable_record`

Creates an Airtable record with campaign information.

**Input fields:**

| Field           | Type   | Description                                                                 |
| --------------- | ------ | --------------------------------------------------------------------------- |
| `campaign_name` | string | Name of the campaign                                                        |
| `initiated_by`  | string | Name of the person who initiated the campaign                               |
| `start_date`    | string | Start date of the campaign                                                  |
| `social_media`  | string | Which social media the content is for (e.g., LinkedIn, X, Instagram, Facebook) |
| `content`       | string | Content of the campaign                                                     |

## Prerequisites

- Python 3.9+
- An Airtable account with a base containing a `Campaigns` table
- An Airtable personal access token (PAT) with write access to your base
- Access to Opal (or any client that can call Opal tools)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-org>/<your-repo>.git
   cd <your-repo>
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt` yet, install directly:

   ```bash
   pip install fastapi uvicorn opal-tools-sdk python-dotenv pydantic
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
AUTH_TOKEN=Bearer patXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TABLE_ID=appXXXXXXXXXXXXXX
```

| Variable     | Description                                                                                  |
| ------------ | -------------------------------------------------------------------------------------------- |
| `AUTH_TOKEN` | Airtable authorization header value (must include the `Bearer ` prefix)                      |
| `TABLE_ID`   | The Airtable base ID (e.g., `appXXXXXXXXXXXXXX`) — the table name `Campaigns` is hardcoded   |

> **Note:** Your Airtable `Campaigns` table must contain the columns: `Campaign Name`, `Initiated By`, `Start Date`, `Social Media`, and `Content`.

## Running the Server

Start the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Replace `main` with the filename of the script if it's different.

Verify the server is running by visiting:

```
http://localhost:8000/
```

You should see:

```json
{ "message": "Server is running" }
```

The Opal tool discovery endpoint is automatically exposed by the Opal Tools SDK.

## Registering the Tool in Opal

1. Deploy the server to a publicly accessible URL (or expose it via a tunnel like ngrok during development).
2. In Opal, register the tool's discovery URL so the `create_airtable_record` tool becomes available to your agents.
3. Invoke the tool from Opal — Opal will pass the campaign parameters, and a new record will appear in your Airtable `Campaigns` table.

## Project Structure

```
.
├── main.py            # FastAPI app and Opal tool definition
├── requirements.txt   # Python dependencies
├── .env               # Environment variables (not committed)
└── README.md
```

## Error Handling

The tool raises descriptive exceptions when:

- The Airtable API returns a non-2xx status code
- The response is missing the expected `records` field
- The response body cannot be parsed as JSON

Errors are logged to stdout and propagated back through the Opal Tools SDK.

## Security Notes

- Never commit your `.env` file. Add it to `.gitignore`.
- Treat your `AUTH_TOKEN` like a password — rotate it if it's ever exposed.
- Consider scoping your Airtable PAT to only the base and permissions this tool requires.

## License

Specify your license here (e.g., MIT, Apache-2.0).

## Contributing

Contributions, issues, and feature requests are welcome. Please open an issue first to discuss any major changes.
