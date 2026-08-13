import sqlite3
from contextlib import contextmanager
from datetime import datetime

from config import DB_PATH

@contextmanager
def get_connection():
    """Yields a SQLite connection and guarantees it is closed afterwards."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Creates the transcation table if it doesn't already exist. Call once at startup."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id   INTEGER NOT NULL,
                type          TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                amount        REAL NOT NULL,
                category      TEXT NOT NULL,
                description   TEXT,
                date          TEXT NOT NULL
            )
            """
        )
        # Helps balance/report queries scale once a user has many transactions
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_telegram_id ON transactions (telegram_id)"
        )


def add_transaction(telegram_id: int, tx_type: str, amount: float, category: str, description: str = None) -> int:
    """
    Inserts a new income/expense record.
    Returns the new row's id.
    """
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO transactions (telegram_id, type, amount, category, description, date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (telegram_id, tx_type, amount, category, description, datetime.now().isoformat(timespec="seconds")),
        )
        return cursor.lastrowid


def get_totals(telegram_id: int) -> dict:
    """
    Returns {'income': float, 'expense': float, 'balance': float} for a user.
    Missing transaction types default to 0.
    """
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT type, COALESCE(SUM(amount), 0) AS total
            FROM transactions
            WHERE telegram_id = ?
            GROUP BY type
            """,
            (telegram_id,),
        ).fetchall()

    totals = {"income": 0.0, "expense": 0.0}
    for row in rows:
        totals[row["type"]] = row["total"]

    totals["balance"] = totals["income"] - totals["expense"]
    return totals


def get_transactions(telegram_id: int, tx_type: str = None, limit: int = None):
    """
    Returns a list of transactions for a user, most recent first.
    Optionally filter by type ('income'/'expense') and limit the number of rows.
    """
    query = "SELECT * FROM transactions WHERE telegram_id = ?"
    params = [telegram_id]

    if tx_type:
        query += "AND type = ?"
        params.append(tx_type)

    query += " ORDER BY date DESC"

    if limit:
        query += "LIMIT ?"
        params.append(limit)

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()

    return [dict(row) for row in rows]