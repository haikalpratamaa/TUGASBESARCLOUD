def template_email_pengajuan_baru(nama_mahasiswa, nama_mata_kuliah):
    subject = "Pengajuan izin baru — KelasKita"
    body = (
        f"Yth. Dosen Pengampu,\n\n"
        f"Ada pengajuan izin baru dari {nama_mahasiswa} "
        f"untuk mata kuliah {nama_mata_kuliah}.\n\n"
        f"Silakan login ke KelasKita untuk memproses pengajuan ini.\n\n"
        f"Salam,\nSistem KelasKita"
    )
    return subject, body


def template_email_izin_disetujui(nama_mahasiswa, nama_mata_kuliah, nomor_izin):
    subject = f"Izin disetujui: {nomor_izin} — KelasKita"
    body = (
        f"Yth. {nama_mahasiswa},\n\n"
        f"Pengajuan izin Anda untuk mata kuliah {nama_mata_kuliah} "
        f"dengan nomor {nomor_izin} telah DISETUJUI.\n\n"
        f"Anda dapat login ke KelasKita untuk mencetak surat izin.\n\n"
        f"Salam,\nSistem KelasKita"
    )
    return subject, body


def template_email_izin_ditolak(nama_mahasiswa, nama_mata_kuliah, nomor_izin, catatan=None):
    subject = f"Izin ditolak: {nomor_izin} — KelasKita"
    body = (
        f"Yth. {nama_mahasiswa},\n\n"
        f"Pengajuan izin Anda untuk mata kuliah {nama_mata_kuliah} "
        f"dengan nomor {nomor_izin} telah DITOLAK."
    )
    if catatan:
        body += f"\n\nCatatan dosen:\n{catatan}"
    body += "\n\nSilakan login ke KelasKita untuk melihat detail.\n\nSalam,\nSistem KelasKita"
    return subject, body
