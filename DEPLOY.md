# 🚀 Panduan Deploy KelasKita — Cloud Run + MySQL Production

Panduan lengkap deployment KelasKita ke Google Cloud Run dan basis data MySQL (seperti Cloud SQL, PlanetScale, Aiven, atau hosting MySQL lainnya).

---

## 📋 Daftar Isi

1. [Yang Harus Disiapkan (Checklist)](#1-yang-harus-disiapkan-checklist)
2. [Fase A — Setup MySQL Database](#2-fase-a--setup-mysql-database)
3. [Fase B — Setup GCP Project](#3-fase-b--setup-gcp-project)
4. [Fase C — Konfigurasi `.env.production`](#4-fase-c--konfigurasi-envproduction)
5. [Fase D — Migrasi Skema ke Database Production](#5-fase-d--migrasi-skema-ke-database-production)
6. [Fase E — Deploy ke Cloud Run](#6-fase-e--deploy-ke-cloud-run)
7. [Fase F — Verifikasi Production](#7-fase-f--verifikasi-production)

---

## 1. Yang Harus Disiapkan (Checklist)

Sebelum memulai, pastikan Anda memiliki:
- [ ] **Akun Google** dengan billing aktif di Google Cloud Platform (GCP).
- [ ] **gcloud CLI** terinstall di komputer Anda.
  - Unduh: [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- [ ] **Instance MySQL** aktif (mis. Cloud SQL, PlanetScale, Aiven MySQL, dll).
- [ ] **Python 3.12+** dan **pip** terinstall secara lokal untuk menjalankan migrasi database.

---

## 2. Fase A — Setup MySQL Database

1. Buat database baru bernama `kelaskita` di instance MySQL Anda.
2. Catat informasi koneksi MySQL:
   - Host
   - Port (default: `3306`)
   - Username
   - Password
   - Nama Database (`kelaskita`)
3. Susun URL koneksi dengan format berikut:
   ```
   mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/kelaskita
   ```
   *(Penting: Kita menggunakan `pymysql` sebagai driver MySQL).*

---

## 3. Fase B — Setup GCP Project

Buka terminal (bash atau PowerShell) di direktori proyek `PROJECTHAIKAL`:

### B.1 Login & Inisialisasi Project
```bash
# Login ke akun Google Anda
gcloud auth login

# Buat project GCP baru (ID harus unik secara global)
gcloud projects create kelaskita-app-2026 --name="KelasKita"

# Set project tersebut sebagai project aktif
gcloud config set project kelaskita-app-2026
```

### B.2 Hubungkan Billing Account
```bash
# Link project ke billing account (ganti ID sesuai billing account Anda)
gcloud billing projects link kelaskita-app-2026 --billing-account=YOUR_BILLING_ACCOUNT_ID
```

### B.3 Aktifkan API Layanan
```bash
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com
```

### B.4 Buat Artifact Registry
```bash
gcloud artifacts repositories create kelaskita-repo \
    --repository-format=docker \
    --location=asia-southeast1 \
    --description="KelasKita Container Repository"
```

---

## 4. Fase C — Konfigurasi `.env.production`

1. Salin berkas template `.env.production.example` menjadi `.env.production`:
   ```bash
   cp .env.production.example .env.production
   ```
2. Generate `SECRET_KEY` baru secara acak:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
3. Edit berkas `.env.production` dan isi nilai-nilainya:
   - `SECRET_KEY`: Tempel hasil generator di atas.
   - `DATABASE_URL`: Tempel MySQL Connection URL dari **Fase A**.
   - `SMTP_*` & `MAIL_*`: Isi dengan kredensial server SMTP pengiriman email Anda (Gmail App Password, Mailgun, dsb).

---

## 5. Fase D — Migrasi Skema ke Database Production

Jalankan perintah berikut secara lokal untuk mengunggah skema database baru Anda ke MySQL production:

### Windows (PowerShell):
```powershell
.\migrate.ps1
```

### Linux / macOS / Cloud Shell (Bash):
```bash
chmod +x migrate.sh
./migrate.sh
```

Script migrasi ini akan mendeteksi isi tabel migrasi dari direktori `migrations/` dan menerapkannya langsung ke server MySQL Anda.

---

## 6. Fase E — Deploy ke Cloud Run

Setelah migrasi selesai, Anda dapat langsung men-deploy KelasKita ke GCP Cloud Run:

### Windows (PowerShell):
```powershell
.\deploy.ps1
```

### Linux / macOS / Cloud Shell (Bash):
```bash
chmod +x deploy.sh
./deploy.sh
```

**Hasil akhir yang diharapkan**:
```
============================================================
  DEPLOY BERHASIL
============================================================
  Service URL : https://kelaskita-app-xxxxx-as.a.run.app
  Health      : https://kelaskita-app-xxxxx-as.a.run.app/healthz
  Login       : https://kelaskita-app-xxxxx-as.a.run.app/login
```

---

## 7. Fase F — Verifikasi Production

1. Buka `<SERVICE_URL>/healthz` di browser. Hasilnya harus berupa JSON:
   ```json
   {"status": "ok", "service": "kelaskita"}
   ```
2. Buka `<SERVICE_URL>/login` untuk masuk ke platform KelasKita di server production Anda.
3. Anda dapat memeriksa log secara *real-time* dengan menjalankan:
   ```bash
   gcloud run services logs tail kelaskita-app --region=asia-southeast1
   ```
