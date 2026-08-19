import random
from datetime import datetime, timezone, timedelta

from telegram import Update
from telegram.ext import ContextTypes

from database import (
    ensure_player,
    get_player,
    add_progress,
    set_daily,
    set_kill_time,
    set_protection,
    record_kill,
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


async def protect(
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

    player = get_player(
        user.id,
        chat.id,
    )

    if not context.args:
        await update.message.reply_html(
            "<b>Protection</b>\n\n"
            "Choose a protection duration:\n\n"
            "/protect 1h — 149 Coins\n"
            "/protect 12h — 500 Coins\n"
            "/protect 24h — 900 Coins"
        )
        return

    duration = context.args[0].lower()

    prices = {
        "1h": (1, 149),
        "12h": (12, 500),
        "24h": (24, 900),
    }

    if duration not in prices:
        await update.message.reply_html(
            "<b>Invalid protection duration.</b>\n\n"
            "/protect 1h — 149 Coins\n"
            "/protect 12h — 500 Coins\n"
            "/protect 24h — 900 Coins"
        )
        return

    hours, price = prices[duration]

    if player["coins"] < price:
        await update.message.reply_html(
            "<b>Not enough coins.</b>\n\n"
            f"Required: <b>{price}</b> coins\n"
            f"Your coins: <b>{player['coins']}</b>"
        )
        return

    current_protection = parse_time(
        player["protected_until"]
    )

    current_time = now_utc()

    if current_protection and current_protection > current_time:
        await update.message.reply_html(
            "<b>You are already protected.</b>\n\n"
            f"Protection ends at:\n"
            f"<code>{current_protection.isoformat()}</code>"
        )
        return

    protected_until = current_time + timedelta(
        hours=hours
    )

    add_progress(
        user.id,
        chat.id,
        coins=-price,
    )

    set_protection(
        user.id,
        chat.id,
        protected_until.isoformat(),
    )

    await update.message.reply_html(
        "<b>Protection Activated</b>\n\n"
        f"Duration: <b>{duration}</b>\n"
        f"Cost: <b>{price} Coins</b>\n\n"
        "Other players cannot kill you "
        "while your protection is active."
    )


async def kill(
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

    killer = get_player(
        user.id,
        chat.id,
    )

    # Kill cooldown
    last_kill = parse_time(
        killer["last_kill"]
    )

    current_time = now_utc()

    if last_kill:
        next_kill = last_kill + timedelta(hours=24)

        if next_kill > current_time:
            remaining = next_kill - current_time

            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60

            await update.message.reply_html(
                "<b>Kill Cooldown Active</b>\n\n"
                f"You can kill again in "
                f"<b>{hours}h {minutes}m</b>."
            )
            return

    # Target must be a replied message
    if not update.message.reply_to_message:
        await update.message.reply_html(
            "<b>How to use /kill</b>\n\n"
            "Reply to the player's message with:\n"
            "<code>/kill</code>"
        )
        return

    target_user = (
        update.message.reply_to_message.from_user
    )

    if not target_user:
        await update.message.reply_text(
            "This user cannot be targeted."
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

    # Protection check
    protected_until = parse_time(
        target["protected_until"]
    )

    if protected_until and protected_until > current_time:
        await update.message.reply_html(
            f"<b>{target['name']}</b> is currently protected."
        )
        return

    # Reward calculation
    target_points = max(
        0,
        target["points"],
    )

    target_coins = max(
        0,
        target["coins"],
    )

    if target_coins > 0:
        reward_coins = target_coins
    else:
        reward_coins = random.randint(
            100,
            200,
        )

    record_kill(
        user.id,
        chat.id,
        target_user.id,
        chat.id,
        reward_coins,
        target_points,
    )

    set_kill_time(
        user.id,
        chat.id,
        current_time.isoformat(),
    )

    bonus_xp = random.randint(
        30,
        60,
    )

    add_progress(
        user.id,
        chat.id,
        xp=bonus_xp,
    )

    await update.message.reply_html(
        "<b>Target Eliminated</b>\n\n"
        f"Target: <b>{target['name']}</b>\n\n"
        f"+{reward_coins} Coins\n"
        f"+{target_points} Points\n"
        f"+{bonus_xp} XP\n\n"
        "Your next kill will be available "
        "after 24 hours."
    )


async def train(
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

    xp = random.randint(
        10,
        25,
    )

    coins = random.randint(
        5,
        15,
    )

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

    locations = [
        "Mystic Forest",
        "Crystal Valley",
        "Ancient Ruins",
        "Moonlit Village",
        "Sky Island",
    ]

    location = random.choice(
        locations
    )

    xp = random.randint(
        15,
        35,
    )

    coins = random.randint(
        15,
        50,
    )

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