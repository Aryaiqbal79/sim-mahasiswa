# src/utils.py
"""Utilitas pembantu untuk program SIM Mahasiswa."""

from datetime import datetime


def format_timestamp() -> str:
    """Kembalikan timestamp saat ini dalam format yang mudah dibaca."""
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def validasi_angkatan(angkatan: int) -> bool:
    """
    Validasi tahun angkatan mahasiswa.
    Angkatan valid: antara 2000 dan tahun saat ini.
    """
    tahun_sekarang = datetime.now().year
    return 2000 <= angkatan <= tahun_sekarang


def format_ipk(ipk: float) -> str:
    """
    Format IPK menjadi label predikat kelulusan.

    Args:
        ipk: Nilai IPK antara 0.0 dan 4.0

    Returns:
        String predikat: Cumlaude, Sangat Memuaskan, Memuaskan, atau Cukup
    """
    if ipk >= 3.51:
        return f"{ipk:.2f} (Cumlaude)"
    elif ipk >= 3.01:
        return f"{ipk:.2f} (Sangat Memuaskan)"
    elif ipk >= 2.76:
        return f"{ipk:.2f} (Memuaskan)"
    else:
        return f"{ipk:.2f} (Cukup)"
