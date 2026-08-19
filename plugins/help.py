from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from config import BRAND_CHANNEL


SUPPORT_GROUP = "https://t.me/Solurix_support"
ADD_TO_GROUP = "https://t.me/Makimagamebot?startgroup=true"


def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "Support Group",
                url=SUPPORT_GROUP,
            ),
        ],
        [
            InlineKeyboardButton(
                "Support Channel",
                url=BRAND_CHANNEL,
            ),
        ],
        [
            InlineKeyboardButton(
                "Add me in your group",
                url=ADD_TO_GROUP,
            ),
        ],
    ])


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    text = (
        "<b>Welcome to Solurix</b>\n\n"

        "Enter the RPG arena, eliminate "
        "opponents, earn coins and XP, "
        "and become the strongest player "
        "in your group.\n\n"

        "<b>Quick Commands</b>\n"
        "/profile — View your profile\n"
        "/daily — Claim your daily reward\n"
        "/kill — Eliminate another player\n"
        "/protect — Protect yourself\n"
        "/train — Train and earn XP\n"
        "/explore — Explore for rewards\n"
        "/rank — View group ranking\n"
        "/help — Show all commands\n\n"

        f"<a href=\"{BRAND_CHANNEL}\">Solurix Bots</a>"
    )

    await update.message.reply_html(
        text,
        reply_markup=main_keyboard(),
    )


async def help_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    text = (
        "<b>Solurix Command Guide</b>\n\n"

        "<b>PLAYER</b>\n"
        "/profile — View your profile\n"
        "/me — View your profile\n"
        "/stats — View your statistics\n"
        "/coins — Check your coins\n"
        "/level — Check your level\n"
        "/daily — Claim daily reward\n"
        "/kill — Eliminate another player\n"
        "/protect — Activate protection\n"
        "/train — Train and earn XP\n"
        "/explore — Explore and find rewards\n"
        "/rank — Group leaderboard\n"
        "/ranking — Group leaderboard\n\n"

        "<b>PROTECTION</b>\n"
        "/protect\n\n"
        "1 Hour — 149 Coins\n"
        "12 Hours — 500 Coins\n"
        "24 Hours — 900 Coins\n\n"

        "<b>ADMIN</b>\n"
        "/reset — Reset this group's game data\n\n"

        "<b>HOW KILL WORKS</b>\n"
        "Use /kill by replying to a player's "
        "message or by selecting a target.\n\n"

        "A successful kill rewards the killer "
        "with the target's points and a coin reward.\n\n"

        "After killing, the killer has to wait "
        "24 hours before killing again.\n\n"

        "Protected players cannot be killed "
        "while their protection is active."
    )

    await update.message.reply_html(
        text,
        reply_markup=main_keyboard(),
    )