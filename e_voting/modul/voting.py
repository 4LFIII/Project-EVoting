"""
voting.py - Modul proses voting
Menangani alur dan validasi proses pemungutan suara
"""

from modul.utils import (
    cetak_header, cetak_sukses, cetak_error, cetak_info, cetak_peringatan,
    cetak_garis, input_dengan_validasi, konfirmasi, catat_log, Warna
)
from modul.pemilih import get_semua_pemilih, simpan_semua_pemilih, cari_pemilih_by_id
from modul.calon   import get_semua_calon, simpan_semua_calon, cari_calon_by_id, tampilkan_calon_ringkas


# ─────────────────────────────────────────────
# Fungsi inti voting
# ─────────────────────────────────────────────
def proses_voting() -> None:
    """
    Alur utama proses pemungutan suara:
    1. Verifikasi ID pemilih
    2. Cek status sudah_memilih
    3. Tampilkan calon
    4. Pemilih pilih calon
    5. Konfirmasi dan simpan
    """
    cetak_header("Proses Pemungutan Suara")

    # ── Langkah 1: Verifikasi ID pemilih ──
    id_pemilih = input_dengan_validasi("Masukkan ID Pemilih Anda: ").upper()
    pemilih = cari_pemilih_by_id(id_pemilih)

    if not pemilih:
        cetak_error(f"ID Pemilih '{id_pemilih}' tidak terdaftar dalam sistem.")
        catat_log("GAGAL_VOTING", f"ID tidak ditemukan: {id_pemilih}")
        return

    # ── Langkah 2: Cek apakah sudah memilih ──
    if pemilih["sudah_memilih"]:
        cetak_peringatan(f"Pemilih {pemilih['nama']} ({id_pemilih}) sudah memberikan suara.")
        cetak_info("Setiap pemilih hanya diperbolehkan memilih satu kali.")
        catat_log("GAGAL_VOTING", f"Pemilih sudah memilih: {id_pemilih} - {pemilih['nama']}")
        return

    # ── Langkah 3: Sambut pemilih ──
    print(f"\n{Warna.HIJAU}Selamat datang, {Warna.BOLD}{pemilih['nama']}{Warna.RESET}")
    print(f"{Warna.BIRU}Jurusan : {pemilih['jurusan']}{Warna.RESET}")

    # ── Langkah 4: Tampilkan daftar calon ──
    calon_list = get_semua_calon()
    if not calon_list:
        cetak_error("Belum ada calon yang terdaftar. Hubungi panitia.")
        return

    print(f"\n{Warna.BOLD}Daftar Calon Ketua:{Warna.RESET}")
    tampilkan_calon_ringkas()

    # ── Langkah 5: Pilih calon ──
    id_calon = input_dengan_validasi("\nMasukkan ID Calon yang Anda pilih: ").upper()
    calon = cari_calon_by_id(id_calon)

    if not calon:
        cetak_error(f"ID Calon '{id_calon}' tidak ditemukan.")
        catat_log("GAGAL_VOTING", f"ID calon tidak ditemukan: {id_calon} oleh {id_pemilih}")
        return

    # ── Langkah 6: Konfirmasi pilihan ──
    print(f"\n{Warna.BOLD}Konfirmasi Pilihan Anda:{Warna.RESET}")
    cetak_garis("-", 45)
    print(f"  Pemilih : {pemilih['nama']} ({id_pemilih})")
    print(f"  Pilihan : {calon['nama']} ({id_calon})")
    cetak_garis("-", 45)

    if not konfirmasi(f"\nAnda memilih {calon['nama']}. Lanjutkan?"):
        cetak_peringatan("Proses voting dibatalkan. Anda dapat mencoba kembali.")
        return

    # ── Langkah 7: Simpan suara ──
    berhasil = _simpan_suara(id_pemilih, id_calon)

    if berhasil:
        print()
        cetak_garis("*", 60)
        cetak_sukses(f"Suara Anda untuk {calon['nama']} telah tercatat!")
        cetak_info("Terima kasih telah berpartisipasi dalam pemilihan.")
        cetak_garis("*", 60)
        catat_log("SUKSES_VOTING", f"{id_pemilih} ({pemilih['nama']}) memilih {id_calon} ({calon['nama']})")
    else:
        cetak_error("Terjadi kesalahan saat menyimpan suara. Hubungi panitia.")


def _simpan_suara(id_pemilih: str, id_calon: str) -> bool:
    """
    Fungsi internal: menyimpan perubahan setelah voting.
    Mengupdate sudah_memilih pada pemilih dan jumlah_suara pada calon.
    Mengembalikan True jika berhasil.
    """
    # Update status pemilih
    pemilih_list = get_semua_pemilih()
    for p in pemilih_list:
        if p["id"].upper() == id_pemilih:
            p["sudah_memilih"] = True
            break

    # Update jumlah suara calon
    calon_list = get_semua_calon()
    for c in calon_list:
        if c["id"].upper() == id_calon:
            c["jumlah_suara"] += 1
            break

    # Simpan keduanya
    ok_pemilih = simpan_semua_pemilih(pemilih_list)
    ok_calon   = simpan_semua_calon(calon_list)

    return ok_pemilih and ok_calon


# ─────────────────────────────────────────────
# Lihat hasil sementara
# ─────────────────────────────────────────────
def tampilkan_hasil_sementara() -> None:
    """Menampilkan hasil voting sementara beserta ranking."""
    cetak_header("Hasil Sementara Pemilihan")

    calon_list = get_semua_calon()
    if not calon_list:
        cetak_info("Belum ada data calon.")
        return

    total_suara = sum(c["jumlah_suara"] for c in calon_list)

    # Urutkan berdasarkan jumlah suara (terbanyak dahulu)
    calon_terurut = sorted(calon_list, key=lambda x: x["jumlah_suara"], reverse=True)

    print(f"\n{'Rank':<6} {'ID':<8} {'Nama':<25} {'Suara':<8} {'Persentase'}")
    cetak_garis("-", 60)

    for i, c in enumerate(calon_terurut, 1):
        persen = (c["jumlah_suara"] / total_suara * 100) if total_suara > 0 else 0
        bar    = "█" * int(persen / 5)  # progress bar sederhana

        # Tandai pemimpin sementara
        tanda = f" {Warna.KUNING}★ UNGGUL{Warna.RESET}" if i == 1 and total_suara > 0 else ""
        print(f"  #{i:<4} {c['id']:<8} {c['nama']:<25} {c['jumlah_suara']:<8} {persen:>5.1f}% {bar}{tanda}")

    cetak_garis("-", 60)
    print(f"Total suara masuk: {Warna.BOLD}{total_suara}{Warna.RESET}")

    if total_suara == 0:
        cetak_info("Belum ada suara yang masuk.")


# ─────────────────────────────────────────────
# Menu voting
# ─────────────────────────────────────────────
def menu_voting() -> None:
    """Menampilkan sub-menu voting."""
    while True:
        cetak_header("Menu Voting")
        print("  1. Mulai Proses Voting")
        print("  2. Lihat Hasil Sementara")
        print("  0. Kembali ke Menu Utama")
        cetak_garis()

        pilihan = input("Pilih menu: ").strip()
        print()

        if pilihan == "1":
            proses_voting()
        elif pilihan == "2":
            tampilkan_hasil_sementara()
        elif pilihan == "0":
            break
        else:
            cetak_error("Pilihan tidak valid.")

        input("\nTekan Enter untuk melanjutkan...")
