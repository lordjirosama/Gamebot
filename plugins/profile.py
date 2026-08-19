from datetime import datetime, timezone

from telegram import Update
from telegram.ext import ContextTypes

from database import (
    ensure_player,
    get_player,
)


def xp_bar(xp, size=10):
    current = xp % 100
    filled = int(
        current / 100 * size
    )

    return (
        "▰" * filled
        + "▱" * (size - filled)
    )


def get_remaining_time(stamp):
    if not stamp:
        return None

    try:
        target = datetime.fromisoformat(stamp)

        if target.tzinfo is None:
            target = target.replace(
                tzinfo=timezone.utc
            )

        remaining = (
            target -
            datetime.now(timezone.utc)
        )

        if remaining.total_seconds() <= 0:
            return None

        total_minutes = int(
            remaining.total_seconds() // 60
        )

        hours = total_minutes // 60
        minutes = total_minutes % 60

        return hours, minutes

    except ValueError:
        return None


def get_player_data(update):
    user = update.effective_user
    chat = update.effective_chat

    ensure_player(
        user.id,
        chat.id,
        user.username,
        user.full_name,
    )

    return (
        user,
        chat,
        get_player(
            user.id,
            chat.id,
        ),
    )


async def profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user, chat, player = get_player_data(
        update
    )

    total_games = (
        player["wins"] +
        player["losses"]
    )

    winrate = (
        player["wins"] /
        total_games *
        100
        if total_games
        else 0
    )

    protection = get_remaining_time(
        player["protected_until"]
    )

    kill_cooldown = get_remaining_time(
        player["last_kill"]
    )

    protection_text = (
        f"{protection[0]}h {protection[1]}m"
        if protection
        else "Not active"
    )

    if kill_cooldown:
        kill_text = (
            f"{kill_cooldown[0]}h "
            f"{kill_cooldown[1]}m"
        )
    else:
        kill_text = "Available"

    text = (
        "<b>PLAYER PROFILE</b>\n\n"

        f"Name: <b>{player['name']}</b>\n"
        f"Level: <b>{player['level']}</b>\n"
        f"Points: <b>{player['points']}</b>\n"
        f"XP: <b>{player['xp']}</b>\n"
        f"Coins: <b>{player['coins']}</b>\n\n"

        f"Wins: <b>{player['wins']}</b>\n"
        f"Losses: <b>{player['losses']}</b>\n"
        f"Win Rate: <b>{winrate:.0f}%</b>\n\n"

        f"Protection: <b>{protection_text}</b>\n"
        f"Next Kill: <b>{kill_text}</b>\n\n"

        f"{xp_bar(player['xp'])}"
    )

    await update.message.reply_html(
        text
    )


async def stats(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user, chat, player = get_player_data(
        update
    )

    total_games = (
        player["wins"] +
        player["losses"]
    )

    winrate = (
        player["wins"] /
        total_games *
        100
        if total_games
        else 0
    )

    await update.message.reply_html(
        "<b>YOUR STATISTICS</b>\n\n"

        f"Level: <b>{player['level']}</b>\n"
        f"XP: <b>{player['xp']}</b>\n"
        f"Coins: <b>{player['coins']}</b>\n"
        f"Points: <b>{player['points']}</b>\n\n"

        f"Wins: <b>{player['wins']}</b>\n"
        f"Losses: <b>{player['losses']}</b>\n"
        f"Total Games: <b>{total_games}</b>\n"
        f"Win Rate: <b>{winrate:.0f}%</b>"
    )


async def coins(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user, chat, player = get_player_data(
        update
    )

    await update.message.reply_html(
        "<b>YOUR COINS</b>\n\n"
        f"You currently have "
        f"<b>{player['coins']}</b> coins."
    )


async def level(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user, chat, player = get_player_data(
        update
    )

    next_level_xp = (
        player["level"] * 100
    )

    remaining = max(
        0,
        next_level_xp -
        player["xp"],
    )

    await update.message.reply_html(
        "<b>LEVEL INFORMATION</b>\n\n"

        f"Current Level: "
        f"<b>{player['level']}</b>\n"

        f"Current XP: "
        f"<b>{player['xp']}</b>\n"

        f"XP to next level: "
        f"<b>{remaining}</b>\n\n"

        "Keep playing to level up!"
    )