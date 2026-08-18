import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TOKEN
from database import init_db
from plugins.profile import profile
from plugins.game import daily, battle
from plugins.ranking import rank
from plugins.admin import reset
from plugins.help import help_cmd, start

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("solurix")

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is missing. Put it in .env")
    init_db()
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("me", profile))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("battle", battle))
    app.add_handler(CommandHandler("rank", rank))
    app.add_handler(CommandHandler("ranking", rank))
    app.add_handler(CommandHandler("reset", reset))

    logger.info("Solurix is starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
