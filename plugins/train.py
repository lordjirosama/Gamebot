import random
import time

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from database import (
    ensure_user,
    add_xp,
    add_history,
    get_cooldown,
    set_cooldown,
)


# ============================================================
# TRAIN SETTINGS
# ============================================================

TRAIN_COOLDOWN = 60

TRAIN_MIN_XP = 10
TRAIN_MAX_XP = 30

TRAIN_ACTIONS = [
    "Strength Training",
    "Speed Training",
    "Combat Practice",
    "Weapon Practice",
    "Endurance Training",
]


# ============================================================
# /TRAIN
# ============================================================

async def train_command(
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
        "train",
    )

    remaining = TRAIN_COOLDOWN - (
        time.time() - last_used
    )

    if remaining > 0:

        await update.message.reply_text(
            "🏋️ <b>Training Cooldown</b>\n\n"
            f"Train again in <b>{int(remaining)}s</b>.",
            parse_mode="HTML",
        )

        return

    set_cooldown(
        user.id,
        "train",
        time.time(),
    )

    # --------------------------------------------------------
    # TRAINING RESULT
    # --------------------------------------------------------

    action = random.choice(
        TRAIN_ACTIONS
    )

    xp = random.randint(
        TRAIN_MIN_XP,
        TRAIN_MAX_XP,
    )

    add_xp(
        user.id,
        xp,
    )

    add_history(
        user.id,
        "train",
        action,
        0,
    )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    await update.message.reply_text(
        "🏋️ <b>Training Complete!</b>\n\n"
        f"🥋 Training: <b>{action}</b>\n"
        f"✨ XP gained: <b>+{xp}</b>\n\n"
        "Keep training to become stronger! ⚔️",
        parse_mode="HTML",
    )


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register the /train command."""

    application.add_handler(
        CommandHandler(
            "train",
            train_command,
        )
    )