import logging
import sys

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | "
    "%(filename)s:%(lineno)d | %(message)s"
)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("bot.log", encoding="utf-8")
        ],
        force=True
    )

    logging.getLogger("pyrogram").setLevel(logging.INFO)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)

    return logging.getLogger("AI-CAPTION-BOT")
