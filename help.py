import logging
from pyrogram import Client, filters

logger = logging.getLogger(__name__)


@Client.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    try:
        await message.reply_text(
            "📚 AI Caption Bot Help\n\n"
            "📝 নতুন Caption:\n"
            "যে বিষয়ে caption চান সেটি লিখে পাঠান।\n\n"
            "✏️ Caption Edit:\n"
            "পুরনো caption পাঠিয়ে কী পরিবর্তন চান তা লিখুন।\n\n"
            "🌐 Languages:\n"
            "🇧🇩 বাংলা\n"
            "🇬🇧 English\n"
            "🇮🇳 हिन्दी\n"
            "🇰🇷 한국어\n\n"
            "Commands:\n"
            "/start\n"
            "/help\n"
            "/settings"
        )
    except Exception:
        logger.exception("Error in /help command")
