import random
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import ContextTypes
from database import ensure_player, get_player, add_progress, set_daily

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u, c = update.effective_user, update.effective_chat
    ensure_player(u.id, c.id, u.username, u.full_name)
    p = get_player(u.id, c.id)
    today = datetime.now(timezone.utc).date().isoformat()

    if p["last_daily"] == today:
        await update.message.reply_text("⏳ You already claimed today's reward. Come back tomorrow!")
        return

    set_daily(u.id, c.id, today)
    add_progress(u.id, c.id, xp=50, coins=100, points=25)
    await update.message.reply_html(
        "🎁 <b>Daily Reward Claimed!</b>\n\n"
        "✨ +50 XP\n🪙 +100 Coins\n⭐ +25 Points\n\n"
        "Come back tomorrow for another reward!"
    )

async def battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u, c = update.effective_user, update.effective_chat
    ensure_player(u.id, c.id, u.username, u.full_name)
    enemy = random.choice(["Shadow Beast", "Iron Golem", "Void Knight", "Crimson Wolf", "Storm Drake"])
    won = random.random() < 0.58

    if won:
        xp, coins, points = random.randint(25, 50), random.randint(20, 45), random.randint(10, 25)
        add_progress(u.id, c.id, xp=xp, coins=coins, points=points, win=True)
        await update.message.reply_html(
            f"⚔️ <b>Battle Won!</b>\n\n"
            f"👾 Enemy: <b>{enemy}</b>\n"
            f"✨ +{xp} XP\n🪙 +{coins} Coins\n⭐ +{points} Points"
        )
    else:
        xp = random.randint(8, 18)
        add_progress(u.id, c.id, xp=xp, loss=True)
        await update.message.reply_html(
            f"💥 <b>Battle Lost</b>\n\n"
            f"👾 Enemy: <b>{enemy}</b>\n"
            f"✨ +{xp} XP consolation XP\n\n"
            "Train harder and return to the arena!"
        )
