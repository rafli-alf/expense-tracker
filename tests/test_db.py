from pathlib import Path
import pytest
from expense_tracker import db

# Fixture: Menyiapkan environment sementara
@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    # Buat Path Sementara
    test_db_path = tmp_path / "test_expenses.db"

    # Timpa environment variabel EXPENSE_DB agar db.py menggunakan file sementara ini
    monkeypatch.setenv("EXPENSE_DB", str(test_db_path))

    # Paksa db.py untuk membaca ulang path baru
    monkeypatch.setattr(db, "DB_PATH", Path(test_db_path))

    # Buat Tabel
    db.init_db()

    return test_db_path

def test_add_dan_total(temp_db):
    # Awalnya harus kosong
    assert db.total_expenses() == 0

    # Tambah data
    db.add_expense(10000, "gorengan", "makanan")
    db.add_expense(25000, "kopi fm", "minuman")

    # Cek Total
    assert db.total_expenses() == 35000

def test_filter_kategori(temp_db):
    db.add_expense(10000, "gorengan", "makanan")
    db.add_expense(25000, "kopi fm", "minuman")

    # Ambil data khusus "minuman"
    hasil = db.list_expenses("minuman")

    # Pastikan hanya ada 1 data, dan keterangannya "kopi fm"
    assert len(hasil) == 1
    assert hasil[0][2] == "kopi fm" # Hasil berupa tuple: (id, amount, category)

def test_delete(temp_db):
    db.add_expense(5000, "parkir", "transport")

    # Hapus ID 1 (harus return True)
    assert db.delete_expense(1) is True

    # Hapus ID 99 yang tidak ada (harus return False)
    assert db.delete_expense(99) is False

    # Pastikan database sekarang kosong
    assert db.total_expenses() == 0