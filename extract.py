import json
import os
import re
from datetime import datetime



# Account ID Generator

def generate_account_id(company_name: str) -> str:
    return company_name.lower().replace(" ", "_").replace("'", "")



# Create Base Account Memo (v1
def create_empty_account_memo(company_name: str) -> dict:
    return {
        "account_id": generate_account_id(company_name),
        "company_name": company_name,
        "business_hours": {
            "days": [],
            "start": "",
            "end": "",
            "timezone": ""
        },
        "office_address": "",
        "services_supported": [],
        "emergency_definition": [],
        "emergency_routing_rules": {},
        "non_emergency_routing_rules": {},
        "call_transfer_rules": {},
        "integration_constraints": [],
        "after_hours_flow_summary": "",
        "office_hours_flow_summary": "",
        "questions_or_unknowns": [],
        "notes": "",
        "version": "v1",
        "created_at": datetime.utcnow().isoformat()
    }



# Extract Structured Fields (Rule-Based, Safe)

def extract_basic_fields(transcript: str, memo: dict) -> dict:
    lower_text = transcript.lower()

    # Business Hours Extraction
    
    time_match = re.search(
        r"(\d{1,2})\s*(am|pm)\s*to\s*(\d{1,2})\s*(am|pm)",
        lower_text
    )

    tz_match = re.search(r"\b(cst|est|pst|mst)\b", lower_text)

    if time_match:
        start_hour = time_match.group(1) + " " + time_match.group(2).upper()
        end_hour = time_match.group(3) + " " + time_match.group(4).upper()

        memo["business_hours"]["start"] = start_hour
        memo["business_hours"]["end"] = end_hour
        memo["business_hours"]["days"] = ["Monday-Friday"]
        memo["office_hours_flow_summary"] = "Business hours mentioned in transcript."
    else:
        memo["questions_or_unknowns"].append("Business hours time not clearly found")

    if tz_match:
        memo["business_hours"]["timezone"] = tz_match.group(1).upper()
    else:
        memo["questions_or_unknowns"].append("Timezone not clearly found")

   
    # Emergency Definition Extraction
    
    emergency_match = re.search(r"emergency.*?include[s]?\s*(.*)", lower_text)

    if emergency_match:
        emergency_text = emergency_match.group(1).strip().capitalize()
        memo["emergency_definition"].append(emergency_text)
    else:
        memo["questions_or_unknowns"].append("Emergency definition not clearly found")

   
    # After Hours Logic

    after_hours_detected = "after hours" in lower_text

    if after_hours_detected:
        memo["after_hours_flow_summary"] = "After-hours routing mentioned in transcript."
    else:
        memo["questions_or_unknowns"].append("After-hours handling not clearly found")

   
    # Routing Rules Generation
   

    # Emergency routing
    memo["emergency_routing_rules"] = {
        "during_business_hours": "Transfer to technician immediately",
        "after_hours": "Transfer to technician immediately"
    }

    # Non-emergency routing
    memo["non_emergency_routing_rules"] = {
        "during_business_hours": "Collect caller details and schedule service",
        "after_hours": "Take message and schedule callback next business day"
    }

    # Call transfer rules
    memo["call_transfer_rules"] = {
        "max_retries": 2,
        "retry_delay_seconds": 10,
        "fallback": "If transfer fails, inform caller and collect callback number"
    }

    return memo



# Save Account Memo to Versioned Folder

def save_account_memo(memo: dict):
    account_id = memo["account_id"]
    base_path = f"outputs/accounts/{account_id}/v1"

    os.makedirs(base_path, exist_ok=True)

    file_path = os.path.join(base_path, "account_memo.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(memo, f, indent=4)

    print(f"✅ Account memo saved at {file_path}")