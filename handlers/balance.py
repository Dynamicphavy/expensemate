from telegram import Update
from telegram.ext import ContextTypes

from config import CURRENCY_SYMBOL
from database import get_totals

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    totals = get_totals(telegram_id)

    income_str = f"{CURRENCY_SYMBOL}{totals['income']:,.2f}"
    expense_str = f"{CURRENCY_SYMBOL}{totals['expense']:,.2f}"
    balance_str = f"{CURRENCY_SYMBOL}{totals['balance']:,.2f}"

    # Pad so the numbers roughly line up in a monospace block
    width = max(len(income_str), len(expense_str), len(balance_str)) + 2

    message = (
        "📊 *Your Balance*\n\n"
        "```\n"
        f"Total income:    {income_str}\n"
        f"Total expenses:  {expense_str}\n"
        f"{'-' * width}\n"
        f"Balance:         {balance_str}\n"
        "```"
    )

    await update.message.reply_text(message, parse_mode="Markdown")