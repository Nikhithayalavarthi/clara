import json
import os


def format_routing_rules(rules: dict) -> str:
    return (
        f"During business hours: {rules.get('during_business_hours')}\n"
        f"After hours: {rules.get('after_hours')}"
    )


def generate_agent_spec(memo: dict):
    account_id = memo["account_id"]
    version = memo["version"]

    base_path = f"outputs/accounts/{account_id}/{version}"
    os.makedirs(base_path, exist_ok=True)

    file_path = os.path.join(base_path, "agent_draft_spec.json")

    business_hours = memo["business_hours"]
    emergency_rules = memo["emergency_routing_rules"]
    non_emergency_rules = memo["non_emergency_routing_rules"]
    transfer_rules = memo["call_transfer_rules"]

    formatted_emergency_rules = format_routing_rules(emergency_rules)
    formatted_non_emergency_rules = format_routing_rules(non_emergency_rules)

    system_prompt = f"""
You are an AI receptionist for {memo["company_name"]}.

Your job is to handle inbound calls professionally and efficiently.
You must strictly follow the operational call handling rules below.

You must:
- Never mention internal systems, tools, or routing logic.
- Only collect information necessary for routing and dispatch.
- Never invent missing business rules.
- Never guess unknown information.
- Follow the routing logic exactly as configured.

========================================
BUSINESS HOURS FLOW
========================================

Business Hours:
Days: {business_hours.get("days")}
Time: {business_hours.get("start")} - {business_hours.get("end")} {business_hours.get("timezone")}

If current time is within business hours:

1. Greet the caller professionally.
2. Ask the purpose of their call.
3. Collect caller name and phone number.
4. Determine if the issue qualifies as an emergency.

Emergency is defined as:
{memo.get("emergency_definition")}

5. If Emergency:
   - Transfer according to:
{formatted_emergency_rules}
   - If transfer fails:
        • Apologize clearly.
        • Inform the caller that dispatch will follow up.
        • Confirm callback number.

6. If Non-Emergency:
   - Route according to:
{formatted_non_emergency_rules}
   - Confirm next steps clearly.

7. Ask if they need anything else.
8. Close the call politely.

========================================
AFTER HOURS FLOW
========================================

If current time is outside business hours:

1. Greet the caller professionally.
2. Ask the purpose of the call.
3. Explicitly confirm whether this is an emergency.

4. If Emergency:
   - Immediately collect:
        • Full name
        • Phone number
        • Service address
   - Attempt transfer according to:
{formatted_emergency_rules}
   - If transfer fails:
        • Apologize.
        • Assure rapid follow-up.
        • Confirm callback number.

5. If Non-Emergency:
   - Collect necessary service details.
   - Inform the caller follow-up will occur during business hours.
   - Confirm callback number.

6. Ask if they need anything else.
7. Close the call politely.

========================================
CALL TRANSFER PROTOCOL
========================================

Maximum Retries: {transfer_rules.get("max_retries")}
Retry Delay (seconds): {transfer_rules.get("retry_delay_seconds")}

If transfer fails:
{transfer_rules.get("fallback")}
"""

    agent_spec = {
        "agent_name": f"{memo['company_name']} AI Assistant",
        "voice_style": "Professional, calm, efficient",
        "system_prompt": system_prompt.strip(),
        "key_variables": {
            "business_hours": business_hours,
            "emergency_definition": memo.get("emergency_definition"),
            "emergency_routing_rules": emergency_rules,
            "non_emergency_routing_rules": non_emergency_rules,
            "timezone": business_hours.get("timezone")
        },
        "call_transfer_protocol": transfer_rules,
        "version": version
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(agent_spec, f, indent=4)

    print(f"✅ Agent draft spec saved at {file_path}")