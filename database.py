# FIXME: Integrating transactions data to the supabase database
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from datetime import date, datetime

from config import SUPABASE_DB_URL


@contextmanager
def get_connection():
    """Yields a Postgres connection and guarantees"""
    conn = psycopg2.connect(SUPABASE_DB_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Creates the transactions table if it doesn't already exist. Call once at startup."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id            SERIAL PRIMARY KEY,
                    telegram_id   BIGINT NOT NULL,
                    type          TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                    amount        NUMERIC NOT NULL,
                    category      TEXT NOT NULL,
                    description   TEXT,
                    date          TIMESTAMP NOT NULL
                )
                """
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_telegram_id ON transactions (telegram_id)"
            )


def add_transaction(telegram_id: int, tx_type: str, amount: float, category: str, description: str = None) -> int:
    """
    Inserts a new income/expense record
    Returns the new row's id.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO transactions (telegram_id, type, amount, category, description, date)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (telegram_id, tx_type, amount, category, description, datetime.now())
            )
            return cur.fetchone()["id"]


def get_totals(telegram_id: int) -> dict:
    """
    Returns {'income': float, 'expense': float, 'balance': float} for a user.
    Missing transaction types default to 0.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT type, COALESCE(SUM(amount), 0) AS total
                FROM transactions
                WHERE telegram_id = %s
                GROUP BY type
                """,
                (telegram_id,),
            )
            rows = cur.fetchall()

    totals = {"income": 0.0, "expense": 0.0}
    for row in rows:
        totals[row["type"]] = float(row["total"])

    totals["balance"] = totals["income"] - totals["expense"]
    return totals


def get_transactions(telegram_id: int, tx_type: str = None, limit: int = None):
    """
    Returns a list of transactions for a user, most recent first.
    Optionally filter by type ('income'/'expense') and limit the number of rows.
    """
    query = "SELECT * FROM transactions WHERE telegram_id = %s"
    params = [telegram_id]

    if tx_type:
        query += " AND type = %s"
        params.append(tx_type)

    query += " ORDER BY date DESC"

    if limit:
        query += " LIMIT %s"
        params.append(limit)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

    return [dict(row) for row in rows]