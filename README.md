# Expense Tracker CLI 
CLI Sederhana untuk mencatat pengeluaran harian dari terminal.
Data disimpan lokal di SQLite tanpa server.

## Fitur
- `add` - Tambah pengeluaran (jumlah, keterangan, kategori opsional)
- `list` - Tampilkan semua pengeluaran
- `total` - Hitung total pengeluaran
- `delete` - Hapus pengeluaran berdasarkan ID

## Instalasi
Pastikan Python 3.10+ sudah terpasang. Clone repositori ini dan jalankan:
```bash
git clone https://github.com/rafli-alf/expense-tracker.git
cd expense-tracker
pip install -e .
```

## Contoh Penggunaan
```bash
expense add 50000 "makan siang" -c food
expense add 20000 "kopi" -c food
expense list
expense list -c food
expense total
expense delete 1
```

## Struktur
src/expense_tracker/cli.py -> Logika antarmuka terminal (argparse)
src/expense_tracker/db.py -> Logika database (SQLite)
pyproject.toml -> Konfigurasi package Python

## Teknologi 
Python 3, SQLite, Standard Library (tanpa dependency eksternal)

## Roadmap
- [x] `add`, `list`, `total`
- [x] `delete` berdasarkan ID
- [x] Filter `list` berdasarkan kategori
- [x] Pindah ke argparse
- [x] Struktur package [x] src/ dan pyproject.toml
- [ ] Unit test dengan pytest