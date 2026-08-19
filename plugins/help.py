from telegram import Update
from telegram.ext import ContextTypes
from config import BRAND_CHANNEL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "⚔️ <b>Welcome to Solurix</b>\n\n"
        "Enter the RPG arena, earn XP, collect coins, and climb your group's leaderboard.\n\n"
        "🎮 <b>Quick Commands</b>\n"
        "/profile — View your stats\n"
        "/daily — Claim your daily reward\n"
        "/battle — Fight for XP and points\n"
        "/rank — View the group ranking\n"
        "/help — Show all commands\n\n"
        f"✨ <a href=\"{BRAND_CHANNEL}\">Solurix Bots</a>"
    )
    await update.message.reply_html(text)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📖 <b>Solurix Command Guide</b>\n\n"
        "👤 <b>Player</b>\n"
        "/profile — Your profile and stats\n"
        "/daily — Daily coins and XP\n"
        "/battle — Random RPG battle\n"
        "/rank — Group leaderboard\n\n"
        "🛡️ <b>Admin</b>\n"
        "/reset — Reset this group's Solurix data\n\n"
        "💡 Battle, earn XP, level up, and compete with your group."
    )
    await update.message.reply_html(text)
