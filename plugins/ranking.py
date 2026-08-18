from telegram import Update
from telegram.ext import ContextTypes
from database import ensure_player, top_players

async def rank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u, c = update.effective_user, update.effective_chat
    ensure_player(u.id, c.id, u.username, u.full_name)
    rows = top_players(c.id)

    if not rows:
        await update.message.reply_text("🏆 No players yet.")
        return

    medals = ["🥇", "🥈", "🥉"]
    lines = ["🏆 <b>Solurix Group Ranking</b>\n"]
    for i, p in enumerate(rows, 1):
        medal = medals[i-1] if i <= 3 else f"<b>{i}.</b>"
        lines.append(
            f"{medal} {p['name']} — ⭐ {p['points']} pts • "
            f"⚔️ Lv.{p['level']} • ✨ {p['xp']} XP"
        )
    await update.message.reply_html("\n".join(lines))
