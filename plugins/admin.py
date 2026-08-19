from telegram import Update
from telegram.ext import ContextTypes

from database import (
    reset_chat,
    get_all_users,
)


async def is_admin(update: Update):
    user = update.effective_user
    chat = update.effective_chat

    if not user or not chat:
        return False

    if chat.type not in ("group", "supergroup"):
        return False

    member = await chat.get_member(user.id)

    return member.status in (
        "administrator",
        "creator",
    )


async def reset(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not await is_admin(update):
        await update.message.reply_text(
            "Only group administrators can use /reset."
        )
        return

    reset_chat(
        update.effective_chat.id
    )

    await update.message.reply_text(
        "Solurix data for this group "
        "has been reset successfully."
    )


async def broadcast(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not await is_admin(update):
        await update.message.reply_text(
            "Only group administrators can use /broadcast."
        )
        return

    if not context.args:
        await update.message.reply_text(
            "Usage:\n"
            "/broadcast Your message here"
        )
        return

    message = " ".join(context.args)

    users = get_all_users()

    if not users:
        await update.message.reply_text(
            "There are no registered users yet."
        )
        return

    status_message = await update.message.reply_text(
        "Broadcast started..."
    )

    sent = 0
    failed = 0

    for row in users:
        user_id = row["user_id"]

        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=message,
            )

            sent += 1

        except Exception:
            failed += 1

    await status_message.edit_text(
        "Broadcast completed.\n\n"
        f"Sent: {sent}\n"
        f"Failed: {failed}"
    )