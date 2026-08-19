from datetime import datetime, timezone

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from config import WEEKLY_REWARD
from database import (
    ensure_user,
    add_coins,
    add_xp,
    get_last_weekly_claim,
    set_weekly_claim,
    add_history,
)


# ============================================================
# WEEKLY REWARD
# ============================================================

WEEKLY_COOLDOWN = 7 * 24 * 60 * 60
WEEKLY_XP = 250


# ============================================================
# /WEEKLY
# ============================================================

async def weekly_command(
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

    last_claim = get_last_weekly_claim(user.id)

    # --------------------------------------------------------
    # CHECK COOLDOWN
    # --------------------------------------------------------

    if last_claim:

        try:
            last_time = datetime.fromisoformat(last_claim)

            if last_time.tzinfo is None:
                last_time = last_time.replace(
                    tzinfo=timezone.utc
                )

            elapsed = (
                datetime.now(timezone.utc)
                - last_time
            ).total_seconds()

            if elapsed < WEEKLY_COOLDOWN:

                remaining = int(
                    WEEKLY_COOLDOWN - elapsed
                )

                days = remaining // 86400
                hours = (remaining % 86400) // 3600
                minutes = (remaining % 3600) // 60

                await update.message.reply_text(
                    "🎁 <b>Weekly Reward</b>\n\n"
                    "You have already claimed your weekly reward.\n\n"
                    f"⏳ Come back in "
                    f"<b>{days}d {hours}h {minutes}m</b>.",
                    parse_mode="HTML",
                )

                return

        except ValueError:
            pass

    # --------------------------------------------------------
    # GIVE REWARD
    # --------------------------------------------------------

    add_coins(
        user.id,
        WEEKLY_REWARD,
    )

    add_xp(
        user.id,
        WEEKLY_XP,
    )

    set_weekly_claim(
        user.id,
    )

    add_history(
        user.id,
        "weekly",
        "claimed",
        WEEKLY_REWARD,
    )

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    await update.message.reply_text(
        "🎁 <b>Weekly Reward Claimed!</b>\n\n"
        f"💰 Coins: <b>+{WEEKLY_REWARD}</b>\n"
        f"✨ XP: <b>+{WEEKLY_XP}</b>\n\n"
        "Come back next week for another reward! 🌟",
        parse_mode="HTML",
    )


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register the /weekly command."""

    application.add_handler(
        CommandHandler(
            "weekly",
            weekly_command,
        )
    )