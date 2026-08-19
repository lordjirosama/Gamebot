from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from config import BRAND_CHANNEL


SUPPORT_GROUP = "https://t.me/+1PeOFri-U2phYjd"


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    text = (
        "<b>Welcome to Solurix</b>\n\n"
        "Enter the RPG arena, earn XP, collect coins, "
        "eliminate opponents, and climb the leaderboard.\n\n"
        "<b>Quick Commands</b>\n"
        "/profile — View your profile\n"
        "/daily — Claim your daily reward\n"
        "/kill — Eliminate another player\n"
        "/protect — Protect yourself\n"
        "/rank — View group ranking\n"
        "/help — Show all commands\n\n"
        "<b>Protection</b>\n"
        "/protect 1h — 149 Coins\n"
        "/protect 12h — 500 Coins\n"
        "/protect 24h — 900 Coins\n\n"
        "<b>Kill System</b>\n"
        "Reply to a player's message with /kill.\n"
        "Each player can kill once every 24 hours.\n"
        "Protected players cannot be killed."
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "Support Group",
                url=SUPPORT_GROUP,
            ),
            InlineKeyboardButton(
                "Support Channel",
                url=BRAND_CHANNEL,
            ),
        ],
        [
            InlineKeyboardButton(
                "Add me in your group",
                url="https://t.me/Makimagamebot?startgroup=true",
            ),
        ],
    ])

    await update.message.reply_html(
        text,
        reply_markup=keyboard,
    )


async def help_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    text = (
        "<b>Solurix Command Guide</b>\n\n"

        "<b>Player Commands</b>\n"
        "/start — Start Solurix\n"
        "/help — Show this command guide\n"
        "/profile — View your profile\n"
        "/me — View your profile\n"
        "/stats — View your statistics\n"
        "/coins — Check your coins\n"
        "/level — Check your level\n\n"

        "<b>Game Commands</b>\n"
        "/daily — Claim your daily reward\n"
        "/kill — Eliminate another player\n"
        "/protect — Activate protection\n"
        "/train — Train and earn XP\n"
        "/explore — Explore and find rewards\n\n"

        "<b>Protection</b>\n"
        "/protect 1h — 149 Coins\n"
        "/protect 12h — 500 Coins\n"
        "/protect 24h — 900 Coins\n\n"

        "<b>Kill System</b>\n"
        "Reply to a player's message and use /kill.\n"
        "You can kill once every 24 hours.\n"
        "The target's points are transferred to you.\n"
        "If the target has no coins, you receive "
        "a random 100–200 coin reward.\n\n"

        "<b>Ranking</b>\n"
        "/rank — View group ranking\n"
        "/ranking — View group leaderboard\n\n"

        "<b>Admin</b>\n"
        "/reset — Reset this group's Solurix data\n\n"

        "Play, earn, eliminate, protect, and become "
        "the strongest player in your group."
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "Support Group",
                url=SUPPORT_GROUP,
            ),
            InlineKeyboardButton(
                "Support Channel",
                url=BRAND_CHANNEL,
            ),
        ],
        [
            InlineKeyboardButton(
                "Add me in your group",
                url="https://t.me/Makimagamebot?startgroup=true",
            ),
        ],
    ])

    await update.message.reply_html(
        text,
        reply_markup=keyboard,
    )