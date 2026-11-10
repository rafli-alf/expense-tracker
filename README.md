# Expense Tracker CLI 
CLI Sederhana untuk mencatat pengeluaran harian dari terminal.
Data disimpan lokal di SQLite tanpa server.

## Fitur
 - 'add' - Tambah pengeluaran (jumlah, keterangan, kategori (opsional))
 - 'list' - Tampilkan semua pengeluaran
 - 'total' - Hitung total pengeluaran

## Instalasi
    ```bash
    git clone https://github.com/rafli-alf/expense-tracker.git
    cd expense-tracker
    python expense.py

## Contoh Penggunaan
    python expense.py add 50000 "makan siang" food
    python expense.py add 20000 "kopi" food
    python expense.py list
    python expense.py total

## Struktur
    ```bash
    expense.py -> Seluruh logika CLI + Akses SQLite
    expenses.db -> database lokal (dibuat otomatis, tidak dicommit)

## Teknologi 
    Python 3, SQLite, Standart Library (tanpa dependency eksternal)

## Roadmap
    - [x] `add`, `list`, `total`
    - [x] `delete` berdasarkan ID
    - [x] Filter `list` berdasarkan kategori
    - [ ] Pindah ke argparse
    - [ ] Unit test dengan pytest