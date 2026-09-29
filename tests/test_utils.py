# tests/test_utils.py
import pytest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import format_timestamp, validasi_angkatan, format_ipk


class TestUtils:
    """Pengujian untuk modul utils."""

    def test_format_timestamp_bukan_kosong(self):
        """Timestamp tidak boleh string kosong."""
        ts = format_timestamp()
        assert ts != ""
        assert len(ts) > 0

    def test_format_timestamp_format_benar(self):
        """Timestamp harus mengandung tanggal dan waktu."""
        ts = format_timestamp()
        # Format: DD/MM/YYYY HH:MM:SS
        assert "/" in ts
        assert ":" in ts

    def test_validasi_angkatan_valid(self):
        """Angkatan dalam range yang valid harus return True."""
        assert validasi_angkatan(2020) is True
        assert validasi_angkatan(2024) is True
        assert validasi_angkatan(2000) is True

    def test_validasi_angkatan_terlalu_lama(self):
        """Angkatan sebelum 2000 harus return False."""
        assert validasi_angkatan(1999) is False
        assert validasi_angkatan(1990) is False

    def test_validasi_angkatan_masa_depan(self):
        """Angkatan melebihi tahun sekarang harus return False."""
        tahun_depan = datetime.now().year + 1
        assert validasi_angkatan(tahun_depan) is False

    def test_format_ipk_cumlaude(self):
        """IPK >= 3.51 harus mendapat predikat Cumlaude."""
        assert "Cumlaude" in format_ipk(3.51)
        assert "Cumlaude" in format_ipk(4.0)
        assert "Cumlaude" in format_ipk(3.75)

    def test_format_ipk_sangat_memuaskan(self):
        """IPK 3.01-3.50 harus Sangat Memuaskan."""
        assert "Sangat Memuaskan" in format_ipk(3.01)
        assert "Sangat Memuaskan" in format_ipk(3.50)
        assert "Sangat Memuaskan" in format_ipk(3.25)

    def test_format_ipk_memuaskan(self):
        """IPK 2.76-3.00 harus Memuaskan."""
        assert "Memuaskan" in format_ipk(2.76)
        assert "Memuaskan" in format_ipk(3.00)

    def test_format_ipk_cukup(self):
        """IPK < 2.76 harus Cukup."""
        assert "Cukup" in format_ipk(2.75)
        assert "Cukup" in format_ipk(0.0)
        assert "Cukup" in format_ipk(2.0)

    def test_format_ipk_mengandung_angka(self):
        """Output format_ipk harus mengandung nilai IPK aslinya."""
        result = format_ipk(3.50)
        assert "3.50" in result
