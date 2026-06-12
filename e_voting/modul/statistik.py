"""
statistik.py - Modul analisis statistik pemilu
Menyediakan laporan lengkap dan analisis data pemilihan
"""

from modul.utils import (
    cetak_header, cetak_info, cetak_garis, cetak_sukses,
    cetak_error, Warna, timestamp_sekarang, LOG_FILE
)
from modul.pemilih import get_semua_pemilih
from modul.calon   import get_semua_calon


# ─────────────────────────────────────────────
# Fungsi kalkulasi statistik
# ─────────────────────────────────────────────
def hitung_statistik() -> dict:
    """
    Menghitung seluruh statistik pemilu.
    Mengembalikan dict berisi semua metrik.
    """
    pemilih_list = get_semua_pemilih()
    calon_list   = get_semua_calon()

    total_pemilih    = len(pemilih_list)
    sudah_memilih    = sum(1 for p in pemilih_list if p["sudah_memilih"])
    belum_memilih    = total_pemilih - sudah_memilih
    partisipasi_pct  = (sudah_memilih / total_pemilih * 100) if total_pemilih > 0 else 0

    total_suara = sum(c["jumlah_suara"] for c in calon_list)

    # Temukan calon dengan suara terbanyak
    calon_terbanyak = None
    if calon_list:
        calon_terbanyak = max(calon_list, key=lambda x: x["jumlah_suara"])

    # Statistik per jurusan
    jurusan_stats: dict[str, dict] = {}
    for p in pemilih_list:
        j = p["jurusan"]
        if j not in jurusan_stats:
            jurusan_stats[j] = {"total": 0, "sudah": 0}
        jurusan_stats[j]["total"] += 1
        if p["sudah_memilih"]:
            jurusan_stats[j]["sudah"] += 1

    return {
        "total_pemilih":    total_pemilih,
        "sudah_memilih":    sudah_memilih,
        "belum_memilih":    belum_memilih,
        "partisipasi_pct":  partisipasi_pct,
        "total_suara":      total_suara,
        "calon_terbanyak":  calon_terbanyak,
        "calon_list":       calon_list,
        "jurusan_stats":    jurusan_stats,
    }


# ─────────────────────────────────────────────
# Tampilkan statistik lengkap
# ─────────────────────────────────────────────
def tampilkan_statistik() -> None:
    """Menampilkan laporan statistik pemilu secara lengkap."""
    cetak_header("Statistik & Analisis Pemilu")
    stats = hitung_statistik()

    # ── Bagian 1: Partisipasi ──
    print(f"\n{Warna.BOLD}{'─'*5} PARTISIPASI PEMILIH {'─'*34}{Warna.RESET}")
    print(f"  Total Pemilih Terdaftar : {stats['total_pemilih']}")
    print(f"  Sudah Memilih           : {Warna.HIJAU}{stats['sudah_memilih']}{Warna.RESET}")
    print(f"  Belum Memilih           : {Warna.KUNING}{stats['belum_memilih']}{Warna.RESET}")
    print(f"  Persentase Partisipasi  : ", end="")

    pct = stats["partisipasi_pct"]
    if pct >= 75:
        warna_pct = Warna.HIJAU
    elif pct >= 50:
        warna_pct = Warna.KUNING
    else:
        warna_pct = Warna.MERAH
    print(f"{warna_pct}{Warna.BOLD}{pct:.1f}%{Warna.RESET}")

    # Progress bar partisipasi
    bar_len   = 40
    bar_isi   = int(pct / 100 * bar_len)
    bar_kosong = bar_len - bar_isi
    print(f"  [{Warna.HIJAU}{'█' * bar_isi}{Warna.RESET}{'░' * bar_kosong}] {pct:.1f}%")

    # ── Bagian 2: Hasil voting ──
    print(f"\n{Warna.BOLD}{'─'*5} HASIL PEROLEHAN SUARA {'─'*32}{Warna.RESET}")
    calon_list    = stats["calon_list"]
    total_suara   = stats["total_suara"]

    if not calon_list or total_suara == 0:
        cetak_info("Belum ada suara yang masuk.")
    else:
        calon_terurut = sorted(calon_list, key=lambda x: x["jumlah_suara"], reverse=True)
        for i, c in enumerate(calon_terurut, 1):
            persen = (c["jumlah_suara"] / total_suara * 100) if total_suara > 0 else 0
            bar_c  = int(persen / 100 * 30)
            print(f"\n  #{i} {Warna.BOLD}{c['nama']}{Warna.RESET} ({c['id']})")
            print(f"     Suara : {c['jumlah_suara']} ({persen:.1f}%)")
            print(f"     [{Warna.BIRU}{'█' * bar_c}{Warna.RESET}{'░' * (30 - bar_c)}]")

    # ── Bagian 3: Calon terdepan ──
    print(f"\n{Warna.BOLD}{'─'*5} CALON TERDEPAN {'─'*39}{Warna.RESET}")
    calon_unggulan = stats["calon_terbanyak"]
    if calon_unggulan and total_suara > 0:
        persen_unggulan = calon_unggulan["jumlah_suara"] / total_suara * 100
        print(f"  {Warna.KUNING}★  {calon_unggulan['nama']} ({calon_unggulan['id']}){Warna.RESET}")
        print(f"     {calon_unggulan['jumlah_suara']} suara ({persen_unggulan:.1f}%)")
    else:
        cetak_info("Belum ada suara masuk, belum ada calon terdepan.")

    # ── Bagian 4: Statistik per jurusan ──
    print(f"\n{Warna.BOLD}{'─'*5} PARTISIPASI PER JURUSAN {'─'*30}{Warna.RESET}")
    jurusan_stats = stats["jurusan_stats"]
    if jurusan_stats:
        print(f"  {'Jurusan':<15} {'Total':<8} {'Sudah':<8} {'Partisipasi'}")
        cetak_garis("-", 50)
        for jurusan, data in sorted(jurusan_stats.items()):
            pct_j = (data["sudah"] / data["total"] * 100) if data["total"] > 0 else 0
            print(f"  {jurusan:<15} {data['total']:<8} {data['sudah']:<8} {pct_j:.1f}%")
    else:
        cetak_info("Tidak ada data per jurusan.")

    print(f"\n  {Warna.BIRU}Laporan dibuat pada: {timestamp_sekarang()}{Warna.RESET}")
    cetak_garis()


# ─────────────────────────────────────────────
# Ekspor laporan ke file teks
# ─────────────────────────────────────────────
def ekspor_laporan() -> None:
    """Mengekspor laporan statistik ke file .txt."""
    import os
    from modul.utils import BASE_DIR

    stats      = hitung_statistik()
    output_path = os.path.join(BASE_DIR, "data", "laporan_hasil.txt")
    calon_list  = stats["calon_list"]
    total_suara = stats["total_suara"]

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("         LAPORAN HASIL PEMILIHAN KETUA\n")
            f.write("         ORGANISASI MAHASISWA\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Tanggal  : {timestamp_sekarang()}\n\n")

            f.write("PARTISIPASI PEMILIH\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total Pemilih  : {stats['total_pemilih']}\n")
            f.write(f"Sudah Memilih  : {stats['sudah_memilih']}\n")
            f.write(f"Belum Memilih  : {stats['belum_memilih']}\n")
            f.write(f"Partisipasi    : {stats['partisipasi_pct']:.1f}%\n\n")

            f.write("PEROLEHAN SUARA\n")
            f.write("-" * 40 + "\n")
            if calon_list:
                calon_terurut = sorted(calon_list, key=lambda x: x["jumlah_suara"], reverse=True)
                for i, c in enumerate(calon_terurut, 1):
                    persen = (c["jumlah_suara"] / total_suara * 100) if total_suara > 0 else 0
                    f.write(f"#{i} {c['nama']} ({c['id']}): {c['jumlah_suara']} suara ({persen:.1f}%)\n")
            f.write("\n")

            if stats["calon_terbanyak"] and total_suara > 0:
                f.write("CALON TERDEPAN\n")
                f.write("-" * 40 + "\n")
                c = stats["calon_terbanyak"]
                pct_c = c["jumlah_suara"] / total_suara * 100
                f.write(f"★ {c['nama']} dengan {c['jumlah_suara']} suara ({pct_c:.1f}%)\n")

        cetak_sukses(f"Laporan berhasil disimpan ke: {output_path}")
    except IOError as e:
        cetak_error(f"Gagal mengekspor laporan: {e}")


# ─────────────────────────────────────────────
# Lihat log aktivitas
# ─────────────────────────────────────────────
def lihat_log() -> None:
    """Menampilkan log aktivitas voting."""
    cetak_header("Log Aktivitas Voting")
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            baris = f.readlines()
        if not baris:
            cetak_info("Log masih kosong.")
            return
        for b in baris[-30:]:   # tampilkan 30 entri terakhir
            print(f"  {b}", end="")
        if len(baris) > 30:
            cetak_info(f"... menampilkan 30 dari {len(baris)} entri terakhir.")
    except FileNotFoundError:
        cetak_info("File log belum dibuat. Belum ada aktivitas voting.")


# ─────────────────────────────────────────────
# Menu statistik
# ─────────────────────────────────────────────
def menu_statistik() -> None:
    """Menampilkan sub-menu statistik."""
    while True:
        cetak_header("Statistik Pemilu")
        print("  1. Tampilkan Statistik Lengkap")
        print("  2. Ekspor Laporan ke File")
        print("  3. Lihat Log Aktivitas")
        print("  0. Kembali ke Menu Utama")
        cetak_garis()

        pilihan = input("Pilih menu: ").strip()
        print()

        if pilihan == "1":
            tampilkan_statistik()
        elif pilihan == "2":
            ekspor_laporan()
        elif pilihan == "3":
            lihat_log()
        elif pilihan == "0":
            break
        else:
            cetak_error("Pilihan tidak valid.")

        input("\nTekan Enter untuk melanjutkan...")
