from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from database import ensure_user, get_user


# ============================================================
# LEVEL SYSTEM
# ============================================================

def xp_required(level: int) -> int:
    """XP required to reach the next level."""

    return level * 100


def make_progress_bar(
    current_xp: int,
    required_xp: int,
    length: int = 10,
) -> str:

    if required_xp <= 0:
        return "██████████"

    progress = min(
        1,
        current_xp / required_xp,
    )

    filled = int(
        progress * length
    )

    empty = length - filled

    return (
        "█" * filled
        + "░" * empty
    )


# ============================================================
# /LEVEL
# ============================================================

async def level_command(
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

    data = get_user(
        user.id
    )

    if not data:

        await update.message.reply_text(
            "❌ Unable to load your level."
        )

        return

    level = data.get(
        "level",
        1,
    )

    xp = data.get(
        "xp",
        0,
    )

    required = xp_required(
        level
    )

    progress = min(
        xp,
        required,
    )

    percentage = int(
        (progress / required) * 100
    ) if required else 100

    bar = make_progress_bar(
        progress,
        required,
    )

    await update.message.reply_text(
        "⭐ <b>Solurix Level</b>\n\n"
        f"⭐ Level: <b>{level}</b>\n"
        f"✨ XP: <b>{xp}</b>\n\n"
        f"<code>{bar}</code>\n"
        f"<b>{percentage}%</b> progress\n\n"
        f"✨ Next level: "
        f"<b>{required} XP</b>",
        parse_mode="HTML",
    )


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register the /level command."""

    application.add_handler(
        CommandHandler(
            "level",
            level_command,
        )
    )