import random
import time

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from config import (
    XP_PER_MESSAGE,
    XP_COOLDOWN,
    BATTLE_COOLDOWN,
    BATTLE_MIN_REWARD,
    BATTLE_MAX_REWARD,
    HUNT_COOLDOWN,
    HUNT_MIN_REWARD,
    HUNT_MAX_REWARD,
)

from database import (
    ensure_user,
    get_user,
    add_coins,
    add_xp,
    increment_stat,
    add_history,
    get_cooldown,
    set_cooldown,
    add_group_member,
)


# ============================================================
# LEVEL SYSTEM
# ============================================================

def xp_required(level: int) -> int:
    """Return XP required for the next level."""

    return level * 100


def process_xp(user_id: int, amount: int) -> tuple[int, bool]:
    """
    Add XP and automatically handle level ups.

    Returns:
        (new_level, level_up)
    """

    user = get_user(user_id)

    if not user:
        return 1, False

    old_level = user["level"]

    add_xp(user_id, amount)

    user = get_user(user_id)

    if not user:
        return old_level, False

    current_level = user["level"]
    current_xp = user["xp"]

    new_level = current_level

    while current_xp >= xp_required(new_level):
        current_xp -= xp_required(new_level)
        new_level += 1

    if new_level != current_level:

        # Keep total XP in database.
        from database import set_level

        set_level(
            user_id,
            new_level,
        )

        return new_level, True

    return old_level, False


# ============================================================
# COOLDOWN
# ============================================================

def cooldown_remaining(
    user_id: int,
    action: str,
    cooldown: int,
) -> int:
    """Return remaining cooldown seconds."""

    last_used = get_cooldown(
        user_id,
        action,
    )

    remaining = cooldown - (
        time.time() - last_used
    )

    return max(
        0,
        int(remaining),
    )


def use_action(
    user_id: int,
    action: str,
) -> None:
    """Save action usage time."""

    set_cooldown(
        user_id,
        action,
        time.time(),
    )


# ============================================================
# MESSAGE XP
# ============================================================

async def message_xp(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    if not update.effective_user:
        return

    user = update.effective_user

    # Ignore commands
    if update.message and update.message.text:
        if update.message.text.startswith("/"):
            return

    ensure_user(
        user_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "",
    )

    # Register group member
    if update.effective_chat and update.effective_chat.type in (
        "group",
        "supergroup",
    ):
        add_group_member(
            update.effective_chat.id,
            user.id,
        )

    remaining = cooldown_remaining(
        user.id,
        "message_xp",
        XP_COOLDOWN,
    )

    if remaining > 0:
        return

    use_action(
        user.id,
        "message_xp",
    )

    increment_stat(
        user.id,
        "messages",
    )

    old_user = get_user(user.id)

    old_level = (
        old_user["level"]
        if old_user
        else 1
    )

    new_level, level_up = process_xp(
        user.id,
        XP_PER_MESSAGE,
    )

    if level_up and update.message:

        await update.message.reply_text(
            f"🎉 <b>Level Up!</b>\n\n"
            f"You reached <b>Level {new_level}</b>! ⭐",
            parse_mode="HTML",
        )


# ============================================================
# /BATTLE
# ============================================================

async def battle_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    user = update.effective_user

    if not user or not update.message:
        return

    ensure_user(
        user.id,
        user.username or "",
        user.first_name or "",
    )

    remaining = cooldown_remaining(
        user.id,
        "battle",
        BATTLE_COOLDOWN,
    )

    if remaining > 0:

        await update.message.reply_text(
            f"⚔️ Your battle cooldown is active.\n"
            f"Try again in <b>{remaining}s</b>.",
            parse_mode="HTML",
        )

        return

    use_action(
        user.id,
        "battle",
    )

    increment_stat(
        user.id,
        "battles",
    )

    won = random.choice(
        [True, False]
    )

    if won:

        reward = random.randint(
            BATTLE_MIN_REWARD,
            BATTLE_MAX_REWARD,
        )

        add_coins(
            user.id,
            reward,
        )

        increment_stat(
            user.id,
            "wins",
        )

        process_xp(
            user.id,
            20,
        )

        add_history(
            user.id,
            "battle",
            "win",
            reward,
        )

        text = (
            "⚔️ <b>Battle Result</b>\n\n"
            "🏆 You won the battle!\n\n"
            f"💰 Reward: <b>+{reward} coins</b>\n"
            "✨ XP: <b>+20</b>"
        )

    else:

        increment_stat(
            user.id,
            "losses",
        )

        process_xp(
            user.id,
            5,
        )

        add_history(
            user.id,
            "battle",
            "loss",
            0,
        )

        text = (
            "⚔️ <b>Battle Result</b>\n\n"
            "💔 You lost the battle.\n\n"
            "✨ XP: <b>+5</b>"
        )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
    )


# ============================================================
# /HUNT
# ============================================================

async def hunt_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    user = update.effective_user

    if not user or not update.message:
        return

    ensure_user(
        user.id,
        user.username or "",
        user.first_name or "",
    )

    remaining = cooldown_remaining(
        user.id,
        "hunt",
        HUNT_COOLDOWN,
    )

    if remaining > 0:

        await update.message.reply_text(
            f"🎯 Hunt cooldown is active.\n"
            f"Try again in <b>{remaining}s</b>.",
            parse_mode="HTML",
        )

        return

    use_action(
        user.id,
        "hunt",
    )

    increment_stat(
        user.id,
        "hunts",
    )

    reward = random.randint(
        HUNT_MIN_REWARD,
        HUNT_MAX_REWARD,
    )

    add_coins(
        user.id,
        reward,
    )

    process_xp(
        user.id,
        10,
    )

    add_history(
        user.id,
        "hunt",
        "success",
        reward,
    )

    await update.message.reply_text(
        "🎯 <b>Hunt Complete!</b>\n\n"
        f"💰 Coins found: <b>+{reward}</b>\n"
        "✨ XP gained: <b>+10</b>",
        parse_mode="HTML",
    )


# ============================================================
# /TRAIN
# ============================================================

async def train_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    user = update.effective_user

    if not user or not update.message:
        return

    ensure_user(
        user.id,
        user.username or "",
        user.first_name or "",
    )

    remaining = cooldown_remaining(
        user.id,
        "train",
        60,
    )

    if remaining > 0:

        await update.message.reply_text(
            f"🏋️ Training cooldown is active.\n"
            f"Try again in <b>{remaining}s</b>.",
            parse_mode="HTML",
        )

        return

    use_action(
        user.id,
        "train",
    )

    xp = random.randint(
        10,
        30,
    )

    process_xp(
        user.id,
        xp,
    )

    add_history(
        user.id,
        "train",
        "success",
        0,
    )

    await update.message.reply_text(
        "🏋️ <b>Training Complete!</b>\n\n"
        f"✨ XP gained: <b>+{xp}</b>",
        parse_mode="HTML",
    )


# ============================================================
# /EXPLORE
# ============================================================

async def explore_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    user = update.effective_user

    if not user or not update.message:
        return

    ensure_user(
        user.id,
        user.username or "",
        user.first_name or "",
    )

    remaining = cooldown_remaining(
        user.id,
        "explore",
        60,
    )

    if remaining > 0:

        await update.message.reply_text(
            f"🗺 Exploration cooldown is active.\n"
            f"Try again in <b>{remaining}s</b>.",
            parse_mode="HTML",
        )

        return

    use_action(
        user.id,
        "explore",
    )

    locations = [
        "Ancient Forest",
        "Mystic Valley",
        "Forgotten Ruins",
        "Shadow Mountains",
        "Crystal Lake",
    ]

    location = random.choice(
        locations
    )

    reward = random.randint(
        10,
        50,
    )

    add_coins(
        user.id,
        reward,
    )

    process_xp(
        user.id,
        15,
    )

    add_history(
        user.id,
        "explore",
        location,
        reward,
    )

    await update.message.reply_text(
        "🗺 <b>Exploration Complete!</b>\n\n"
        f"📍 Location: <b>{location}</b>\n"
        f"💰 Coins found: <b>+{reward}</b>\n"
        "✨ XP gained: <b>+15</b>",
        parse_mode="HTML",
    )


# ============================================================
# PLUGIN SETUP
# ============================================================

def setup(application) -> None:
    """Register all game handlers."""

    application.add_handler(
        CommandHandler(
            "battle",
            battle_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "hunt",
            hunt_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "train",
            train_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "explore",
            explore_command,
        )
    )

    # Message XP handler
    application.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND,
            message_xp,
        )
    )