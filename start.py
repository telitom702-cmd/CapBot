import logging
from pyrogram import Client, filters

logger = logging.getLogger(__name__)


@Client.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    try:
        name = message.from_user.first_name if message.from_user else "User"

        await message.reply_text(
            f"👋 Hello {name}!\n\n"
            "🤖 Welcome to AI Caption Bot.\n\n"
            "📝 Caption তৈরি বা edit করতে আপনার text পাঠান.\n\n"
            "🌐 বাংলা • English • हिन्दी • 한국어\n\n"
            "Commands:\n"
            "/start - Start Bot\n"
            "/help - Help\n"
            "/settings - Language Settings"
        )

        logger.info(
            "START | user_id=%s",
            message.from_user.id if message.from_user else 0
        )

    except Exception:
        logger.exception("Error in /start command")
