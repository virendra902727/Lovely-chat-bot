import json
import os

def add_movie_to_json(title, msg_id, filename):
    movie_entry = {
        "title": title,
        "msg_id": msg_id,
        "filename": filename
    }

    if os.path.exists("Conversation.json"):
        with open("conversation.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(movie_entry)

    with open("Conversation.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)