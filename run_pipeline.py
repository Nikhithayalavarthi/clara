import os

import re
from scripts.extract import (
    create_empty_account_memo,
    save_account_memo,
    extract_basic_fields
)
from scripts.generate_agent import generate_agent_spec

DEMO_FOLDER = "data/demo"


def read_transcript(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_company_name(transcript: str, filename: str) -> str:
    """
    Extract company name from transcript.
    Priority:
    1. Look for 'Customer Name:' pattern
    2. Fallback to filename (without extension)
    """

    # Try extracting from transcript
    match = re.search(r"customer\s*name\s*:\s*(.+)", transcript, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Fallback to filename
    fallback_name = os.path.splitext(filename)[0]
    print(f"⚠️ Customer Name not found. Using filename as account: {fallback_name}")
    return fallback_name


def main():
    print("🚀 Clara AI Automation Pipeline Started")

    if not os.path.exists(DEMO_FOLDER):
        print("❌ Demo folder not found.")
        return

    for filename in os.listdir(DEMO_FOLDER):
        if filename.endswith(".txt"):

            file_path = os.path.join(DEMO_FOLDER, filename)
            print(f"\n📄 Processing file: {filename}")

            transcript = read_transcript(file_path)

            company_name = extract_company_name(transcript, filename)
            print(f"🏢 Using Company Name: {company_name}")

            memo = create_empty_account_memo(company_name)
            memo = extract_basic_fields(transcript, memo)

            save_account_memo(memo)
            generate_agent_spec(memo)

    print("\n✅ Pipeline execution completed.")


if __name__ == "__main__":
    main()