# Sistem E-Voting Pemilihan Ketua Organisasi Mahasiswa

Sistem simulasi pemilihan elektronik (e-voting) berbasis Python untuk memilih ketua
organisasi mahasiswa. Dibangun dengan arsitektur modular dan menyimpan data dalam
format JSON.

---

## Struktur Folder

```
e_voting/
├── main.py              # Entry point — jalankan file ini
├── README.md
├── data/
│   ├── pemilih.json     # Data pemilih terdaftar
│   ├── calon.json       # Data calon ketua
│   ├── log_voting.txt   # Log aktivitas (dibuat otomatis)
│   └── laporan_hasil.txt# Laporan ekspor (dibuat saat diekspor)
└── modul/
    ├── __init__.py
    ├── utils.py         # Fungsi utilitas & konstanta
    ├── pemilih.py       # Manajemen data pemilih
    ├── calon.py         # Manajemen data calon
    ├── voting.py        # Proses pemungutan suara
    └── statistik.py     # Analisis & laporan statistik
```

---

## Cara Menjalankan

```bash
# Masuk ke direktori project
cd e_voting

# Jalankan program
python main.py
```

> **Syarat:** Python 3.10 atau lebih baru (menggunakan `dict | None` type hint).

---

## Fitur Utama

| No | Fitur | Deskripsi |
|----|-------|-----------|
| 1 | Manajemen Pemilih | Tambah, hapus, dan lihat daftar pemilih |
| 2 | Manajemen Calon | Tambah, hapus, dan lihat profil calon |
| 3 | Proses Voting | Voting dengan validasi ID dan pencegahan double voting |
| 4 | Hasil Sementara | Peringkat calon secara real-time |
| 5 | Statistik Lengkap | Partisipasi, perolehan suara, analisis per jurusan |
| 6 | Ekspor Laporan | Simpan hasil ke file teks |
| 7 | Log Aktivitas | Pencatatan seluruh aktivitas voting |
| 8 | Reset Simulasi | Reset data untuk menjalankan simulasi ulang |

---

## Struktur Data

### Pemilih (`pemilih.json`)
```json
{
    "id": "PM001",
    "nama": "Ayu Rahayu",
    "jurusan": "SI",
    "sudah_memilih": false
}
```

### Calon (`calon.json`)
```json
{
    "id": "CL001",
    "nama": "Rizky Aditya",
    "jurusan": "Teknik Informatika",
    "visi": "...",
    "misi": ["...", "..."],
    "jumlah_suara": 0
}
```

---

## Validasi & Keamanan

- **ID unik**: Tidak boleh ada duplikasi ID pemilih maupun calon.
- **Format ID**: Pemilih `PM` + 3 digit (PM001); Calon `CL` + 3 digit (CL001).
- **Satu suara**: Setiap pemilih hanya dapat memilih satu kali.
- **Konfirmasi**: Setiap aksi penting memerlukan konfirmasi y/n.
- **Log audit**: Seluruh aktivitas voting dicatat dengan timestamp.
- **Proteksi hapus**: Pemilih yang sudah memilih dan calon yang sudah punya suara tidak dapat dihapus.

---

## Penggunaan Git

```bash
# Inisialisasi repository
git init
git add .
git commit -m "Initial commit: struktur proyek e-voting"

# Workflow pengembangan
git add modul/pemilih.py
git commit -m "feat: tambah validasi format ID pemilih"

git add modul/voting.py
git commit -m "feat: implementasi proses voting dengan konfirmasi"

git add modul/statistik.py
git commit -m "feat: tambah analisis statistik per jurusan"
```

---

## Materi yang Dicakup

- **Git & Version Control** — workflow commit per fitur
- **Variabel & Tipe Data** — string, int, float, bool, list, dict, tuple
- **Input/Output & Validasi** — `input()`, format ID, cek duplikasi
- **Percabangan & Perulangan** — `if/elif/else`, `for`, `while`
- **List & Dictionary** — list of dicts, operasi CRUD, sorting
- **Function & Modularisasi** — setiap modul punya tanggung jawab tunggal
- **Import** — antar modul dengan path relatif
- **Analisis Sederhana** — persentase, ranking, statistik per kelompok

---

## Kontributor

Proyek ini dibuat sebagai tugas mata kuliah Pemrograman Python.
