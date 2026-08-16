import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError(
        "BOT_TOKEN is missing."
    )

CURRENCY_SYMBOL = os.getenv("CURRENCY_SYMBOL", "₦")

# FIXME: Configuring the database using supabase
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

if not SUPABASE_DB_URL:
    raise ValueError(
        "SUPABASE_DB_URL is missing. Add it to your .env file. "
        "Find it in your Supabase project: Settings > Database > Connection string"
    )