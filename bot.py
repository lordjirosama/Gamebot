import logging

from telegram import (
    Update,
    BotCommand,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
)
from telegram.ext import Application, CommandHandler

from config import TOKEN
from database import init_db

from plugins.profile import profile, stats, coins, level
from plugins.game import daily, battle, train, explore
from plugins.ranking import rank
from plugins.admin import reset
from plugins.help import help_cmd, start


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("solurix")


# Commands shown when users type "/" in Telegram
PLAYER_COMMANDS = [
    BotCommand("start", "Start Solurix"),
    BotCommand("help", "Show all commands"),
    BotCommand("profile", "View your profile"),
    BotCommand("me", "View your profile"),
    BotCommand("stats", "View your game statistics"),
    BotCommand("coins", "Check your coins"),
    BotCommand("level", "Check your level"),
    BotCommand("daily", "Claim your daily reward"),
    BotCommand("battle", "Enter a random battle"),
    BotCommand("train", "Train and earn XP"),
    BotCommand("explore", "Explore and find rewards"),
    BotCommand("rank", "View group ranking"),
    BotCommand("ranking", "View group leaderboard"),
]

ADMIN_COMMANDS = PLAYER_COMMANDS + [
    BotCommand("reset", "Reset this group's game data"),
]


async def setup_commands(app: Application):
    # Private chat command menu
    await app.bot.set_my_commands(
        PLAYER_COMMANDS,
        scope=BotCommandScopeAllPrivateChats(),
    )

    # Group chat command menu
    await app.bot.set_my_commands(
        PLAYER_COMMANDS,
        scope=BotCommandScopeAllGroupChats(),
    )

    logger.info("Telegram command menus configured.")


def main():
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing. Put it in your .env file."
        )

    init_db()

    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(setup_commands)
        .build()
    )

    # Basic
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))

    # Profile
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("me", profile))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("coins", coins))
    app.add_handler(CommandHandler("level", level))

    # Game
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("battle", battle))
    app.add_handler(CommandHandler("train", train))
    app.add_handler(CommandHandler("explore", explore))

    # Ranking
    app.add_handler(CommandHandler("rank", rank))
    app.add_handler(CommandHandler("ranking", rank))

    # Admin
    app.add_handler(CommandHandler("reset", reset))

    logger.info("Solurix is starting...")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()