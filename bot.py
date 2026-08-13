import logging

from telegram.ext import ApplicationBuilder, CommandHandler

from config import BOT_TOKEN
from database import init_db
from handlers.start import start, help_command
from handlers.expense import expense
from handlers.income import income
from handlers.balance import balance

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    init_db()
    logger.info("Database ready.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("expense", expense))
    app.add_handler(CommandHandler("income", income))
    app.add_handler(CommandHandler("balance", balance))

    logger.info("ExpenseMate is starting... press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()