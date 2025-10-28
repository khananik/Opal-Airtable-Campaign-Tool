import http.client
import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from opal_tools_sdk import ToolsService, tool
from pydantic import BaseModel, Field

load_dotenv()
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TABLE_ID = os.getenv("TABLE_ID")

app = FastAPI()
tools_service = ToolsService(app)


# Basic root endpoint to verify server is running
@app.get("/")
def root():
    return {"message": "Server is running"}


conn = http.client.HTTPSConnection("api.airtable.com")


class AirtableRecordInput(BaseModel):
    campaign_name: str = Field("", description="Name of the campaign")
    initiated_by: str = Field(
        "", description="Name of the person who initiated the campaign"
    )
    start_date: str = Field("", description="Start date of the campaign")
    social_media: str = Field(
        "",
        description="Which social media the content is created for. Example: LinkedIn, X, Instagram, Facebook.",
    )
    content: str = Field("", description="Content of the campaign")


@tool("create_airtable_record", "Creates and Airtable record with campaign information")
async def create_record(parameters: AirtableRecordInput):
    print("test")

    payload_dict = {
        "records": [
            {
                "fields": {
                    "Campaign Name": parameters.campaign_name,
                    "Initiated By": parameters.initiated_by,
                    "Start Date": parameters.start_date,
                    "Social Media": parameters.social_media,
                    "Content": parameters.content,
                }
            }
        ]
    }
    payload = json.dumps(payload_dict)

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "insomnia/11.3.0",
        "Authorization": AUTH_TOKEN,
    }
    try:
        conn.request("POST", f"/v0/{TABLE_ID}/Campaigns", payload, headers)

        res = conn.getresponse()
        data = res.read()

        if res.status != 200 and res.status != 201:
            raise Exception(
                f"Airtable API request failed with status code {res.status}: {data.decode('utf-8')}"
            )
        else:
            try:
                response_json = json.loads(data.decode("utf-8"))

                if "records" not in response_json or len(response_json["records"]) == 0:
                    raise Exception(
                        "Airtable API response is missing 'records' field or it is empty."
                    )
                return response_json

            except json.JSONDecodeError as e:
                raise Exception(f"Failed to parse Airtable API response: {str(e)}")
    except http.client.HTTPException as e:
        print("HTTP exception occurred:", str(e))
    except Exception as e:
        print("Unexpected error:", str(e))


# ---> uvicorn airtable_tool:app --reload --host 0.0.0.0 --port 8000
# ---> ngrok http 8000
