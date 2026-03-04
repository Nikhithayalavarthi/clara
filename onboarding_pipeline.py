import os
import json
import re
from copy import deepcopy
from scripts.generate_agent import generate_agent_spec

ONBOARDING_FOLDER = "data/onboarding"
ACCOUNTS_FOLDER = "outputs/accounts"


def read_transcript(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_v1_memo(account_id):
    path = os.path.join(ACCOUNTS_FOLDER, account_id, "v1", "account_memo.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_updates(transcript, memo):
    updated_memo = deepcopy(memo)
    changes = {}

    lower_text = transcript.lower()

    # Business hours update
    time_match = re.search(
        r"(\d{1,2})\s*(am|pm)\s*to\s*(\d{1,2})\s*(am|pm)",
        lower_text
    )

    if time_match:
        new_start = time_match.group(1) + " " + time_match.group(2).upper()
        new_end = time_match.group(3) + " " + time_match.group(4).upper()

        if memo["business_hours"]["start"] != new_start:
            changes["business_hours.start"] = [memo["business_hours"]["start"], new_start]
            updated_memo["business_hours"]["start"] = new_start

        if memo["business_hours"]["end"] != new_end:
            changes["business_hours.end"] = [memo["business_hours"]["end"], new_end]
            updated_memo["business_hours"]["end"] = new_end

    # Retry update
    retry_match = re.search(r"retry.*?(\d+)", lower_text)
    if retry_match:
        new_retry = int(retry_match.group(1))
        old_retry = memo["call_transfer_rules"]["max_retries"]

        if old_retry != new_retry:
            changes["call_transfer_rules.max_retries"] = [old_retry, new_retry]
            updated_memo["call_transfer_rules"]["max_retries"] = new_retry

    return updated_memo, changes


def save_v2(account_id, updated_memo, changes):
    base_path = os.path.join(ACCOUNTS_FOLDER, account_id, "v2")
    os.makedirs(base_path, exist_ok=True)

    updated_memo["version"] = "v2"

    memo_path = os.path.join(base_path, "account_memo.json")
    with open(memo_path, "w", encoding="utf-8") as f:
        json.dump(updated_memo, f, indent=4)

    changelog = {
        "version_from": "v1",
        "version_to": "v2",
        "changes": changes
    }

    changelog_path = os.path.join(base_path, "changelog.json")
    with open(changelog_path, "w", encoding="utf-8") as f:
        json.dump(changelog, f, indent=4)

    generate_agent_spec(updated_memo)

    print(f"✅ v2 created for {account_id}")


def main():
    print("🚀 Onboarding Pipeline Started")

    for filename in os.listdir(ONBOARDING_FOLDER):
        if filename.endswith(".txt"):
            file_path = os.path.join(ONBOARDING_FOLDER, filename)
            transcript = read_transcript(file_path)

            first_line = transcript.split("\n")[0]
            account_name = first_line.split(":")[1].strip()
            account_id = account_name.lower().replace(" ", "_").replace("'", "")

            print(f"🔄 Updating account: {account_id}")

            v1_memo = load_v1_memo(account_id)

            updated_memo, changes = extract_updates(transcript, v1_memo)

            save_v2(account_id, updated_memo, changes)

    print("✅ Onboarding processing completed.")


if __name__ == "__main__":
    main()