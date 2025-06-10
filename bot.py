import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- Configuration ---
# Set up logging to see errors and bot activity
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Bot Functions ---

# This function runs when a user first starts a chat with the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message with an interactive menu."""
    
    # Define the interactive buttons (the "keyboard")
    keyboard = [
        [InlineKeyboardButton("❓ View FAQs", callback_data='faq')],
        [InlineKeyboardButton("🗣️ Speak to a Human Agent", callback_data='agent')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # The welcome message text
    welcome_text = (
        'Welcome to our Customer Support Demo!\n\n'
        'I am a bot assistant. Please choose an option below to get started.'
    )
    
    # Send the message with the buttons
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# This function runs when a user clicks one of the inline buttons
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    
    # Acknowledge the button press to remove the "loading" icon on the user's end
    await query.answer()

    # Logic to handle different button presses based on their `callback_data`
    if query.data == 'faq':
        faq_text = (
            "*Frequently Asked Questions*\n\n"
            "*Q: What are your business hours?*\n"
            "A: Our team is available from 9 AM to 5 PM, Monday to Friday.\n\n"
            "Type /start to return to the main menu."
        )
        await query.edit_message_text(text=faq_text, parse_mode='Markdown')
        
    elif query.data == 'agent':
        agent_text = (
            "*Agent Handoff*\n\n"
            "All our human agents are currently assisting other customers. "
            "To ensure you get help, please send an email to support@example.com and one of our team members will get back to you shortly.\n\n"
            "Type /start to return to the main menu."
        )
        await query.edit_message_text(text=agent_text, parse_mode='Markdown')

# --- Main Bot Logic ---
def main() -> None:
    """Sets up and runs the Telegram Bot."""
    
    # Get the bot token from the environment variable
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TELEGRAM_TOKEN:
        logger.error("FATAL: TELEGRAM_TOKEN environment variable not set.")
        return

    # Create the Application object
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register the command and callback handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Start the bot by continuously polling for updates
    logger.info("Bot is starting...")
    application.run_polling()
    logger.info("Bot has stopped.")

if __name__ == '__main__':
    main()
