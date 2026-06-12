"""
utils.py - Modul utilitas untuk sistem e-voting
Berisi fungsi-fungsi pembantu umum
"""

import json
import os
from datetime import datetime


# ─────────────────────────────────────────────
# Konstanta path
# ─────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR    = os.path.join(BASE_DIR, "data")
PEMILIH_FILE = os.path.join(DATA_DIR, "pemilih.json")
CALON_FILE   = os.path.join(DATA_DIR, "calon.json")
LOG_FILE     = os.path.join(DATA_DIR, "log_voting.txt")


# ─────────────────────────────────────────────
# Warna terminal (ANSI)
# ─────────────────────────────────────────────
class Warna:
    HEADER  = "\033[95m"
    BIRU    = "\033[94m"
    HIJAU   = "\033[92m"
    KUNING  = "\033[93m"
    MERAH   = "\033[91m"
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    GARIS   = "\033[4m"


# ─────────────────────────────────────────────
# Fungsi baca / tulis JSON
# ─────────────────────────────────────────────
def baca_json(filepath: str) -> list:
    """Membaca file JSON dan mengembalikan list."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Warna.MERAH}[ERROR] File tidak ditemukan: {filepath}{Warna.RESET}")
        return []
    except json.JSONDecodeError:
        print(f"{Warna.MERAH}[ERROR] Format JSON tidak valid: {filepath}{Warna.RESET}")
        return []


def tulis_json(filepath: str, data: list) -> bool:
    """Menulis data ke file JSON."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"{Warna.MERAH}[ERROR] Gagal menulis file: {e}{Warna.RESET}")
        return False


# ─────────────────────────────────────────────
# Fungsi tampilan
# ─────────────────────────────────────────────
def cetak_garis(karakter: str = "=", panjang: int = 60) -> None:
    """Mencetak garis pemisah."""
    print(karakter * panjang)


def cetak_header(judul: str) -> None:
    """Mencetak header dengan format yang rapi."""
    cetak_garis()
    print(f"{Warna.BOLD}{Warna.HEADER}{'':^5}{judul.upper():^50}{Warna.RESET}")
    cetak_garis()


def cetak_sukses(pesan: str) -> None:
    print(f"{Warna.HIJAU}[✓] {pesan}{Warna.RESET}")


def cetak_error(pesan: str) -> None:
    print(f"{Warna.MERAH}[✗] {pesan}{Warna.RESET}")


def cetak_info(pesan: str) -> None:
    print(f"{Warna.BIRU}[i] {pesan}{Warna.RESET}")


def cetak_peringatan(pesan: str) -> None:
    print(f"{Warna.KUNING}[!] {pesan}{Warna.RESET}")


# ─────────────────────────────────────────────
# Fungsi log
# ─────────────────────────────────────────────
def catat_log(aksi: str, detail: str) -> None:
    """Mencatat aktivitas voting ke file log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    baris_log = f"[{timestamp}] {aksi}: {detail}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(baris_log)
    except IOError:
        pass  # Log gagal tidak menghentikan program


# ─────────────────────────────────────────────
# Fungsi validasi
# ─────────────────────────────────────────────
def validasi_format_id(id_str: str, prefix: str) -> bool:
    """
    Memvalidasi format ID (misal PM001 atau CL001).
    prefix: 'PM' untuk pemilih, 'CL' untuk calon.
    """
    if not id_str.startswith(prefix):
        return False
    nomor = id_str[len(prefix):]
    return nomor.isdigit() and len(nomor) == 3


def input_dengan_validasi(prompt: str, boleh_kosong: bool = False) -> str:
    """Meminta input dari pengguna dengan validasi tidak kosong."""
    while True:
        nilai = input(prompt).strip()
        if nilai or boleh_kosong:
            return nilai
        cetak_error("Input tidak boleh kosong. Silakan coba lagi.")


def konfirmasi(pertanyaan: str) -> bool:
    """Meminta konfirmasi ya/tidak dari pengguna."""
    while True:
        jawaban = input(f"{pertanyaan} (y/n): ").strip().lower()
        if jawaban in ("y", "yes", "ya"):
            return True
        if jawaban in ("n", "no", "tidak"):
            return False
        cetak_error("Masukkan 'y' untuk Ya atau 'n' untuk Tidak.")


def timestamp_sekarang() -> str:
    """Mengembalikan timestamp saat ini dalam format yang mudah dibaca."""
    return datetime.now().strftime("%d %B %Y, %H:%M:%S")
