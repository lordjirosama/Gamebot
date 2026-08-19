from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    ContextTypes,
    CommandHandler,
)

from config import (
    BOT_NAME,
    SUPPORT_CHANNEL,
    SUPPORT_GROUP,
    OWNER_USERNAME,
    START_IMAGE,
)

from database import ensure_user


# ============================================================
# START MESSAGE
# ============================================================

START_TEXT = """
<b>⚔️ Welcome to Solurix!</b>

Hello, {name}! 👋

Solurix is a group-based RPG game where you can
battle, hunt, train, explore, earn coins and level up.

<b>🎮 What you can do:</b>
• ⚔️ Battle other players
• 🎯 Go on hunts
• 🏋️ Train your character
• 🗺 Explore the world
• 🎁 Claim daily & weekly rewards
• 🏆 Compete on the group leaderboard
• ⭐ Level up and gain XP

Type /help to see all available commands.

<b>👑 Owner:</b> {owner}
"""


# ============================================================
# START BUTTONS
# ============================================================

def start_keyboard() -> InlineKeyboardMarkup:

    keyboard = [
        [
            InlineKeyboardButton(
                "Sᴜᴘᴘᴏʀᴛ Cʜᴀɴɴᴇʟ",
                url=SUPPORT_CHANNEL,
            ),
            InlineKeyboardButton(
                "Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ",
                url=SUPPORT_GROUP,
            ),
        ],
        [
            InlineKeyboardButton(
                "📖 Hᴇʟᴘ",
                callback_data="help_menu",
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# /START
# ============================================================

async def start_command(
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

    text = START_TEXT.format(
        name=user.first_name or "Player",
        owner=OWNER_USERNAME,
    )

    keyboard = start_keyboard()

    # --------------------------------------------------------
    # WITH IMAGE
    # --------------------------------------------------------

    if START_IMAGE:

        try:

            await update.message.reply_photo(
                photo=START_IMAGE,
                caption=text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )

            return

        except Exception:
            pass

    # --------------------------------------------------------
    # WITHOUT IMAGE
    # --------------------------------------------------------

    await update.message.reply_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register the /start command."""

    application.add_handler(
        CommandHandler(
            "start",
            start_command,
        )
    )