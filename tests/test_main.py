# tests/test_main.py
import pytest
import sys
import os

# Tambahkan root proyek ke sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Mahasiswa, DaftarMahasiswa


# ─────────────────────────────────────────────
#  TestMahasiswa — Unit Test Model Mahasiswa
# ─────────────────────────────────────────────

class TestMahasiswa:
    """Pengujian untuk kelas Mahasiswa."""

    def test_buat_mahasiswa_valid(self):
        """Mahasiswa valid harus berhasil dibuat."""
        mhs = Mahasiswa("2024SI001", "Andi Pratama",
                        "Sistem Informasi", 2024, 3.50)
        assert mhs.nim == "2024SI001"
        assert mhs.nama == "Andi Pratama"
        assert mhs.program_studi == "Sistem Informasi"
        assert mhs.angkatan == 2024
        assert mhs.ipk == 3.50

    def test_nim_tidak_valid_terlalu_pendek(self):
        """NIM kurang dari 6 karakter harus raise ValueError."""
        with pytest.raises(ValueError, match="NIM tidak valid"):
            Mahasiswa("abc", "Test", "SI", 2024, 3.0)

    def test_nim_kosong(self):
        """NIM kosong harus raise ValueError."""
        with pytest.raises(ValueError):
            Mahasiswa("", "Test", "SI", 2024, 3.0)

    def test_nama_kosong(self):
        """Nama kosong harus raise ValueError."""
        with pytest.raises(ValueError, match="Nama tidak boleh kosong"):
            Mahasiswa("2024SI001", "", "SI", 2024, 3.0)

    def test_ipk_diluar_range_atas(self):
        """IPK > 4.0 harus raise ValueError."""
        with pytest.raises(ValueError, match="IPK harus 0.0-4.0"):
            Mahasiswa("2024SI002", "Test", "SI", 2024, 5.0)

    def test_ipk_diluar_range_bawah(self):
        """IPK < 0.0 harus raise ValueError."""
        with pytest.raises(ValueError, match="IPK harus 0.0-4.0"):
            Mahasiswa("2024SI003", "Test", "SI", 2024, -0.1)

    def test_ipk_boundary_minimum(self):
        """IPK tepat 0.0 harus valid (boundary)."""
        mhs = Mahasiswa("2024SI004", "Test Min", "SI", 2024, 0.0)
        assert mhs.ipk == 0.0

    def test_ipk_boundary_maximum(self):
        """IPK tepat 4.0 harus valid (boundary)."""
        mhs = Mahasiswa("2024SI005", "Test Max", "SI", 2024, 4.0)
        assert mhs.ipk == 4.0

    def test_ipk_default_nol(self):
        """IPK default harus 0.0 jika tidak diberikan."""
        mhs = Mahasiswa("2024SI006", "Default IPK", "SI", 2024)
        assert mhs.ipk == 0.0

    def test_str_representation(self):
        """__str__ harus mengandung NIM dan nama."""
        mhs = Mahasiswa("2024SI007", "Budi", "SI", 2024, 3.25)
        result = str(mhs)
        assert "2024SI007" in result
        assert "Budi" in result
        assert "3.25" in result

    def test_nama_sangat_panjang(self):
        """Nama sangat panjang tetap harus valid (tidak ada batasan panjang)."""
        nama_panjang = "A" * 200
        mhs = Mahasiswa("2024SI008", nama_panjang, "SI", 2024, 3.0)
        assert mhs.nama == nama_panjang


# ─────────────────────────────────────────────
#  TestDaftarMahasiswa — Unit Test CRUD
# ─────────────────────────────────────────────

class TestDaftarMahasiswa:
    """Pengujian untuk kelas DaftarMahasiswa."""

    def setup_method(self):
        """Inisialisasi DaftarMahasiswa baru sebelum setiap test."""
        self.db = DaftarMahasiswa()
        self.mhs1 = Mahasiswa("2024SI001", "Andi Pratama", "SI", 2024, 3.50)
        self.mhs2 = Mahasiswa("2024SI002", "Budi Santoso", "SI", 2024, 3.20)

    # ── Tambah ──

    def test_tambah_dan_cari(self):
        """Mahasiswa yang ditambahkan harus bisa dicari."""
        self.db.tambah(self.mhs1)
        assert self.db.cari("2024SI001") == self.mhs1
        assert self.db.jumlah == 1

    def test_nim_duplikat_raise_error(self):
        """Menambahkan NIM yang sama harus raise ValueError."""
        m2_duplikat = Mahasiswa("2024SI001", "Budi", "SI", 2024)
        self.db.tambah(self.mhs1)
        with pytest.raises(ValueError, match="sudah terdaftar"):
            self.db.tambah(m2_duplikat)

    def test_tambah_beberapa_mahasiswa(self):
        """Menambah beberapa mahasiswa harus berhasil dan jumlah sesuai."""
        self.db.tambah(self.mhs1)
        self.db.tambah(self.mhs2)
        assert self.db.jumlah == 2

    # ── Cari ──

    def test_cari_nim_tidak_ada(self):
        """Mencari NIM yang tidak ada harus return None."""
        self.db.tambah(self.mhs1)
        assert self.db.cari("9999XX999") is None

    def test_cari_pada_daftar_kosong(self):
        """Mencari di daftar kosong harus return None."""
        assert self.db.cari("2024SI001") is None

    # ── Hapus ──

    def test_hapus_mahasiswa_ada(self):
        """Hapus mahasiswa yang ada harus return True dan jumlah berkurang."""
        self.db.tambah(self.mhs1)
        self.db.tambah(self.mhs2)
        result = self.db.hapus("2024SI001")
        assert result is True
        assert self.db.jumlah == 1
        assert self.db.cari("2024SI001") is None

    def test_hapus_nim_tidak_ada(self):
        """Hapus NIM yang tidak ada harus return False."""
        result = self.db.hapus("9999XX999")
        assert result is False

    def test_hapus_lalu_tambah_kembali(self):
        """Setelah dihapus, NIM yang sama boleh ditambahkan kembali."""
        self.db.tambah(self.mhs1)
        self.db.hapus("2024SI001")
        mhs_baru = Mahasiswa("2024SI001", "Andi Baru", "SI", 2025, 3.75)
        self.db.tambah(mhs_baru)
        assert self.db.jumlah == 1
        assert self.db.cari("2024SI001").nama == "Andi Baru"

    # ── Edit IPK ──

    def test_edit_ipk_valid(self):
        """Edit IPK dengan nilai valid harus berhasil."""
        self.db.tambah(self.mhs1)
        result = self.db.edit_ipk("2024SI001", 3.75)
        assert result is True
        assert self.db.cari("2024SI001").ipk == 3.75

    def test_edit_ipk_tidak_valid(self):
        """Edit IPK di luar range harus raise ValueError."""
        self.db.tambah(self.mhs1)
        with pytest.raises(ValueError, match="IPK harus 0.0-4.0"):
            self.db.edit_ipk("2024SI001", 4.5)

    def test_edit_ipk_nim_tidak_ada(self):
        """Edit IPK untuk NIM yang tidak ada harus return False."""
        result = self.db.edit_ipk("9999XX999", 3.0)
        assert result is False

    # ── Jumlah ──

    def test_jumlah_awal_nol(self):
        """Daftar baru harus punya jumlah 0."""
        assert self.db.jumlah == 0

    def test_jumlah_setelah_operasi_crud(self):
        """Jumlah harus akurat setelah serangkaian operasi CRUD."""
        self.db.tambah(self.mhs1)
        self.db.tambah(self.mhs2)
        assert self.db.jumlah == 2
        self.db.hapus("2024SI001")
        assert self.db.jumlah == 1
