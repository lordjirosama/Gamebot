from telegram import BotCommand


# ============================================================
# SOLURIX COMMANDS
# ============================================================

COMMANDS = [
    BotCommand("start", "Start Solurix"),
    BotCommand("help", "Show all commands"),

    BotCommand("profile", "View your profile"),
    BotCommand("stats", "View your statistics"),
    BotCommand("rank", "View group ranking"),

    BotCommand("daily", "Claim your daily reward"),
    BotCommand("weekly", "Claim your weekly reward"),
    BotCommand("coins", "Check your coin balance"),

    BotCommand("battle", "Battle another player"),
    BotCommand("hunt", "Go on a hunt"),
    BotCommand("train", "Train your character"),
    BotCommand("explore", "Explore the world"),

    BotCommand("level", "Check your level"),
    BotCommand("history", "View your game history"),

    BotCommand("support", "Open Solurix support"),

    BotCommand("reset", "Reset a player's progress"),
]


def get_commands():
    """Return the complete Solurix command list."""
    return COMMANDS