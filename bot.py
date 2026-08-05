import os
import sys
import time
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN environment variable is missing!", file=sys.stderr)
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# 1. CRYPTO PROMO MESSAGE
MESSAGE_TEXT = (
    "🚀 <b>WELCOME TO MOBIUS PAY CRYPTO</b> 🚀\n\n"
    "⚡ <b>VIP daily return increased to 3.5% + 3📌</b>\n\n"
    "✅ Earn passive income daily on your crypto assets!\n"
    "✅ Up to 0.6% team commission & monthly salaries for team leaders.\n\n"
    "📢 <b>Official Channel:</b> https://t.me/mobiuspayofficial1\n"
    "💬 <b>Support:</b> @puya1521\n\n"
    "<i>Click the button below to register your account! 👇</i>"
)

# 2. CREATE INLINE BUTTON
def get_crypto_keyboard():
    markup = InlineKeyboardMarkup()
    register_btn = InlineKeyboardButton(
        text="🪙 REGISTER NOW ⏩", 
        url="https://app-web.mobiuspe-app.com/regist?code=earnmoney426"
    )
    markup.add(register_btn)
    return markup

users = set()

def send_promo(chat_id):
    """Sends the photo along with the crypto promo text and inline button."""
    image_filename = "promo.jpg"
    image_path = os.path.join(os.path.dirname(__file__), image_filename)
    keyboard = get_crypto_keyboard()
    
    try:
        if os.path.exists(image_path):
            with open(image_path, 'rb') as photo:
                bot.send_photo(
                    chat_id, 
                    photo, 
                    caption=MESSAGE_TEXT, 
                    parse_mode='HTML', 
                    reply_markup=keyboard
                )
        else:
            print(f"File not found at {image_path}, sending text with button.")
            bot.send_message(
                chat_id, 
                MESSAGE_TEXT, 
                parse_mode='HTML', 
                reply_markup=keyboard, 
                disable_web_page_preview=True
            )
    except Exception as e:
        print(f"Error sending photo to {chat_id}: {e}")
        try:
            bot.send_message(
                chat_id, 
                MESSAGE_TEXT, 
                parse_mode='HTML', 
                reply_markup=keyboard, 
                disable_web_page_preview=True
            )
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
    """Broadcasts to all active users every 2 hours."""
    interval = 7200 
    while True:
        time.sleep(interval)
        print(f"Broadcasting scheduled crypto update to {len(users)} users...")
        for user_id in list(users):
            send_promo(user_id)

if __name__ == "__main__":
    print("Launching Crypto Promotional Bot...")
    
    # Start background scheduler thread
    scheduler_thread = threading.Thread(target=broadcast_scheduler, daemon=True)
    scheduler_thread.start()
    
    bot.infinity_polling()
