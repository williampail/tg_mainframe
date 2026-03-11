from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, CHANNEL_ID

bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def publish_to_channel(text: str) -> int:
    """
    Publish a message to the configured Telegram channel.
    
    Args:
        text: The message text to publish
        
    Returns:
        The message_id of the published message
    """
    message = await bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        parse_mode="HTML"
    )
    return message.message_id


async def publish_to_channel_with_media(text: str, photo_file_id: str) -> int:
    """
    Publish a message with photo to the configured Telegram channel.
    
    Args:
        text: The caption text
        photo_file_id: The file_id of the photo to send
        
    Returns:
        The message_id of the published message
    """
    message = await bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=photo_file_id,
        caption=text,
        parse_mode="HTML"
    )
    return message.message_id
