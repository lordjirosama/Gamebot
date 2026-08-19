import os

from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv(
    "BOT_TOKEN",
    "8814559046:AAEhnqF2marDTD5q1akAFKGeqkdjACgy088"
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

START_IMAGE = "https://image.zaw-myo.workers.dev/image/19ea287a-74c5-4d45-b319-d4f919450c1c"

PROFILE_IMAGE = "https://image.zaw-myo.workers.dev/image/d045a331-c349-44ca-8bfb-a942c5dc598d"

DAILY_IMAGE = "https://image.zaw-myo.workers.dev/image/7b6bb415-5ab0-495d-b2f2-6256cf67b9e1"

KILL_IMAGE = "https://image.zaw-myo.workers.dev/image/619502fc-69bf-4e43-9928-7e10856f5dc8"

PROTECT_IMAGE = "https://image.zaw-myo.workers.dev/image/97b4e0ee-cbe8-4292-b35d-400e0b91c044"

TRAIN_IMAGE = "https://image.zaw-myo.workers.dev/image/d045a331-c349-44ca-8bfb-a942c5dc598d"

EXPLORE_IMAGE = "https://image.zaw-myo.workers.dev/image/19ea287a-74c5-4d45-b319-d4f919450c1c"

RANKING_IMAGE = "https://image.zaw-myo.workers.dev/image/4168b611-f100-48ac-b57f-23deb802bd01"

HELP_IMAGE = "https://image.zaw-myo.workers.dev/image/19ea287a-74c5-4d45-b319-d4f919450c1c"