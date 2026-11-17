from data import users, transaksi, sesi
from tampilan import bersihkan_layar, banner, tekan_enter, pilih, konfirmasi, input_password, tampilkan_tabel, rupiah
from validasi_input import kumpulkan, cek_nama, cek_umur, cek_no_hp, cek_alamat, cek_password_baru


def kelola_akun():
    while True:
        akun = users[sesi["nama"]]
        bersihkan_layar()
        banner("KELOLA AKUN")
        tampilkan_tabel(["Data", "Isi"], [
            ["Nama", sesi["nama"]],
            ["Umur", akun["umur"]],
            ["NIK", akun["nik"]],
            ["No. HP", akun["no_hp"]],
            ["Alamat", akun["alamat"]],
            ["Saldo", rupiah(akun["saldo"])],
            ["Password", akun["password"]],
        ])
        print()

        pilihan = pilih("Pilih menu", [
            "1. Ubah Password",
            "2. Ubah Data Diri",
            "3. Kembali",
        ])
        if pilihan == 1:
            ubah_password()
        elif pilihan == 2:
            ubah_data_diri()
        else:
            break


def ubah_password():
    akun = users[sesi["nama"]]

    bersihkan_layar()
    banner("UBAH PASSWORD")
    print("Persyaratan password: baru tidak boleh kosong, tidak sama dengan lama\n")

    lama = input_password("Password lama")
    if lama != akun["password"]:
        print("\nError: Password lama salah!")
        tekan_enter()
        return

    baru = input_password("Password baru")
    if cek_password_baru(baru) or baru == lama:
        print("\nError: Password baru tidak boleh kosong dan tidak boleh sama dengan password lama!")
        tekan_enter()
        return

    if input_password("Konfirmasi password baru") != baru:
        print("\nError: Konfirmasi password tidak sama dengan password baru!")
        tekan_enter()
        return

    print()
    if konfirmasi("Yakin ingin mengubah password?"):
        akun["password"] = baru
        print("\nPassword berhasil diubah!")
    else:
        print("\nPerubahan password dibatalkan.")
    tekan_enter()


def ubah_data_diri():
    nama_lama = sesi["nama"]
    akun = users[nama_lama]

    bersihkan_layar()
    banner("UBAH DATA DIRI")
    print("Persyaratan:")
    print("  Nama   : tidak boleh kosong, belum digunakan akun lain")
    print("  Umur   : angka, minimal 18")
    print("  No. HP : angka, 10-13 digit, diawali 08")
    print("  Alamat : tidak boleh kosong")
    print("  (NIK tidak bisa diubah)\n")

    pilihan = pilih("Pilih data yang ingin diubah", [
        "1. Ubah Nama",
        "2. Ubah Umur",
        "3. Ubah No. HP",
        "4. Ubah Alamat",
        "5. Kembali",
    ])
    if pilihan == 5:
        return

    if pilihan == 1:
        nama_baru = input("\nNama baru: ").strip()
        password = input_password("Password saat ini")
        error = kumpulkan(
            cek_nama(nama_baru, kecuali=nama_lama),
            None if password == akun["password"] else "Password salah!",
        )
    elif pilihan == 2:
        umur = input("\nUmur baru: ").strip()
        error = kumpulkan(cek_umur(umur))
    elif pilihan == 3:
        no_hp = input("\nNo. HP baru: ").strip()
        error = kumpulkan(cek_no_hp(no_hp))
    else:
        alamat = input("\nAlamat baru: ").strip()
        error = kumpulkan(cek_alamat(alamat))

    if error:
        print()
        for pesan in error:
            print(f"Error: {pesan}")
        tekan_enter()
        return

    if pilihan == 1:
        if nama_baru != nama_lama:
            users[nama_baru] = users.pop(nama_lama)
            sesi["nama"] = nama_baru
            for t in transaksi:
                if t["nik"] == akun["nik"]:
                    t["customer"] = nama_baru
    elif pilihan == 2:
        akun["umur"] = int(umur)
    elif pilihan == 3:
        akun["no_hp"] = no_hp
    else:
        akun["alamat"] = alamat

    print("\nData berhasil diperbarui!")
    tekan_enter()
