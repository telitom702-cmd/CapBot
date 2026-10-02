import os
import re
import logging
import asyncio
from aiohttp import web
from pyrogram import Client, filters
from pyrogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient

# =========================================================
# CONFIG IMPORT FROM info.py
# =========================================================
from info import BOT_TOKEN, API_ID, API_HASH, DB_URL, ADMIN_ID, PORT

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

log = logging.getLogger(__name__)

# =========================================================
# DATABASE
# =========================================================

# নিশ্চিত হোন DB_URL খালি নয়
if not DB_URL:
    raise ValueError("Database URL is missing! Please set DB_URL in info.py or environment variables.")

mongo = AsyncIOMotorClient(DB_URL)
db = mongo["post_edit_bot"]
rules_db = db["rules"]

# =========================================================
# PYROGRAM
# =========================================================

app = Client(
    "PostEditBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =========================================================
# DEFAULT RULES
# =========================================================

DEFAULT_RULES = [
    r"\[CineBari\.com\]",
    r"\[MovieBaaz\.com\]\s*-?",
]

# =========================================================
# DATABASE FUNCTIONS
# =========================================================

async def get_rules():
    data = await rules_db.find_one({"_id": "global"})

    if not data:
        await rules_db.update_one(
            {"_id": "global"},
            {"$set": {"rules": DEFAULT_RULES}},
            upsert=True
        )
        return DEFAULT_RULES

    return data.get("rules", [])


async def save_rules(rules):
    await rules_db.update_one(
        {"_id": "global"},
        {"$set": {"rules": rules}},
        upsert=True
    )


# =========================================================
# CAPTION EDITOR
# =========================================================

async def clean_caption(caption):
    if not caption:
        return caption

    rules = await get_rules()

    new_caption = caption

    for pattern in rules:
        try:
            new_caption = re.sub(
                pattern,
                "",
                new_caption,
                flags=re.IGNORECASE
            )
        except Exception as e:
            log.error(f"Regex error: {pattern} | {e}")

    # একাধিক blank line কমানো
    new_caption = re.sub(r"\n{3,}", "\n\n", new_caption)

    # লাইনের শুরু/শেষের extra space
    new_caption = "\n".join(
        line.rstrip()
        for line in new_caption.splitlines()
    )

    return new_caption.strip()


# =========================================================
# CHANNEL POST EDITOR
# =========================================================

@app.on_message(filters.channel)
async def edit_channel_post(client: Client, message: Message):

    # Caption না থাকলে কিছু করার নেই
    if not message.caption:
        return

    try:
        old_caption = message.caption
        new_caption = await clean_caption(old_caption)

        # কোনো পরিবর্তন না হলে edit করার দরকার নেই
        if new_caption == old_caption:
            return

        await client.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.id,
            caption=new_caption
        )

        log.info(
            f"Edited post: {message.chat.title} | "
            f"Message ID: {message.id}"
        )

    except Exception as e:
        log.error(
            f"Failed to edit post {message.id}: {e}"
        )


# =========================================================
# ADMIN COMMAND CHECK
# =========================================================

def is_admin(message):
    return (
        message.from_user
        and message.from_user.id == ADMIN_ID
    )


# =========================================================
# /start
# =========================================================

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):

    if not is_admin(message):
        await message.reply_text(
            "❌ আপনি এই Bot ব্যবহার করার অনুমতি পাননি।"
        )
        return

    await message.reply_text(
        "🤖 **Post Edit Bot Online!**\n\n"
        "এই Bot Channel Post-এর caption automatically edit করবে.\n\n"
        "Commands:\n"
        "`/rules` - বর্তমান rules দেখুন\n"
        "`/add text` - নতুন text remove rule\n"
        "`/remove text` - rule remove করুন\n"
        "`/test text` - text test করুন"
    )


# =========================================================
# /rules
# =========================================================

@app.on_message(filters.command("rules") & filters.private)
async def rules_command(client, message):

    if not is_admin(message):
        return

    rules = await get_rules()

    if not rules:
        await message.reply_text("📋 কোনো rule নেই।")
        return

    text = "📋 **Current Rules:**\n\n"

    for i, rule in enumerate(rules, 1):
        text += f"`{i}. {rule}`\n"

    await message.reply_text(text)


# =========================================================
# /add
# =========================================================

@app.on_message(filters.command("add") & filters.private)
async def add_rule(client, message):

    if not is_admin(message):
        return

    if len(message.command) < 2:
        await message.reply_text(
            "ব্যবহার:\n"
            "`/add [CineBari.com]`"
        )
        return

    value = message.text.split(" ", 1)[1].strip()

    # User-এর normal text কে regex-safe করা
    pattern = re.escape(value)

    rules = await get_rules()

    if pattern in rules:
        await message.reply_text(
            "⚠️ এই rule আগে থেকেই আছে।"
        )
        return

    rules.append(pattern)
    await save_rules(rules)

    await message.reply_text(
        f"✅ Rule added:\n`{value}`"
    )


# =========================================================
# /remove
# =========================================================

@app.on_message(filters.command("remove") & filters.private)
async def remove_rule(client, message):

    if not is_admin(message):
        return

    if len(message.command) < 2:
        await message.reply_text(
            "ব্যবহার:\n"
            "`/remove [CineBari.com]`"
        )
        return

    value = message.text.split(" ", 1)[1].strip()
    pattern = re.escape(value)

    rules = await get_rules()

    if pattern not in rules:
        await message.reply_text(
            "❌ এই rule পাওয়া যায়নি।"
        )
        return

    rules.remove(pattern)
    await save_rules(rules)

    await message.reply_text(
        f"🗑 Rule removed:\n`{value}`"
    )


# =========================================================
# /test
# =========================================================

@app.on_message(filters.command("test") & filters.private)
async def test_command(client, message):

    if not is_admin(message):
        return

    if len(message.command) < 2:
        await message.reply_text(
            "ব্যবহার:\n"
            "`/test আপনার caption এখানে`"
        )
        return

    original = message.text.split(" ", 1)[1]

    result = await clean_caption(original)

    await message.reply_text(
        "**Original:**\n"
        f"{original}\n\n"
        "**After Edit:**\n"
        f"{result}"
    )


# =========================================================
# HEALTH CHECK FOR RENDER
# =========================================================

async def health(request):
    return web.Response(
        text="Post Edit Bot is running!"
    )


async def start_web():
    web_app = web.Application()
    web_app.router.add_get("/", health)

    runner = web.AppRunner(web_app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        PORT
    )

    await site.start()

    log.info(f"Web server running on port {PORT}")


# =========================================================
# MAIN
# =========================================================

async def main():
    await app.start()
    await start_web()

    me = await app.get_me()
    log.info(f"Bot started: @{me.username}")

    # Bot চলতে থাকবে - idle() এর বিকল্প
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        log.info("Bot stopped.")
    finally:
        await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
