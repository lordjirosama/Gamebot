import random
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import ContextTypes

from database import (
    ensure_player,
    get_player,
    add_progress,
    set_daily,
)


async def daily(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user
    chat = update.effective_chat

    ensure_player(
        user.id,
        chat.id,
        user.username,
        user.full_name,
    )

    player = get_player(user.id, chat.id)

    today = datetime.now(
        timezone.utc
    ).date().isoformat()

    if player["last_daily"] == today:
        await update.message.reply_text(
            "⏳ You already claimed today's reward.\n"
            "Come back tomorrow!"
        )
        return

    set_daily(
        user.id,
        chat.id,
        today,
    )

    add_progress(
        user.id,
        chat.id,
        xp=50,
        coins=100,
        points=25,
    )

    await update.message.reply_html(
        "🎁 <b>Daily Reward Claimed!</b>\n\n"
        "✨ +50 XP\n"
        "🪙 +100 Coins\n"
        "⭐ +25 Points\n\n"
        "Come back tomorrow for another reward!"
    )


async def battle(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user
    chat = update.effective_chat

    ensure_player(
        user.id,
        chat.id,
        user.username,
        user.full_name,
    )

    enemy = random.choice([
        "Shadow Beast",
        "Iron Golem",
        "Void Guardian",
        "Crimson Wolf",
        "Storm Drake",
    ])

    won = random.random() < 0.58

    if won:
        xp = random.randint(25, 50)
        coins = random.randint(20, 45)
        points = random.randint(10, 25)

        add_progress(
            user.id,
            chat.id,
            xp=xp,
            coins=coins,
            points=points,
            win=True,
        )

        await update.message.reply_html(
            "🏆 <b>Battle Won!</b>\n\n"
            f"👾 Encounter: <b>{enemy}</b>\n\n"
            f"✨ +{xp} XP\n"
            f"🪙 +{coins} Coins\n"
            f"⭐ +{points} Points"
        )

    else:
        xp = random.randint(8, 18)

        add_progress(
            user.id,
            chat.id,
            xp=xp,
            loss=True,
        )

        await update.message.reply_html(
            "💫 <b>Battle Lost</b>\n\n"
            f"👾 Encounter: <b>{enemy}</b>\n\n"
            f"✨ +{xp} consolation XP\n\n"
            "Train harder and try again!"
        )


async def train(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user
    chat = update.effective_chat

    ensure_player(
        user.id,
        chat.id,
        user.username,
        user.full_name,
    )

    xp = random.randint(10, 25)
    coins = random.randint(5, 15)

    add_progress(
        user.id,
        chat.id,
        xp=xp,
        coins=coins,
        points=5,
    )

    await update.message.reply_html(
        "🏋️ <b>Training Complete!</b>\n\n"
        f"✨ +{xp} XP\n"
        f"🪙 +{coins} Coins\n"
        "⭐ +5 Points"
    )


async def explore(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user
    chat = update.effective_chat

    ensure_player(
        user.id,
        chat.id,
        user.username,
        user.full_name,
    )

    locations = [
        "Mystic Forest",
        "Crystal Valley",
        "Ancient Ruins",
        "Moonlit Village",
        "Sky Island",
    ]

    location = random.choice(locations)
    xp = random.randint(15, 35)
    coins = random.randint(15, 50)

    add_progress(
        user.id,
        chat.id,
        xp=xp,
        coins=coins,
        points=8,
    )

    await update.message.reply_html(
        "🗺️ <b>Exploration Complete!</b>\n\n"
        f"📍 Location: <b>{location}</b>\n\n"
        f"✨ +{xp} XP\n"
        f"🪙 +{coins} Coins\n"
        "⭐ +8 Points"
    )