# info.py

import os

# পরিবেশ ভেরিয়েবল (Environment Variables) থেকে ডাটা নেওয়া হচ্ছে
# যদি Env Variable না পাওয়া যায়, তবে ডিফল্ট মান ব্যবহার হবে (যা আপনি দিয়েছেন)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8982103415:AAH5meSpQewu-0nBm-yTk1-BBhLyaaOXjS4")
API_ID = int(os.environ.get("API_ID", "24776633"))
API_HASH = os.environ.get("API_HASH", "57b1f632044b4e718f5dce004a988d69")
DB_URL = os.environ.get("DB_URL", "mongodb+srv://rendamd1_db_user:M7vb8ZD9rx0AfHnP@cluster0.uzqvib6.mongodb.net/?appName=Cluster0") # আপনার MongoDB URL এখানে দিন অথবা Env থেকে নিন
ADMIN_ID = int(os.environ.get("ADMIN_ID", "8248792819")) # আপনার Telegram User ID দিন
PORT = int(os.environ.get("PORT", 8080))
