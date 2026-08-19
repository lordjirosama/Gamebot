from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from config import OWNER_ID
from database import reset_user, get_user


# ============================================================
# ADMIN CHECK
# ============================================================

def is_owner(user_id: int) -> bool:
    """Check whether the user is the bot owner."""

    return user_id == OWNER_ID


# ============================================================
# /RESET
# ============================================================

async def reset_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    user = update.effective_user

    if not user or not update.message:
        return

    # --------------------------------------------------------
    # OWNER ONLY
    # --------------------------------------------------------

    if not is_owner(user.id):

        await update.message.reply_text(
            "❌ You are not authorized to use this command."
        )

        return

    # --------------------------------------------------------
    # TARGET USER
    # --------------------------------------------------------

    target_id = None

    # Reply to a user's message
    if update.message.reply_to_message:

        target_id = (
            update.message
            .reply_to_message
            .from_user
            .id
        )

    # /reset USER_ID
    elif context.args:

        try:
            target_id = int(
                context.args[0]
            )

        except ValueError:

            await update.message.reply_text(
                "❌ Invalid user ID.\n\n"
                "Use /reset USER_ID or reply to a user's message."
            )

            return

    if not target_id:

        await update.message.reply_text(
            "🛠 <b>Reset User</b>\n\n"
            "Reply to a user's message with:\n"
            "<code>/reset</code>\n\n"
            "Or use:\n"
            "<code>/reset USER_ID</code>",
            parse_mode="HTML",
        )

        return

    # --------------------------------------------------------
    # CHECK USER
    # --------------------------------------------------------

    target = get_user(
        target_id
    )

    if not target:

        await update.message.reply_text(
            "❌ User not found in the database."
        )

        return

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    reset_user(
        target_id
    )

    await update.message.reply_text(
        "✅ <b>User Reset Successfully</b>\n\n"
        f"👤 User ID: <code>{target_id}</code>\n"
        "⭐ Level: 1\n"
        "✨ XP: 0\n"
        "💰 Coins: 100\n"
        "⚔️ Stats: Reset",
        parse_mode="HTML",
    )


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register admin commands."""

    application.add_handler(
        CommandHandler(
            "reset",
            reset_command,
        )
    )