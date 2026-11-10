"""Expense Tracker - v 0"""

import sqlite3
import sys

DB_Path = 'expenses.db'

SCHEMA = """
CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount INTEGER NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL
);
"""

def format_rupiah(amount: int) -> str:
    return "Rp " + f"{amount:,}".replace(",", ".")

def init_db():
    with sqlite3.connect(DB_Path) as conn:
        conn.execute(SCHEMA)

def add_expense(amount: int, description: str, category: str) -> None:
    with sqlite3.connect(DB_Path) as conn:
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

    with sqlite3.connect(DB_Path) as conn:
        rows = conn.execute(query, param).fetchall()

    if not rows:
        print(f"Belum ada Pengeluaran" + (f" untuk kategori '{target_category}'" if target_category else ""))
        return

    print(f"{'ID':>3} {'Jumlah':>15} {'Kategori':>15} Keterangan")
    print("-" * 60)

    for id_, amount, desc, cat in rows: 
        print(f"{id_:>3} {format_rupiah(amount):>15} {cat:>15} {desc}")

def total_expenses() -> int:
    with sqlite3.connect(DB_Path) as conn:
        total = conn.execute(
            "SELECT SUM(amount) FROM expenses"
        ).fetchone()
    return total[0] if total[0] is not None else 0

def delete_expense(expense_id: int) -> None:
    with sqlite3.connect(DB_Path) as conn:
        cursor = conn.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )
        return cursor.rowcount > 0

def main():
    init_db()
    if len(sys.argv) < 2:
        print("Pemakaian: ")
        print(" python expense.py add <jumlah> <keterangan> [kategori]")
        print(" python expense.py list")
        print(" python expense.py total")
        print(" python expense.py delete <id>")
        return

    command = sys.argv[1]
    if command == "add":
        if len(sys.argv) < 4:
            print("Butuh: add <jumlah> <keterangan> [kategori]")
            return
        try:
            amount = int(sys.argv[2])
        except ValueError:
            print("Jumlah harus berupa angka")
            return
        description = sys.argv[3]
        category = sys.argv[4] if len(sys.argv) > 4 else "Umum"
        add_expense(amount, description, category)
        print(f"✔ Ditambahkan: {amount} — {description} ({category})")
    elif command == "list":
        if len(sys.argv) == 4 and sys.argv[2] == "--category":
            list_expenses(sys.argv[3])
        else:
            list_expenses()
    elif command == "total":
        print(f"Total Pengeluaran: {format_rupiah(total_expenses())}")
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Butuh: delete <id>")
            return
        try:
            expense_id = int(sys.argv[2])
        except ValueError:
            print("ID harus berupa angka")
            return

        if delete_expense(expense_id):
            print(f"✔ Pengeluaran dengan ID {expense_id} telah dihapus")
        else:
            print(f"❌ Tidak ada pengeluaran dengan ID {expense_id}")
    else:
        print(f"Perintah tidak dikenal: {command}")

if __name__ == "__main__":
    main()