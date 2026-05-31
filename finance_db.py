import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


DB_FILE = Path(__file__).resolve().parent / "finance_bot.db"


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_FILE)
    try:
        conn.row_factory = sqlite3.Row
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                tx_type TEXT NOT NULL CHECK(tx_type IN ('income', 'expense')),
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                note TEXT,
                created_at TEXT NOT NULL
            )
            """
        )


def add_transaction(
    user_id: int,
    tx_type: str,
    amount: float,
    category: str,
    note: Optional[str] = None,
) -> int:
    created_at = datetime.utcnow().isoformat(timespec="seconds")
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO transactions (user_id, tx_type, amount, category, note, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, tx_type, amount, category.strip(), (note or "").strip(), created_at),
        )
        return int(cur.lastrowid)


def get_monthly_report(user_id: int, month: str) -> Dict[str, object]:
    # month format: YYYY-MM
    like_value = f"{month}%"
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT tx_type, COALESCE(SUM(amount), 0) AS total
            FROM transactions
            WHERE user_id = ? AND created_at LIKE ?
            GROUP BY tx_type
            """,
            (user_id, like_value),
        )
        rows = {row["tx_type"]: float(row["total"]) for row in cur.fetchall()}

        income_total = rows.get("income", 0.0)
        expense_total = rows.get("expense", 0.0)

        cur.execute(
            """
            SELECT tx_type, category, SUM(amount) AS total
            FROM transactions
            WHERE user_id = ? AND created_at LIKE ?
            GROUP BY tx_type, category
            ORDER BY tx_type, total DESC
            """,
            (user_id, like_value),
        )
        by_category = [
            (str(row["tx_type"]), str(row["category"]), float(row["total"]))
            for row in cur.fetchall()
        ]

    return {
        "month": month,
        "income_total": income_total,
        "expense_total": expense_total,
        "balance": income_total - expense_total,
        "by_category": by_category,
    }


def get_all_transactions(user_id: int) -> List[Dict]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, user_id, tx_type, amount, category, note, created_at
            FROM transactions
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,),
        )
        return [dict(row) for row in cur.fetchall()]


def parse_month_or_current(raw: Optional[str]) -> str:
    if raw:
        datetime.strptime(raw, "%Y-%m")
        return raw
    return datetime.utcnow().strftime("%Y-%m")
