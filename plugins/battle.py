import random

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from config import (
    BATTLE_COOLDOWN,
    BATTLE_MIN_REWARD,
    BATTLE_MAX_REWARD,
)

from database import (
    ensure_user,
    get_user,
    add_coins,
    add_xp,
    increment_stat,
    add_history,
    get_cooldown,
    set_cooldown,
)

import time


# ============================================================
# BATTLE
# ============================================================

async def battle_command(
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
        "battle",
    )

    remaining = BATTLE_COOLDOWN - (
        time.time() - last_used
    )

    if remaining > 0:

        await update.message.reply_text(
            "⚔️ <b>Battle Cooldown</b>\n\n"
            f"Try again in <b>{int(remaining)}s</b>.",
            parse_mode="HTML",
        )

        return

    set_cooldown(
        user.id,
        "battle",
        time.time(),
    )

    # --------------------------------------------------------
    # BATTLE RESULT
    # --------------------------------------------------------

    increment_stat(
        user.id,
        "battles",
    )

    won = random.choice(
        [True, False]
    )

    if won:

        reward = random.randint(
            BATTLE_MIN_REWARD,
            BATTLE_MAX_REWARD,
        )

        add_coins(
            user.id,
            reward,
        )

        add_xp(
            user.id,
            20,
        )

        increment_stat(
            user.id,
            "wins",
        )

        add_history(
            user.id,
            "battle",
            "win",
            reward,
        )

        await update.message.reply_text(
            "⚔️ <b>Battle Result</b>\n\n"
            "🏆 <b>You won!</b>\n\n"
            f"💰 Coins: <b>+{reward}</b>\n"
            "✨ XP: <b>+20</b>",
            parse_mode="HTML",
        )

    else:

        add_xp(
            user.id,
            5,
        )

        increment_stat(
            user.id,
            "losses",
        )

        add_history(
            user.id,
            "battle",
            "loss",
            0,
        )

        await update.message.reply_text(
            "⚔️ <b>Battle Result</b>\n\n"
            "💔 <b>You lost!</b>\n\n"
            "✨ XP: <b>+5</b>",
            parse_mode="HTML",
        )


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register the battle command."""

    application.add_handler(
        CommandHandler(
            "battle",
            battle_command,
        )
    )