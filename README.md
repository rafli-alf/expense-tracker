# Expense Tracker CLI 
CLI Sederhana untuk mencatat pengeluaran harian dari terminal.
Data disimpan lokal di SQLite tanpa server.

## Fitur
- `add` - Tambah pengeluaran (jumlah, keterangan, kategori opsional)
- `list` - Tampilkan semua pengeluaran
- `total` - Hitung total pengeluaran
- `delete` - Hapus pengeluaran berdasarkan ID

## Instalasi
```bash
git clone https://github.com/rafli-alf/expense-tracker.git
cd expense-tracker
python expense.py
```

## Contoh Penggunaan
```bash
python expense.py add 50000 "makan siang" -c food
python expense.py add 20000 "kopi" -c food
python expense.py list
python expense.py list -c food
python expense.py total
python expense.py delete 1
```

## Struktur
- expense.py -> Seluruh logika CLI + Akses SQLite
- expenses.db -> database lokal (dibuat otomatis, tidak dicommit)

## Teknologi 
Python 3, SQLite, Standard Library (tanpa dependency eksternal)

## Roadmap
    -[x] `add`, `list`, `total`
    -[x] `delete` berdasarkan ID
    -[x] Filter `list` berdasarkan kategori
    -[x] Pindah ke argparse
    -[ ] Unit test dengan pytest