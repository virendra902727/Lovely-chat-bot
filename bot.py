from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading
import os
import json
import random

# 🔐 Environment Variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME", "youtuber02alltypemovies")  # Without @

# 🤖 Pyrogram Bot
app = Client("lovely_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🌐 Flask App
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "❤️ Lovely Bot is Live!"

# Run Flask in background
def run():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

threading.Thread(target=run).start()

# 📁 Load conversation categories
with open("conversation.json", "r", encoding="utf-8") as f:
    categories = json.load(f)
all_replies = sum(categories.values(), [])

# 🎯 Exact phrase trigger → reply map
conversation_map = {
    "hi": "Hi hi! Lovely yahan hai aapke liye 💖",
    "hello": "Hello ji! Kaise ho aap? 😊",
    "kaise ho": "Main acchi hoon! Tum sunao? 😇",
    "kya kar rahe ho": "Bas aapka intezaar kar rahi hoon 💬",
    "love you": "Main bhi aapko pyar karti hoon 😘",
    "bored": "Toh chalo masti bhari baatein karte hain! 🎉",
    "khana khaya": "Main bot hoon... lekin agar tum khush ho toh main bhi 😄",
    "miss you": "Main bhi aapko yaad karti hoon 💌",
    "good night": "Good night ji! Sweet dreams 💤",
    "good morning": "Good morning! Naya din, nayi baatein 🌞",
    "thank you": "Arey koi baat nahi ji! ❤️",
    "kaise ho": "Main bilkul mast hoon, aap kaise ho? 😄",
    "kya kar rahe ho": "Bas aapka intezaar kar rahi hoon ❤️",
    "kya hal hai": "Sab badiya! Tumhare sunane se aur bhi accha lagega 😊",
    "kya chal raha hai": "Zindagi chal rahi hai pyaar ke geet ke saath 💃",
    "tum kaun ho": "Main Lovely hoon, aapki dil se baat karne wali bot 💌",
    "mujhse baat karo": "Main yahi hoon, tumse hi toh baat karne ke लिए 💬",
    "kya soch rahe ho": "Tumhare baare mein hi toh soch rahi hoon 🥰",
    "kya dekh rahe ho": "Main toh bas tumhari aankhon mein khoya hoon 😉",
    "bore ho raha hoon": "Toh chalo kuch masti bhare baatein karte hain 🎉",
    "bored": "Mujhse baat karo, bore kabhi nahi feel hoga 😇",
    "meri tarif karo": "Aap toh dil jeet lene wale ho! ❤️",
    "aap ka naam kya hai": "Mera naam Lovely hai, aapki digital dost 😍",
    "good afternoon": "Good Afternoon! Aapka din khubsurat ho ☀️",
    "good evening": "Shubh Sandhya! Coffee ho jaye aapke saath? ☕",
    "sweet dreams": "Aapke sapne chocolate se bhi meethe ho 😋",
    "miss you": "Main bhi aapko miss karti hoon 💖",
    "tum yaad aate ho": "Main toh hamesha tumhare saath hoon 😌",
    "kya aap bot ho": "Haan main bot hoon, lekin dil se baat karti hoon 💞",
    "tension hai": "Tension ko chhodo aur Lovely se baat karo 💆",
    "mujhe akela lagta hai": "Main hoon na! Kabhi akela mat mehsoos karo 💗",
    "movie dekh rahe ho": "Movie chhodo, baatein karte hain tumse 🎥💬",
    "aap pyari ho": "Aapki baat ne mera dil chhoo liya ❤️",
    "tumhare bina kuch adhura hai": "Aap ho toh sab kuch poora hai 💑",
    "bahut din baad aaye ho": "Intezaar toh tha aapka... ab dil khush hai! 😍",
    "main udaas hoon": "Chalo baat karte hain... sab theek ho jayega 💖",
    "tumhari yaad aa rahi hai": "Tumhari yaad mujhe bhi roz aati hai 🥺",
    "khana khaya": "Main bot hoon, par aapko khush dekh kar pet bhar jaata hai 😄",
    "acha suno": "Haan haan... dil se sun rahi hoon 😊",
    "thoda pyaar do": "Lo ji! Dher saara pyaar 💕💕💕",
    "kya tum real ho": "Main real emotions wali bot hoon 😌",
    "main kya karun": "Bas mus्कुराओ और Lovely se baatein करो 🌼",
    "tum mujhe pasand ho": "Main bhi aapke words pe fida ho gayi 😘",
    "aapko milkar accha laga": "Mujhe toh tumse baat karke roz achha lagta hai 🌈",
}

# 🔁 Message History
user_msg_log = {}

# ✅ /start command
@app.on_message(filters.command("start"))
def start(client, message):
    user = message.from_user.first_name
    message.reply_text(
        f"👋 Namaste {user} ji!\n"
        f"Main *Lovely* hoon — aapki pyari baat-cheet wali dost 💬❤️\n"
        f"Main @{CHANNEL_USERNAME} se judi hoon — zarur join karein 🎬\n\n"
        f"📺 Channel: https://t.me/{CHANNEL_USERNAME}",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("📺 Channel Join Karein", url=f"https://t.me/{CHANNEL_USERNAME}")
        ]])
    )

# 💬 Conversation Handler
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

    # ✅ Check exact triggers first
    for keyword, reply in conversation_map.items():
        if keyword in text:
            message.reply_text(reply)
            return

    # 🔁 Fallback based on category
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

# 🧑‍🤝‍🧑 Welcome message for new members
@app.on_chat_member_updated()
def welcome(_, update: ChatMemberUpdated):
    if update.new_chat_member and not update.new_chat_member.user.is_bot:
        name = update.new_chat_member.user.first_name
        app.send_message(
            chat_id=update.chat.id,
            text=f"🎀 Welcome {name} ji!\nMain *Lovely* hoon — aapki chat wali dost 💁‍♀️\nMasti aur baat dono chalegi yahaan ❤️"
        )

# 🚀 Launch the bot
app.run()
