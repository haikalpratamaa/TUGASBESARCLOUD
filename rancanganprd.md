# PRD FINAL

# KelasKita — Sistem Izin Tidak Masuk Kelas

**Versi:** 1.0
**Status:** Final MVP
**Stack:** HTML, CSS, JavaScript, Flask, MySQL, Google Cloud Platform
**Deployment Target:** Google Cloud Run + Cloud SQL
**Warna Utama:** Merah

---

## Daftar Isi

1. [Judul Project](#1-judul-project)
2. [Latar Belakang](#2-latar-belakang)
3. [Tujuan Project](#3-tujuan-project)
4. [Target Pengguna](#4-target-pengguna)
5. [Scope Project](#5-scope-project)
6. [User Flow Utama](#6-user-flow-utama)
7. [Fitur Utama](#7-fitur-utama)
8. [Functional Requirements](#8-functional-requirements)
9. [Non-Functional Requirements](#9-non-functional-requirements)
10. [Role dan Permission](#10-role-dan-permission)
11. [Data dan Database](#11-data-dan-database)
12. [UI/UX Requirements](#12-uiux-requirements)
13. [Technical Requirements](#13-technical-requirements)
14. [Halaman yang Dibutuhkan](#14-halaman-yang-dibutuhkan)
15. [API / Backend Requirements](#15-api--backend-requirements)
16. [Acceptance Criteria](#16-acceptance-criteria)
17. [Edge Cases dan Error Handling](#17-edge-cases-dan-error-handling)
18. [Risiko dan Mitigasi](#18-risiko-dan-mitigasi)
19. [Roadmap Implementasi](#19-roadmap-implementasi)
20. [Checklist Final](#20-checklist-final)

---

# 1. Judul Project

## Nama Project

**KelasKita**

## Nama Lengkap

**KelasKita — Sistem Izin Tidak Masuk Kelas dengan Approval Dosen**

## Deskripsi Singkat

KelasKita adalah aplikasi web yang membantu mahasiswa mengajukan izin tidak masuk kelas secara rapi, terdokumentasi, dan mudah diverifikasi. Mahasiswa dapat membuat pengajuan izin, dosen menerima notifikasi melalui email, lalu dosen memberikan keputusan berupa disetujui atau ditolak.

Jika izin disetujui, sistem dapat menghasilkan surat izin yang bisa dicetak dan dilengkapi QR code untuk verifikasi keaslian approval. Project ini dirancang sebagai aplikasi nyata yang dapat digunakan oleh dosen dalam skala kecil, misalnya untuk satu kelas, satu mata kuliah, satu program studi, atau kebutuhan internal kampus.

---

# 2. Latar Belakang

Proses izin tidak masuk kelas sering dilakukan melalui chat pribadi, grup WhatsApp, atau pesan informal. Cara tersebut memang cepat, tetapi memiliki beberapa masalah. Pesan izin mudah tertumpuk, status persetujuan tidak selalu jelas, dosen harus mengecek chat secara manual, dan mahasiswa tidak memiliki bukti izin yang rapi apabila dibutuhkan kembali.

Dalam kondisi nyata, mahasiswa juga sering membutuhkan bukti bahwa izinnya benar-benar sudah disetujui. Bukti berupa screenshot chat kurang ideal karena mudah hilang, kurang formal, dan sulit diverifikasi.

Dosen juga tidak selalu memiliki rekap izin yang tersusun dengan baik. Akibatnya, proses izin yang seharusnya sederhana menjadi kurang terdokumentasi.

KelasKita hadir untuk membuat proses izin menjadi lebih tertib. Mahasiswa mengajukan izin melalui sistem, dosen menerima email notifikasi, dosen cukup melakukan approval tanpa tanda tangan manual, lalu sistem menyimpan keputusan tersebut.

Surat izin dapat dicetak oleh mahasiswa hanya jika izin sudah disetujui. QR code pada surat digunakan untuk membuktikan bahwa izin tersebut benar-benar berasal dari sistem.

---

# 3. Tujuan Project

## 3.1 Tujuan Utama

Membangun aplikasi web untuk mengelola pengajuan izin tidak masuk kelas dengan alur:

> Mahasiswa mengajukan izin → dosen menerima email → dosen melakukan approval → mahasiswa menerima hasil approval → mahasiswa dapat mencetak surat izin dengan QR verification.

## 3.2 Tujuan Produk

Project ini bertujuan untuk:

1. Membantu mahasiswa mengajukan izin secara lebih tertib.
2. Membantu dosen menerima dan memproses izin tanpa bergantung pada chat manual.
3. Menyediakan riwayat izin yang terdokumentasi.
4. Menyediakan bukti izin dalam bentuk surat cetak.
5. Menyediakan validasi dokumen melalui QR code.
6. Menyediakan email notification agar dosen dan mahasiswa tidak perlu terus-menerus membuka sistem.

## 3.3 Tujuan Akademik

Project ini menunjukkan kemampuan membangun aplikasi CRUD yang tidak hanya menyimpan data, tetapi juga memiliki:

* workflow nyata,
* role permission,
* approval system,
* email notification,
* QR verification,
* print layout,
* database relasional,
* dan deployment cloud.

## 3.4 Hasil Akhir

Hasil akhir berupa aplikasi web MVP real-use yang dapat:

* digunakan mahasiswa untuk mengajukan izin,
* digunakan dosen untuk memproses izin,
* digunakan admin untuk mengelola data dasar,
* mengirim email notifikasi,
* menghasilkan surat izin print-ready,
* memvalidasi surat melalui QR code,
* berjalan di cloud menggunakan GCP.

---

# 4. Target Pengguna

## 4.1 Mahasiswa

Mahasiswa adalah pengguna yang mengajukan izin tidak masuk kelas.

### Masalah Mahasiswa

* Izin sering tercecer di chat.
* Tidak selalu tahu apakah izin sudah dibaca dosen.
* Tidak memiliki bukti izin yang rapi.
* Sulit melihat riwayat izin sebelumnya.

### Kebutuhan Mahasiswa

* Form pengajuan izin yang sederhana.
* Status izin yang jelas.
* Riwayat izin pribadi.
* Email pemberitahuan ketika izin disetujui atau ditolak.
* Surat izin yang bisa dicetak jika sudah disetujui.
* QR code untuk membuktikan bahwa surat izin valid.

### Ekspektasi Mahasiswa

Mahasiswa dapat mengajukan izin dengan cepat, melihat statusnya, menerima email hasil keputusan, dan mencetak surat izin jika sudah disetujui.

---

## 4.2 Dosen

Dosen adalah pengguna utama yang memproses pengajuan izin mahasiswa.

### Masalah Dosen

* Izin mahasiswa sering masuk dari banyak jalur.
* Sulit membedakan izin yang belum dan sudah diproses.
* Sulit melihat rekap izin secara cepat.
* Chat izin bisa tertumpuk oleh pesan lain.

### Kebutuhan Dosen

* Email notifikasi ketika ada izin baru.
* Daftar pengajuan izin dalam sistem.
* Detail izin yang jelas.
* Tombol setujui dan tolak.
* Catatan keputusan.
* Riwayat izin yang sudah diproses.

### Ekspektasi Dosen

Dosen tidak perlu memberikan tanda tangan manual. Dosen cukup membuka sistem, membaca pengajuan, lalu klik setujui atau tolak. Sistem yang akan mencatat keputusan dan menghasilkan bukti validasi.

---

## 4.3 Admin Sistem

Admin sistem adalah pengguna yang mengelola data dasar aplikasi.

### Kebutuhan Admin

* Mengelola user.
* Mengelola jadwal kelas.
* Mengelola kategori izin.
* Melihat log email.
* Memastikan data sistem tetap rapi.

### Ekspektasi Admin

Admin dapat menjaga sistem tetap siap dipakai tanpa harus mengubah kode aplikasi.

---

## 4.4 Public Verifier

Public verifier adalah siapa pun yang memindai QR code pada surat izin.

### Kebutuhan Public Verifier

* Memastikan apakah surat izin valid.
* Melihat status approval secara ringkas.
* Tidak perlu login.

### Batasan Public Verifier

Public verifier hanya dapat melihat informasi ringkas, bukan seluruh alasan izin secara detail.

---

# 5. Scope Project

## 5.1 Fitur yang Masuk MVP Final

### Auth dan Role

* Login.
* Logout.
* Role mahasiswa.
* Role dosen.
* Role admin.
* Proteksi halaman berdasarkan role.

### Pengajuan Izin

* Mahasiswa membuat pengajuan izin.
* Mahasiswa melihat riwayat izin pribadi.
* Mahasiswa melihat detail izin.
* Mahasiswa mengedit pengajuan selama status masih `Diajukan`.
* Mahasiswa membatalkan pengajuan selama status masih `Diajukan`.

### Approval Dosen

* Dosen melihat daftar izin masuk.
* Dosen melihat detail izin.
* Dosen menyetujui izin.
* Dosen menolak izin.
* Dosen memberi catatan keputusan.
* Sistem mencatat nama dosen dan waktu approval.

### Email Notification

* Email ke dosen ketika mahasiswa mengajukan izin baru.
* Email ke mahasiswa ketika izin disetujui.
* Email ke mahasiswa ketika izin ditolak.
* Email log untuk mencatat pengiriman berhasil atau gagal.

### Surat Izin dan QR Verification

* Mahasiswa dapat mencetak surat izin jika status sudah `Disetujui`.
* Surat izin menampilkan QR code.
* QR code mengarah ke halaman verifikasi.
* Halaman verifikasi menampilkan status valid atau tidak valid.
* Surat izin tidak membutuhkan tanda tangan manual dosen.

### Master Data

* CRUD kategori izin.
* CRUD jadwal kelas.
* CRUD user sederhana.
* Dashboard mahasiswa.
* Dashboard dosen.
* Dashboard admin.

---

## 5.2 Fitur yang Tidak Masuk MVP

Agar project tetap realistis, fitur berikut tidak masuk MVP:

* Upload surat dokter.
* Upload file bukti izin.
* Notifikasi WhatsApp.
* Notifikasi Telegram.
* Tanda tangan digital legal.
* Multi-level approval.
* Approval oleh lebih dari satu dosen.
* Integrasi sistem akademik kampus.
* Integrasi presensi resmi.
* QR untuk presensi masuk kelas.
* Mobile app native Android/iOS.
* Kalender otomatis.
* Chat antara mahasiswa dan dosen.
* AI untuk membaca alasan izin.
* Rekap absensi semester penuh.

---

## 5.3 Batasan Sistem

KelasKita hanya berfokus pada pengajuan izin tidak masuk kelas, approval dosen, email notification, surat cetak, dan QR verification.

Sistem ini tidak menggantikan sistem akademik resmi kampus dan tidak menghitung absensi secara otomatis.

Untuk MVP, sistem cukup digunakan pada ruang lingkup kecil, misalnya:

* satu dosen,
* beberapa kelas,
* beberapa mata kuliah,
* atau satu program studi.

---

## 5.4 Hal yang Tidak Boleh Dibangun agar Scope Tidak Melebar

* Jangan mengubah sistem menjadi LMS.
* Jangan mengubah sistem menjadi aplikasi presensi penuh.
* Jangan memasukkan fitur upload dokumen pada MVP.
* Jangan membuat mobile app native.
* Jangan menambahkan notifikasi WhatsApp sebelum MVP selesai.
* Jangan membuat approval bertingkat.
* Jangan membuat tanda tangan digital legal.
* Jangan menambahkan fitur pembayaran atau fitur di luar izin kelas.

---

# 6. User Flow Utama

## 6.1 Flow Mahasiswa Mengajukan Izin

1. Mahasiswa membuka aplikasi.
2. Mahasiswa login menggunakan email/NIM dan password.
3. Mahasiswa masuk ke dashboard.
4. Mahasiswa memilih menu **Ajukan Izin**.
5. Mahasiswa memilih jadwal kelas.
6. Mahasiswa memilih kategori izin.
7. Mahasiswa memilih tanggal izin.
8. Mahasiswa menulis alasan izin.
9. Mahasiswa menekan tombol **Kirim Pengajuan**.
10. Sistem memvalidasi input.
11. Sistem menyimpan pengajuan dengan status `Diajukan`.
12. Sistem membuat nomor izin dan token verifikasi.
13. Sistem mengirim email notifikasi ke dosen.
14. Mahasiswa diarahkan ke halaman riwayat izin.
15. Mahasiswa menunggu keputusan dosen.

---

## 6.2 Flow Dosen Memproses Izin

1. Dosen menerima email notifikasi izin baru.
2. Dosen membuka link detail pengajuan dari email.
3. Jika belum login, dosen diarahkan ke halaman login.
4. Dosen login.
5. Dosen membuka detail izin.
6. Dosen membaca data mahasiswa, jadwal, kategori, tanggal, dan alasan.
7. Dosen memilih **Setujui** atau **Tolak**.
8. Dosen dapat menambahkan catatan.
9. Sistem memperbarui status izin.
10. Sistem mencatat nama dosen dan waktu approval.
11. Sistem mengirim email hasil keputusan ke mahasiswa.
12. Data izin masuk ke riwayat approval dosen.

---

## 6.3 Flow Mahasiswa Mencetak Surat Izin

1. Mahasiswa menerima email bahwa izin disetujui.
2. Mahasiswa login ke sistem.
3. Mahasiswa membuka riwayat izin.
4. Mahasiswa memilih izin yang sudah disetujui.
5. Mahasiswa menekan tombol **Cetak Surat**.
6. Sistem menampilkan preview surat izin.
7. Surat izin menampilkan data izin, status approval, nama dosen, waktu approval, dan QR code.
8. Mahasiswa menekan tombol print.
9. Browser membuka dialog cetak.
10. Mahasiswa dapat mencetak atau menyimpan sebagai PDF.

---

## 6.4 Flow QR Verification

1. Dosen, asisten, admin, atau pihak lain memindai QR code pada surat izin.
2. QR code membuka halaman `/verify/{token}`.
3. Sistem mencari data izin berdasarkan token.
4. Jika token valid, sistem menampilkan status dokumen valid.
5. Jika token tidak ditemukan, sistem menampilkan dokumen tidak valid.
6. Halaman verifikasi hanya menampilkan data ringkas.

---

## 6.5 Flow Admin Mengelola Data

1. Admin login.
2. Admin masuk ke dashboard admin.
3. Admin mengelola user mahasiswa dan dosen.
4. Admin mengelola kategori izin.
5. Admin mengelola jadwal kelas.
6. Admin melihat log email jika ada masalah pengiriman notifikasi.

---

# 7. Fitur Utama

## 7.1 Login dan Logout

| Komponen      | Penjelasan                                                                    |
| ------------- | ----------------------------------------------------------------------------- |
| Tujuan        | Mengamankan akses sistem berdasarkan role pengguna.                           |
| Pengguna      | Mahasiswa, dosen, admin.                                                      |
| Input         | Email/NIM dan password.                                                       |
| Proses        | Sistem memvalidasi akun dan role.                                             |
| Output        | User masuk ke dashboard sesuai role.                                          |
| Validasi      | Email/NIM dan password wajib diisi.                                           |
| Error State   | Login gagal jika akun tidak ditemukan, password salah, atau akun tidak aktif. |
| Empty State   | Form kosong menampilkan pesan wajib isi.                                      |
| Success State | User berhasil login dan diarahkan ke dashboard.                               |

---

## 7.2 Dashboard Mahasiswa

| Komponen      | Penjelasan                                                     |
| ------------- | -------------------------------------------------------------- |
| Tujuan        | Menampilkan ringkasan izin milik mahasiswa.                    |
| Pengguna      | Mahasiswa.                                                     |
| Input         | Tidak ada input utama.                                         |
| Proses        | Sistem mengambil izin berdasarkan user login.                  |
| Output        | Total izin, izin diajukan, disetujui, ditolak, dan dibatalkan. |
| Validasi      | User harus login sebagai mahasiswa.                            |
| Error State   | Data gagal dimuat.                                             |
| Empty State   | Belum ada pengajuan izin.                                      |
| Success State | Dashboard tampil dengan statistik izin.                        |

---

## 7.3 Dashboard Dosen

| Komponen      | Penjelasan                                                            |
| ------------- | --------------------------------------------------------------------- |
| Tujuan        | Menampilkan pengajuan izin yang perlu diproses dosen.                 |
| Pengguna      | Dosen.                                                                |
| Input         | Filter status, tanggal, atau kelas.                                   |
| Proses        | Sistem mengambil daftar izin sesuai jadwal kelas yang dikelola dosen. |
| Output        | Total izin masuk, menunggu approval, disetujui, dan ditolak.          |
| Validasi      | User harus login sebagai dosen.                                       |
| Error State   | Data gagal dimuat.                                                    |
| Empty State   | Belum ada izin masuk.                                                 |
| Success State | Dashboard menampilkan pengajuan terbaru.                              |

---

## 7.4 Dashboard Admin

| Komponen      | Penjelasan                                                         |
| ------------- | ------------------------------------------------------------------ |
| Tujuan        | Menampilkan ringkasan seluruh aktivitas sistem.                    |
| Pengguna      | Admin.                                                             |
| Input         | Filter periode.                                                    |
| Proses        | Sistem mengambil data user, izin, jadwal, kategori, dan email log. |
| Output        | Statistik sistem dan daftar aktivitas terbaru.                     |
| Validasi      | User harus login sebagai admin.                                    |
| Error State   | Data gagal dimuat.                                                 |
| Empty State   | Belum ada data sistem.                                             |
| Success State | Dashboard admin tampil.                                            |

---

## 7.5 Pengajuan Izin

| Komponen      | Penjelasan                                                                     |
| ------------- | ------------------------------------------------------------------------------ |
| Tujuan        | Mahasiswa dapat mengajukan izin tidak masuk kelas.                             |
| Pengguna      | Mahasiswa.                                                                     |
| Input         | Jadwal kelas, kategori izin, tanggal izin, alasan izin.                        |
| Proses        | Sistem menyimpan pengajuan dengan status `Diajukan`.                           |
| Output        | Pengajuan masuk ke riwayat dan email terkirim ke dosen.                        |
| Validasi      | Jadwal, kategori, tanggal, dan alasan wajib diisi. Alasan minimal 10 karakter. |
| Error State   | Pengajuan gagal jika data tidak lengkap.                                       |
| Empty State   | Jika belum ada jadwal kelas, tampilkan pesan “Jadwal kelas belum tersedia”.    |
| Success State | Pengajuan berhasil dikirim.                                                    |

---

## 7.6 Approval Izin

| Komponen      | Penjelasan                                                             |
| ------------- | ---------------------------------------------------------------------- |
| Tujuan        | Dosen dapat memberi keputusan atas izin mahasiswa.                     |
| Pengguna      | Dosen.                                                                 |
| Input         | Keputusan dan catatan opsional.                                        |
| Proses        | Sistem mengubah status izin menjadi `Disetujui` atau `Ditolak`.        |
| Output        | Status izin diperbarui dan email hasil keputusan dikirim ke mahasiswa. |
| Validasi      | Hanya izin berstatus `Diajukan` yang bisa diproses.                    |
| Error State   | Approval gagal jika izin sudah diproses sebelumnya.                    |
| Empty State   | Tidak ada izin yang perlu diproses.                                    |
| Success State | Status izin berhasil diperbarui.                                       |

---

## 7.7 Email Notification

| Komponen      | Penjelasan                                                                           |
| ------------- | ------------------------------------------------------------------------------------ |
| Tujuan        | Memberikan pemberitahuan otomatis kepada dosen dan mahasiswa.                        |
| Pengguna      | Mahasiswa dan dosen.                                                                 |
| Input         | Event sistem seperti pengajuan baru, izin disetujui, dan izin ditolak.               |
| Proses        | Sistem membuat email berdasarkan template dan mengirimkannya melalui provider email. |
| Output        | Email terkirim dan dicatat pada email log.                                           |
| Validasi      | Email penerima harus valid.                                                          |
| Error State   | Jika email gagal, data izin tetap tersimpan dan kegagalan dicatat.                   |
| Empty State   | Jika email dosen belum diatur, sistem menampilkan peringatan kepada admin.           |
| Success State | Email berhasil dikirim dan tercatat.                                                 |

---

## 7.8 Surat Izin Cetak

| Komponen      | Penjelasan                                                |
| ------------- | --------------------------------------------------------- |
| Tujuan        | Mahasiswa dapat mencetak bukti izin yang sudah disetujui. |
| Pengguna      | Mahasiswa.                                                |
| Input         | Izin dengan status `Disetujui`.                           |
| Proses        | Sistem menampilkan surat izin dalam format print-ready.   |
| Output        | Surat izin dengan QR code.                                |
| Validasi      | Hanya izin berstatus `Disetujui` yang bisa dicetak.       |
| Error State   | Tombol cetak tidak tersedia jika izin belum disetujui.    |
| Empty State   | Tidak ada surat yang dapat dicetak.                       |
| Success State | Surat izin tampil dan siap dicetak.                       |

---

## 7.9 QR Verification

| Komponen      | Penjelasan                                                |
| ------------- | --------------------------------------------------------- |
| Tujuan        | Memvalidasi keaslian surat izin.                          |
| Pengguna      | Public verifier.                                          |
| Input         | Token dari QR code.                                       |
| Proses        | Sistem mencari data izin berdasarkan token.               |
| Output        | Halaman verifikasi menampilkan status valid atau invalid. |
| Validasi      | Token harus ada dan cocok dengan data izin.               |
| Error State   | Token tidak ditemukan atau dokumen tidak valid.           |
| Empty State   | Tidak berlaku.                                            |
| Success State | Dokumen valid ditampilkan.                                |

---

## 7.10 Manajemen Kategori Izin

| Komponen      | Penjelasan                                               |
| ------------- | -------------------------------------------------------- |
| Tujuan        | Admin mengelola kategori alasan izin.                    |
| Pengguna      | Admin.                                                   |
| Input         | Nama kategori dan deskripsi.                             |
| Proses        | Sistem menyimpan, mengubah, atau menonaktifkan kategori. |
| Output        | Kategori tersedia di form pengajuan izin.                |
| Validasi      | Nama kategori wajib dan tidak boleh duplikat.            |
| Error State   | Kategori tidak dapat dihapus jika sudah digunakan.       |
| Empty State   | Belum ada kategori.                                      |
| Success State | Kategori berhasil disimpan.                              |

---

## 7.11 Manajemen Jadwal Kelas

| Komponen      | Penjelasan                                                |
| ------------- | --------------------------------------------------------- |
| Tujuan        | Admin mengelola jadwal kelas yang bisa dipilih mahasiswa. |
| Pengguna      | Admin.                                                    |
| Input         | Mata kuliah, kelas, dosen, hari, jam, dan ruangan.        |
| Proses        | Sistem menyimpan jadwal kelas.                            |
| Output        | Jadwal muncul pada form pengajuan izin.                   |
| Validasi      | Mata kuliah, kelas, dosen, hari, dan jam wajib diisi.     |
| Error State   | Jadwal gagal disimpan jika data tidak valid.              |
| Empty State   | Belum ada jadwal kelas.                                   |
| Success State | Jadwal berhasil disimpan.                                 |

---

# 8. Functional Requirements

## 8.1 Umum

* Sistem harus bisa melakukan login dan logout.
* Sistem harus bisa membedakan role mahasiswa, dosen, dan admin.
* Sistem harus menampilkan dashboard sesuai role.
* Sistem harus melindungi halaman internal dari user yang belum login.
* Sistem harus mencegah user mengakses halaman yang bukan haknya.
* Sistem harus menampilkan pesan error yang jelas jika aksi gagal.
* Sistem harus menyimpan waktu pembuatan dan pembaruan data.

---

## 8.2 Mahasiswa

* Mahasiswa harus bisa membuat pengajuan izin.
* Mahasiswa harus bisa melihat riwayat izin miliknya sendiri.
* Mahasiswa harus bisa melihat detail izin.
* Mahasiswa harus bisa mengedit izin selama status masih `Diajukan`.
* Mahasiswa harus bisa membatalkan izin selama status masih `Diajukan`.
* Mahasiswa harus bisa menerima email ketika izin disetujui.
* Mahasiswa harus bisa menerima email ketika izin ditolak.
* Mahasiswa harus bisa mencetak surat izin jika status sudah `Disetujui`.
* Mahasiswa tidak boleh mencetak izin yang masih `Diajukan`, `Ditolak`, atau `Dibatalkan`.
* Mahasiswa tidak boleh melihat izin mahasiswa lain.
* Mahasiswa tidak boleh mengakses halaman approval dosen.

---

## 8.3 Dosen

* Dosen harus bisa menerima email ketika ada izin baru.
* Dosen harus bisa melihat daftar izin masuk.
* Dosen harus bisa melihat detail izin.
* Dosen harus bisa menyetujui izin.
* Dosen harus bisa menolak izin.
* Dosen harus bisa memberi catatan.
* Dosen harus bisa melihat riwayat izin yang sudah diproses.
* Dosen tidak perlu memberikan tanda tangan manual.
* Dosen tidak boleh mengubah alasan izin mahasiswa.
* Dosen tidak boleh memproses izin yang sudah disetujui, ditolak, atau dibatalkan.

---

## 8.4 Admin

* Admin harus bisa mengelola user.
* Admin harus bisa mengelola kategori izin.
* Admin harus bisa mengelola jadwal kelas.
* Admin harus bisa melihat seluruh data izin.
* Admin harus bisa melihat email log.
* Admin harus bisa mengaktifkan atau menonaktifkan user.
* Admin tidak boleh mengubah status izin tanpa kebutuhan khusus.
* Admin tidak boleh menghapus riwayat izin yang sudah diproses secara permanen.

---

## 8.5 Email Notification

* Sistem harus mengirim email ke dosen setelah mahasiswa membuat pengajuan izin.
* Sistem harus mengirim email ke mahasiswa setelah dosen menyetujui izin.
* Sistem harus mengirim email ke mahasiswa setelah dosen menolak izin.
* Sistem harus mencatat status pengiriman email.
* Sistem harus tetap menyimpan pengajuan izin meskipun email gagal terkirim.
* Sistem tidak boleh menampilkan API key email di frontend.
* Sistem tidak boleh menyimpan secret email langsung di kode.

---

## 8.6 Print dan QR Verification

* Sistem harus membuat nomor izin unik.
* Sistem harus membuat token verifikasi unik.
* Sistem harus membuat QR code untuk surat izin yang sudah disetujui.
* QR code harus mengarah ke halaman verifikasi.
* Halaman verifikasi harus bisa diakses tanpa login.
* Halaman verifikasi harus menampilkan data ringkas.
* Halaman verifikasi tidak boleh menampilkan alasan izin lengkap jika alasan tersebut bersifat sensitif.
* Surat izin harus memiliki layout yang rapi ketika dicetak.

---

# 9. Non-Functional Requirements

## 9.1 Performance

* Halaman dashboard harus dimuat kurang dari 3 detik pada koneksi normal untuk data MVP.
* Daftar izin harus menggunakan pagination jika data sudah banyak.
* Halaman print harus ringan dan tidak memuat script yang tidak diperlukan.
* Query database harus menggunakan filter dan index pada field penting seperti `status`, `user_id`, `lecturer_id`, dan `created_at`.

---

## 9.2 Security

* Password harus disimpan dalam bentuk hash.
* Role permission harus divalidasi di backend.
* Token QR harus sulit ditebak.
* Secret key, database password, dan email API key tidak boleh ditulis langsung di source code.
* Session harus memiliki masa berlaku.
* Halaman verifikasi publik hanya menampilkan data minimum.
* Input form harus divalidasi di backend.
* Aplikasi harus mencegah akses data antar user tanpa izin.

---

## 9.3 Usability

* Form izin harus singkat dan mudah dipahami.
* Status izin harus menggunakan badge warna.
* Tombol utama harus jelas.
* Email harus memiliki isi yang singkat dan informatif.
* Surat izin harus mudah dibaca ketika dicetak.
* Mahasiswa tidak perlu melewati banyak halaman untuk membuat izin.

---

## 9.4 Responsiveness

* Aplikasi harus nyaman digunakan di laptop dan smartphone.
* Pada desktop, data dapat ditampilkan dalam tabel.
* Pada mobile, daftar izin lebih baik ditampilkan sebagai card.
* Halaman print difokuskan untuk ukuran A4.

---

## 9.5 Reliability

* Data izin tidak boleh hilang ketika email gagal.
* Approval tidak boleh diproses dua kali.
* Sistem harus mencatat status email.
* Sistem harus menampilkan pesan yang jelas ketika terjadi error.
* Sistem harus dapat dijalankan secara lokal dan production.

---

## 9.6 Maintainability

* Struktur project Flask harus modular.
* Route dipisahkan berdasarkan fitur.
* Template HTML dipisahkan berdasarkan halaman.
* CSS menggunakan variabel warna.
* Fungsi email dipisahkan dari route utama.
* Query database dikelola melalui model/ORM.
* Nama file, route, fungsi, dan variabel harus mudah dipahami.

---

## 9.7 Scalability MVP

* Sistem cukup untuk skala kecil sampai menengah.
* Struktur database tetap memungkinkan penambahan banyak dosen dan banyak kelas.
* Email notification dapat dikembangkan ke background job setelah MVP stabil.
* Cloud Run dan Cloud SQL dapat ditingkatkan kapasitasnya jika penggunaan bertambah.

---

# 10. Role dan Permission

## 10.1 Mahasiswa

### Halaman yang Bisa Diakses

* Dashboard mahasiswa.
* Form pengajuan izin.
* Riwayat izin.
* Detail izin.
* Preview surat izin.
* Print surat izin.
* Profil pribadi.

### Aksi yang Boleh Dilakukan

* Membuat izin.
* Mengedit izin yang masih diajukan.
* Membatalkan izin yang masih diajukan.
* Melihat status izin.
* Mencetak izin yang sudah disetujui.

### Aksi yang Tidak Boleh Dilakukan

* Menyetujui izin.
* Menolak izin.
* Mengakses daftar semua izin.
* Mengelola kategori.
* Mengelola jadwal.
* Mengelola user.
* Melihat izin mahasiswa lain.

---

## 10.2 Dosen

### Halaman yang Bisa Diakses

* Dashboard dosen.
* Daftar pengajuan izin.
* Detail izin.
* Riwayat approval.
* Profil pribadi.

### Aksi yang Boleh Dilakukan

* Melihat izin yang ditujukan ke kelas/mata kuliahnya.
* Menyetujui izin.
* Menolak izin.
* Memberikan catatan.
* Melihat riwayat keputusan.

### Aksi yang Tidak Boleh Dilakukan

* Mengubah alasan izin mahasiswa.
* Mengubah data user.
* Mengelola semua jadwal sistem.
* Menghapus izin secara permanen.
* Melakukan approval ulang pada izin yang sudah diproses.

---

## 10.3 Admin

### Halaman yang Bisa Diakses

* Dashboard admin.
* Manajemen user.
* Manajemen kategori izin.
* Manajemen jadwal kelas.
* Seluruh data izin.
* Email log.
* Pengaturan sistem dasar.

### Aksi yang Boleh Dilakukan

* Menambah user.
* Mengedit user.
* Menonaktifkan user.
* Mengelola kategori.
* Mengelola jadwal.
* Melihat email log.
* Melihat seluruh data izin untuk keperluan monitoring.

### Aksi yang Tidak Boleh Dilakukan

* Mengubah alasan izin mahasiswa tanpa jejak.
* Menghapus permanen data izin yang sudah diproses.
* Mengakses password user dalam bentuk asli.

---

## 10.4 Public Verifier

### Halaman yang Bisa Diakses

* Halaman verifikasi QR.

### Aksi yang Boleh Dilakukan

* Melihat status validitas surat izin.

### Aksi yang Tidak Boleh Dilakukan

* Login sebagai user.
* Mengubah data.
* Melihat alasan izin lengkap.
* Melihat seluruh riwayat izin mahasiswa.

---

# 11. Data dan Database

## 11.1 Rekomendasi Database

Database utama menggunakan:

* **MySQL lokal** untuk development.
* **Cloud SQL MySQL** untuk production.

Alasan pemilihan:

* Cocok untuk aplikasi CRUD relasional.
* Struktur data mudah dipahami.
* Relasi antar user, jadwal, kategori, izin, dan email log jelas.
* Sesuai dengan Flask SQLAlchemy.
* Mudah dijelaskan dalam konteks akademik dan implementasi nyata.

---

## 11.2 Entitas Utama

1. `users`
2. `permission_categories`
3. `class_schedules`
4. `leave_requests`
5. `email_logs`
6. `audit_logs`

---

## 11.3 Tabel `users`

| Field          | Tipe     | Keterangan                  |
| -------------- | -------- | --------------------------- |
| id             | integer  | Primary key                 |
| name           | varchar  | Nama pengguna               |
| email          | varchar  | Email login dan notifikasi  |
| password_hash  | varchar  | Password yang sudah di-hash |
| role           | enum     | mahasiswa/dosen/admin       |
| student_number | varchar  | NIM mahasiswa               |
| lecturer_code  | varchar  | Kode dosen, opsional        |
| phone          | varchar  | Nomor HP, opsional          |
| is_active      | boolean  | Status akun                 |
| created_at     | datetime | Waktu dibuat                |
| updated_at     | datetime | Waktu diperbarui            |

### Validasi

* Email wajib unik.
* Password minimal 6 karakter.
* Role wajib berisi `mahasiswa`, `dosen`, atau `admin`.
* Student number wajib untuk mahasiswa.
* Lecturer code opsional untuk dosen.

---

## 11.4 Tabel `permission_categories`

| Field       | Tipe     | Keterangan            |
| ----------- | -------- | --------------------- |
| id          | integer  | Primary key           |
| name        | varchar  | Nama kategori izin    |
| description | text     | Deskripsi kategori    |
| is_active   | boolean  | Status aktif kategori |
| created_at  | datetime | Waktu dibuat          |
| updated_at  | datetime | Waktu diperbarui      |

### Contoh Kategori

* Sakit.
* Kegiatan kampus.
* Urusan keluarga.
* Keperluan mendesak.
* Lainnya.

### Validasi

* Nama kategori wajib diisi.
* Nama kategori tidak boleh duplikat.
* Kategori yang sudah digunakan tidak dihapus permanen, cukup dinonaktifkan.

---

## 11.5 Tabel `class_schedules`

| Field       | Tipe     | Keterangan                 |
| ----------- | -------- | -------------------------- |
| id          | integer  | Primary key                |
| course_name | varchar  | Nama mata kuliah           |
| class_name  | varchar  | Nama kelas                 |
| lecturer_id | integer  | Relasi ke users role dosen |
| day         | varchar  | Hari kuliah                |
| start_time  | time     | Jam mulai                  |
| end_time    | time     | Jam selesai                |
| room        | varchar  | Ruangan                    |
| is_active   | boolean  | Status jadwal              |
| created_at  | datetime | Waktu dibuat               |
| updated_at  | datetime | Waktu diperbarui           |

### Validasi

* Nama mata kuliah wajib diisi.
* Nama kelas wajib diisi.
* Lecturer ID wajib diisi.
* Hari wajib diisi.
* Jam mulai dan selesai wajib diisi.
* Jam selesai harus lebih besar dari jam mulai.

---

## 11.6 Tabel `leave_requests`

| Field              | Tipe     | Keterangan                            |
| ------------------ | -------- | ------------------------------------- |
| id                 | integer  | Primary key                           |
| request_number     | varchar  | Nomor izin unik                       |
| user_id            | integer  | Relasi ke users role mahasiswa        |
| schedule_id        | integer  | Relasi ke class_schedules             |
| category_id        | integer  | Relasi ke permission_categories       |
| permission_date    | date     | Tanggal izin                          |
| reason             | text     | Alasan izin                           |
| status             | enum     | diajukan/disetujui/ditolak/dibatalkan |
| admin_note         | text     | Catatan dosen                         |
| reviewed_by        | integer  | ID dosen yang memproses               |
| reviewed_at        | datetime | Waktu approval                        |
| verification_token | varchar  | Token QR unik                         |
| email_notified_at  | datetime | Waktu email awal dikirim              |
| created_at         | datetime | Waktu dibuat                          |
| updated_at         | datetime | Waktu diperbarui                      |

### Status Izin

* `diajukan`
* `disetujui`
* `ditolak`
* `dibatalkan`

### Validasi

* Satu izin wajib memiliki mahasiswa.
* Satu izin wajib memiliki jadwal.
* Satu izin wajib memiliki kategori.
* Alasan minimal 10 karakter.
* Status awal selalu `diajukan`.
* Verification token harus unik.

---

## 11.7 Tabel `email_logs`

| Field            | Tipe     | Keterangan               |
| ---------------- | -------- | ------------------------ |
| id               | integer  | Primary key              |
| leave_request_id | integer  | Relasi ke leave_requests |
| recipient_email  | varchar  | Email penerima           |
| subject          | varchar  | Subject email            |
| template_name    | varchar  | Jenis template email     |
| status           | enum     | pending/sent/failed      |
| error_message    | text     | Pesan error jika gagal   |
| sent_at          | datetime | Waktu email terkirim     |
| created_at       | datetime | Waktu dibuat             |

### Template Email

* `new_leave_request_to_lecturer`
* `approval_result_to_student`
* `rejection_result_to_student`
* `cancellation_notice_to_lecturer`

### Aturan Penting

Jika email gagal terkirim, pengajuan izin tidak boleh dibatalkan otomatis. Sistem cukup mencatat status `failed` agar admin dapat mengecek.

---

## 11.8 Tabel `audit_logs`

| Field       | Tipe     | Keterangan               |
| ----------- | -------- | ------------------------ |
| id          | integer  | Primary key              |
| user_id     | integer  | User yang melakukan aksi |
| action      | varchar  | Nama aksi                |
| entity_type | varchar  | Jenis data               |
| entity_id   | integer  | ID data                  |
| description | text     | Keterangan aksi          |
| created_at  | datetime | Waktu aksi               |

### Contoh Audit

* Mahasiswa membuat izin.
* Dosen menyetujui izin.
* Dosen menolak izin.
* Mahasiswa mencetak surat.
* Admin mengubah jadwal.

---

## 11.9 Relasi Data

* Satu mahasiswa dapat memiliki banyak pengajuan izin.
* Satu dosen dapat memiliki banyak jadwal kelas.
* Satu jadwal kelas dapat memiliki banyak pengajuan izin.
* Satu kategori dapat digunakan oleh banyak pengajuan izin.
* Satu izin dapat memiliki banyak email log.
* Satu user dapat memiliki banyak audit log.

---

## 11.10 Data Sensitif

Data yang perlu dijaga:

* Password user.
* NIM mahasiswa.
* Alasan izin.
* Catatan dosen.
* Riwayat izin.
* Email pengguna.
* API key email provider.
* Secret key aplikasi.
* Database password.

---

## 11.11 Data yang Ditampilkan di Halaman QR Verification

Halaman verifikasi publik hanya menampilkan:

* Nomor izin.
* Nama mahasiswa.
* NIM, dapat disamarkan sebagian jika diperlukan.
* Mata kuliah.
* Kelas.
* Tanggal izin.
* Status izin.
* Nama dosen yang menyetujui.
* Waktu approval.
* Status validitas dokumen.

Halaman verifikasi publik tidak menampilkan:

* Password.
* Email pribadi.
* Alasan izin lengkap.
* Catatan dosen yang sensitif.
* Riwayat izin lainnya.

---

# 12. UI/UX Requirements

## 12.1 Karakter Desain

Desain harus modern, bersih, akademik, dan mudah digunakan. Karena warna utama adalah merah, warna merah digunakan sebagai aksen utama, bukan sebagai warna dominan penuh agar tampilan tidak terasa berat.

---

## 12.2 Color Palette

Gunakan warna utama merah dengan kombinasi putih, abu muda, dan teks gelap.

```css
:root {
  --primary-red: #C62828;
  --deep-red: #8E1B1B;
  --soft-red: #FDECEC;
  --accent-red: #EF5350;

  --background: #F9FAFB;
  --surface: #FFFFFF;
  --dark-text: #1F2937;
  --muted-text: #6B7280;
  --border-color: #E5E7EB;

  --success: #2E7D32;
  --warning: #F59E0B;
  --danger: #DC2626;
  --info: #2563EB;
}
```

---

## 12.3 Penggunaan Warna

* Merah utama untuk tombol utama, sidebar active, heading accent, dan link penting.
* Merah lembut untuk background card informatif.
* Hijau untuk status `Disetujui`.
* Kuning/oranye untuk status `Diajukan`.
* Merah danger untuk status `Ditolak`.
* Abu muda untuk background halaman.
* Putih untuk card dan form.

---

## 12.4 Gaya Visual

* Clean dashboard.
* Card-based layout.
* Badge status.
* Tabel sederhana.
* Form ringkas.
* Modal konfirmasi.
* Toast notification.
* Print layout A4.
* QR code tampil jelas pada surat.

---

## 12.5 Layout Desktop

* Sidebar kiri.
* Header atas.
* Konten utama.
* Card statistik di bagian atas.
* Tabel data di bagian bawah.
* Tombol aksi utama di kanan atas halaman.

---

## 12.6 Layout Mobile

* Sidebar berubah menjadi menu collapsible.
* Tabel berubah menjadi card list.
* Tombol aksi utama dibuat lebar dan mudah ditekan.
* Form tetap satu kolom.
* Badge status tetap terlihat jelas.

---

## 12.7 Loading State

* Tombol submit menampilkan teks `Mengirim...`.
* Halaman data menampilkan skeleton atau teks `Memuat data...`.
* Saat email sedang dikirim, user tetap mendapat feedback bahwa data sudah disimpan.

---

## 12.8 Empty State

Contoh empty state:

* `Belum ada pengajuan izin.`
* `Belum ada izin yang perlu diproses.`
* `Belum ada jadwal kelas.`
* `Belum ada kategori izin.`
* `Belum ada log email.`

---

## 12.9 Success State

Contoh success state:

* `Pengajuan izin berhasil dikirim.`
* `Izin berhasil disetujui.`
* `Izin berhasil ditolak.`
* `Surat izin siap dicetak.`
* `Kategori berhasil ditambahkan.`

---

## 12.10 Error State

Contoh error state:

* `Alasan izin wajib diisi.`
* `Tanggal izin tidak valid.`
* `Izin sudah diproses.`
* `Email notifikasi gagal dikirim, tetapi data izin berhasil disimpan.`
* `Anda tidak memiliki akses ke halaman ini.`

---

# 13. Technical Requirements

## 13.1 Stack Final

### Frontend

* HTML
* CSS
* JavaScript vanilla
* Jinja2 template

### Backend

* Python Flask

### Database

* MySQL lokal untuk development.
* Cloud SQL MySQL untuk production.

### ORM

* Flask-SQLAlchemy

### Migration

* Flask-Migrate / Alembic

### Authentication

* Flask-Login
* Werkzeug password hashing

### Email

* SMTP/API provider pihak ketiga.
* Rekomendasi: Brevo atau SendGrid.
* Email log disimpan di database.

### QR Code

* Python package `qrcode`

### Print

* CSS print media.
* Browser print.
* Tidak perlu generate PDF server-side pada MVP.

### Deployment

* Google Cloud Run.
* Cloud SQL MySQL.
* Secret Manager.
* Cloud Logging.

---

## 13.2 Struktur Project Flask

```text
kelaskita/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── utils/
│   │   ├── decorators.py
│   │   ├── helpers.py
│   │   └── validators.py
│   ├── auth/
│   │   ├── routes.py
│   │   └── services.py
│   ├── dashboard/
│   │   └── routes.py
│   ├── leave_requests/
│   │   ├── routes.py
│   │   ├── services.py
│   │   └── qr_service.py
│   ├── notifications/
│   │   ├── email_service.py
│   │   └── templates.py
│   ├── categories/
│   │   └── routes.py
│   ├── schedules/
│   │   └── routes.py
│   ├── users/
│   │   └── routes.py
│   ├── verification/
│   │   └── routes.py
│   ├── templates/
│   │   ├── layout.html
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── leave_requests/
│   │   ├── categories/
│   │   ├── schedules/
│   │   ├── users/
│   │   └── verification/
│   └── static/
│       ├── css/
│       │   ├── main.css
│       │   └── print.css
│       ├── js/
│       │   └── main.js
│       └── img/
├── migrations/
├── requirements.txt
├── Dockerfile
├── .env.example
├── run.py
└── README.md
```

---

## 13.3 Environment Variable

```env
FLASK_ENV=production
SECRET_KEY=[PERLU_DIISI]
APP_URL=https://[PERLU_DIISI]

DATABASE_URL=mysql+pymysql://[USER]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
CLOUD_SQL_CONNECTION_NAME=[PERLU_DIISI]

MAIL_PROVIDER=[PERLU_DIISI]
MAIL_FROM_NAME=KelasKita
MAIL_FROM_EMAIL=[PERLU_DIISI]
SMTP_HOST=[PERLU_DIISI]
SMTP_PORT=587
SMTP_USERNAME=[PERLU_DIISI]
SMTP_PASSWORD=[PERLU_DIISI]
SMTP_USE_TLS=true
```

Untuk development lokal:

```env
FLASK_ENV=development
SECRET_KEY=local-development-secret
APP_URL=http://localhost:5000

DATABASE_URL=mysql+pymysql://root:password@localhost:3306/kelaskita

MAIL_PROVIDER=smtp
MAIL_FROM_NAME=KelasKita Dev
MAIL_FROM_EMAIL=[PERLU_DIISI]
SMTP_HOST=[PERLU_DIISI]
SMTP_PORT=587
SMTP_USERNAME=[PERLU_DIISI]
SMTP_PASSWORD=[PERLU_DIISI]
SMTP_USE_TLS=true
```

---

## 13.4 Email Sending Strategy

Pada MVP, email dikirim langsung setelah aksi utama berhasil.

Alur pengiriman email:

1. Mahasiswa mengirim izin.
2. Sistem menyimpan data izin.
3. Sistem mencoba mengirim email ke dosen.
4. Jika email berhasil, status email log menjadi `sent`.
5. Jika email gagal, status email log menjadi `failed`.
6. Pengajuan izin tetap dianggap berhasil.

Catatan:

Untuk MVP, belum perlu background queue. Jika sistem berkembang, email dapat dipindahkan ke task queue agar lebih stabil.

---

## 13.5 QR Strategy

QR code berisi URL seperti:

```text
https://domain-kelaskita/verify/{verification_token}
```

Token tidak boleh berupa ID angka biasa. Token harus berupa string acak yang panjang, misalnya UUID atau random secure token.

---

## 13.6 Print Strategy

Surat izin menggunakan halaman HTML khusus dengan CSS print.

Ukuran print:

* A4 portrait.
* Margin rapi.
* QR code di bagian bawah atau kanan bawah.
* Tombol print tidak muncul ketika dicetak.

---

# 14. Halaman yang Dibutuhkan

## 14.1 Login Page

| Bagian   | Penjelasan                                           |
| -------- | ---------------------------------------------------- |
| Fungsi   | User masuk ke sistem.                                |
| Komponen | Form email/NIM, password, tombol login, pesan error. |
| Aksi     | Login.                                               |

---

## 14.2 Dashboard Mahasiswa

| Bagian   | Penjelasan                                                         |
| -------- | ------------------------------------------------------------------ |
| Fungsi   | Ringkasan izin mahasiswa.                                          |
| Komponen | Card total izin, diajukan, disetujui, ditolak, tombol ajukan izin. |
| Aksi     | Melihat ringkasan dan membuka form izin.                           |

---

## 14.3 Form Pengajuan Izin

| Bagian   | Penjelasan                                                                         |
| -------- | ---------------------------------------------------------------------------------- |
| Fungsi   | Mahasiswa membuat izin baru.                                                       |
| Komponen | Dropdown jadwal, dropdown kategori, input tanggal, textarea alasan, tombol submit. |
| Aksi     | Mengirim pengajuan izin.                                                           |

---

## 14.4 Riwayat Izin Mahasiswa

| Bagian   | Penjelasan                                                                          |
| -------- | ----------------------------------------------------------------------------------- |
| Fungsi   | Menampilkan daftar izin milik mahasiswa.                                            |
| Komponen | List izin, badge status, filter status, tombol detail, tombol cetak jika disetujui. |
| Aksi     | Melihat detail, edit, batal, cetak.                                                 |

---

## 14.5 Detail Izin Mahasiswa

| Bagian   | Penjelasan                                                            |
| -------- | --------------------------------------------------------------------- |
| Fungsi   | Menampilkan detail izin mahasiswa.                                    |
| Komponen | Data izin, status, catatan dosen, waktu approval.                     |
| Aksi     | Melihat status, edit/batal jika masih diajukan, cetak jika disetujui. |

---

## 14.6 Dashboard Dosen

| Bagian   | Penjelasan                                              |
| -------- | ------------------------------------------------------- |
| Fungsi   | Ringkasan izin untuk dosen.                             |
| Komponen | Card izin masuk, menunggu approval, disetujui, ditolak. |
| Aksi     | Membuka daftar izin.                                    |

---

## 14.7 Daftar Pengajuan Dosen

| Bagian   | Penjelasan                                                     |
| -------- | -------------------------------------------------------------- |
| Fungsi   | Menampilkan pengajuan izin yang perlu diproses.                |
| Komponen | Tabel/list izin, filter status, filter tanggal, tombol detail. |
| Aksi     | Membuka detail izin.                                           |

---

## 14.8 Detail Approval Dosen

| Bagian   | Penjelasan                                                                          |
| -------- | ----------------------------------------------------------------------------------- |
| Fungsi   | Dosen memproses izin.                                                               |
| Komponen | Detail mahasiswa, detail kelas, alasan izin, catatan, tombol setujui, tombol tolak. |
| Aksi     | Approve atau reject.                                                                |

---

## 14.9 Preview Surat Izin

| Bagian   | Penjelasan                                                                                         |
| -------- | -------------------------------------------------------------------------------------------------- |
| Fungsi   | Menampilkan surat izin sebelum dicetak.                                                            |
| Komponen | Kop surat sederhana, nomor izin, data mahasiswa, data kelas, status approval, nama dosen, QR code. |
| Aksi     | Print.                                                                                             |

---

## 14.10 Halaman QR Verification

| Bagian   | Penjelasan                                                                        |
| -------- | --------------------------------------------------------------------------------- |
| Fungsi   | Memvalidasi dokumen dari QR.                                                      |
| Komponen | Status valid/invalid, nomor izin, nama mahasiswa, mata kuliah, tanggal, approver. |
| Aksi     | Tidak ada aksi edit.                                                              |

---

## 14.11 Dashboard Admin

| Bagian   | Penjelasan                                         |
| -------- | -------------------------------------------------- |
| Fungsi   | Monitoring seluruh sistem.                         |
| Komponen | Statistik user, izin, jadwal, kategori, email log. |
| Aksi     | Membuka manajemen data.                            |

---

## 14.12 Manajemen User

| Bagian   | Penjelasan                                  |
| -------- | ------------------------------------------- |
| Fungsi   | Admin mengelola akun.                       |
| Komponen | Tabel user, form tambah/edit, status aktif. |
| Aksi     | Tambah, edit, aktif/nonaktif user.          |

---

## 14.13 Manajemen Kategori

| Bagian   | Penjelasan                                            |
| -------- | ----------------------------------------------------- |
| Fungsi   | Admin mengelola kategori izin.                        |
| Komponen | Tabel kategori, form tambah/edit, tombol nonaktifkan. |
| Aksi     | CRUD kategori.                                        |

---

## 14.14 Manajemen Jadwal

| Bagian   | Penjelasan                                     |
| -------- | ---------------------------------------------- |
| Fungsi   | Admin mengelola jadwal kelas.                  |
| Komponen | Tabel jadwal, form tambah/edit, pilihan dosen. |
| Aksi     | CRUD jadwal.                                   |

---

## 14.15 Email Log

| Bagian   | Penjelasan                                          |
| -------- | --------------------------------------------------- |
| Fungsi   | Admin melihat status pengiriman email.              |
| Komponen | Tabel email log, status sent/failed, error message. |
| Aksi     | Melihat detail log.                                 |

---

# 15. API / Backend Requirements

Karena aplikasi menggunakan Flask dengan HTML, CSS, JS, dan Jinja2, route utama menggunakan server-rendered web routes. JSON API hanya digunakan jika diperlukan untuk interaksi JavaScript ringan.

---

## 15.1 Auth Routes

| Method | Route     | Tujuan                    |
| ------ | --------- | ------------------------- |
| GET    | `/login`  | Menampilkan halaman login |
| POST   | `/login`  | Memproses login           |
| POST   | `/logout` | Logout                    |

---

## 15.2 Student Routes

| Method | Route                                 | Tujuan                |
| ------ | ------------------------------------- | --------------------- |
| GET    | `/student/dashboard`                  | Dashboard mahasiswa   |
| GET    | `/student/leave-requests`             | Riwayat izin          |
| GET    | `/student/leave-requests/create`      | Form pengajuan izin   |
| POST   | `/student/leave-requests`             | Simpan pengajuan izin |
| GET    | `/student/leave-requests/{id}`        | Detail izin           |
| GET    | `/student/leave-requests/{id}/edit`   | Form edit izin        |
| POST   | `/student/leave-requests/{id}/update` | Update izin           |
| POST   | `/student/leave-requests/{id}/cancel` | Batalkan izin         |
| GET    | `/student/leave-requests/{id}/print`  | Preview surat izin    |

---

## 15.3 Lecturer Routes

| Method | Route                                   | Tujuan            |
| ------ | --------------------------------------- | ----------------- |
| GET    | `/lecturer/dashboard`                   | Dashboard dosen   |
| GET    | `/lecturer/leave-requests`              | Daftar izin masuk |
| GET    | `/lecturer/leave-requests/{id}`         | Detail izin       |
| POST   | `/lecturer/leave-requests/{id}/approve` | Setujui izin      |
| POST   | `/lecturer/leave-requests/{id}/reject`  | Tolak izin        |

---

## 15.4 Admin Routes

| Method | Route                                  | Tujuan                  |
| ------ | -------------------------------------- | ----------------------- |
| GET    | `/admin/dashboard`                     | Dashboard admin         |
| GET    | `/admin/users`                         | Daftar user             |
| POST   | `/admin/users`                         | Tambah user             |
| POST   | `/admin/users/{id}/update`             | Update user             |
| POST   | `/admin/users/{id}/toggle-active`      | Aktif/nonaktif user     |
| GET    | `/admin/categories`                    | Daftar kategori         |
| POST   | `/admin/categories`                    | Tambah kategori         |
| POST   | `/admin/categories/{id}/update`        | Update kategori         |
| POST   | `/admin/categories/{id}/toggle-active` | Aktif/nonaktif kategori |
| GET    | `/admin/schedules`                     | Daftar jadwal           |
| POST   | `/admin/schedules`                     | Tambah jadwal           |
| POST   | `/admin/schedules/{id}/update`         | Update jadwal           |
| POST   | `/admin/schedules/{id}/toggle-active`  | Aktif/nonaktif jadwal   |
| GET    | `/admin/email-logs`                    | Daftar email log        |

---

## 15.5 Public Verification Route

| Method | Route             | Tujuan                        |
| ------ | ----------------- | ----------------------------- |
| GET    | `/verify/{token}` | Verifikasi surat izin dari QR |

---

## 15.6 Request dan Response Penting

### Create Leave Request

**POST** `/student/leave-requests`

Request form:

```json
{
  "schedule_id": 1,
  "category_id": 2,
  "permission_date": "2026-06-12",
  "reason": "Saya tidak dapat mengikuti kelas karena sakit."
}
```

Success:

```json
{
  "message": "Pengajuan izin berhasil dikirim",
  "status": "diajukan"
}
```

Error:

```json
{
  "message": "Jadwal, kategori, tanggal, dan alasan wajib diisi"
}
```

---

### Approve Leave Request

**POST** `/lecturer/leave-requests/{id}/approve`

Request:

```json
{
  "admin_note": "Izin disetujui."
}
```

Success:

```json
{
  "message": "Izin berhasil disetujui",
  "status": "disetujui"
}
```

Error:

```json
{
  "message": "Izin tidak dapat diproses karena status sudah berubah"
}
```

---

### Reject Leave Request

**POST** `/lecturer/leave-requests/{id}/reject`

Request:

```json
{
  "admin_note": "Alasan izin belum cukup jelas."
}
```

Success:

```json
{
  "message": "Izin berhasil ditolak",
  "status": "ditolak"
}
```

Error:

```json
{
  "message": "Izin tidak dapat diproses"
}
```

---

### QR Verification

**GET** `/verify/{token}`

Valid response display:

```json
{
  "document_status": "valid",
  "request_number": "IZN-20260612-0001",
  "student_name": "Nama Mahasiswa",
  "course_name": "Pemrograman Web",
  "class_name": "IT-06-02",
  "permission_date": "2026-06-12",
  "approval_status": "disetujui",
  "approved_by": "Nama Dosen",
  "approved_at": "2026-06-12 10:30"
}
```

Invalid response display:

```json
{
  "document_status": "invalid",
  "message": "Dokumen tidak ditemukan atau token tidak valid"
}
```

---

# 16. Acceptance Criteria

Project dianggap berhasil jika:

* [ ] Mahasiswa, dosen, dan admin dapat login.
* [ ] Sistem menampilkan dashboard sesuai role.
* [ ] Mahasiswa dapat membuat pengajuan izin.
* [ ] Mahasiswa dapat melihat riwayat izinnya sendiri.
* [ ] Mahasiswa dapat mengedit izin selama status masih `Diajukan`.
* [ ] Mahasiswa dapat membatalkan izin selama status masih `Diajukan`.
* [ ] Dosen menerima email ketika ada izin baru.
* [ ] Dosen dapat membuka detail izin dari sistem.
* [ ] Dosen dapat menyetujui izin.
* [ ] Dosen dapat menolak izin.
* [ ] Sistem mencatat nama dosen yang memproses izin.
* [ ] Sistem mencatat waktu approval.
* [ ] Mahasiswa menerima email ketika izin disetujui.
* [ ] Mahasiswa menerima email ketika izin ditolak.
* [ ] Mahasiswa dapat mencetak surat izin jika status disetujui.
* [ ] Mahasiswa tidak dapat mencetak surat izin jika status belum disetujui.
* [ ] Surat izin menampilkan QR code.
* [ ] QR code membuka halaman verifikasi.
* [ ] Halaman verifikasi menampilkan dokumen valid jika token benar.
* [ ] Halaman verifikasi menampilkan invalid jika token salah.
* [ ] Admin dapat mengelola user.
* [ ] Admin dapat mengelola kategori izin.
* [ ] Admin dapat mengelola jadwal kelas.
* [ ] Admin dapat melihat email log.
* [ ] Sistem tetap menyimpan izin meskipun email gagal terkirim.
* [ ] Data tersimpan di database dengan benar.
* [ ] Aplikasi dapat dijalankan lokal.
* [ ] Aplikasi dapat dideploy ke GCP.

---

# 17. Edge Cases dan Error Handling

## 17.1 Data Kosong

Jika belum ada izin, sistem menampilkan empty state, bukan tabel kosong tanpa penjelasan.

## 17.2 Input Tidak Lengkap

Jika jadwal, kategori, tanggal, atau alasan kosong, sistem menampilkan pesan validasi.

## 17.3 Alasan Terlalu Pendek

Jika alasan kurang dari 10 karakter, sistem menampilkan pesan:

> Alasan izin terlalu singkat.

## 17.4 Jadwal Tidak Aktif

Jika jadwal sudah dinonaktifkan, mahasiswa tidak dapat memilih jadwal tersebut.

## 17.5 Kategori Tidak Aktif

Jika kategori sudah dinonaktifkan, mahasiswa tidak dapat memilih kategori tersebut.

## 17.6 User Tidak Punya Akses

Jika mahasiswa membuka URL dosen/admin, sistem menampilkan 403 atau mengarahkan ke dashboard mahasiswa.

## 17.7 Izin Sudah Diproses

Jika izin sudah disetujui atau ditolak, mahasiswa tidak dapat mengedit atau membatalkan izin.

## 17.8 Approval Ganda

Jika dosen mencoba approval ulang, sistem menolak dengan pesan:

> Izin sudah diproses.

## 17.9 Email Gagal Terkirim

Jika email gagal, sistem tetap menyimpan data izin dan mencatat status `failed` pada email log.

## 17.10 Email Dosen Kosong

Jika jadwal tidak memiliki dosen dengan email valid, sistem menampilkan peringatan kepada admin.

## 17.11 Token QR Tidak Valid

Jika token tidak ditemukan, halaman verifikasi menampilkan pesan dokumen tidak valid.

## 17.12 Surat Belum Bisa Dicetak

Jika izin belum disetujui, tombol cetak tidak ditampilkan.

## 17.13 Session Expired

Jika sesi berakhir, user diarahkan kembali ke login.

## 17.14 Database Error

Jika database gagal, sistem menampilkan pesan umum dan tidak membocorkan detail teknis.

## 17.15 Server Error

Jika terjadi error internal, sistem menampilkan halaman error yang ramah dan mencatat error di log.

---

# 18. Risiko dan Mitigasi

## 18.1 Risiko Scope Melebar

**Risiko:** Project berkembang menjadi sistem akademik penuh.
**Mitigasi:** Scope dikunci pada izin kelas, approval, email, surat cetak, dan QR verification.

## 18.2 Risiko Email Tidak Masuk

**Risiko:** Email masuk spam atau gagal terkirim.
**Mitigasi:** Gunakan provider email transactional, siapkan sender email yang jelas, dan simpan email log.

## 18.3 Risiko QR Mudah Dipalsukan

**Risiko:** QR hanya berisi ID yang mudah ditebak.
**Mitigasi:** Gunakan token acak yang panjang dan unik.

## 18.4 Risiko Data Pribadi Terbuka

**Risiko:** Halaman verifikasi publik menampilkan terlalu banyak data.
**Mitigasi:** Tampilkan hanya data ringkas dan sembunyikan alasan izin lengkap.

## 18.5 Risiko Role Permission Lemah

**Risiko:** Mahasiswa dapat mengakses halaman dosen/admin.
**Mitigasi:** Gunakan validasi role di backend pada setiap route penting.

## 18.6 Risiko Deployment GCP

**Risiko:** Salah konfigurasi Cloud SQL, environment variable, atau secret.
**Mitigasi:** Gunakan `.env.example`, Secret Manager, dan dokumentasi deployment yang jelas.

## 18.7 Risiko Biaya GCP

**Risiko:** Trial cepat habis jika resource terlalu besar.
**Mitigasi:** Gunakan resource kecil, pantau billing, dan matikan resource yang tidak digunakan.

## 18.8 Risiko UI Terlalu Berat

**Risiko:** Warna merah terlalu dominan dan tampilan terasa agresif.
**Mitigasi:** Gunakan merah sebagai aksen utama dan kombinasikan dengan putih/abu muda.

## 18.9 Risiko Dosen Tidak Mau Login Terlalu Sering

**Risiko:** Dosen merasa proses approval tetap merepotkan.
**Mitigasi:** Email berisi ringkasan dan link langsung ke detail izin agar proses cepat.

---

# 19. Roadmap Implementasi

## Tahap 1: Fondasi Project

* Setup Flask.
* Setup struktur folder.
* Setup template layout.
* Setup CSS global dengan tema merah.
* Setup JavaScript dasar.
* Setup database lokal.
* Setup SQLAlchemy dan migration.

## Tahap 2: Auth dan Role

* Membuat model user.
* Membuat login dan logout.
* Membuat password hashing.
* Membuat role mahasiswa, dosen, admin.
* Membuat route protection.
* Membuat seed user awal.

## Tahap 3: Master Data

* Membuat CRUD user.
* Membuat CRUD kategori izin.
* Membuat CRUD jadwal kelas.
* Menghubungkan jadwal dengan dosen.
* Membuat validasi data master.

## Tahap 4: Pengajuan Izin

* Membuat form pengajuan izin.
* Membuat nomor izin otomatis.
* Membuat token verifikasi.
* Menyimpan pengajuan.
* Membuat riwayat izin mahasiswa.
* Membuat detail izin mahasiswa.
* Membuat edit dan cancel izin.

## Tahap 5: Approval Dosen

* Membuat dashboard dosen.
* Membuat daftar izin masuk.
* Membuat detail approval.
* Membuat approve.
* Membuat reject.
* Menyimpan catatan dosen.
* Menyimpan `reviewed_by` dan `reviewed_at`.

## Tahap 6: Email Notification

* Setup provider email.
* Membuat email service.
* Membuat template email izin baru.
* Membuat template email izin disetujui.
* Membuat template email izin ditolak.
* Membuat email log.
* Menangani kondisi email gagal.

## Tahap 7: Surat Cetak dan QR Verification

* Generate QR code.
* Membuat halaman preview surat.
* Membuat CSS print A4.
* Membuat halaman verifikasi publik.
* Membatasi data yang tampil di halaman publik.
* Menguji QR scan dari HP.

## Tahap 8: UI Polishing

* Merapikan dashboard.
* Membuat badge status.
* Membuat empty state.
* Membuat toast notification.
* Membuat modal konfirmasi.
* Membuat responsive mobile.
* Merapikan warna merah agar tetap profesional.

## Tahap 9: Testing

* Test login semua role.
* Test permission semua role.
* Test CRUD user.
* Test CRUD kategori.
* Test CRUD jadwal.
* Test pengajuan izin.
* Test approval.
* Test email notification.
* Test email gagal.
* Test print surat.
* Test QR valid.
* Test QR invalid.
* Test responsive mobile.

## Tahap 10: Deployment GCP

* Membuat project GCP.
* Membuat Cloud SQL MySQL.
* Membuat database production.
* Menyiapkan Secret Manager.
* Menyiapkan environment variable.
* Membuat Dockerfile.
* Deploy Flask ke Cloud Run.
* Menghubungkan Cloud Run ke Cloud SQL.
* Menguji email di production.
* Menguji QR dengan domain production.
* Monitoring log dasar.

---

# 20. Checklist Final

## Product

* [ ] Nama project sudah jelas.
* [ ] Masalah utama sudah jelas.
* [ ] Target user sudah jelas.
* [ ] Scope MVP sudah terkunci.
* [ ] Project tidak melebar menjadi sistem akademik penuh.
* [ ] Fitur email masuk ke scope real-use.
* [ ] Fitur print dan QR masuk ke scope final.

## Flow

* [ ] Flow mahasiswa jelas.
* [ ] Flow dosen jelas.
* [ ] Flow admin jelas.
* [ ] Flow email jelas.
* [ ] Flow approval jelas.
* [ ] Flow print jelas.
* [ ] Flow QR verification jelas.

## Database

* [ ] Tabel users jelas.
* [ ] Tabel permission_categories jelas.
* [ ] Tabel class_schedules jelas.
* [ ] Tabel leave_requests jelas.
* [ ] Tabel email_logs jelas.
* [ ] Tabel audit_logs jelas.
* [ ] Relasi data jelas.
* [ ] Data sensitif sudah ditentukan.

## UI/UX

* [ ] Warna utama merah sudah ditentukan.
* [ ] Layout dashboard jelas.
* [ ] Form izin jelas.
* [ ] Badge status jelas.
* [ ] Empty state jelas.
* [ ] Error state jelas.
* [ ] Print layout A4 jelas.
* [ ] Halaman QR verification jelas.
* [ ] Responsive behavior jelas.

## Backend

* [ ] Flask structure jelas.
* [ ] Route auth jelas.
* [ ] Route mahasiswa jelas.
* [ ] Route dosen jelas.
* [ ] Route admin jelas.
* [ ] Route verification jelas.
* [ ] Role permission jelas.
* [ ] Email service jelas.
* [ ] QR service jelas.
* [ ] Error handling jelas.

## Deployment

* [ ] Database production siap.
* [ ] Environment variable siap.
* [ ] Secret Manager siap.
* [ ] Cloud Run siap.
* [ ] Cloud SQL siap.
* [ ] Email provider siap.
* [ ] Domain production atau URL Cloud Run siap.
* [ ] Testing production siap.

## Scope Control

* [ ] Tidak ada upload file di MVP.
* [ ] Tidak ada WhatsApp notification di MVP.
* [ ] Tidak ada mobile app native di MVP.
* [ ] Tidak ada tanda tangan digital legal.
* [ ] Tidak ada integrasi sistem akademik resmi.
* [ ] Siap dilanjutkan ke desain UI.
* [ ] Siap dilanjutkan ke coding frontend.
* [ ] Siap dilanjutkan ke coding backend.
* [ ] Siap dilanjutkan ke deployment GCP.

---

# Keputusan Final MVP

Project final yang akan dibangun adalah:

> **KelasKita — Sistem Izin Tidak Masuk Kelas dengan Approval Dosen, Email Notification, Surat Cetak, dan QR Verification.**

## Stack Final

* HTML
* CSS
* JavaScript
* Flask
* MySQL
* Cloud SQL
* Cloud Run
* Secret Manager
* Email provider pihak ketiga
* QR code
* CSS print

## Fitur Inti Final

1. Login multi-role.
2. Pengajuan izin mahasiswa.
3. Approval dosen.
4. Email notification.
5. Riwayat izin.
6. Surat izin cetak.
7. QR verification.
8. Dashboard.
9. CRUD user.
10. CRUD kategori izin.
11. CRUD jadwal kelas.

## Prinsip Utama Project

Dosen tidak perlu tanda tangan manual. Approval di sistem sudah menjadi dasar validasi, dan QR code digunakan untuk membuktikan bahwa surat izin benar-benar valid dari sistem.

---
