import os
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# BASIC BOT SETTINGS
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

BOT_NAME = os.getenv(
    "BOT_NAME",
    "Solurix"
).strip()

BOT_USERNAME = os.getenv(
    "BOT_USERNAME",
    ""
).strip()

# ============================================================
# BRANDING
# ============================================================

SUPPORT_CHANNEL = os.getenv(
    "SUPPORT_CHANNEL",
    "https://t.me/Solurix_bots"
).strip()

SUPPORT_GROUP = os.getenv(
    "SUPPORT_GROUP",
    "https://t.me/Solurix_Support_Group"
).strip()

OWNER_USERNAME = os.getenv(
    "OWNER_USERNAME",
    "@senpain_jiro"
).strip()

OWNER_LINK = os.getenv(
    "OWNER_LINK",
    "https://t.me/senpain_jiro"
).strip()

REPOSITORY_URL = os.getenv(
    "REPOSITORY_URL",
    "https://github.com/lordjirosama/Gamebot"
).strip()


# ============================================================
# DATABASE
# ============================================================

DB_PATH = os.getenv(
    "DB_PATH",
    "data/solurix.db"
).strip()


# ============================================================
# IMAGES
# ============================================================
# Add Telegram file_id later.
# Leave empty for now.

START_IMAGE = os.getenv("START_IMAGE", "").strip()
HELP_IMAGE = os.getenv("HELP_IMAGE", "").strip()
PROFILE_IMAGE = os.getenv("PROFILE_IMAGE", "").strip()
RANKING_IMAGE = os.getenv("RANKING_IMAGE", "").strip()
BATTLE_IMAGE = os.getenv("BATTLE_IMAGE", "").strip()
DAILY_IMAGE = os.getenv("DAILY_IMAGE", "").strip()
SHOP_IMAGE = os.getenv("SHOP_IMAGE", "").strip()
QUEST_IMAGE = os.getenv("QUEST_IMAGE", "").strip()
EVENT_IMAGE = os.getenv("EVENT_IMAGE", "").strip()


# ============================================================
# GAME SETTINGS
# ============================================================

STARTING_COINS = int(
    os.getenv("STARTING_COINS", "100")
)

STARTING_LEVEL = int(
    os.getenv("STARTING_LEVEL", "1")
)

STARTING_XP = int(
    os.getenv("STARTING_XP", "0")
)

XP_PER_MESSAGE = int(
    os.getenv("XP_PER_MESSAGE", "5")
)

XP_COOLDOWN = int(
    os.getenv("XP_COOLDOWN", "30")
)

DAILY_REWARD = int(
    os.getenv("DAILY_REWARD", "100")
)

WEEKLY_REWARD = int(
    os.getenv("WEEKLY_REWARD", "500")
)


# ============================================================
# BATTLE SETTINGS
# ============================================================

BATTLE_COOLDOWN = int(
    os.getenv("BATTLE_COOLDOWN", "30")
)

BATTLE_MIN_REWARD = int(
    os.getenv("BATTLE_MIN_REWARD", "10")
)

BATTLE_MAX_REWARD = int(
    os.getenv("BATTLE_MAX_REWARD", "100")
)


# ============================================================
# HUNT SETTINGS
# ============================================================

HUNT_COOLDOWN = int(
    os.getenv("HUNT_COOLDOWN", "60")
)

HUNT_MIN_REWARD = int(
    os.getenv("HUNT_MIN_REWARD", "5")
)

HUNT_MAX_REWARD = int(
    os.getenv("HUNT_MAX_REWARD", "75")
)


# ============================================================
# AUTO REPLY
# ============================================================

AUTO_REPLY_ENABLED = os.getenv(
    "AUTO_REPLY_ENABLED",
    "True"
).lower() in ("true", "1", "yes", "on")

AUTO_REPLY_COOLDOWN = int(
    os.getenv("AUTO_REPLY_COOLDOWN", "20")
)


# ============================================================
# COMMAND SETTINGS
# ============================================================

SET_COMMANDS = os.getenv(
    "SET_COMMANDS",
    "True"
).lower() in ("true", "1", "yes", "on")


# ============================================================
# LOGGING
# ============================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
).upper()


# ============================================================
# VALIDATION
# ============================================================

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is missing. Add BOT_TOKEN to your .env file."
    )

if OWNER_ID <= 0:
    raise RuntimeError(
        "OWNER_ID is missing or invalid. Add your Telegram user ID to .env."
    )