"""
pemilih.py - Modul manajemen data pemilih
Menangani operasi CRUD untuk data pemilih
"""

from modul.utils import (
    baca_json, tulis_json,
    cetak_header, cetak_sukses, cetak_error, cetak_info, cetak_peringatan,
    cetak_garis, input_dengan_validasi, konfirmasi, validasi_format_id,
    PEMILIH_FILE, Warna
)


# ─────────────────────────────────────────────
# Fungsi baca data pemilih
# ─────────────────────────────────────────────
def get_semua_pemilih() -> list:
    """Mengambil seluruh data pemilih dari file JSON."""
    return baca_json(PEMILIH_FILE)


def simpan_semua_pemilih(data_pemilih: list) -> bool:
    """Menyimpan seluruh data pemilih ke file JSON."""
    return tulis_json(PEMILIH_FILE, data_pemilih)


def cari_pemilih_by_id(id_pemilih: str) -> dict | None:
    """Mencari pemilih berdasarkan ID. Mengembalikan dict atau None."""
    pemilih_list = get_semua_pemilih()
    for pemilih in pemilih_list:
        if pemilih["id"].upper() == id_pemilih.upper():
            return pemilih
    return None


# ─────────────────────────────────────────────
# Fungsi tampil data pemilih
# ─────────────────────────────────────────────
def tampilkan_semua_pemilih() -> None:
    """Menampilkan tabel seluruh data pemilih."""
    cetak_header("Daftar Pemilih")
    pemilih_list = get_semua_pemilih()

    if not pemilih_list:
        cetak_info("Belum ada data pemilih.")
        return

    # Header tabel
    print(f"{'No':<5} {'ID':<8} {'Nama':<20} {'Jurusan':<10} {'Status'}")
    cetak_garis("-", 60)

    for i, p in enumerate(pemilih_list, 1):
        status = (f"{Warna.HIJAU}Sudah Memilih{Warna.RESET}"
                  if p["sudah_memilih"]
                  else f"{Warna.KUNING}Belum Memilih{Warna.RESET}")
        print(f"{i:<5} {p['id']:<8} {p['nama']:<20} {p['jurusan']:<10} {status}")

    cetak_garis("-", 60)
    total       = len(pemilih_list)
    sudah_pilih = sum(1 for p in pemilih_list if p["sudah_memilih"])
    print(f"Total: {total} pemilih | Sudah memilih: {sudah_pilih} | Belum: {total - sudah_pilih}")


# ─────────────────────────────────────────────
# Fungsi tambah pemilih
# ─────────────────────────────────────────────
def tambah_pemilih() -> None:
    """Menambahkan pemilih baru ke daftar."""
    cetak_header("Tambah Pemilih Baru")
    pemilih_list = get_semua_pemilih()

    while True:
        id_baru = input_dengan_validasi("Masukkan ID Pemilih (format PM001): ").upper()
        if not validasi_format_id(id_baru, "PM"):
            cetak_error("Format ID tidak valid. Gunakan format PM diikuti 3 digit angka (contoh: PM011).")
            continue
        if cari_pemilih_by_id(id_baru):
            cetak_error(f"ID {id_baru} sudah terdaftar. Gunakan ID lain.")
            continue
        break

    nama    = input_dengan_validasi("Masukkan Nama Pemilih: ")
    jurusan = input_dengan_validasi("Masukkan Jurusan: ")

    pemilih_baru = {
        "id": id_baru,
        "nama": nama,
        "jurusan": jurusan,
        "sudah_memilih": False
    }

    print(f"\n{Warna.BOLD}Data yang akan disimpan:{Warna.RESET}")
    print(f"  ID      : {pemilih_baru['id']}")
    print(f"  Nama    : {pemilih_baru['nama']}")
    print(f"  Jurusan : {pemilih_baru['jurusan']}")

    if konfirmasi("\nSimpan data pemilih ini?"):
        pemilih_list.append(pemilih_baru)
        if simpan_semua_pemilih(pemilih_list):
            cetak_sukses(f"Pemilih {nama} ({id_baru}) berhasil ditambahkan!")
        else:
            cetak_error("Gagal menyimpan data pemilih.")
    else:
        cetak_peringatan("Penambahan pemilih dibatalkan.")


# ─────────────────────────────────────────────
# Fungsi hapus pemilih
# ─────────────────────────────────────────────
def hapus_pemilih() -> None:
    """Menghapus pemilih dari daftar (hanya yang belum memilih)."""
    cetak_header("Hapus Data Pemilih")
    id_hapus = input_dengan_validasi("Masukkan ID Pemilih yang akan dihapus: ").upper()

    pemilih = cari_pemilih_by_id(id_hapus)
    if not pemilih:
        cetak_error(f"Pemilih dengan ID {id_hapus} tidak ditemukan.")
        return

    if pemilih["sudah_memilih"]:
        cetak_error("Tidak dapat menghapus pemilih yang sudah memberikan suara.")
        return

    print(f"\nData pemilih yang akan dihapus:")
    print(f"  ID      : {pemilih['id']}")
    print(f"  Nama    : {pemilih['nama']}")
    print(f"  Jurusan : {pemilih['jurusan']}")

    if konfirmasi("\nYakin ingin menghapus?"):
        pemilih_list = get_semua_pemilih()
        pemilih_list = [p for p in pemilih_list if p["id"].upper() != id_hapus]
        if simpan_semua_pemilih(pemilih_list):
            cetak_sukses(f"Pemilih {pemilih['nama']} berhasil dihapus.")
        else:
            cetak_error("Gagal menyimpan perubahan.")
    else:
        cetak_peringatan("Penghapusan dibatalkan.")


# ─────────────────────────────────────────────
# Fungsi reset status voting
# ─────────────────────────────────────────────
def reset_status_pemilih() -> None:
    """Mereset seluruh status sudah_memilih menjadi False (untuk simulasi ulang)."""
    cetak_peringatan("Tindakan ini akan mereset seluruh status pemilihan!")
    if not konfirmasi("Lanjutkan reset?"):
        cetak_peringatan("Reset dibatalkan.")
        return

    pemilih_list = get_semua_pemilih()
    for p in pemilih_list:
        p["sudah_memilih"] = False

    if simpan_semua_pemilih(pemilih_list):
        cetak_sukses("Seluruh status pemilih berhasil direset.")
    else:
        cetak_error("Gagal mereset status pemilih.")


# ─────────────────────────────────────────────
# Menu manajemen pemilih
# ─────────────────────────────────────────────
def menu_pemilih() -> None:
    """Menampilkan sub-menu manajemen pemilih."""
    while True:
        cetak_header("Manajemen Pemilih")
        print("  1. Lihat Semua Pemilih")
        print("  2. Tambah Pemilih Baru")
        print("  3. Hapus Pemilih")
        print("  4. Reset Status Pemilihan (Simulasi Ulang)")
        print("  0. Kembali ke Menu Utama")
        cetak_garis()

        pilihan = input("Pilih menu: ").strip()
        print()

        if pilihan == "1":
            tampilkan_semua_pemilih()
        elif pilihan == "2":
            tambah_pemilih()
        elif pilihan == "3":
            hapus_pemilih()
        elif pilihan == "4":
            reset_status_pemilih()
        elif pilihan == "0":
            break
        else:
            cetak_error("Pilihan tidak valid.")

        input("\nTekan Enter untuk melanjutkan...")
