# 🚗 RentGo – Sistem Rental Kendaraan Sederhana

> Simulasi sistem rental kendaraan berbasis Python dengan autentikasi, validasi input, hitungan sewa berbasis waktu nyata, dan antarmuka terminal interaktif.

---

## 🔍 Ringkasan
RentGo adalah program rental kendaraan (mobil & motor) yang mengimplementasikan **multi user dengan 2 peran: admin & customer**. Sistem ini menampilkan menu berbeda sesuai peran akun, menjamin keamanan autentikasi, dan menjaga integritas data melalui validasi input. Semua data disimpan di memori (dictionary), jadi **otomatis hilang saat program berhenti**.

---

## ✨ Fitur Utama

- **🔐 Autentikasi**:
  - Login memakai **Nama atau NIK**, dengan proteksi percobaan gagal (max 3x) yang langsung menawarkan fitur lupa password.
  - Registrasi akun baru, lupa password (verifikasi Nama + NIK), dan logout.
  - Input password tersamar (`*`) menggunakan `pwinput`.
- **✅ Validasi Input**:
  - Nama unik, umur minimal 18, NIK 16 digit & belum terdaftar, No. HP 10–13 digit diawali `08`.
  - Lama sewa, harga kendaraan, dan nominal top up harus angka bulat > 0.
- **👥 Menerapkan Multiuser**:
  - Bisa registrasi sebagai customer lewat menu utama
  - Bisa logout dan login sebagai akun lain
- **🛡️ Akses fitur berdasarkan role**:
  - **Admin**:
    - Kelola kendaraan (tambah, ubah, hapus) dengan status `Tersedia`, `Disewa`, atau `Maintenance`.
    - Lihat semua transaksi, filter berdasarkan status (Berjalan / Selesai), dan **diagram garis** perkembangan rental per hari.
    - Lihat & hapus akun customer (ditolak jika customer masih punya transaksi berjalan).
  - **Customer**:
    - Pesan kendaraan dengan **DP 50%** dari saldo, lalu lunasi sisanya saat pengembalian.
    - Pengembalian kendaraan dengan **denda otomatis** jika terlambat.
    - Lihat riwayat transaksi, top up saldo, ubah password, dan ubah data diri.
- **⏱️ Waktu Sewa**:
  - Waktu yang tampil adalah **jam asli**. Durasi sewa dihitung **1 hari = 3 menit waktu nyata**, sehingga sewa 1 hari jatuh tempo 3 menit setelah dipesan dan fitur denda mudah dicoba.
- **🔧 Status Maintenance**:
  - Kendaraan rusak/bermasalah bisa diubah admin menjadi Maintenance; kendaraan tersebut tidak muncul di daftar pesan customer.
- **🎨 Visualisasi Data**:
  - Menu interaktif (panah atas/bawah + Enter) dengan `inquirer`.
  - Tabel cantik dan bersih dengan `PrettyTable`.
  - Diagram garis dengan `matplotlib`.
- **📁 Modular**: Kode terstruktur dalam beberapa modul untuk kemudahan debugging.

---

## 📦 Akun & Password bawaan:
- **Akun dengan role Admin**
  - Username: admin1 | Password: admin1
  - Username: admin2 | Password: admin2
  - Username: admin3 | Password: admin3

- **Akun dengan role Customer**
  - Username: user1 | Password: user1
  - Username: user2 | Password: user2
  - Username: user3 | Password: user3

> Login juga bisa memakai NIK. NIK bawaan: admin `6401010101900001` s.d. `…0003`, customer `6401010101950001` s.d. `…0003`.

---

## ▶️ Cara Menjalankan
```bash
pip install -r requirements.txt
python main.py
```
Gunakan panah atas/bawah + Enter untuk memilih menu. Tekan `Ctrl+C` untuk keluar kapan saja.

---

## 🗂️ Struktur Modul

| File | Isi |
|------|-----|
| `main.py` | Menu utama (Login, Daftar Akun, Lupa Password, Keluar) |
| `autentikasi.py` | Login, registrasi, lupa password |
| `menu_admin.py` | Menu admin, transaksi rental, diagram, akun customer |
| `kendaraan.py` | Tambah, ubah, hapus kendaraan |
| `menu_user.py` | Menu customer: pesan, pengembalian, riwayat, top up |
| `kelola_akun.py` | Ubah password & ubah data diri |
| `data.py` | Dictionary data (users, kendaraan, transaksi), akun bawaan, aturan DP & denda |
| `waktu.py` | Hitungan waktu sewa (1 hari = 3 menit waktu nyata) |
| `validasi_input.py` | Fungsi validasi input |
| `tampilan.py` | Helper tampilan (menu inquirer, tabel, format Rupiah) |

---

## ⚙️ Aturan Bisnis (bisa diubah)

| Pengaturan | Lokasi | Nilai awal |
|------------|--------|-----------|
| Persentase DP | `data.py` → `DP_PERSEN` | 50 |
| Denda per hari terlambat | `data.py` → `DENDA_PERSEN_PER_HARI` | 50% dari harga sewa/hari |
| Durasi 1 hari sewa | `waktu.py` → `DETIK_PER_HARI` | 180 detik (3 menit) |
| Maks. percobaan login | `autentikasi.py` → `MAKS_PERCOBAAN` | 3 |

---

## 📚 Library yang Digunakan
`inquirer` · `pwinput` · `prettytable` · `matplotlib` · module bawaan Python (`os`, `math`, `datetime`)
