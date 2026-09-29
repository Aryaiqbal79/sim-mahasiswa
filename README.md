# Sistem Informasi Mahasiswa (SIM)

Aplikasi console-based untuk mengelola data mahasiswa
pada Program Studi Sistem Informasi.

## Identitas

| Field  | Isian                     |
|--------|---------------------------|
| Nama   | Arya Adi Muhammad Iqbal   |
| NIM    | 20241320018               |
| Kelas  | A1 - Sistem Informasi     |

---

## Fitur

- ✅ **Tambah** data mahasiswa (NIM, nama, prodi, angkatan, IPK)
- ✅ **Tampilkan** seluruh data dalam tabel terformat
- ✅ **Cari** mahasiswa berdasarkan NIM
- ✅ **Hapus** data mahasiswa (dengan konfirmasi)
- ✅ **Edit IPK** mahasiswa berdasarkan NIM
- ✅ **Validasi** input data secara otomatis

---

## Prasyarat

- Python **3.10+**
- pip

---

## Instalasi

```bash
git clone https://github.com/USERNAME/sim-mahasiswa.git
cd sim-mahasiswa

# Buat dan aktifkan virtual environment
python -m venv venv

# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

# Instal dependensi
pip install -r requirements.txt
```

---

## Penggunaan

```bash
# Jalankan dari root direktori proyek
python -m src.main
```

---

## Pengujian

```bash
pytest tests/ -v
```

---

## Struktur Proyek

```
sim-mahasiswa/
├── src/
│   ├── __init__.py       # Package init
│   ├── main.py           # Program utama & menu interaktif
│   └── models.py         # Model data Mahasiswa & DaftarMahasiswa
├── tests/
│   ├── __init__.py
│   └── test_main.py      # Unit test (20+ test cases)
├── docs/                 # Dokumentasi & screenshot
├── requirements.txt      # Daftar dependensi
├── .gitignore            # Daftar file yang diabaikan Git
└── README.md             # Dokumentasi proyek ini
```

---

## Dependensi Utama

| Paket     | Kegunaan                              |
|-----------|---------------------------------------|
| `rich`    | Output console terformat & berwarna   |
| `requests`| HTTP library (untuk API nanti)        |
| `pytest`  | Framework pengujian                   |
| `black`   | Code formatter otomatis               |
| `ruff`    | Linter Python yang cepat              |

---

## Setup Checklist

- [x] Python 3.10+ terinstal (versi: `python --version`)
- [x] pip terinstal dan berfungsi
- [x] Virtual environment dibuat & diaktivasi
- [x] Paket dependensi terinstal via `requirements.txt`
- [x] Program berjalan tanpa error (`python -m src.main`)
- [x] Semua unit test lulus (`pytest tests/ -v`)
- [x] Repositori Git diinisiasi (`git init`)
- [x] Minimal 3 commit bermakna dibuat
- [x] Push ke GitHub berhasil
- [x] README.md lengkap dengan identitas & checklist

---

## Riwayat Commit (Conventional Commits)

```
feat: inisiasi proyek SIM Mahasiswa
feat: tambah model data Mahasiswa dengan validasi
feat: implementasi menu CRUD lengkap di main.py
test: tambah unit test komprehensif untuk models
docs: lengkapi README.md dengan identitas dan checklist
```

---

*Praktikum 1 — Setup Tools & Environment | Mata Kuliah Pemrograman Python*
