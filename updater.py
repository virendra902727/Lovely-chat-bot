import json
import os

def add_reply_to_conversation(category, new_reply):
    file_path = "conversations.json"

    # Load existing data
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    # Ensure category exists
    if category not in data:
        data[category] = []

    # Avoid duplicate
    if new_reply not in data[category]:
        data[category].append(new_reply)

    # Save back to JSON
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Reply added to category '{category}'")
