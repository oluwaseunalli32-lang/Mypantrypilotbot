import os
import sys
import telebot

# 1. Fetch the token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN environment variable is missing!", file=sys.stderr)
    sys.exit(1)

# 2. Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Simple local database of recipes based on keywords
RECIPES = [
    {
        "name": "Classic Egg Fried Rice",
        "ingredients": ["egg", "rice", "onion", "soy sauce"],
        "instructions": "1. Heat oil in a pan and sauté chopped onions.\n2. Push onions aside, crack eggs into the pan, and scramble.\n3. Add cooked rice and toss everything together.\n4. Drizzle with soy sauce and stir-fry on high heat for 2 minutes."
    },
    {
        "name": "Quick Garlic Chicken Rice",
        "ingredients": ["chicken", "rice", "garlic", "oil"],
        "instructions": "1. Cut chicken into bite-sized pieces.\n2. Fry minced garlic in oil until fragrant, then add chicken and cook until brown.\n3. Stir in your cooked rice, season with salt/pepper, and serve hot."
    },
    {
        "name": "Simple Tomato Beef Pasta",
        "ingredients": ["beef", "tomato", "pasta", "onion"],
        "instructions": "1. Boil pasta according to package instructions.\n2. Brown the ground beef with onions in a pan.\n3. Add chopped tomatoes or tomato sauce and simmer for 10 minutes.\n4. Toss the pasta into the sauce and mix well."
    },
    {
        "name": "Cheesy Tomato Omelet",
        "ingredients": ["egg", "tomato", "cheese"],
        "instructions": "1. Whisk eggs in a bowl with a pinch of salt.\n2. Pour into a hot, greased skillet.\n3. Place sliced tomatoes and cheese on one half.\n4. Fold over and cook until the cheese is beautifully melted."
    }
]

# /start and /help command handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "<b>🧑‍🍳 Welcome to PantryPilot!</b>\n\n"
        "Tell me what ingredients you have in your fridge (separated by commas), "
        "and I will look up a simple recipe for you!\n\n"
        "<i>Example: egg, rice, chicken</i>"
    )
    # Using parse_mode='HTML' to avoid Markdown rendering crashes
    bot.reply_to(message, welcome_text, parse_mode='HTML')

# Handler for incoming ingredient text
@bot.message_handler(func=lambda message: True)
def suggest_recipe(message):
    # Standardize input text
    user_input = message.text.lower()
    user_ingredients = [ing.strip() for ing in user_input.split(",") if ing.strip()]
    
    if not user_ingredients:
        bot.reply_to(message, "⚠️ Please enter at least one valid ingredient.", parse_mode='HTML')
        return

    matched_recipes = []

    # Find matches where at least one user ingredient hits a recipe staple
    for recipe in RECIPES:
        match_count = sum(1 for ing in user_ingredients if ing in recipe["ingredients"])
        if match_count > 0:
            matched_recipes.append((recipe, match_count))

    # Sort recipes by the highest number of ingredient matches
    matched_recipes.sort(key=lambda x: x[1], reverse=True)

    if not matched_recipes:
        no_match_text = (
            "<b>No exact match found!</b> 🧑‍🍳\n\n"
            "Try listing basic staples like: <i>egg, rice, chicken, beef, tomato, or pasta</i>."
        )
        bot.reply_to(message, no_match_text, parse_mode='HTML')
        return

    # Build the response message safely using HTML
    response = "<b>💡 Here is what you can make:</b>\n\n"
    
    # Show top 2 matching recipes max to keep it clean
    for recipe, count in matched_recipes[:2]:
        ingredients_list = ", ".join([f"<u>{i}</u>" for i in recipe["ingredients"]])
        response += f"🍳 <b>{recipe['name']}</b>\n"
        response += f"<b>Ingredients needed:</b> {ingredients_list}\n"
        response += f"<b>Instructions:</b>\n{recipe['instructions']}\n\n"
        response += "───────────────────\n\n"

    bot.reply_to(message, response, parse_mode='HTML')

if __name__ == "__main__":
    print("PantryPilot is launching...")
    # infinity_polling keeps the bot running even if individual requests time out or hit errors
    bot.infinity_polling()
    
