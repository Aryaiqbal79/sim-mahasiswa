# src/main.py
import sys
import os

# Tambahkan parent directory ke sys.path agar import src.models bekerja
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich import box

from src.models import Mahasiswa, DaftarMahasiswa

console = Console()
db = DaftarMahasiswa()


def tampilkan_menu():
    """Tampilkan menu utama."""
    menu_text = (
        "[bold cyan]Sistem Informasi Mahasiswa[/]\n\n"
        "[bold white]1.[/] Tambah Mahasiswa\n"
        "[bold white]2.[/] Tampilkan Semua Mahasiswa\n"
        "[bold white]3.[/] Cari Mahasiswa (NIM)\n"
        "[bold white]4.[/] Hapus Mahasiswa\n"
        "[bold white]5.[/] Edit IPK Mahasiswa\n"
        "[bold white]0.[/] Keluar"
    )
    console.print(Panel(menu_text, title="[bold cyan]≡ MENU UTAMA[/]",
                        border_style="cyan", padding=(1, 4)))


def tambah_mahasiswa():
    """Form tambah mahasiswa baru."""
    console.print("\n[bold cyan]─── Tambah Mahasiswa Baru ───[/]")
    nim = Prompt.ask("  [cyan]NIM[/]")
    nama = Prompt.ask("  [cyan]Nama[/]")
    prodi = Prompt.ask("  [cyan]Program Studi[/]")

    try:
        angkatan = int(Prompt.ask("  [cyan]Angkatan[/]"))
        ipk = float(Prompt.ask("  [cyan]IPK[/]"))
        mhs = Mahasiswa(nim, nama, prodi, angkatan, ipk)
        db.tambah(mhs)
        console.print(f"\n  [bold green]✓ Berhasil:[/] {nama} berhasil ditambahkan!\n")
    except ValueError as e:
        console.print(f"\n  [bold red]✗ Gagal:[/] {e}\n")


def tampilkan_semua():
    """Tampilkan seluruh data dalam tabel."""
    console.print()
    if not db.data:
        console.print(Panel("[yellow]⚠  Belum ada data mahasiswa.[/]",
                            border_style="yellow"))
        return

    table = Table(
        title=f"[bold]Daftar Mahasiswa[/] — Total: [cyan]{db.jumlah}[/] mahasiswa",
        box=box.ROUNDED,
        border_style="cyan",
        header_style="bold cyan",
        show_lines=True
    )
    table.add_column("No", style="dim", width=4, justify="right")
    table.add_column("NIM", style="cyan bold", min_width=12)
    table.add_column("Nama", min_width=20)
    table.add_column("Program Studi", min_width=18)
    table.add_column("Angkatan", justify="center", width=10)
    table.add_column("IPK", justify="center", width=6)

    for i, m in enumerate(db.data, 1):
        # Warnai IPK berdasarkan nilai
        if m.ipk >= 3.5:
            ipk_str = f"[bold green]{m.ipk:.2f}[/]"
        elif m.ipk >= 3.0:
            ipk_str = f"[green]{m.ipk:.2f}[/]"
        elif m.ipk >= 2.5:
            ipk_str = f"[yellow]{m.ipk:.2f}[/]"
        else:
            ipk_str = f"[red]{m.ipk:.2f}[/]"

        table.add_row(str(i), m.nim, m.nama, m.program_studi,
                      str(m.angkatan), ipk_str)

    console.print(table)
    console.print()


def cari_mahasiswa():
    """Cari mahasiswa berdasarkan NIM."""
    console.print("\n[bold cyan]─── Cari Mahasiswa ───[/]")
    nim = Prompt.ask("  [cyan]Masukkan NIM[/]")
    mhs = db.cari(nim)

    if mhs:
        table = Table(box=box.ROUNDED, border_style="green",
                      header_style="bold green", title="[bold green]✓ Mahasiswa Ditemukan[/]")
        table.add_column("Field", style="bold")
        table.add_column("Nilai", style="white")
        table.add_row("NIM", mhs.nim)
        table.add_row("Nama", mhs.nama)
        table.add_row("Program Studi", mhs.program_studi)
        table.add_row("Angkatan", str(mhs.angkatan))
        table.add_row("IPK", f"{mhs.ipk:.2f}")
        console.print()
        console.print(table)
    else:
        console.print(f"\n  [bold red]✗ Mahasiswa dengan NIM '{nim}' tidak ditemukan.[/]\n")


def hapus_mahasiswa():
    """Hapus mahasiswa berdasarkan NIM."""
    console.print("\n[bold cyan]─── Hapus Mahasiswa ───[/]")
    nim = Prompt.ask("  [cyan]Masukkan NIM mahasiswa yang akan dihapus[/]")
    mhs = db.cari(nim)

    if not mhs:
        console.print(f"\n  [bold red]✗ Mahasiswa dengan NIM '{nim}' tidak ditemukan.[/]\n")
        return

    console.print(f"\n  Data yang akan dihapus: [bold]{mhs.nama}[/] ({mhs.nim})")
    konfirmasi = Prompt.ask("  [yellow]Yakin ingin menghapus? (y/N)[/]").lower()

    if konfirmasi == "y":
        db.hapus(nim)
        console.print(f"\n  [bold green]✓ Berhasil:[/] Data {mhs.nama} telah dihapus.\n")
    else:
        console.print("\n  [dim]Penghapusan dibatalkan.[/]\n")


def edit_ipk():
    """Edit IPK mahasiswa berdasarkan NIM."""
    console.print("\n[bold cyan]─── Edit IPK Mahasiswa ───[/]")
    nim = Prompt.ask("  [cyan]Masukkan NIM[/]")
    mhs = db.cari(nim)

    if not mhs:
        console.print(f"\n  [bold red]✗ Mahasiswa dengan NIM '{nim}' tidak ditemukan.[/]\n")
        return

    console.print(f"\n  Mahasiswa: [bold]{mhs.nama}[/] — IPK saat ini: [cyan]{mhs.ipk:.2f}[/]")

    try:
        ipk_baru = float(Prompt.ask("  [cyan]IPK baru (0.0 - 4.0)[/]"))
        if db.edit_ipk(nim, ipk_baru):
            console.print(f"\n  [bold green]✓ Berhasil:[/] IPK {mhs.nama} diperbarui menjadi {ipk_baru:.2f}\n")
    except ValueError as e:
        console.print(f"\n  [bold red]✗ Gagal:[/] {e}\n")


def main():
    """Loop utama aplikasi."""
    console.print(Panel(
        "[bold cyan]Selamat datang di Sistem Informasi Mahasiswa[/]\n"
        "[dim]Program Studi Sistem Informasi — Praktikum Python[/]",
        border_style="cyan",
        padding=(1, 4)
    ))

    while True:
        tampilkan_menu()
        pilihan = Prompt.ask("\n  [bold]Pilih menu[/]", choices=["0", "1", "2", "3", "4", "5"])

        if pilihan == "1":
            tambah_mahasiswa()
        elif pilihan == "2":
            tampilkan_semua()
        elif pilihan == "3":
            cari_mahasiswa()
        elif pilihan == "4":
            hapus_mahasiswa()
        elif pilihan == "5":
            edit_ipk()
        elif pilihan == "0":
            console.print("\n[bold cyan]Sampai jumpa! Terima kasih.[/]\n")
            break


if __name__ == "__main__":
    main()
