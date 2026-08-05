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

# 1. GENERIC CRYPTO MESSAGE
MESSAGE_TEXT = (
    "⚡ <b>WELCOME TO THE CRYPTO REWARDS BOT</b> ⚡\n\n"
    "💎 <b>Daily Yield & Staking Rewards</b>\n"
    "• High-yield daily returns on major crypto assets\n"
    "• Instant automated daily payouts\n"
    "• Earn team commissions & referral bonuses\n"
    "• Safe, secure, and decentralized\n\n"
    "<i>Select an option below to get started! 👇</i>"
)

# 2. INLINE BUTTONS
def get_crypto_keyboard():
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="📈 View Daily Rates", callback_data="rates")
    btn2 = InlineKeyboardButton(text="🪙 Start Staking", callback_data="stake")
    btn3 = InlineKeyboardButton(text="👥 Referral Program", callback_data="referral")
    markup.row(btn1, btn2)
    markup.row(btn3)
    return markup

users = set()

def send_promo(chat_id):
    """Sends the photo along with the text and inline keyboard."""
    # Build absolute path to ensure Render finds the image in the root directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, "promo.jpg")
    keyboard = get_crypto_keyboard()

    if os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as photo:
                bot.send_photo(
                    chat_id, 
                    photo, 
                    caption=MESSAGE_TEXT, 
                    parse_mode='HTML', 
                    reply_markup=keyboard
                )
                return
        except Exception as e:
            print(f"[ERROR] Failed sending photo: {e}", file=sys.stderr)
    else:
        print(f"[WARNING] image file not found at: {image_path}", file=sys.stderr)

    # Fallback to text message if photo fails or doesn't exist
    bot.send_message(
        chat_id, 
        MESSAGE_TEXT, 
        parse_mode='HTML', 
        reply_markup=keyboard, 
        disable_web_page_preview=True
    )

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

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    if call.data == "rates":
        response = "📊 <b>Current Daily Yield Rates:</b>\n\n• USDT: 3.5% / day\n• BTC: 2.8% / day\n• ETH: 3.0% / day"
    elif call.data == "stake":
        response = "🪙 <b>Staking Active:</b> Your account is ready to receive daily crypto distributions."
    elif call.data == "referral":
        response = "👥 <b>Referral Rewards:</b> Earn up to 0.6% commission on your team's total volume."
    else:
        response = "Welcome to Crypto Rewards!"

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, response, parse_mode='HTML')

def broadcast_scheduler():
    interval = 7200 
    while True:
        time.sleep(interval)
        print(f"Broadcasting scheduled crypto update to {len(users)} users...")
        for user_id in list(users):
            send_promo(user_id)

if __name__ == "__main__":
    print("Launching Crypto Bot Worker...")
    
    scheduler_thread = threading.Thread(target=broadcast_scheduler, daemon=True)
    scheduler_thread.start()
    
    bot.infinity_polling()
