from telegram import Update
from telegram.ext import ContextTypes

from database import (
    ensure_player,
    top_players,
)


async def rank(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user = update.effective_user
    chat = update.effective_chat

    ensure_player(
        user.id,
        chat.id,
        user.username,
        user.full_name,
    )

    rows = top_players(
        chat.id,
        limit=10,
    )

    if not rows:
        await update.message.reply_text(
            "No players have joined the leaderboard yet."
        )
        return

    medals = [
        "🥇",
        "🥈",
        "🥉",
    ]

    lines = [
        "<b>Solurix Group Ranking</b>",
        "",
    ]

    for position, player in enumerate(
        rows,
        start=1,
    ):
        if position <= 3:
            prefix = medals[
                position - 1
            ]
        else:
            prefix = f"<b>{position}.</b>"

        name = player["name"]

        lines.append(
            f"{prefix} "
            f"<b>{name}</b>\n"
            f"   Points: "
            f"<b>{player['points']}</b> • "
            f"Level: "
            f"<b>{player['level']}</b> • "
            f"XP: "
            f"<b>{player['xp']}</b>"
        )

    await update.message.reply_html(
        "\n".join(lines)
    )