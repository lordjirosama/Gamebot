import logging

from telegram import BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config import (
    BOT_TOKEN,
    BOT_NAME,
    SET_COMMANDS,
)


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("solurix")


# ============================================================
# TELEGRAM COMMAND MENU
# ============================================================

COMMANDS = [
    BotCommand("start", "Start Solurix"),
    BotCommand("help", "Show all commands"),
    BotCommand("profile", "View your profile"),
    BotCommand("stats", "View your statistics"),
    BotCommand("rank", "View group ranking"),
    BotCommand("daily", "Claim your daily reward"),
    BotCommand("battle", "Start a battle"),
    BotCommand("hunt", "Go on a hunt"),
    BotCommand("train", "Train your character"),
    BotCommand("explore", "Explore the world"),
    BotCommand("coins", "Check your coins"),
    BotCommand("level", "Check your level"),
]


# ============================================================
# COMMAND SETUP
# ============================================================

async def setup_commands(application: Application) -> None:
    """Register Telegram command suggestions."""

    if not SET_COMMANDS:
        return

    await application.bot.set_my_commands(COMMANDS)

    logger.info(
        "Telegram command menu configured for %s.",
        BOT_NAME,
    )


# ============================================================
# IMPORT PLUGINS
# ============================================================

def load_plugins(application: Application) -> None:
    """
    Load all Solurix plugins.

    Each plugin can expose a setup(application)
    function. Missing plugins are skipped so the
    bot can still start during development.
    """

    plugin_names = [
        "start",
        "help",
        "game",
        "profile",
        "ranking",
        "daily",
        "battle",
        "hunt",
        "admin",
        "auto_reply",
    ]

    for plugin_name in plugin_names:
        try:
            module = __import__(
                f"plugins.{plugin_name}",
                fromlist=["setup"],
            )

            setup = getattr(module, "setup", None)

            if setup is None:
                logger.warning(
                    "Plugin %s has no setup() function.",
                    plugin_name,
                )
                continue

            setup(application)

            logger.info(
                "Loaded plugin: %s",
                plugin_name,
            )

        except ModuleNotFoundError:
            logger.warning(
                "Plugin not found yet: %s",
                plugin_name,
            )

        except Exception:
            logger