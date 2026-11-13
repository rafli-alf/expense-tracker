import sqlite3
import os
from pathlib import Path

DB_PATH = Path(os.environ.get("EXPENSE_DB", "expenses.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount INTEGER NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL
);
"""

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(SCHEMA)

def add_expense(amount: int, description: str, category: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO expenses(amount, description, category) VALUES (?, ?, ?)",
            (amount, description, category)
        )

def list_expenses(target_category: str | None = None) -> None:
    query = "SELECT id, amount, description, category FROM expenses"
    param = []

    if target_category:
        query += " WHERE category = ?"
        param.append(target_category)

    query += " ORDER BY id"

    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(query, param).fetchall()


def total_expenses() -> int:
    with sqlite3.connect(DB_PATH) as conn:
        total = conn.execute(
            "SELECT SUM(amount) FROM expenses"
        ).fetchone()
    return total[0] if total[0] is not None else 0


def delete_expense(expense_id: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )
        return cursor.rowcount > 0
