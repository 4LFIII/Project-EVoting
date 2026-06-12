"""
main.py - Entry point sistem e-voting pemilihan ketua organisasi mahasiswa
Jalankan file ini untuk memulai program: python main.py
"""

import os
import sys

# Pastikan direktori project masuk ke path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modul.utils      import cetak_header, cetak_garis, cetak_error, cetak_info, Warna, timestamp_sekarang
from modul.pemilih    import menu_pemilih
from modul.calon      import menu_calon
from modul.voting     import menu_voting, tampilkan_hasil_sementara
from modul.statistik  import menu_statistik, tampilkan_statistik


# ─────────────────────────────────────────────
# Banner aplikasi
# ─────────────────────────────────────────────
def tampilkan_banner() -> None:
    """Menampilkan banner selamat datang."""
    os.system("cls" if os.name == "nt" else "clear")
    print(f"\n{Warna.BOLD}{Warna.HEADER}")
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║          SISTEM E-VOTING ORGANISASI MAHASISWA        ║")
    print("  ║              Pemilihan Ketua Organisasi              ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print(f"{Warna.RESET}")
    print(f"  {Warna.BIRU}Selamat datang di sistem pemilihan elektronik{Warna.RESET}")
    print(f"  {Warna.BIRU}Waktu: {timestamp_sekarang()}{Warna.RESET}\n")


# ─────────────────────────────────────────────
# Menu utama
# ─────────────────────────────────────────────
def menu_utama() -> None:
    """Menampilkan dan menangani menu utama."""
    while True:
        tampilkan_banner()
        cetak_header("Menu Utama")
        print(f"  {Warna.BOLD}1.{Warna.RESET} Manajemen Pemilih")
        print(f"  {Warna.BOLD}2.{Warna.RESET} Manajemen Calon Ketua")
        print(f"  {Warna.BOLD}3.{Warna.RESET} Proses Voting")
        print(f"  {Warna.BOLD}4.{Warna.RESET} Hasil Sementara")
        print(f"  {Warna.BOLD}5.{Warna.RESET} Statistik & Analisis")
        print(f"  {Warna.MERAH}{Warna.BOLD}0.{Warna.RESET} Keluar")
        cetak_garis()

        pilihan = input("Pilih menu [0-5]: ").strip()
        print()

        if pilihan == "1":
            menu_pemilih()
        elif pilihan == "2":
            menu_calon()
        elif pilihan == "3":
            menu_voting()
        elif pilihan == "4":
            tampilkan_hasil_sementara()
            input("\nTekan Enter untuk kembali...")
        elif pilihan == "5":
            menu_statistik()
        elif pilihan == "0":
            print(f"\n{Warna.HIJAU}Terima kasih telah menggunakan sistem e-voting.")
            print(f"Sampai jumpa!{Warna.RESET}\n")
            sys.exit(0)
        else:
            cetak_error("Pilihan tidak valid. Masukkan angka 0-5.")
            input("\nTekan Enter untuk melanjutkan...")


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    try:
        menu_utama()
    except KeyboardInterrupt:
        print(f"\n\n{Warna.KUNING}Program dihentikan oleh pengguna.{Warna.RESET}\n")
        sys.exit(0)
