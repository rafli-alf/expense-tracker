"""Expense Tracker - v 0"""

import sqlite3
import argparse

DB_PATH = 'expenses.db'

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
        rows = conn.execute(query, param).fetchall()

    if not rows:
        print(f"Belum ada Pengeluaran" + (f" untuk kategori '{target_category}'" if target_category else ""))
        return

    print(f"{'ID':>3} {'Jumlah':>15} {'Kategori':>15} Keterangan")
    print("-" * 60)

    for id_, amount, desc, cat in rows: 
        print(f"{id_:>3} {format_rupiah(amount):>15} {cat:>15} {desc}")

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

def main():
    parser = argparse.ArgumentParser(description="Aplikasi Pencatat Pengeluaran")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Perintah yang tersedia")

    # --- Setup perintah "add" ---
    parser_add = subparsers.add_parser("add", help="Tambah pengeluaran baru")
    parser_add.add_argument("amount", type=int, help="Jumlah pengeluaran (angka)")
    parser_add.add_argument("description", type=str, help="Keterangan pengeluaran")
    parser_add.add_argument("--category", "-c", type=str, default="Umum", help="Kategori pengeluaran (default:Umum)")

    # --- Setup perintah "list" ---
    parser_list = subparsers.add_parser("list", help="Daftar Pengeluaran")
    parser_list.add_argument("--category", "-c", type=str, help="Filter berdasarkan kategori (default:Umum)")

    # --- Setup perintah "total" ---
    subparsers.add_parser("total", help="Hitung Total Pengeluaran")

    # --- Setup perintah "delete" ---
    parser_delete = subparsers.add_parser("delete", help="Hapus pengeluaran berdasarkan ID")
    parser_delete.add_argument("id", type=int, help="Id pengeluaran yang akan dihapus")

    args = parser.parse_args()

    init_db()

    # --- Menjalankan fungsi berdasarkan input ---
    if args.command == "add":
        add_expense(args.amount, args.description, args.category)
        print(f"✔ Ditambahkan: {format_rupiah(args.amount)} — {args.description} ({args.category})")
        
    elif args.command == "list":
        list_expenses(args.category)
    
    elif args.command == "total":
        print(f"Total Pengeluaran: {format_rupiah(total_expenses())}")
        
    elif args.command == "delete":
        if delete_expense(args.id):
            print(f"✔ Pengeluaran dengan ID {args.id} berhasil dihapus.")
        else:
            print(f"❌ Pengeluaran dengan ID {args.id} tidak ditemukan.")


if __name__ == "__main__":
    main()