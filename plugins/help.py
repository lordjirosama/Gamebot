from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from config import (
    HELP_IMAGE,
    SUPPORT_CHANNEL,
    SUPPORT_GROUP,
)


# ============================================================
# HELP TEXT
# ============================================================

HELP_TEXT = """
<b>Solurix — Help & Commands</b> ⚔️

<b>🎮 Basic</b>
/start — Start Solurix
/help — Show this help menu

<b>👤 Profile</b>
/profile — View your profile
/stats — View your statistics
/rank — View the group ranking
/level — Check your level
/coins — Check your coins
/history — View your game history

<b>🎁 Rewards</b>
/daily — Claim your daily reward
/weekly — Claim your weekly reward

<b>⚔️ Game</b>
/battle — Battle another player
/hunt — Go on a hunt
/train — Train your character
/explore — Explore the world

<b>🛠 Admin</b>
/reset — Reset a player's progress

<b>💬 Support</b>
If you find a bug or something doesn't work correctly,
please contact us through the support group.
"""


# ============================================================
# HELP KEYBOARD
# ============================================================

def help_keyboard() -> InlineKeyboardMarkup:

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
    ]

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# /HELP
# ============================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    keyboard = help_keyboard()

    # --------------------------------------------------------
    # WITH IMAGE
    # --------------------------------------------------------

    if HELP_IMAGE:

        try:
            await update.message.reply_photo(
                photo=HELP_IMAGE,
                caption=HELP_TEXT,
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
        HELP_TEXT,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


# ============================================================
# HELP CALLBACK
# ============================================================

async def help_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    query = update.callback_query

    if not query:
        return

    await query.answer()

    keyboard = help_keyboard()

    # --------------------------------------------------------
    # If help image is configured
    # --------------------------------------------------------

    if HELP_IMAGE:

        try:
            await query.message.delete()

            await query.message.chat.send_photo(
                photo=HELP_IMAGE,
                caption=HELP_TEXT,
                reply_markup=keyboard,
                parse_mode="HTML",
            )

            return

        except Exception:
            pass

    # --------------------------------------------------------
    # Normal text help
    # --------------------------------------------------------

    try:

        await query.edit_message_text(
            HELP_TEXT,
            reply_markup=keyboard,
            parse_mode="HTML",
        )

    except Exception:
        pass


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register help handlers."""

    application.add_handler(
        CommandHandler(
            "help",
            help_command,
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            help_callback,
            pattern=r"^help_menu$",
        )
    )