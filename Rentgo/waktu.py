import math
from datetime import datetime, timedelta

DETIK_PER_HARI = 180
MENIT_PER_HARI = DETIK_PER_HARI / 60
HARI = timedelta(seconds=DETIK_PER_HARI)

MULAI_PROGRAM = datetime.now().replace(microsecond=0)


def _sekarang_nyata():
    return datetime.now()


def waktu_sekarang():
    return _sekarang_nyata()


def hitung_jatuh_tempo(waktu_sewa, lama_sewa):
    return waktu_sewa + lama_sewa * HARI


def hitung_hari_terlambat(jatuh_tempo, waktu):
    selisih = waktu - jatuh_tempo
    if selisih <= timedelta(0):
        return 0
    return math.ceil(selisih / HARI)


def nomor_hari(waktu):
    return math.floor((waktu - MULAI_PROGRAM) / HARI)


def awal_hari(nomor):
    return MULAI_PROGRAM + nomor * HARI