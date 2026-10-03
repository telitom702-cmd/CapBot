import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)

LANGUAGES = {
    "bn": "বাংলা",
    "en": "English",
    "hi": "हिन्दी",
    "ko": "한국어",
}


@Client.on_message(filters.command("settings") & filters.private)
async def settings_command(client, message):
    try:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🇧🇩 বাংলা", callback_data="lang_bn"),
                InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            ],
            [
                InlineKeyboardButton("🇮🇳 हिन्दी", callback_data="lang_hi"),
                InlineKeyboardButton("🇰🇷 한국어", callback_data="lang_ko"),
            ],
        ])

        await message.reply_text(
            "⚙️ Caption Language নির্বাচন করুন:",
            reply_markup=keyboard
        )

    except Exception:
        logger.exception("Error in /settings command")


@Client.on_callback_query(filters.regex(r"^lang_(bn|en|hi|ko)$"))
async def language_callback(client, query):
    try:
        code = query.data.split("_", 1)[1]
        language = LANGUAGES[code]

        await query.answer(f"Language: {language}")

        await query.message.edit_text(
            f"✅ Language selected: {language}\n\n"
            "এখন আপনার caption/text পাঠান।"
        )

    except Exception:
        logger.exception("Language callback failed")
        await query.answer("❌ Error occurred", show_alert=True)
