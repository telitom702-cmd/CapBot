import logging

from pyrogram import Client, filters

from helpers.ai import generate_caption

logger = logging.getLogger(__name__)

# Per-user language. Default is Bengali.
USER_LANGUAGES = {}


@Client.on_callback_query(filters.regex(r"^lang_(bn|en|hi|ko)$"))
async def save_language(client, query):
    # This handler intentionally does not process the callback.
    # Language selection is handled by settings.py.
    pass


@Client.on_message(
    filters.text
    & filters.private
    & ~filters.command(["start", "help", "settings"])
)
async def caption_handler(client, message):
    user_id = message.from_user.id if message.from_user else 0

    try:
        text = (message.text or "").strip()

        if not text:
            await message.reply_text("❌ Text পাওয়া যায়নি।")
            return

        language = USER_LANGUAGES.get(user_id, "বাংলা")

        logger.info(
            "CAPTION REQUEST | user_id=%s | language=%s | text_length=%s",
            user_id,
            language,
            len(text)
        )

        status = await message.reply_text(
            "🤖 AI caption তৈরি হচ্ছে... ⏳"
        )

        result = await generate_caption(
            text=text,
            language=language
        )

        await status.edit_text(
            f"✨ AI Caption\n\n{result}"
        )

        logger.info(
            "CAPTION SUCCESS | user_id=%s",
            user_id
        )

    except Exception as error:
        logger.exception(
            "CAPTION ERROR | user_id=%s | error=%s",
            user_id,
            error
        )

        try:
            await message.reply_text(
                "❌ Caption তৈরি করতে সমস্যা হয়েছে.\n\n"
                f"Error: `{type(error).__name__}`\n\n"
                "বিস্তারিত error Render/Acode log এবং bot.log-এ দেখুন।"
            )
        except Exception:
            logger.exception("Failed to send error message")
