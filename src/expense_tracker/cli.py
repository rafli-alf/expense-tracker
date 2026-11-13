import argparse
from . import db

def format_rupiah(amount: int) -> str:
    return "Rp " + f"{amount:,}".replace(",", ".")

def main() -> None:
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

    db.init_db()

    if args.command == "add":
        db.add_expense(args.amount, args.description, args.category)
        print(f"✔ Ditambahkan: {format_rupiah(args.amount)} — {args.description} ({args.category})")

    elif args.command == "list":
        rows = db.list_expenses(args.category)

        if not rows :
            print(f"Belum ada pengeluaran" + (f" Untuk kategori '{args.category}'" if args.category else ""))
            return

        print(f"{'ID':>3} {'Jumlah':>15} {'Kategori':>15} Keterangan")
        print("-" * 60)
        for id_, amount, desc, cat in rows: 
            print(f"{id_:>3} {format_rupiah(amount):>15} {cat:>15} {desc}")

    elif args.command == "total":
        print(f"Total Pengeluaran: {format_rupiah(db.total_expenses())}")

    elif args.command == "delete":
        if db.delete_expense(args.id):
            print(f"✔ Pengeluaran dengan ID {args.id} berhasil dihapus.")
        else:
            print(f"❌ Pengeluaran dengan ID {args.id} tidak ditemukan.")
    