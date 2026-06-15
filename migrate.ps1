# ============================================================
# KelasKita - Migrate skema ke MySQL production
# ============================================================
# Pemakaian:
#   .\migrate.ps1
#
# Membaca seluruh variabel lingkungan dari .env.production.
# ============================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "==> KelasKita Migration to Production DB" -ForegroundColor Cyan
Write-Host ""

# Validasi .env.production ada
if (-not (Test-Path ".env.production")) {
    Write-Host "ERROR: .env.production tidak ditemukan." -ForegroundColor Red
    Write-Host "  Copy .env.production.example -> .env.production, isi nilainya, lalu jalankan ulang."
    exit 1
}

# Cek & install dependency Python jika belum ada
Write-Host "==> Cek dependency Python..." -ForegroundColor Cyan
python -c "import flask, flask_migrate, sqlalchemy, pymysql" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "    Beberapa modul belum terinstall. Menginstall dari requirements.txt..." -ForegroundColor Gray
    pip install -r requirements.txt
}

# Memuat seluruh env vars dari .env.production ke session PowerShell
Write-Host "==> Memuat env dari .env.production..." -ForegroundColor Cyan
Get-Content .env.production | ForEach-Object {
    $line = $_.Trim()
    # Hiraukan baris kosong, komentar, atau baris tanpa '='
    if ($line -and -not $line.StartsWith("#") -and $line -like "*=*") {
        $parts = $line.Split('=', 2)
        $key = $parts[0].Trim()
        $rawVal = $parts[1].Trim()
        
        # Bersihkan komentar inline jika ada
        $val = $rawVal.Split('#', 2)[0].Trim()
        
        # Bersihkan tanda kutip pembungkus jika ada
        if (($val.StartsWith('"') -and $val.EndsWith('"')) -or ($val.StartsWith("'") -and $val.EndsWith("'"))) {
            $val = $val.Substring(1, $val.Length - 2)
        }
        
        $env:$key = $val
    }
}

# Validasi DATABASE_URL ada
if (-not $env:DATABASE_URL) {
    Write-Host "ERROR: DATABASE_URL tidak ditemukan di .env.production" -ForegroundColor Red
    exit 1
}

Write-Host "Target DB: $($env:DATABASE_URL -replace ':[^:@]+@', ':****@')" -ForegroundColor Gray
Write-Host ""

# Set FLASK_APP eksplisit
$env:FLASK_APP = "run.py"

Write-Host "==> flask db upgrade..." -ForegroundColor Cyan
flask db upgrade
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Migrasi gagal." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==> Selesai. Skema berhasil dimigrasi ke MySQL Production." -ForegroundColor Green
Write-Host ""
Write-Host "Sekarang aman untuk deploy menggunakan .\deploy.ps1"
Write-Host ""
