import os
import sys
import time
import threading
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN environment variable is missing!", file=sys.stderr)
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# 1. MESSAGE TEXT
MESSAGE_TEXT = (
    "✅ VIP has increased to 3.5% + 3📌\n\n"
    "🪙REGISTER HERE ⏩⏩\n"
    "https://app-web.mobiuspe-app.com/regist?code=earnmoney426\n\n"
    "✅ We offer team leader salaries and up to 0.6% team commission. "
    "Please contact us to apply for a team leader position. 🛒\n\n"
    "Official channel link ⭐️\n"
    "https://t.me/mobiuspayofficial1\n\n"
    "Contact support ⭐️@puya1521"
)

users = set()

def send_promo(chat_id):
    """Sends the photo along with the promo caption."""
    # Ensure working directory path is absolute
    image_filename = "promo.jpg"
    image_path = os.path.join(os.path.dirname(__file__), image_filename)
    
    try:
        if os.path.exists(image_path):
            with open(image_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, caption=MESSAGE_TEXT)
        else:
            print(f"File not found at {image_path}, falling back to text.")
            bot.send_message(chat_id, MESSAGE_TEXT, disable_web_page_preview=True)
    except Exception as e:
        print(f"Error sending photo to {chat_id}: {e}")
        # Fallback to plain text if Telegram rejects the photo request
        try:
            bot.send_message(chat_id, MESSAGE_TEXT, disable_web_page_preview=True)
        except Exception as inner_e:
            print(f"Failed to send text fallback: {inner_e}")

@bot.message_handler(commands=['start', 'help'])
def start_handler(message):
    chat_id = message.chat.id
    users.add(chat_id)
    send_promo(chat_id)

@bot.message_handler(func=lambda message: True)
def default_handler(message):
    chat_id = message.chat.id
    users.add(chat_id)
    send_promo(chat_id)

def broadcast_scheduler():
    """Broadcasts to all known users every 2 hours (7200 seconds)."""
    interval = 7200 
    while True:
        time.sleep(interval)
        print(f"Broadcasting scheduled update to {len(users)} users...")
        for user_id in list(users):
            send_promo(user_id)

if __name__ == "__main__":
    print("Launching promotional bot worker...")
    
    # Start broadcast timer in background
    scheduler_thread = threading.Thread(target=broadcast_scheduler, daemon=True)
    scheduler_thread.start()
    
    bot.infinity_polling()
