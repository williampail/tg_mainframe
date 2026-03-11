import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from config import TELEGRAM_BOT_TOKEN
from style_rewriter import rewrite_post
from channel_publisher import publish_to_channel, publish_to_channel_with_media

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    await update.message.reply_text(
        "👋 Bot is ready!\n\n"
        "Forward any post to me and I'll rewrite it in your style "
        "and publish it to the channel.\n\n"
        "Commands:\n"
        "/start - Show this message\n"
        "/status - Check bot status"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command."""
    await update.message.reply_text("✅ Bot is running and ready to receive posts!")


async def handle_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle forwarded posts - rewrite and publish to channel."""
    user_message = await update.message.reply_text("⏳ Processing...")
    
    try:
        # Get the original message (could be forwarded)
        original_message = update.message.forward_from or update.message
        
        # Extract text
        text = update.message.text or update.message.caption
        if not text:
            await user_message.edit_text("❌ Please forward a message with text or caption.")
            return
        
        # Rewrite the post
        await user_message.edit_text("✍️ Rewriting in your style...")
        rewritten_text = rewrite_post(text)
        
        # Publish to channel
        await user_message.edit_text("📢 Publishing to channel...")
        
        # Check if there's media
        if update.message.photo:
            # Get the largest photo
            photo = update.message.photo[-1]
            await publish_to_channel_with_media(rewritten_text, photo.file_id)
        else:
            await publish_to_channel(rewritten_text)
        
        await user_message.edit_text("✅ Successfully published to channel!")
        
    except Exception as e:
        logger.error(f"Error processing post: {e}")
        await user_message.edit_text(f"❌ Error: {str(e)}")


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    
    # Handle forwarded messages (posts from other channels)
    application.add_handler(MessageHandler(
        filters.FORWARDED & (filters.TEXT | filters.CAPTION | filters.PHOTO),
        handle_post
    ))
    
    # Error handler
    application.add_error_handler(handle_error)
    
    # Start the bot
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
