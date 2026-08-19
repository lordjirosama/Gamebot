from telegram import BotCommand
from telegram.ext import Application


# ============================================================
# SOLURIX COMMANDS
# ============================================================

COMMANDS = [
    # Basic
    BotCommand("start", "Start Solurix"),
    BotCommand("help", "Show all commands"),

    # Profile
    BotCommand("profile", "View your profile"),
    BotCommand("stats", "View your statistics"),
    BotCommand("rank", "View group ranking"),

    # Rewards
    BotCommand("daily", "Claim your daily reward"),
    BotCommand("weekly", "Claim your weekly reward"),
    BotCommand("coins", "Check your coin balance"),

    # Game
    BotCommand("battle", "Battle another player"),
    BotCommand("hunt", "Go on a hunt"),
    BotCommand("train", "Train your character"),
    BotCommand("explore", "Explore the world"),

    # Game information
    BotCommand("level", "Check your level"),
    BotCommand("history", "View your game history"),

    # Support
    BotCommand("support", "Open Solurix support"),

    # Admin
    BotCommand("reset", "Reset a player's progress"),
]


# ============================================================
# SET COMMANDS
# ============================================================

async def set_commands(application: Application) -> None:
    """
    Set Solurix commands in Telegram.

    These commands appear when the user types "/".
    """

    await application.bot.set_my_commands(COMMANDS)


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application: Application) -> None:
    """
    Register command menu setup.

    bot.py calls this when loading plugins.
    """

    application.post_init = set_commands