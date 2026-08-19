import random
import time

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from config import (
    HUNT_COOLDOWN,
    HUNT_MIN_REWARD,
    HUNT_MAX_REWARD,
)

from database import (
    ensure_user,
    add_coins,
    add_xp,
    increment_stat,
    add_history,
    get_cooldown,
    set_cooldown,
)


# ============================================================
# /HUNT
# ============================================================

async def hunt_command(
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
        "hunt",
    )

    remaining = HUNT_COOLDOWN - (
        time.time() - last_used
    )

    if remaining > 0:

        await update.message.reply_text(
            "🎯 <b>Hunt Cooldown</b>\n\n"
            f"Try again in <b>{int(remaining)}s</b>.",
            parse_mode="HTML",
        )

        return

    set_cooldown(
        user.id,
        "hunt",
        time.time(),
    )

    # --------------------------------------------------------
    # HUNT RESULT
    # --------------------------------------------------------

    increment_stat(
        user.id,
        "hunts",
    )

    reward = random.randint(
        HUNT_MIN_REWARD,
        HUNT_MAX_REWARD,
    )

    xp = random.randint(
        5,
        15,
    )

    add_coins(
        user.id,
        reward,
    )

    add_xp(
        user.id,
        xp,
    )

    add_history(
        user.id,
        "hunt",
        "success",
        reward,
    )

    # --------------------------------------------------------
    # RESULT MESSAGE
    # --------------------------------------------------------

    await update.message.reply_text(
        "🎯 <b>Hunt Complete!</b>\n\n"
        "You explored the area and found a reward.\n\n"
        f"💰 Coins: <b>+{reward}</b>\n"
        f"✨ XP: <b>+{xp}</b>\n\n"
        "Come back later for another hunt! 🌟",
        parse_mode="HTML",
    )


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register the /hunt command."""

    application.add_handler(
        CommandHandler(
            "hunt",
            hunt_command,
        )
    )