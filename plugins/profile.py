from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CommandHandler

from database import ensure_user, get_user


# ============================================================
# PROFILE TEXT
# ============================================================

def build_profile(user_data: dict) -> str:
    """Create the player profile message."""

    username = user_data.get("username") or "Not set"
    first_name = user_data.get("first_name") or "Player"

    return f"""
<b>👤 Solurix Profile</b>

<b>Name:</b> {first_name}
<b>Username:</b> @{username if username != "Not set" else username}

━━━━━━━━━━━━━━━━━━

<b>⭐ Level:</b> {user_data.get("level", 1)}
<b>✨ XP:</b> {user_data.get("xp", 0)}
<b>💰 Coins:</b> {user_data.get("coins", 0)}

━━━━━━━━━━━━━━━━━━

<b>⚔️ Battles:</b> {user_data.get("battles", 0)}
<b>🏆 Wins:</b> {user_data.get("wins", 0)}
<b>💔 Losses:</b> {user_data.get("losses", 0)}
<b>🎯 Hunts:</b> {user_data.get("hunts", 0)}
<b>💬 Messages:</b> {user_data.get("messages", 0)}
"""


# ============================================================
# PROFILE BUTTONS
# ============================================================

def profile_keyboard() -> InlineKeyboardMarkup:

    keyboard = [
        [
            InlineKeyboardButton(
                "🔄 Refresh",
                callback_data="profile_refresh",
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# /PROFILE
# ============================================================

async def profile_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    user = update.effective_user

    if not user or not update.message:
        return

    # Register/update user
    ensure_user(
        user_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "",
    )

    user_data = get_user(user.id)

    if not user_data:
        await update.message.reply_text(
            "Unable to load your profile right now."
        )
        return

    await update.message.reply_text(
        build_profile(user_data),
        reply_markup=profile_keyboard(),
        parse_mode="HTML",
    )


# ============================================================
# REFRESH PROFILE
# ============================================================

async def profile_refresh(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    query = update.callback_query

    if not query:
        return

    await query.answer("Profile updated.")

    user = query.from_user

    ensure_user(
        user_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "",
    )

    user_data = get_user(user.id)

    if not user_data:
        return

    try:
        await query.edit_message_text(
            build_profile(user_data),
            reply_markup=profile_keyboard(),
            parse_mode="HTML",
        )

    except Exception:
        pass


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register profile handlers."""

    application.add_handler(
        CommandHandler(
            "profile",
            profile_command,
        )
    )

    from telegram.ext import CallbackQueryHandler

    application.add_handler(
        CallbackQueryHandler(
            profile_refresh,
            pattern=r"^profile_refresh$",
        )
    )