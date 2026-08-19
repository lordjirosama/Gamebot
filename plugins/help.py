from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from config import (
    BRAND_CHANNEL,
    SUPPORT_GROUP,
)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    keyboard = [
        [
            InlineKeyboardButton(
                "Solurix Bots",
                url=BRAND_CHANNEL,
            )
        ],
        [
            InlineKeyboardButton(
                "Support Group",
                url=SUPPORT_GROUP,
            )
        ],
        [
            InlineKeyboardButton(
                "Add me in your group",
                url=(
                    "https://t.me/"
                    "SolurixGameBot"
                    "?startgroup=true"
                ),
            )
        ],
    ]

    text = (
        "<b>Welcome to Solurix</b>\n\n"
        "Enter the RPG arena, earn XP, "
        "collect coins, eliminate rivals, "
        "and climb your group leaderboard.\n\n"

        "<b>Quick Commands</b>\n"
        "/profile — View your profile\n"
        "/daily — Claim your daily reward\n"
        "/kill — Eliminate another player\n"
        "/protect — Activate protection\n"
        "/rank — View group ranking\n"
        "/help — Show all commands\n\n"

        "Use /help to see the complete "
        "command guide."
    )

    await update.message.reply_html(
        text,
        reply_markup=InlineKeyboardMarkup(
            keyboard
        ),
        disable_web_page_preview=True,
    )


async def help_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    text = (
        "<b>Solurix Command Guide</b>\n\n"

        "<b>Player Commands</b>\n"
        "/profile — Your profile and stats\n"
        "/me — Your profile\n"
        "/stats — Detailed statistics\n"
        "/coins — Check your coins\n"
        "/level — Check your level\n\n"

        "<b>Game Commands</b>\n"
        "/daily — Claim your daily reward\n"
        "/kill — Eliminate another player\n"
        "/protect — Activate protection\n"
        "/train — Train and earn XP\n"
        "/explore — Explore and find rewards\n\n"

        "<b>Ranking</b>\n"
        "/rank — Group leaderboard\n"
        "/ranking — Group leaderboard\n\n"

        "<b>Admin Commands</b>\n"
        "/reset — Reset group game data\n"
        "/broadcast — Broadcast a message\n\n"

        "<b>Protection</b>\n"
        "/protect 1h — 149 Coins\n"
        "/protect 12h — 500 Coins\n"
        "/protect 24h — 900 Coins\n\n"

        "<b>Kill System</b>\n"
        "Reply to a player's message and use "
        "/kill to eliminate them.\n"
        "Each player can kill once every 24 hours.\n"
        "Protected players cannot be eliminated."
    )

    await update.message.reply_html(
        text,
        disable_web_page_preview=True,
    )