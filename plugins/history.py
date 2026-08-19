from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from database import (
    ensure_user,
    get_user_history,
)


# ============================================================
# HISTORY FORMAT
# ============================================================

def format_history(history: list) -> str:

    if not history:
        return (
            "<b>📜 Solurix History</b>\n\n"
            "No game activity found yet.\n\n"
            "Start playing to build your history! ⚔️"
        )

    lines = [
        "<b>📜 Solurix Game History</b>",
        "",
    ]

    icons = {
        "battle": "⚔️",
        "hunt": "🎯",
        "daily": "🎁",
        "weekly": "🏆",
        "train": "🏋️",
        "explore": "🗺",
    }

    for item in history:

        action = item.get(
            "action",
            "game",
        )

        result = item.get(
            "result",
            "completed",
        )

        reward = item.get(
            "reward",
            0,
        )

        icon = icons.get(
            action,
            "🎮",
        )

        lines.append(
            f"{icon} <b>{action.title()}</b> — "
            f"{result}"
        )

        if reward:
            lines.append(
                f"   💰 Reward: <b>+{reward}</b> coins"
            )

    return "\n".join(lines)


# ============================================================
# /HISTORY
# ============================================================

async def history_command(
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

    history = get_user_history(
        user.id,
        limit=10,
    )

    text = format_history(
        history
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
    )


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register the /history command."""

    application.add_handler(
        CommandHandler(
            "history",
            history_command,
        )
    )