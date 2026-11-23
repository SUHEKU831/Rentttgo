# 🚗 RentGo – Sistem Rental Kendaraan

RentGo adalah aplikasi simulasi rental kendaraan berbasis Python yang dijalankan melalui terminal. Aplikasi menyediakan dua peran pengguna, yaitu **admin** dan **customer**, dengan fitur pengelolaan kendaraan, pemesanan, pengembalian, transaksi, serta pengelolaan akun.

Seluruh data disimpan di dalam struktur `dictionary` dan `list` pada memori program. **Perubahan data selama program berjalan tidak disimpan secara permanen** dan akan kembali ke data awal ketika program dijalankan ulang.

## ✨ Fitur

### 🔐 Autentikasi dan akun
- Login menggunakan nama akun atau NIK.
- Maksimal 3 kali percobaan login. Setelah gagal 3 kali, pengguna ditawari menu lupa password.
- Registrasi akun customer.
- Lupa password dengan verifikasi nama dan NIK.
- Logout dengan memilih menu keluar dari menu admin/customer.
- Password dimasukkan dengan karakter yang disamarkan (`*`) menggunakan `pwinput`.

### ✅ Validasi input
- Nama tidak boleh kosong, tidak boleh hanya angka, dan harus unik.
- Umur harus berupa angka dan minimal 18 tahun.
- NIK harus terdiri dari 16 digit dan belum digunakan.
- Nomor HP harus terdiri dari 10–13 digit dan diawali `08`.
- Alamat dan password tidak boleh kosong.
- Tipe kendaraan hanya boleh berisi huruf dan spasi.
- Harga rental, lama sewa, dan nominal top up harus berupa bilangan bulat positif.
- Nominal top up dibatasi maksimal Rp5.000.000 setiap transaksi.

### 👤 Fitur Admin
- Melihat dan mengelola daftar kendaraan.
- Menambah kendaraan dengan menentukan tipe, merek, harga per hari, dan status.
- Mengubah data kendaraan.
- Menghapus kendaraan selama kendaraan tidak memiliki transaksi yang masih berjalan.
- Melihat seluruh transaksi rental.
- Memfilter transaksi berdasarkan status **Berjalan** atau **Selesai**.
- Melihat diagram garis perkembangan jumlah rental per hari.
- Melihat daftar akun customer dan menghapus akun customer yang tidak memiliki transaksi berjalan.

### 🧑‍💼 Fitur Customer
- Melihat dan memesan kendaraan dengan status **Tersedia**.
- Membayar DP sebesar 50% dari total biaya sewa.
- Melakukan pengembalian kendaraan dan membayar sisa pelunasan.
- Mendapatkan perhitungan denda otomatis jika terlambat.
- Melihat riwayat transaksi.
- Melakukan top up saldo.
- Melihat dan mengubah data akun.
- Mengubah password dengan verifikasi password lama dan konfirmasi password baru.

## ⏱️ Perhitungan Waktu Sewa dan Denda

Program menggunakan waktu aktual perangkat saat pemesanan dan pengembalian.

| Pengaturan | Nilai |
|---|---:|
| Durasi simulasi 1 hari sewa | 180 detik (3 menit) |
| DP | 50% dari total biaya |
| Pelunasan | Sisa 50% dari total biaya |
| Denda keterlambatan | 50% dari harga rental per hari untuk setiap hari keterlambatan |

Pengaturan DP dan denda dapat diubah pada `data.py`. Durasi satu hari simulasi dapat diubah melalui `DETIK_PER_HARI` pada `waktu.py`.

## 🔑 Akun Bawaan

Akun berikut tersedia pada data awal program. Password bersifat **case-sensitive**.

| Role | Nama / Username | Password | NIK |
|---|---|---|---|
| Admin | `admin1` | `admin123` | `6401010101900001` |
| Admin | `admin2` | `admin123` | `6401010101900002` |
| Customer | `Belva` | `Belva123` | `6401010101900005` |
| Customer | `Hendra` | `Hendra123` | `6401010101900011` |
| Customer | `Kahfi` | `Kahfi123` | `6401010101900013` |
| Customer | `Ferdi` | `Ferdi123` | `6401010101900018` |

Data awal juga sudah berisi beberapa kendaraan dan transaksi contoh, termasuk transaksi yang berstatus **Berjalan** dan **Selesai**. Karena itu, daftar kendaraan, saldo, dan riwayat transaksi yang tampil saat pertama dijalankan mengikuti data pada `data.py`.

## 🗂️ Struktur File

| File | Keterangan |
|---|---|
| `main.py` | Titik masuk aplikasi dan menu utama: login, daftar akun, lupa password, dan keluar. |
| `autentikasi.py` | Proses login, registrasi, dan lupa password. |
| `menu_admin.py` | Menu admin, daftar transaksi, filter status, diagram transaksi, dan pengelolaan akun customer. |
| `kendaraan.py` | Fitur tambah, ubah, hapus, dan pengelolaan status kendaraan. |
| `menu_user.py` | Menu customer: pemesanan, pengembalian, riwayat transaksi, dan top up saldo. |
| `kelola_akun.py` | Fitur ubah password dan ubah data diri customer. |
| `data.py` | Data awal akun, kendaraan, transaksi, sesi, counter, serta pengaturan DP dan denda. |
| `waktu.py` | Fungsi waktu aktual, jatuh tempo, keterlambatan, dan kalender simulasi. |
| `validasi_input.py` | Fungsi validasi dan parsing input pengguna. |
| `tampilan.py` | Tampilan terminal, menu interaktif, input password, tabel, dan format Rupiah. |

## 📚 Library yang Digunakan

`inquirer` · `pwinput` · `prettytable` · `matplotlib` `os` · `re` · `math` · `datetime`
