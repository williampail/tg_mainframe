import logging
import signal
import sys
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from config import TELEGRAM_BOT_TOKEN, CHANNEL_ID
from style_rewriter import rewrite_post
from channel_publisher import publish_to_channel, publish_to_channel_with_media

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

application = None


def shutdown_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Received shutdown signal, stopping bot...")
    if application:
        application.stop()
    sys.exit(0)


# Register signal handlers for graceful shutdown
signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    await update.message.reply_text(
        "🤖 **MAINFRAME Bot**\n\n"
        "Я переписываю посты в стиле MAINFRAME и публикую в @mainframe_sh\n\n"
        "**Как использовать:**\n"
        "1. Перешли пост из другого канала\n"
        "2. Отправь команду /rewrite\n"
        "3. Я перепишу и опубликую\n\n"
        "**Команды:**\n"
        "/start - Эта справка\n"
        "/rewrite - Переписать и опубликовать последний пересланный пост\n"
        "/status - Проверить статус бота"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command."""
    await update.message.reply_text(
        "✅ **Бот работает нормально**\n\n"
        f"📡 Канал: `{CHANNEL_ID}`\n"
        f"🌐 Render: `{os.getenv('RENDER', 'Local')}`\n\n"
        "Готов переписывать посты!"
    )


async def rewrite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /rewrite command - rewrite and publish forwarded post."""
    user_message = update.message
    
    # Check if there's a forwarded message
    if not user_message.reply_to_message or not user_message.reply_to_message.forward_from:
        await user_message.reply_text(
            "❌ **Нет пересланного поста**\n\n"
            "Сначала перешли пост из канала, затем отправь /rewrite"
        )
        return
    
    forwarded_msg = user_message.reply_to_message
    
    # Extract text
    text = forwarded_msg.text or forwarded_msg.caption
    if not text:
        await user_message.reply_text(
            "❌ **Нет текста**\n\n"
            "Перешлите пост с текстом или подписью к фото"
        )
        return
    
    # Step 1: Acknowledge
    status_msg = await user_message.reply_text("⏳ **Принял!** Переписываю пост...")
    
    try:
        # Step 2: Rewrite
        logger.info(f"Rewriting post: {text[:100]}...")
        rewritten_text = rewrite_post(text)
        await status_msg.edit_text("✍️ **Переписал!** Публикую в канал...")
        
        # Step 3: Publish
        if forwarded_msg.photo:
            photo = forwarded_msg.photo[-1]
            await publish_to_channel_with_media(rewritten_text, photo.file_id)
        else:
            await publish_to_channel(rewritten_text)
        
        logger.info("Successfully published to channel")
        await status_msg.edit_text(
            "✅ **Опубликовано!**\n\n"
            f"Пост добавлен в {CHANNEL_ID}"
        )
        
    except Exception as e:
        logger.error(f"Error processing post: {e}")
        await status_msg.edit_text(
            f"❌ **Ошибка:** {str(e)[:200]}\n\n"
            "Попробуй ещё раз или проверь логи"
        )


async def handle_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle forwarded messages - just acknowledge, wait for /rewrite."""
    if update.message.forward_from or update.message.forward_from_chat:
        await update.message.reply_text(
            "👌 **Пост получен!**\n\n"
            "Отправь /rewrite чтобы переписать и опубликовать"
        )


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            f"⚠️ **Ошибка:** {str(context.error)[:100]}"
        )


def main():
    """Start the bot."""
    global application
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("rewrite", rewrite))
    
    # Handle forwarded messages (acknowledge only)
    application.add_handler(MessageHandler(
        filters.FORWARDED,
        handle_forward
    ))
    
    # Error handler
    application.add_error_handler(handle_error)
    
    # Start the bot
    logger.info("Bot is starting...")
    logger.info(f"Running on Render: {os.getenv('RENDER', 'Local')}")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        timeout=30
    )


if __name__ == "__main__":
    main()
