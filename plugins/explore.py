import random
import time

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from config import (
    HUNT_COOLDOWN,
)

from database import (
    ensure_user,
    add_coins,
    add_xp,
    add_history,
    get_cooldown,
    set_cooldown,
)


# ============================================================
# EXPLORE SETTINGS
# ============================================================

EXPLORE_COOLDOWN = 60

EXPLORE_LOCATIONS = [
    "Ancient Forest",
    "Mystic Valley",
    "Forgotten Ruins",
    "Shadow Mountains",
    "Crystal Lake",
    "Lost Kingdom",
    "Moonlight Village",
]

EXPLORE_MIN_COINS = 10
EXPLORE_MAX_COINS = 50

EXPLORE_MIN_XP = 10
EXPLORE_MAX_XP = 25


# ============================================================
# /EXPLORE
# ============================================================

async def explore_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    user = update.effective_user

    if not user or not update.message:
        return

    ensure_user(
        user_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "",
    )

    # --------------------------------------------------------
    # COOLDOWN
    # --------------------------------------------------------

    last_used = get_cooldown(
        user.id,
        "explore",
    )

    remaining = EXPLORE_COOLDOWN - (
        time.time() - last_used
    )

    if remaining > 0:

        await update.message.reply_text(
            "🗺 <b>Explore Cooldown</b>\n\n"
            f"Try again in <b>{int(remaining)}s</b>.",
            parse_mode="HTML",
        )

        return

    set_cooldown(
        user.id,
        "explore",
        time.time(),
    )

    # --------------------------------------------------------
    # EXPLORE RESULT
    # --------------------------------------------------------

    location = random.choice(
        EXPLORE_LOCATIONS
    )

    coins = random.randint(
        EXPLORE_MIN_COINS,
        EXPLORE_MAX_COINS,
    )

    xp = random.randint(
        EXPLORE_MIN_XP,
        EXPLORE_MAX_XP,
    )

    add_coins(
        user.id,
        coins,
    )

    add_xp(
        user.id,
        xp,
    )

    add_history(
        user.id,
        "explore",
        location,
        coins,
    )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    await update.message.reply_text(
        "🗺 <b>Exploration Complete!</b>\n\n"
        f"📍 Location: <b>{location}</b>\n\n"
        f"💰 Coins found: <b>+{coins}</b>\n"
        f"✨ XP gained: <b>+{xp}</b>\n\n"
        "Keep exploring the world of Solurix! 🌟",
        parse_mode="HTML",
    )


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register the /explore command."""

    application.add_handler(
        CommandHandler(
            "explore",
            explore_command,
        )
    )