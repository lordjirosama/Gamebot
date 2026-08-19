from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from database import ensure_user, get_user


# ============================================================
# /COINS
# ============================================================

async def coins_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    user = update.effective_user

    if not user or not update.message:
        return

    # --------------------------------------------------------
    # REGISTER USER
    # --------------------------------------------------------

    ensure_user(
        user_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "",
    )

    user_data = get_user(
        user.id
    )

    if not user_data:

        await update.message.reply_text(
            "❌ Unable to load your coin balance."
        )

        return

    coins = user_data.get(
        "coins",
        0,
    )

    level = user_data.get(
        "level",
        1,
    )

    # --------------------------------------------------------
    # BALANCE
    # --------------------------------------------------------

    await update.message.reply_text(
        "💰 <b>Solurix Wallet</b>\n\n"
        f"💰 Coins: <b>{coins}</b>\n"
        f"⭐ Level: <b>{level}</b>\n\n"
        "Earn more coins by playing games, "
        "hunting, battling and claiming rewards! ⚔️",
        parse_mode="HTML",
    )


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register the /coins command."""

    application.add_handler(
        CommandHandler(
            "coins",
            coins_command,
        )
    )