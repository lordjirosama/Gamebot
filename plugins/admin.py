from telegram import Update
from telegram.ext import ContextTypes
from database import reset_chat

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = await update.effective_chat.get_member(update.effective_user.id)
    if member.status not in ("administrator", "creator"):
        await update.message.reply_text("🛡️ Only group administrators can use /reset.")
        return

    reset_chat(update.effective_chat.id)
    await update.message.reply_text(
        "♻️ Solurix data for this group has been reset successfully."
    )
