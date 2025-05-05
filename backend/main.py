from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import requests
import os
import re
from dotenv import load_dotenv
from datetime import datetime
from fastapi.responses import PlainTextResponse, JSONResponse

load_dotenv()

app = FastAPI()

# Load environment variables
AXISCARE_API_TOKEN = os.getenv("AXISCARE_API_TOKEN")
AXISCARE_SITE_ID = os.getenv("AXISCARE_SITE_ID")
OPENPHONE_API_KEY = os.getenv("OPENPHONE_API_KEY")

AXISCARE_BASE_URL = "https://{AXISCARE_SITE_ID}.axiscare.com/api"

# Sample model of incoming webhook data (adjust fields as needed)
class OpenPhoneSummaryEvent(BaseModel):
    callId: str
    summary: str
    from_number: str
    to_number: str
    timestamp: str

@app.post("/webhook")
async def openphone_webhook(event: OpenPhoneSummaryEvent):
    print(f"Received webhook: {event}")

    if not (10 <= len(event.summary) <= 500):
        log_validation_failure(event)
        raise HTTPException(status_code=400, detail="Call summary must be between 10 and 500 characters.")

    formatted_phone = format_phone_number(event.from_number)
    print(f"Raw phone: {event.from_number}, Formatted phone: {formatted_phone}")

    caregiver_id = match_caregiver_by_phone(formatted_phone)
    if not caregiver_id:
        log_phone_not_found(event.callId, formatted_phone)
        raise HTTPException(status_code=404, detail="Caregiver not found")

    update_success = update_caregiver_notes(caregiver_id, event.summary)
    if not update_success:
        raise HTTPException(status_code=500, detail="Failed to update caregiver profile")

    if not sanity_check(caregiver_id, event.summary, formatted_phone):
        raise HTTPException(status_code=500, detail="Sanity check failed")

    return {"status": "ok"}

@app.get("/logs/validation-failures", response_class=PlainTextResponse)
def get_validation_failures():
    if not os.path.exists("validation_failures.log"):
        return "No validation failures logged."
    with open("validation_failures.log", "r") as f:
        return f.read()

@app.get("/mock/caregiver")
def mock_caregiver():
    return {
        "id": "fake-id-123",
        "phone": "1-512-555-1234",
        "notes": "Previous notes."
    }

@app.post("/mock/correct")
def correct_mock():
    fake_id = "fake-id-123"
    corrected_summary = "Mock corrected summary that is meaningful."
    corrected_phone = "1-512-555-1234"
    print(f"Correcting record for {fake_id} with summary: {corrected_summary}")
    return JSONResponse({"corrected": True, "caregiver_id": fake_id, "summary": corrected_summary})

def log_validation_failure(event: OpenPhoneSummaryEvent):
    """Log invalid call summaries that fail length check."""
    timestamp = datetime.utcnow().isoformat()
    log_message = (
        f"[VALIDATION FAILURE] {timestamp} - Call ID: {event.callId}, "
        f"From: {event.from_number}, To: {event.to_number}, "
        f"Summary Length: {len(event.summary)}\nSummary: {event.summary}\n"
    )
    print(log_message)
    with open("validation_failures.log", "a") as log_file:
        log_file.write(log_message)

def log_phone_not_found(call_id: str, phone: str):
    """Log when a caregiver phone number is not found."""
    timestamp = datetime.utcnow().isoformat()
    log_message = f"[PHONE NOT FOUND] {timestamp} - Call ID: {call_id}, Phone: {phone}\n"
    print(log_message)
    with open("validation_failures.log", "a") as log_file:
        log_file.write(log_message)

def format_phone_number(phone: str) -> str:
    """Format phone number as X-XXX-XXX-XXXX"""
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 11:
        return f"{digits[0]}-{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    elif len(digits) == 10:
        return f"1-{digits[0:3]}-{digits[3:6]}-{digits[6:]}"
    return phone

def match_caregiver_by_phone(phone_number: str):
    """Match caregiver in AxisCare by phone number"""
    headers = {"Authorization": f"Bearer {AXISCARE_API_TOKEN}"}
    response = requests.get(f"{AXISCARE_BASE_URL}/caregivers", headers=headers)

    if response.status_code != 200:
        print("Failed to fetch caregivers from AxisCare")
        return None

    caregivers = response.json()
    for caregiver in caregivers:
        if caregiver.get("phone") == phone_number:
            return caregiver.get("id")

    return None

def update_caregiver_notes(caregiver_id: str, summary: str):
    """Append call summary to caregiver notes"""
    headers = {
        "Authorization": f"Bearer {AXISCARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "notes": f"OpenPhone Summary:\n{summary}"
    }
    response = requests.patch(f"{AXISCARE_BASE_URL}/caregivers/{caregiver_id}", json=payload, headers=headers)

    return response.status_code == 200

def sanity_check(caregiver_id: str, expected_summary: str, expected_phone: str) -> bool:
    """Verify that the caregiver's notes and phone number match the expected values."""
    headers = {"Authorization": f"Bearer {AXISCARE_API_TOKEN}"}
    response = requests.get(f"{AXISCARE_BASE_URL}/caregivers/{caregiver_id}", headers=headers)

    if response.status_code != 200:
        print("Sanity check failed: unable to retrieve caregiver profile.")
        return False

    caregiver_data = response.json()
    notes = caregiver_data.get("notes", "")
    phone = caregiver_data.get("phone", "")

    print(f"Sanity check - expected phone: {expected_phone}, actual phone: {phone}")
    print(f"Sanity check - expected summary fragment: {expected_summary[:30]}...")

    if expected_summary not in notes:
        print("Sanity check failed: summary text not found in notes.")
        return False

    if expected_phone != phone:
        print(f"Sanity check failed: expected phone {expected_phone}, got {phone}.")
        return False

    return True
