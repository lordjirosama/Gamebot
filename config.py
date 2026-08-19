import os

from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv(
    "BOT_TOKEN",
    ""
).strip()


BOT_NAME = "Solurix"

BRAND_CHANNEL = (
    "https://t.me/Solurix_bots"
)

SUPPORT_GROUP = (
    "https://t.me/+1PeOFri-U2phYjd"
)


DB_PATH = os.getenv(
    "DB_PATH",
    "data/solurix.db"
)


# Optional Telegram images.
# Add Telegram file_id or image URL later.

START_IMAGE = ""

PROFILE_IMAGE = ""

DAILY_IMAGE = ""

KILL_IMAGE = ""

PROTECT_IMAGE = ""

TRAIN_IMAGE = ""

EXPLORE_IMAGE = ""

RANKING_IMAGE = ""

HELP_IMAGE = ""