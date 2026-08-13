import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError(
        "BOT_TOKEN is missing."
    )

CURRENCY_SYMBOL = os.getenv("CURRENCY_SYMBOL", "₦")

DB_PATH = os.getenv("DB_PATH", "expensemate.db")