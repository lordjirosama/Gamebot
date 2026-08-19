from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CommandHandler

from config import (
    BOT_NAME,
    SUPPORT_CHANNEL,
    SUPPORT_GROUP,
    OWNER_USERNAME,
    OWNER_LINK,
    REPOSITORY_URL,
    START_IMAGE,
)

from database import ensure_user


# ============================================================
# START MESSAGE
# ============================================================

START_TEXT = """
<b>Welcome to Solurix</b> ⚔️

A fictional RPG game for Telegram groups.

🎮 Play games
⚔️ Battle players
🗺 Explore the world
🎯 Hunt for rewards
💰 Earn coins
⭐ Gain XP and level up
🏆 Compete in group rankings

Use the buttons below or type /help to see all available commands.
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
                f"Oᴡɴᴇʀ {OWNER_USERNAME}",
                url=OWNER_LINK,
            ),
        ],
        [
            InlineKeyboardButton(
                "GɪᴛHᴜʙ Rᴇᴘᴏsɪᴛᴏʀʏ",
                url=REPOSITORY_URL,
            ),
        ],
        [
            InlineKeyboardButton(
                "Hᴇʟᴘ",
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

    if not user:
        return

    # Register player
    ensure_user(
        user_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "",
    )

    keyboard = start_keyboard()

    # --------------------------------------------------------
    # WITH IMAGE
    # --------------------------------------------------------

    if START_IMAGE:

        try:
            await update.message.reply_photo(
                photo=START_IMAGE,
                caption=START_TEXT,
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
        START_TEXT,
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