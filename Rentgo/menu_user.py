from data import users, kendaraan, transaksi, sesi, counter, DP_PERSEN, DENDA_PERSEN_PER_HARI
from tampilan import bersihkan_layar, banner, tekan_enter, pilih, konfirmasi, tampilkan_tabel, cetak_rincian, rupiah, format_waktu
from validasi_input import parse_angka
from kelola_akun import kelola_akun
from waktu import waktu_sekarang, hitung_jatuh_tempo, hitung_hari_terlambat, MENIT_PER_HARI


def menu_user():
    while True:
        bersihkan_layar()
        banner("MENU USER")
        pilihan = pilih("Pilih menu", [
            "1. Pesan Kendaraan",
            "2. Pengembalian Kendaraan",
            "3. Riwayat Transaksi",
            "4. Top Up Saldo",
            "5. Kelola Akun",
            "6. Keluar",
        ])
        if pilihan == 1:
            pesan_kendaraan()
        elif pilihan == 2:
            pengembalian_kendaraan()
        elif pilihan == 3:
            riwayat_transaksi()
        elif pilihan == 4:
            top_up_saldo()
        elif pilihan == 5:
            kelola_akun()
        else:
            break


def pesan_kendaraan():
    akun = users[sesi["nama"]]

    bersihkan_layar()
    banner("PESAN KENDARAAN")
    tersedia = [k for k in kendaraan if k["status"] == "Tersedia"]
    if not tersedia:
        print("Belum ada kendaraan yang tersedia.")
        tekan_enter()
        return

    tampilkan_tabel(
        ["No", "Tipe", "Merek", "Harga Rental / Hari"],
        [[no, k["tipe"], k["merek"], rupiah(k["harga"])] for no, k in enumerate(tersedia, 1)],
    )
    print()

    label = [f"{no}. {k['merek']} ({k['tipe']}) - {rupiah(k['harga'])}/hari"
             for no, k in enumerate(tersedia, 1)] + ["Kembali"]
    nomor = pilih("Pilih kendaraan yang akan dipesan", label)
    if nomor == len(label):
        return
    pilihan = tersedia[nomor - 1]

    print(f"\nCatatan: 1 hari sewa = {MENIT_PER_HARI:g} menit waktu nyata.")
    lama, error = parse_angka(input("Lama sewa (hari): "), "Lama sewa", minimal=1, pesan_minimal="Lama sewa minimal 1 hari!")
    if error:
        print(f"\nError: {error}")
        tekan_enter()
        return

    total = pilihan["harga"] * lama
    dp = total * DP_PERSEN // 100
    pelunasan = total - dp
    nama_kendaraan = f"{pilihan['merek']} ({pilihan['tipe']})"

    print("\nRingkasan pesanan:")
    cetak_rincian([
        ("Kendaraan", nama_kendaraan),
        ("Harga / Hari", rupiah(pilihan["harga"])),
        ("Lama Sewa", f"{lama} hari (= {lama * MENIT_PER_HARI:g} menit waktu nyata)"),
        ("Total Biaya", rupiah(total)),
        (f"Wajib DP ({DP_PERSEN}%)", rupiah(dp)),
        (f"Sisa Pembayaran Saat Pengembalian ({100 - DP_PERSEN}%)", rupiah(pelunasan)),
        ("Saldo Saat Ini", rupiah(akun["saldo"])),
    ])

    if akun["saldo"] < dp:
        print(f"\nSaldo tidak cukup untuk membayar DP {DP_PERSEN}%! "
              "Silakan top up saldo terlebih dahulu.")
        tekan_enter()
        return

    print()
    if konfirmasi(f"Konfirmasi pemesanan dan bayar DP ({DP_PERSEN}%)?"):
        waktu_sewa = waktu_sekarang()
        jatuh_tempo = hitung_jatuh_tempo(waktu_sewa, lama)
        akun["saldo"] -= dp
        pilihan["status"] = "Disewa"
        counter["transaksi"] += 1
        id_transaksi = f"TRX-{counter['transaksi']:03d}"
        transaksi.append({
            "id": id_transaksi,
            "nik": akun["nik"],
            "customer": sesi["nama"],
            "id_kendaraan": pilihan["id"],
            "kendaraan": nama_kendaraan,
            "harga_per_hari": pilihan["harga"],
            "lama_sewa": lama,
            "waktu_sewa": waktu_sewa,
            "waktu_kembali": None,
            "total_biaya": total,
            "dp": dp,
            "pelunasan": pelunasan,
            "denda": 0,
            "status": "Berjalan",
        })
        print(f"\nPemesanan berhasil! DP {DP_PERSEN}% terbayar.")
        cetak_rincian([
            ("ID Transaksi", id_transaksi),
            ("Waktu Sewa", format_waktu(waktu_sewa)),
            ("Jatuh Tempo", format_waktu(jatuh_tempo)),
        ])
    else:
        print("\nPemesanan dibatalkan.")
    tekan_enter()


def pengembalian_kendaraan():
    akun = users[sesi["nama"]]

    bersihkan_layar()
    banner("PENGEMBALIAN KENDARAAN")
    berjalan = [t for t in transaksi
                if t["nik"] == akun["nik"] and t["status"] == "Berjalan"]
    if not berjalan:
        print("Tidak ada kendaraan yang sedang disewa.")
        tekan_enter()
        return

    tampilkan_tabel(
        ["No", "ID", "Kendaraan", "Waktu Sewa", "Lama Sewa", "Total Biaya",
         f"Sisa Pelunasan ({100 - DP_PERSEN}%)"],
        [[no, t["id"], t["kendaraan"], format_waktu(t["waktu_sewa"]),
          f"{t['lama_sewa']} hari", rupiah(t["total_biaya"]), rupiah(t["pelunasan"])]
         for no, t in enumerate(berjalan, 1)],
    )
    print()

    label = [f"{no}. {t['id']} - {t['kendaraan']}" for no, t in enumerate(berjalan, 1)] + ["Kembali"]
    nomor = pilih("Pilih transaksi yang dikembalikan", label)
    if nomor == len(label):
        return
    trx = berjalan[nomor - 1]

    sekarang = waktu_sekarang()
    pelunasan = trx["pelunasan"]
    jatuh_tempo = hitung_jatuh_tempo(trx["waktu_sewa"], trx["lama_sewa"])
    hari_terlambat = hitung_hari_terlambat(jatuh_tempo, sekarang)
    if hari_terlambat > 0:
        denda = hari_terlambat * trx["harga_per_hari"] * DENDA_PERSEN_PER_HARI // 100
    else:
        denda = 0
    total_bayar = pelunasan + denda

    print("\nRincian tagihan:")
    cetak_rincian([
        ("Kendaraan", trx["kendaraan"]),
        ("Waktu Sekarang", format_waktu(sekarang)),
        ("Jatuh Tempo", format_waktu(jatuh_tempo)),
        (f"Sisa Pelunasan ({100 - DP_PERSEN}%)", rupiah(pelunasan)),
        ("Hari Terlambat", f"{hari_terlambat} hari"),
        ("Denda", rupiah(denda)),
        ("Total yang Harus Dibayar", rupiah(total_bayar)),
        ("Saldo Saat Ini", rupiah(akun["saldo"])),
    ])

    if akun["saldo"] < total_bayar:
        print("\nSaldo tidak cukup untuk melunasi sisa sewa! Silakan top up saldo.")
        tekan_enter()
        return

    print()
    if konfirmasi("Konfirmasi pelunasan & pengembalian kendaraan?"):
        akun["saldo"] -= total_bayar
        for k in kendaraan:
            if k["id"] == trx["id_kendaraan"] and k["status"] == "Disewa":
                k["status"] = "Tersedia"
        trx["status"] = "Selesai"
        trx["waktu_kembali"] = sekarang
        trx["denda"] = denda
        print("\nKendaraan berhasil dikembalikan!")
        print(f"Pelunasan {100 - DP_PERSEN}% berhasil. Terima kasih.")
    else:
        print("\nPengembalian dibatalkan.")
    tekan_enter()


def riwayat_transaksi():
    akun = users[sesi["nama"]]

    bersihkan_layar()
    banner("RIWAYAT TRANSAKSI")
    riwayat = [t for t in transaksi if t["nik"] == akun["nik"]]
    if not riwayat:
        print("Belum ada riwayat transaksi.")
    else:
        tampilkan_tabel(
            ["No", "ID", "Kendaraan", "Waktu Sewa", "Lama Sewa", "Total Biaya",
             f"DP ({DP_PERSEN}%)", "Denda", "Status"],
            [[no, t["id"], t["kendaraan"], format_waktu(t["waktu_sewa"]),
              f"{t['lama_sewa']} hari", rupiah(t["total_biaya"]), rupiah(t["dp"]),
              rupiah(t["denda"]), t["status"]]
             for no, t in enumerate(riwayat, 1)],
        )
    tekan_enter()


def top_up_saldo():
    akun = users[sesi["nama"]]

    bersihkan_layar()
    banner("TOP UP SALDO")
    print(f"Saldo saat ini: {rupiah(akun['saldo'])}")
    print("Persyaratan nominal: angka, lebih dari 0\n")

    nominal, error = parse_angka(input("Nominal top up: "), "Nominal", minimal=1,
                                 pesan_minimal="Nominal harus lebih dari 0!")
    if error:
        print(f"\nError: {error}")
        tekan_enter()
        return

    akun["saldo"] += nominal
    print(f"\nTop up berhasil! Saldo Anda sekarang: {rupiah(akun['saldo'])}")
    tekan_enter()