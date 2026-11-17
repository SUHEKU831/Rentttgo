from data import users, transaksi
from tampilan import bersihkan_layar, banner, tekan_enter, pilih, konfirmasi, tampilkan_tabel, rupiah, format_waktu
from kendaraan import pengelolaan_kendaraan
from waktu import waktu_sekarang, nomor_hari, awal_hari, MENIT_PER_HARI
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

STATUS_TRANSAKSI = ["Berjalan", "Selesai"]


def menu_admin():
    while True:
        bersihkan_layar()
        banner("MENU ADMIN")
        pilihan = pilih("Pilih menu", [
            "1. Pengelolaan Kendaraan",
            "2. Transaksi Rental",
            "3. Akun Customer",
            "4. Keluar",
        ])
        if pilihan == 1:
            pengelolaan_kendaraan()
        elif pilihan == 2:
            transaksi_rental()
        elif pilihan == 3:
            akun_customer()
        else:
            break


def tabel_transaksi(daftar):
    tampilkan_tabel(
        ["ID", "Nama Customer", "Kendaraan", "Lama Sewa", "Waktu Sewa",
         "Total Biaya", "DP (50%)", "Pelunasan (50%)", "Status"],
        [[t["id"], t["customer"], t["kendaraan"], f"{t['lama_sewa']} hari",
          format_waktu(t["waktu_sewa"]), rupiah(t["total_biaya"]),
          rupiah(t["dp"]), rupiah(t["pelunasan"]), t["status"]]
         for t in daftar],
    )


def transaksi_rental():
    while True:
        bersihkan_layar()
        banner("TRANSAKSI RENTAL")
        pilihan = pilih("Pilih menu", [
            "1. Semua Transaksi",
            "2. Filter Berdasarkan Status",
            "3. Diagram Transaksi",
            "4. Kembali",
        ])

        if pilihan == 1:
            print()
            if not transaksi:
                print("Belum ada data transaksi.")
            else:
                tabel_transaksi(transaksi)
            tekan_enter()

        elif pilihan == 2:
            status = STATUS_TRANSAKSI[pilih("Pilih status", ["1. Berjalan", "2. Selesai"]) - 1]
            hasil = [t for t in transaksi if t["status"] == status]
            print()
            if not hasil:
                print("Tidak ada transaksi dengan status tersebut.")
            else:
                tabel_transaksi(hasil)
            tekan_enter()

        elif pilihan == 3:
            diagram_transaksi()

        else:
            break


def diagram_transaksi():
    if not transaksi:
        print("\nBelum ada data transaksi untuk dibuat diagram.")
        tekan_enter()
        return

    per_hari = {}
    for t in transaksi:
        hari = nomor_hari(t["waktu_sewa"])
        per_hari[hari] = per_hari.get(hari, 0) + 1

    hari_awal = min(per_hari)
    hari_akhir = max(max(per_hari), nomor_hari(waktu_sekarang()))
    daftar_hari = list(range(hari_awal, hari_akhir + 1))
    jumlah = [per_hari.get(hari, 0) for hari in daftar_hari]

    fig, sumbu = plt.subplots(figsize=(8, 4.5))
    sumbu.plot(daftar_hari, jumlah, marker="o", color="#2a7de1", linewidth=2)
    sumbu.set_title("Perkembangan Rental per Hari")
    sumbu.set_xlabel(f"Jam mulai tiap hari (1 hari = {MENIT_PER_HARI:g} menit waktu nyata)")
    sumbu.set_ylabel("Jumlah Rental")
    sumbu.yaxis.set_major_locator(MaxNLocator(integer=True))
    sumbu.set_ylim(0, max(jumlah) + 1)
    sumbu.grid(True, alpha=0.3)

    langkah = max(1, len(daftar_hari) // 12)
    posisi = daftar_hari[::langkah]
    sumbu.set_xticks(posisi)
    sumbu.set_xticklabels([awal_hari(h).strftime("%H:%M") for h in posisi])
    if len(daftar_hari) <= 15:
        for hari, nilai in zip(daftar_hari, jumlah):
            sumbu.annotate(str(nilai), (hari, nilai), textcoords="offset points", xytext=(0, 7), ha="center", fontweight="bold")
    fig.autofmt_xdate()
    fig.tight_layout()

    print("\nDiagram ditampilkan di jendela baru. Tutup jendela diagram untuk melanjutkan.")
    plt.show()
    tekan_enter()


def akun_customer():
    bersihkan_layar()
    banner("AKUN CUSTOMER")
    daftar = [(nama, akun) for nama, akun in users.items() if akun["role"] == "customer"]
    if not daftar:
        print("Belum ada akun customer.")
        tekan_enter()
        return

    tampilkan_tabel(
        ["No", "Nama", "Umur", "NIK", "No. HP", "Alamat", "Saldo"],
        [[no, nama, akun["umur"], akun["nik"], akun["no_hp"], akun["alamat"], rupiah(akun["saldo"])]
         for no, (nama, akun) in enumerate(daftar, 1)],
    )
    print()

    label = [f"{no}. {nama}" for no, (nama, _) in enumerate(daftar, 1)] + ["Kembali"]
    nomor = pilih("Pilih customer yang akan dihapus", label)
    if nomor == len(label):
        return
    nama, akun = daftar[nomor - 1]

    if any(t["nik"] == akun["nik"] and t["status"] == "Berjalan" for t in transaksi):
        print("\nCustomer memiliki transaksi berjalan")
        tekan_enter()
        return

    if konfirmasi(f"Yakin ingin menghapus akun {nama}?"):
        del users[nama]
        print("\nAkun customer berhasil dihapus!")
    else:
        print("\nPenghapusan dibatalkan.")
    tekan_enter()