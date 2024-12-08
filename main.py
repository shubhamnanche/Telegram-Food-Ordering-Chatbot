import re
import asyncio
from typing import Final, Dict, Union
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Bot constants
TOKEN: Final = os.getenv("BOT_TOKEN")
BOT_USERNAME: Final = "@ssk_pro_bot"
ORDER_PREP_TIME: Final = 10  # seconds

# Menu
MENU: Dict[int, str] = {
    1: "Pizza",
    2: "Burger",
    3: "Schwarma",
    4: "Nuggets",
    5: "Brownie",
    6: "Pastry",
    7: "Baguette",
    8: "Ice cream",
}


# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    context.user_data.clear()
    menu_text = "\n".join([f"{key}. {value}" for key, value in MENU.items()])
    await update.message.reply_text(
        "Hello! Thanks for coming to our food stall. What can I get for you?\n"
        + menu_text
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command."""
    await update.message.reply_text("I am your waiter! Use /start to begin your order.")


# Utility functions
def handle_response(text: str, user_data: Dict[str, Union[str, int]]) -> str:
    """Process the user's input and update user data accordingly."""
    food_selected = user_data.get("food_selected", "")
    quantity_selected = user_data.get("quantity_selected", 0)

    if "yes" in text.lower() and quantity_selected > 0:
        user_data["is_ready_to_order"] = True
        return "Order confirmed! Preparing your food..."

    if "no" in text.lower():
        user_data.clear()
        return "Order cancelled! Use /start to start a new order."

    if not food_selected:
        for menu_item in MENU.values():
            if menu_item.lower() in text.lower():
                user_data["food_selected"] = menu_item
                return "How much quantity?"

    if food_selected and quantity_selected <= 0:
        matched = re.findall(r"\d+", text)
        if matched:
            user_data["quantity_selected"] = int(matched[0])
            return (
                f"You've ordered {matched[0]} {food_selected}(s). Are you ready to order? "
                f"Your order will be ready in {ORDER_PREP_TIME} seconds."
            )

    return "I do not understand what you wrote..."


async def order_ready(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message indicating the order is ready."""
    user_data = context.user_data
    food_selected = user_data.get("food_selected", "")
    quantity_selected = user_data.get("quantity_selected", 0)

    if food_selected and quantity_selected:
        await update.message.reply_text(
            f"Your order of {quantity_selected} {food_selected}(s) is ready! Would you like to order anything else?"
        )
        user_data.clear()


# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages."""
    text: str = update.message.text
    user_data = context.user_data

    response: str = handle_response(text, user_data)

    if user_data.get("is_ready_to_order"):
        user_data["is_ready_to_order"] = False
        await update.message.reply_text(response)
        await asyncio.sleep(ORDER_PREP_TIME)
        await order_ready(update, context)
    else:
        await update.message.reply_text(response)


# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates."""
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error)

    # Poll the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
