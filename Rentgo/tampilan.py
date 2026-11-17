import os
import inquirer
import pwinput
from prettytable import PrettyTable

LEBAR = 56
GARIS_GANDA = "=" * LEBAR


def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")


def banner(teks):
    print(GARIS_GANDA)
    print(teks.center(LEBAR))
    print(GARIS_GANDA)


def tekan_enter(pesan="Tekan Enter untuk melanjutkan..."):
    input(f"\n{pesan}")


def pilih(pesan, opsi):
    pertanyaan = [
        inquirer.List(
            "pilihan",
            message=pesan,
            choices=[(label, nomor) for nomor, label in enumerate(opsi, 1)],
            carousel=True,
        )
    ]
    jawaban = inquirer.prompt(pertanyaan, raise_keyboard_interrupt=True)
    return jawaban["pilihan"]


def konfirmasi(pesan):
    return pilih(pesan, ["Ya", "Tidak"]) == 1


def input_password(pesan):
    return pwinput.pwinput(prompt=f"{pesan}: ", mask="*")


def tampilkan_tabel(kolom, baris):
    tabel = PrettyTable()
    tabel.field_names = kolom
    tabel.align = "l"
    tabel.add_rows(baris)
    print(tabel)


def cetak_rincian(baris):
    lebar = max(len(label) for label, _ in baris)
    for label, nilai in baris:
        print(f"  {label.ljust(lebar)} : {nilai}")


def rupiah(nilai):
    return f"Rp{nilai:,}".replace(",", ".")


def format_waktu(waktu):
    return waktu.strftime("%d-%m-%Y %H:%M:%S")