import importlib
import logging
import os
import sys

from pyrogram import Client

from config import SESSION, API_ID, API_HASH, BOT_TOKEN
from helpers.logger import setup_logging

logger = setup_logging()

PLUGINS = [
    "plugins.start",
    "plugins.help",
    "plugins.settings",
    "plugins.caption",
]


def validate_config():
    errors = []

    if not API_ID:
        errors.append("API_ID is missing or invalid")
    if not API_HASH:
        errors.append("API_HASH is missing")
    if not BOT_TOKEN:
        errors.append("BOT_TOKEN is missing")

    if errors:
        for error in errors:
            logger.error("CONFIG ERROR: %s", error)
        raise ValueError("Invalid configuration")


def load_plugins():
    logger.info("Loading %d plugins...", len(PLUGINS))

    for plugin in PLUGINS:
        try:
            importlib.import_module(plugin)
            logger.info("PLUGIN LOADED: %s", plugin)
        except Exception:
            logger.exception("PLUGIN LOAD FAILED: %s", plugin)
            raise


def main():
    try:
        logger.info("=" * 55)
        logger.info("Starting AI Caption Bot")
        logger.info("Python: %s", sys.version)
        logger.info("PID: %s", os.getpid())

        validate_config()
        load_plugins()

        app = Client(
            name=SESSION or "ai_caption_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workdir="."
        )

        logger.info("All plugins loaded successfully.")
        logger.info("Starting Telegram client...")

        app.run()

    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")

    except Exception:
        logger.critical("BOT STARTUP FAILED", exc_info=True)
        raise


if __name__ == "__main__":
    main()
