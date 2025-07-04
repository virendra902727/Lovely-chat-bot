from updater import add_reply_to_conversation
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading
import os
import json
import random

#  Environments Variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME", "youtuber02alltypemovies")  # Channel Ka Naam Bina @ ke

#  Programm Client
app = Client("lovely_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

#  Flask App (Tumhare Bot Ko Hamesha Live Rakhega)
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "❤️ Lovely Bot is Live!"

#  Flask run in background
def run():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

threading.Thread(target=run).start()

#  Load conversations(Conversation.json file se)
with open("conversation.json", "r", encoding="utf-8") as f:
    categories = json.load(f)
all_replies = sum(categories.values(), [])

# 🔁 Message History
user_msg_log = {}

# 🟢 START command
@app.on_message(filters.command("start"))
def start(client, message):
    user = message.from_user.first_name
    message.reply_text(
        f"👋 Namaste {user} ji!\n"
        f"Main *Lovely* hoon — aapki pyari baat-cheet wali dost 💬❤️\n"
        f"Main @{CHANNEL_USERNAME} se judi hoon — zarur join karein 🎬\n\n"
        f"📺 Channel: https://t.me/{CHANNEL_USERNAME}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📺 Channel Join Karein", url=f"https://t.me/{CHANNEL_USERNAME}")]])
    )

# 💬 Conversation
@app.on_message(filters.text & filters.private)
def handle_private(_, message):
    text = message.text.lower().strip()

    if message.from_user.is_bot or text.startswith("/"):
        return

    user_id = message.from_user.id
    if user_id not in user_msg_log:
        user_msg_log[user_id] = {}
    user_msg_log[user_id][text] = user_msg_log[user_id].get(text, 0) + 1
    if user_msg_log[user_id][text] > 2:
        return

    if any(w in text for w in ["love", "crush", "miss"]):
        reply = random.choice(categories.get("love", all_replies))
    elif any(w in text for w in ["sad", "cry", "hurt"]):
        reply = random.choice(categories.get("sad", all_replies))
    elif any(w in text for w in ["happy", "great", "awesome"]):
        reply = random.choice(categories.get("happy", all_replies))
    elif any(w in text for w in ["hi", "hello", "kaise", "kya", "bored"]):
        reply = random.choice(categories.get("daily", all_replies))
    elif any(w in text for w in ["masti", "party", "enjoy"]):
        reply = random.choice(categories.get("fun", all_replies))
    else:
        reply = random.choice(all_replies)

    message.reply_text(reply)

#  New Member Join (Channel par naye member join hone par welcome message karega)
@app.on_chat_member_updated()
def welcome(_, update: ChatMemberUpdated):
    if update.new_chat_member and not update.new_chat_member.user.is_bot:
        name = update.new_chat_member.user.first_name
        app.send_message(
            chat_id=update.chat.id,
            text=f"🎀 Welcome {name} ji!\nMain *Lovely* hoon — aapki chat wali dost 💁‍♀️\nMasti aur baat dono chalegi yahaan ❤️"
        )

# 🚀 Start bot
app.run()
