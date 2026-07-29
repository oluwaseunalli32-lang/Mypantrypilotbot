import os
import sys
import time
import threading
import telebot

# 1. Environment and Bot initialization
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN environment variable is missing!", file=sys.stderr)
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# 2. Path to your promo image
IMAGE_PATH = "promo.jpg"

# 3. Message text to broadcast
MESSAGE_TEXT = (
    "✅ VIP has increased to 3.5% + 3📌\n\n"
    "🪙REGISTER HERE ⏩⏩\n\n"
    "https://app-web.mobiuspe-app.com/regist?code=earnmoney426\n\n\n"
    "✅ We offer team leader salaries and up to 0.6% team commission. "
    "Please contact us to apply for a team leader position. 🛒\n"
    "Official channel link ⭐️\n\n"
    "https://t.me/mobiuspayofficial1\n\n"
    "Contact support ⭐️@puya1521"
)

# Set to keep track of unique active user chat IDs
users = set()

def send_promo(chat_id):
    """Sends the promo image along with the caption text."""
    try:
        if os.path.exists(IMAGE_PATH):
            with open(IMAGE_PATH, 'rb') as photo:
                bot.send_photo(chat_id, photo, caption=MESSAGE_TEXT)
        else:
            # Fallback if the image file is missing
            bot.send_message(chat_id, MESSAGE_TEXT, disable_web_page_preview=True)
    except Exception as e:
        print(f"Failed to send message to {chat_id}: {e}")

# Command handler for /start and /help
@bot.message_handler(commands=['start', 'help'])
def start_handler(message):
    chat_id = message.chat.id
    users.add(chat_id)
    send_promo(chat_id)

# Handler for any generic text messages
@bot.message_handler(func=lambda message: True)
def default_handler(message):
    chat_id = message.chat.id
    users.add(chat_id)
    send_promo(chat_id)

def broadcast_scheduler():
    """Background worker loop that sends the message to all users every 2 hours."""
    # 2 hours = 7200 seconds
    interval = 7200 
    
    while True:
        time.sleep(interval)
        print(f"Broadcasting scheduled update to {len(users)} users...")
        
        # Iterate over a copy of the user set
        for user_id in list(users):
            send_promo(user_id)

if __name__ == "__main__":
    print("Launching promotional bot worker...")
    
    # Start the 2-hour scheduler in a separate daemon thread
    scheduler_thread = threading.Thread(target=broadcast_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Start long-polling
    bot.infinity_polling()
