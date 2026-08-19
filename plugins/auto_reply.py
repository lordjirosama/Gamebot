import random
import time

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from config import (
    AUTO_REPLY_ENABLED,
    AUTO_REPLY_COOLDOWN,
)


# ============================================================
# AUTO REPLIES
# ============================================================

AUTO_REPLIES = {
    "hello": [
        "Hello! 👋",
        "Hey! Welcome to Solurix. ⚔️",
        "Hello, warrior! 🌟",
    ],
    "hi": [
        "Hi! 👋",
        "Hey there! ⚔️",
        "Hello! Ready to play? 🎮",
    ],
    "hey": [
        "Hey! 👋",
        "What's up, warrior? ⚔️",
    ],
    "good morning": [
        "Good morning! ☀️",
        "Good morning, warrior! 🌟",
    ],
    "good night": [
        "Good night! 🌙",
        "Rest well, warrior. ⚔️",
    ],
}


# ============================================================
# COOLDOWN STORAGE
# ============================================================

_reply_cooldowns = {}


def can_reply(chat_id: int) -> bool:
    """Check whether the bot can auto-reply in this chat."""

    now = time.time()

    last_reply = _reply_cooldowns.get(
        chat_id,
        0,
    )

    if now - last_reply < AUTO_REPLY_COOLDOWN:
        return False

    _reply_cooldowns[chat_id] = now

    return True


# ============================================================
# AUTO REPLY HANDLER
# ============================================================

async def auto_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    if not AUTO_REPLY_ENABLED:
        return

    if not update.message:
        return

    if not update.message.text:
        return

    if not update.effective_chat:
        return

    chat = update.effective_chat

    # Only groups
    if chat.type not in (
        "group",
        "supergroup",
    ):
        return

    text = update.message.text.lower().strip()

    # Ignore commands
    if text.startswith("/"):
        return

    reply_list = None

    # Exact match
    if text in AUTO_REPLIES:
        reply_list = AUTO_REPLIES[text]

    # Message contains trigger
    else:
        for trigger, replies in AUTO_REPLIES.items():

            if trigger in text.split():
                reply_list = replies
                break

    if not reply_list:
        return

    if not can_reply(chat.id):
        return

    reply = random.choice(
        reply_list
    )

    await update.message.reply_text(
        reply
    )


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register the auto-reply handler."""

    application.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND,
            auto_reply,
        )
    )