"""
calon.py - Modul manajemen data calon ketua
Menangani operasi CRUD untuk data calon
"""

from modul.utils import (
    baca_json, tulis_json,
    cetak_header, cetak_sukses, cetak_error, cetak_info, cetak_peringatan,
    cetak_garis, input_dengan_validasi, konfirmasi, validasi_format_id,
    CALON_FILE, Warna
)


# ─────────────────────────────────────────────
# Fungsi baca data calon
# ─────────────────────────────────────────────
def get_semua_calon() -> list:
    """Mengambil seluruh data calon dari file JSON."""
    return baca_json(CALON_FILE)


def simpan_semua_calon(data_calon: list) -> bool:
    """Menyimpan seluruh data calon ke file JSON."""
    return tulis_json(CALON_FILE, data_calon)


def cari_calon_by_id(id_calon: str) -> dict | None:
    """Mencari calon berdasarkan ID. Mengembalikan dict atau None."""
    calon_list = get_semua_calon()
    for calon in calon_list:
        if calon["id"].upper() == id_calon.upper():
            return calon
    return None


# ─────────────────────────────────────────────
# Fungsi tampil data calon
# ─────────────────────────────────────────────
def tampilkan_semua_calon(tampilkan_suara: bool = True) -> None:
    """Menampilkan profil seluruh calon ketua."""
    cetak_header("Daftar Calon Ketua")
    calon_list = get_semua_calon()

    if not calon_list:
        cetak_info("Belum ada data calon.")
        return

    for i, c in enumerate(calon_list, 1):
        print(f"\n{Warna.BOLD}{Warna.BIRU}  Calon #{i}{Warna.RESET}")
        cetak_garis("-", 60)
        print(f"  ID      : {c['id']}")
        print(f"  Nama    : {Warna.BOLD}{c['nama']}{Warna.RESET}")
        print(f"  Jurusan : {c['jurusan']}")
        print(f"  Visi    : {c['visi']}")
        if "misi" in c:
            print(f"  Misi    :")
            for m in c["misi"]:
                print(f"    • {m}")
        if tampilkan_suara:
            print(f"  Suara   : {Warna.HIJAU}{c['jumlah_suara']}{Warna.RESET}")

    cetak_garis()


def tampilkan_calon_ringkas() -> None:
    """Menampilkan daftar calon dalam format ringkas (untuk proses voting)."""
    calon_list = get_semua_calon()
    if not calon_list:
        return

    print(f"\n{'ID':<8} {'Nama':<25} {'Jurusan'}")
    cetak_garis("-", 55)
    for c in calon_list:
        print(f"  {c['id']:<6} {c['nama']:<25} {c['jurusan']}")
    cetak_garis("-", 55)


# ─────────────────────────────────────────────
# Fungsi tambah calon
# ─────────────────────────────────────────────
def tambah_calon() -> None:
    """Menambahkan calon ketua baru."""
    cetak_header("Tambah Calon Ketua Baru")
    calon_list = get_semua_calon()

    while True:
        id_baru = input_dengan_validasi("Masukkan ID Calon (format CL001): ").upper()
        if not validasi_format_id(id_baru, "CL"):
            cetak_error("Format ID tidak valid. Gunakan format CL diikuti 3 digit angka (contoh: CL004).")
            continue
        if cari_calon_by_id(id_baru):
            cetak_error(f"ID {id_baru} sudah terdaftar. Gunakan ID lain.")
            continue
        break

    nama    = input_dengan_validasi("Masukkan Nama Calon: ")
    jurusan = input_dengan_validasi("Masukkan Jurusan: ")
    visi    = input_dengan_validasi("Masukkan Visi: ")

    misi = []
    print("Masukkan Misi (ketik 'selesai' jika sudah):")
    while True:
        m = input(f"  Misi {len(misi)+1}: ").strip()
        if m.lower() == "selesai":
            break
        if m:
            misi.append(m)

    calon_baru = {
        "id": id_baru,
        "nama": nama,
        "jurusan": jurusan,
        "visi": visi,
        "misi": misi,
        "jumlah_suara": 0
    }

    print(f"\n{Warna.BOLD}Data yang akan disimpan:{Warna.RESET}")
    print(f"  ID      : {calon_baru['id']}")
    print(f"  Nama    : {calon_baru['nama']}")
    print(f"  Jurusan : {calon_baru['jurusan']}")
    print(f"  Visi    : {calon_baru['visi']}")

    if konfirmasi("\nSimpan data calon ini?"):
        calon_list.append(calon_baru)
        if simpan_semua_calon(calon_list):
            cetak_sukses(f"Calon {nama} ({id_baru}) berhasil ditambahkan!")
        else:
            cetak_error("Gagal menyimpan data calon.")
    else:
        cetak_peringatan("Penambahan calon dibatalkan.")


# ─────────────────────────────────────────────
# Fungsi hapus calon
# ─────────────────────────────────────────────
def hapus_calon() -> None:
    """Menghapus calon dari daftar (hanya jika belum ada suara)."""
    cetak_header("Hapus Data Calon")
    id_hapus = input_dengan_validasi("Masukkan ID Calon yang akan dihapus: ").upper()

    calon = cari_calon_by_id(id_hapus)
    if not calon:
        cetak_error(f"Calon dengan ID {id_hapus} tidak ditemukan.")
        return

    if calon["jumlah_suara"] > 0:
        cetak_error("Tidak dapat menghapus calon yang sudah memiliki suara.")
        return

    print(f"\nData calon yang akan dihapus:")
    print(f"  ID   : {calon['id']}")
    print(f"  Nama : {calon['nama']}")

    if konfirmasi("\nYakin ingin menghapus?"):
        calon_list = get_semua_calon()
        calon_list = [c for c in calon_list if c["id"].upper() != id_hapus]
        if simpan_semua_calon(calon_list):
            cetak_sukses(f"Calon {calon['nama']} berhasil dihapus.")
        else:
            cetak_error("Gagal menyimpan perubahan.")
    else:
        cetak_peringatan("Penghapusan dibatalkan.")


# ─────────────────────────────────────────────
# Fungsi reset suara calon
# ─────────────────────────────────────────────
def reset_suara_calon() -> None:
    """Mereset jumlah suara seluruh calon menjadi 0."""
    cetak_peringatan("Tindakan ini akan mereset seluruh jumlah suara calon!")
    if not konfirmasi("Lanjutkan reset?"):
        cetak_peringatan("Reset dibatalkan.")
        return

    calon_list = get_semua_calon()
    for c in calon_list:
        c["jumlah_suara"] = 0

    if simpan_semua_calon(calon_list):
        cetak_sukses("Seluruh jumlah suara calon berhasil direset.")
    else:
        cetak_error("Gagal mereset suara calon.")


# ─────────────────────────────────────────────
# Menu manajemen calon
# ─────────────────────────────────────────────
def menu_calon() -> None:
    """Menampilkan sub-menu manajemen calon."""
    while True:
        cetak_header("Manajemen Calon Ketua")
        print("  1. Lihat Profil Semua Calon")
        print("  2. Tambah Calon Baru")
        print("  3. Hapus Calon")
        print("  4. Reset Jumlah Suara (Simulasi Ulang)")
        print("  0. Kembali ke Menu Utama")
        cetak_garis()

        pilihan = input("Pilih menu: ").strip()
        print()

        if pilihan == "1":
            tampilkan_semua_calon()
        elif pilihan == "2":
            tambah_calon()
        elif pilihan == "3":
            hapus_calon()
        elif pilihan == "4":
            reset_suara_calon()
        elif pilihan == "0":
            break
        else:
            cetak_error("Pilihan tidak valid.")

        input("\nTekan Enter untuk melanjutkan...")
