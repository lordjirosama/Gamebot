from telegram import Update
from telegram.ext import ContextTypes
from database import ensure_player, get_player

def bar(value, total=100, size=10):
    filled = min(size, int((value % total) / total * size))
    return "▰" * filled + "▱" * (size - filled)

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    c = update.effective_chat
    ensure_player(u.id, c.id, u.username, u.full_name)
    p = get_player(u.id, c.id)
    winrate = (p["wins"] / (p["wins"] + p["losses"]) * 100) if (p["wins"] + p["losses"]) else 0

    text = (
        f"👤 <b>{p['name']}</b>\n"
        f"⚔️ Level <b>{p['level']}</b>  •  ⭐ {p['points']} points\n\n"
        f"✨ XP: <b>{p['xp']}</b>\n"
        f"🪙 Coins: <b>{p['coins']}</b>\n"
        f"🏆 Wins: <b>{p['wins']}</b>\n"
        f"💀 Losses: <b>{p['losses']}</b>\n"
        f"📈 Win rate: <b>{winrate:.0f}%</b>\n\n"
        f"{bar(p['xp'])}"
    )
    await update.message.reply_html(text)
