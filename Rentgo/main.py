from tampilan import bersihkan_layar, banner, pilih
from autentikasi import login, register, lupa_password


def main():
    try:
        while True:
            bersihkan_layar()
            banner("RentGo - Rental dan Go")
            pilihan = pilih("Pilih menu", [
                "1. Login",
                "2. Daftar Akun",
                "3. Lupa Password",
                "4. Keluar",
            ])
            if pilihan == 1:
                login()
            elif pilihan == 2:
                register()
            elif pilihan == 3:
                lupa_password()
            else:
                break
    except (KeyboardInterrupt, EOFError):
        print()

    bersihkan_layar()
    print("Bye-bye!")


if __name__ == "__main__":
    main()
