import argparse
import csv
from pathlib import Path
from rich.console import Console
from rich.table import Table
from . import db

console = Console()

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

    # --- Setup perintah "export" ---
    parser_export = subparsers.add_parser("export", help="Ekspor data ke file CSV")
    parser_export.add_argument("filename", type=str, help="Nama file (contoh: data.csv)")

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

        # Tampilan Tabel Rich 
        table = Table(title="Daftar Pengeluaran", title_style="bold magenta")
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Jumlah", justify="right", style="green")
        table.add_column("Kategori", style="yellow")
        table.add_column("Keterangan", style="white")

        for id_, amount, desc, cat in rows:
            table.add_row(str(id_), format_rupiah(amount), cat, desc)

        console.print(table)

    elif args.command == "total":
        console.print(f"[bold cyan]Total Pengeluaran:[/bold cyan] [bold green]{format_rupiah(db.total_expenses())}[/bold green]")

    elif args.command == "delete":
        if db.delete_expense(args.id):
            console.print(f"[green]✔ Pengeluaran dengan ID {args.id} berhasil dihapus.[/green]")
        else:
            console.print(f"[red]❌ Pengeluaran dengan ID {args.id} tidak ditemukan.[/red]")

    # --- Logika Export CSV ---
    elif args.command == "export":
        rows = db.list_expenses()
        if not rows:
            console.print("[yellow]Tidak ada data untuk diekspor.[/yellow]")
            return
        
        file_path = Path(args.filename)
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Tulis header
            writer.writerow(["ID", "Jumlah", "Keterangan", "Kategori"])
            # Tulis data
            writer.writerows(rows)
            
        console.print(f"[green]✔ Berhasil mengekspor {len(rows)} data ke {file_path.absolute()}[/green]")


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
    