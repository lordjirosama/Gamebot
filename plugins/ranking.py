from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CommandHandler

from database import (
    ensure_user,
    get_group_ranking,
)


# ============================================================
# RANKING
# ============================================================

def ranking_text(ranking: list) -> str:
    """Build the group ranking message."""

    if not ranking:
        return (
            "<b>🏆 Solurix Group Ranking</b>\n\n"
            "No players have joined the ranking yet."
        )

    medals = ["🥇", "🥈", "🥉"]

    lines = [
        "<b>🏆 Solurix Group Ranking</b>",
        "",
    ]

    for position, player in enumerate(ranking, start=1):

        medal = (
            medals[position - 1]
            if position <= 3
            else f"<b>{position}.</b>"
        )

        name = player.get("first_name") or "Player"
        level = player.get("level", 1)
        xp = player.get("xp", 0)
        coins = player.get("coins", 0)

        lines.append(
            f"{medal} <b>{name}</b>\n"
            f"   ⭐ Level {level} • ✨ {xp} XP • 💰 {coins} coins"
        )

    lines.extend(
        [
            "",
            "Keep playing, earn XP and climb the leaderboard! ⚔️",
        ]
    )

    return "\n".join(lines)


# ============================================================
# RANKING BUTTONS
# ============================================================

def ranking_keyboard() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔄 Refresh",
                    callback_data="ranking_refresh",
                )
            ]
        ]
    )


# ============================================================
# /RANK
# ============================================================

async def rank_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    user = update.effective_user
    chat = update.effective_chat

    if not user or not update.message or not chat:
        return

    ensure_user(
        user_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "",
    )

    # Ranking is intended for groups.
    if chat.type not in ("group", "supergroup"):

        await update.message.reply_text(
            "🏆 <b>Group Ranking</b>\n\n"
            "Use /rank inside a group to see its leaderboard.",
            parse_mode="HTML",
        )

        return

    ranking = get_group_ranking(
        chat.id,
        limit=10,
    )

    await update.message.reply_text(
        ranking_text(ranking),
        reply_markup=ranking_keyboard(),
        parse_mode="HTML",
    )


# ============================================================
# REFRESH RANKING
# ============================================================

async def ranking_refresh(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    query = update.callback_query

    if not query:
        return

    await query.answer("Ranking updated.")

    chat = query.message.chat

    if chat.type not in ("group", "supergroup"):
        return

    ranking = get_group_ranking(
        chat.id,
        limit=10,
    )

    try:

        await query.edit_message_text(
            ranking_text(ranking),
            reply_markup=ranking_keyboard(),
            parse_mode="HTML",
        )

    except Exception:
        pass


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register ranking handlers."""

    application.add_handler(
        CommandHandler(
            "rank",
            rank_command,
        )
    )

    from telegram.ext import CallbackQueryHandler

    application.add_handler(
        CallbackQueryHandler(
            ranking_refresh,
            pattern=r"^ranking_refresh$",
        )
    )