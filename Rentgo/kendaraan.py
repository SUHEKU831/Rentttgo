from data import kendaraan, counter
from tampilan import bersihkan_layar, banner, tekan_enter, pilih, konfirmasi, tampilkan_tabel, rupiah
from validasi_input import kumpulkan, parse_angka, cek_teks_wajib

STATUS_KENDARAAN = ["Tersedia", "Disewa", "Maintenance"]


def tabel_kendaraan(daftar):
    tampilkan_tabel(
        ["No", "Tipe", "Merek", "Harga Rental / Hari", "Status"],
        [[no, k["tipe"], k["merek"], rupiah(k["harga"]), k["status"]]
         for no, k in enumerate(daftar, 1)],
    )


def label_kendaraan(daftar):
    label = [f"{no}. {k['merek']} ({k['tipe']}) - {rupiah(k['harga'])}/hari - {k['status']}"
             for no, k in enumerate(daftar, 1)]
    label.append("Kembali")
    return label


def pengelolaan_kendaraan():
    while True:
        bersihkan_layar()
        banner("PENGELOLAAN KENDARAAN")
        if not kendaraan:
            print("Belum ada data kendaraan.")
        else:
            tabel_kendaraan(kendaraan)
        print()

        pilihan = pilih("Pilih menu", [
            "1. Tambah Kendaraan",
            "2. Ubah Kendaraan",
            "3. Hapus Kendaraan",
            "4. Kembali",
        ])
        if pilihan == 1:
            tambah_kendaraan()
        elif pilihan == 2:
            ubah_kendaraan()
        elif pilihan == 3:
            hapus_kendaraan()
        else:
            break


def tambah_kendaraan():
    bersihkan_layar()
    banner("TAMBAH KENDARAAN")
    print("Persyaratan data:")
    print("  Tipe  : tidak boleh kosong")
    print("  Merek : tidak boleh kosong")
    print("  Harga : angka bulat, minimal 1 (per hari, dalam Rupiah)\n")

    tipe = input("Tipe               : ").strip()
    merek = input("Merek              : ").strip()
    harga, error_harga = parse_angka(input("Harga Rental / Hari : "), "Harga rental")

    error = kumpulkan(cek_teks_wajib(tipe, "Tipe"), cek_teks_wajib(merek, "Merek"), error_harga)
    if error:
        print()
        for pesan in error:
            print(f"Error: {pesan}")
        tekan_enter()
        return

    status = STATUS_KENDARAAN[pilih("Status", ["1. Tersedia", "2. Disewa", "3. Maintenance"]) - 1]

    counter["kendaraan"] += 1
    kendaraan.append({
        "id": counter["kendaraan"],
        "tipe": tipe,
        "merek": merek,
        "harga": harga,
        "status": status,
    })
    print("\nKendaraan berhasil ditambahkan!")
    tekan_enter()


def ubah_kendaraan():
    bersihkan_layar()
    banner("UBAH KENDARAAN")
    if not kendaraan:
        print("Belum ada data kendaraan.")
        tekan_enter()
        return

    tabel_kendaraan(kendaraan)
    print()
    label = label_kendaraan(kendaraan)
    nomor = pilih("Pilih kendaraan yang akan diubah", label)
    if nomor == len(label):
        return
    data = kendaraan[nomor - 1]

    print(f"\nData saat ini: {data['merek']} ({data['tipe']}) - "
          f"{rupiah(data['harga'])}/hari - {data['status']}")
    print("Masukkan data baru (Enter = tidak diubah):")
    tipe = input("Tipe               : ").strip()
    merek = input("Merek              : ").strip()
    harga_teks = input("Harga Rental / Hari : ").strip()
    status_baru = pilih("Status", ["1. Tidak diubah", "2. Tersedia", "3. Disewa", "4. Maintenance"])

    harga = None
    error_harga = None
    if harga_teks != "":
        harga, error_harga = parse_angka(harga_teks, "Harga rental")
    if error_harga:
        print(f"\nError: {error_harga}")
        tekan_enter()
        return

    berubah = False
    if tipe:
        data["tipe"] = tipe
        berubah = True
    if merek:
        data["merek"] = merek
        berubah = True
    if harga is not None:
        data["harga"] = harga
        berubah = True
    if status_baru != 1:
        data["status"] = STATUS_KENDARAAN[status_baru - 2]
        berubah = True

    print("\nData kendaraan berhasil diubah!" if berubah else "\nTidak ada data yang diubah.")
    tekan_enter()


def hapus_kendaraan():
    bersihkan_layar()
    banner("HAPUS KENDARAAN")
    if not kendaraan:
        print("Belum ada data kendaraan.")
        tekan_enter()
        return

    tabel_kendaraan(kendaraan)
    print()
    label = label_kendaraan(kendaraan)
    nomor = pilih("Pilih kendaraan yang akan dihapus", label)
    if nomor == len(label):
        return
    data = kendaraan[nomor - 1]

    if konfirmasi(f"Yakin ingin menghapus {data['merek']} ({data['tipe']})?"):
        kendaraan.remove(data)
        print("\nKendaraan berhasil dihapus!")
    else:
        print("\nPenghapusan dibatalkan")
    tekan_enter()
