import os
from os import environ


def get_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


SESSION = environ.get('SESSION', '')
API_ID = get_int(environ.get('API_ID', ''), 0)
API_HASH = environ.get('API_HASH', '')
BOT_TOKEN = environ.get('BOT_TOKEN', '')

AI_API_KEY = environ.get('AI_API_KEY', '')
AI_MODEL = environ.get('AI_MODEL', 'gpt-4o-mini')
