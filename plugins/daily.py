from datetime import datetime, timezone

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from config import DAILY_REWARD
from database import (
    ensure_user,
    add_coins,
    add_xp,
    get_last_daily_claim,
    set_daily_claim,
    add_history,
)


# ============================================================
# DAILY REWARD
# ============================================================

async def daily_command(
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

    last_claim = get_last_daily_claim(user.id)

    # --------------------------------------------------------
    # CHECK LAST CLAIM
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

            cooldown = 24 * 60 * 60

            if elapsed < cooldown:

                remaining = int(
                    cooldown - elapsed
                )

                hours = remaining // 3600
                minutes = (remaining % 3600) // 60

                await update.message.reply_text(
                    "🎁 <b>Daily Reward</b>\n\n"
                    "You have already claimed your daily reward.\n\n"
                    f"⏳ Come back in "
                    f"<b>{hours}h {minutes}m</b>.",
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
        DAILY_REWARD,
    )

    add_xp(
        user.id,
        50,
    )

    set_daily_claim(
        user.id,
    )

    add_history(
        user.id,
        "daily",
        "claimed",
        DAILY_REWARD,
    )

    # --------------------------------------------------------
    # SUCCESS MESSAGE
    # --------------------------------------------------------

    await update.message.reply_text(
        "🎁 <b>Daily Reward Claimed!</b>\n\n"
        f"💰 Coins: <b>+{DAILY_REWARD}</b>\n"
        "✨ XP: <b>+50</b>\n\n"
        "Come back tomorrow for another reward! 🌟",
        parse_mode="HTML",
    )


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register the daily reward command."""

    application.add_handler(
        CommandHandler(
            "daily",
            daily_command,
        )
    )