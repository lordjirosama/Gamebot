import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN", "8997991259:AAHcURkl4XSwEpfFPeyIEPSLjl0WnkJyke0").strip()
BOT_NAME = "Solurix"
BRAND_CHANNEL = "https://t.me/Solurix_bots"
DB_PATH = os.getenv("DB_PATH", "data/solurix.db")
