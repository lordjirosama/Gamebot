import random
from datetime import datetime, timedelta, timezone

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import (
    ensure_player,
    get_player,
    add_progress,
    set_daily,
    set_protection,
    set_kill_cooldown,
    update_coins,
    update_points,
)


def now_utc():
    return datetime.now(timezone.utc)


def parse_time(value):
    if not value:
        return None

    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return None


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

    today = now_utc().date().isoformat()

    if player["last_daily"] == today:
        await update.message.reply_text(
            "You already claimed today's reward.\n"
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
        "<b>Daily Reward Claimed!</b>\n\n"
        "+50 XP\n"
        "+100 Coins\n"
        "+25 Points\n\n"
        "Come back tomorrow for another reward!"
    )


async def kill(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text(
            "The /kill command can only be used in groups."
        )
        return

    ensure_player(
        user.id,
        chat.id,
        user.username,
        user.full_name,
    )

    attacker = get_player(
        user.id,
        chat.id,
    )

    cooldown = parse_time(
        attacker["kill_cooldown_until"]
    )

    if cooldown and cooldown > now_utc():
        remaining = cooldown - now_utc()
        hours = int(remaining.total_seconds() // 3600)
        minutes = int(
            (remaining.total_seconds() % 3600) // 60
        )

        await update.message.reply_text(
            "You cannot kill another player yet.\n"
            f"Cooldown remaining: {hours}h {minutes}m."
        )
        return

    target_user = None

    if update.message.reply_to_message:
        target_user = (
            update.message.reply_to_message.from_user
        )

    elif context.args:
        username = context.args[0].lstrip("@").lower()

        players = []

        from database import get_group_players

        players = get_group_players(chat.id)

        for player in players:
            if (
                player["username"]
                and player["username"].lower() == username
            ):
                member = await chat.get_member(
                    player["user_id"]
                )
                target_user = member.user
                break

    if not target_user:
        await update.message.reply_text(
            "Reply to a user's message and use /kill\n"
            "or use /kill @username."
        )
        return

    if target_user.id == user.id:
        await update.message.reply_text(
            "You cannot kill yourself."
        )
        return

    if target_user.is_bot:
        await update.message.reply_text(
            "Bots cannot be targeted."
        )
        return

    ensure_player(
        target_user.id,
        chat.id,
        target_user.username,
        target_user.full_name,
    )

    target = get_player(
        target_user.id,
        chat.id,
    )

    protected_until = parse_time(
        target["protected_until"]
    )

    if protected_until and protected_until > now_utc():
        remaining = protected_until - now_utc()

        hours = int(
            remaining.total_seconds() // 3600
        )
        minutes = int(
            (remaining.total_seconds() % 3600) // 60
        )

        await update.message.reply_html(
            f"<b>{target['name']}</b> is protected.\n"
            f"Protection remaining: {hours}h {minutes}m."
        )
        return

    transferred_points = max(
        0,
        target["points"]
    )

    if target["coins"] > 0:
        stolen_coins = target["coins"]
    else:
        stolen_coins = random.randint(
            100,
            200
        )

    update_points(
        target_user.id,
        chat.id,
        -transferred_points,
    )

    update_coins(
        target_user.id,
        chat.id,
        -target["coins"],
    )

    add_progress(
        user.id,
        chat.id,
        xp=random.randint(25, 50),
        coins=stolen_coins,
        points=transferred_points,
        win=True,
        kill=True,
    )

    add_progress(
        target_user.id,
        chat.id,
        loss=True,
        death=True,
    )

    cooldown_until = (
        now_utc()
        + timedelta(hours=24)
    ).isoformat()

    set_kill_cooldown(
        user.id,
        chat.id,
        cooldown_until,
    )

    await update.message.reply_html(
        "<b>Player Eliminated</b>\n\n"
        f"Attacker: <b>{user.full_name}</b>\n"
        f"Target: <b>{target['name']}</b>\n\n"
        f"Points gained: <b>+{transferred_points}</b>\n"
        f"Coins gained: <b>+{stolen_coins}</b>\n\n"
        "Your next kill will be available in 24 hours."
    )


async def protect(
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

    player = get_player(
        user.id,
        chat.id,
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "1 Hour — 149 Coins",
                callback_data="protect_1"
            )
        ],
        [
            InlineKeyboardButton(
                "12 Hours — 500 Coins",
                callback_data="protect_12"
            )
        ],
        [
            InlineKeyboardButton(
                "24 Hours — 900 Coins",
                callback_data="protect_24"
            )
        ],
    ]

    await update.message.reply_html(
        "<b>Protection</b>\n\n"
        "Choose your protection duration.\n\n"
        "1 Hour — 149 Coins\n"
        "12 Hours — 500 Coins\n"
        "24 Hours — 900 Coins\n\n"
        f"Your coins: <b>{player['coins']}</b>",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def protection_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    chat = query.message.chat

    ensure_player(
        user.id,
        chat.id,
        user.username,
        user.full_name,
    )

    player = get_player(
        user.id,
        chat.id,
    )

    data = query.data

    plans = {
        "protect_1": (1, 149),
        "protect_12": (12, 500),
        "protect_24": (24, 900),
    }

    if data not in plans:
        return

    hours, price = plans[data]

    if player["coins"] < price:
        await query.edit_message_text(
            f"You need {price} coins.\n"
            f"You currently have {player['coins']} coins."
        )
        return

    current_protection = parse_time(
        player["protected_until"]
    )

    start_time = now_utc()

    if (
        current_protection
        and current_protection > start_time
    ):
        start_time = current_protection

    expires = (
        start_time
        + timedelta(hours=hours)
    ).isoformat()

    update_coins(
        user.id,
        chat.id,
        -price,
    )

    set_protection(
        user.id,
        chat.id,
        expires,
    )

    await query.edit_message_text(
        f"Protection activated for {hours} hour(s).\n\n"
        f"Coins spent: {price}\n"
        f"Remaining coins: {player['coins'] - price}\n\n"
        "Other players cannot kill you while protection is active."
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
        "<b>Training Complete!</b>\n\n"
        f"+{xp} XP\n"
        f"+{coins} Coins\n"
        "+5 Points"
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
        "<b>Exploration Complete!</b>\n\n"
        f"Location: <b>{location}</b>\n\n"
        f"+{xp} XP\n"
        f"+{coins} Coins\n"
        "+8 Points"
    )