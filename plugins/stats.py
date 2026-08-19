from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from database import ensure_user, get_user


# ============================================================
# /STATS
# ============================================================

async def stats_command(
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

    data = get_user(user.id)

    if not data:
        await update.message.reply_text(
            "❌ Unable to load your statistics."
        )
        return

    battles = data.get("battles", 0)
    wins = data.get("wins", 0)
    losses = data.get("losses", 0)
    hunts = data.get("hunts", 0)
    messages = data.get("messages", 0)
    coins = data.get("coins", 0)
    xp = data.get("xp", 0)
    level = data.get("level", 1)

    # Calculate win rate
    if battles > 0:
        win_rate = round(
            (wins / battles) * 100,
            1,
        )
    else:
        win_rate = 0

    await update.message.reply_text(
        "📊 <b>Solurix Statistics</b>\n\n"
        f"⭐ Level: <b>{level}</b>\n"
        f"✨ XP: <b>{xp}</b>\n"
        f"💰 Coins: <b>{coins}</b>\n\n"
        "⚔️ <b>Battle Stats</b>\n"
        f"• Battles: <b>{battles}</b>\n"
        f"• Wins: <b>{wins}</b>\n"
        f"• Losses: <b>{losses}</b>\n"
        f"• Win Rate: <b>{win_rate}%</b>\n\n"
        "🎯 <b>Activity</b>\n"
        f"• Hunts: <b>{hunts}</b>\n"
        f"• Messages: <b>{messages}</b>",
        parse_mode="HTML",
    )


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register the /stats command."""

    application.add_handler(
        CommandHandler(
            "stats",
            stats_command,
        )
    )