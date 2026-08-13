from telegram import Update
from telegram.ext import ContextTypes

from config import CURRENCY_SYMBOL
from database import add_transaction

USAGE = "Usage: `/income <amount> <source>`\nExample: `/income 20000 allowance`"


async def income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) < 2:
        await update.message.reply_text(USAGE, parse_mode="Markdown")
        return

    raw_amount = args[0]
    source = " ".join(args[1:]).strip()

    try:
        amount = float(raw_amount)
    except ValueError:
        await update.message.reply_text(
            f"⚠️ '{raw_amount}' isn't a valid amount. " + USAGE, parse_mode="Markdown"
        )
        return

    if amount <= 0:
        await update.message.reply_text("⚠️ Amount must be greater than 0.")
        return

    telegram_id = update.effective_user.id
    add_transaction(telegram_id, "income", amount, source)

    await update.message.reply_text(
        "✅ *Income recorded*\n\n"
        f"Amount: {CURRENCY_SYMBOL}{amount:,.2f}\n"
        f"Source: {source.title()}",
        parse_mode="Markdown",
    )
    