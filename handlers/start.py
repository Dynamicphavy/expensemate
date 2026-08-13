from telegram import Update
from telegram.ext import ContextTypes

WELCOME_MESSAGE = (
    "👋 *Welcome to ExpenseMate!*\n\n"
    "I help you track your income and expenses.\n\n"
    "Try:\n"
    "/expense \\- record money spent\n"
    "/income \\- record money received\n"
    "/balance \\- see your current balance\n"
    "/help \\- show detailed usage instructions"   
)

HELP_MESSAGE = (
    "🧾 *ExpenseMate Help*\n\n"
    "*Record an expense:*\n"
    "`/expense <amount> <category>`\n"
    "Example: `/expense 1500 food`\n\n"
    "*Record income:*\n"
    "`/income <amount> <source>`\n"
    "Example: `/income 20000 allowance`\n\n"
    "*Check your balance:*\n"
    "`/balance`\n"
    "Shows total income, total expenses, and your remaining balance\\.\n\n"
    "All amounts are numbers only \\(no commas\\)\\. Category/source can be "
    "one word or a short phrase\\."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode="MarkdownV2")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_MESSAGE, parse_mode="MarkdownV2")