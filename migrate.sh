#!/bin/bash
# ============================================================
# KelasKita - Migrate skema ke MySQL production
# ============================================================
# Pemakaian:
#   ./migrate.sh
#
# Script ini dijalankan setiap kali ada migration baru di
# migrations/versions/ sebelum ./deploy.sh
# ============================================================

set -e

echo ""
echo "==> KelasKita Migration to Production DB"
echo ""

# Validasi .env.production ada
if [ ! -f .env.production ]; then
    echo "ERROR: .env.production tidak ditemukan."
    echo "  Copy .env.production.example -> .env.production, isi nilainya, lalu jalankan ulang."
    exit 1
fi

# Baca DATABASE_URL dari .env.production
DB_URL=$(grep "^DATABASE_URL=" .env.production | head -n1 | cut -d= -f2-)

if [ -z "${DB_URL}" ]; then
    echo "ERROR: DATABASE_URL tidak ada di .env.production"
    exit 1
fi

# Pastikan dependency terinstall
echo "==> Cek dependency Python..."
if ! python3 -c "import flask, flask_migrate, sqlalchemy, pymysql" 2>/dev/null; then
    echo "    Install requirements..."
    pip install -q -r requirements.txt
fi

# Export env vars supaya flask CLI bisa baca DATABASE_URL + SECRET_KEY
echo "==> Load env dari .env.production..."
set -a
# shellcheck disable=SC1091
source .env.production
set +a

# Jalankan migration
echo "==> flask db upgrade (target: head)..."
flask --app run db upgrade

echo ""
echo "============================================================"
echo "  MIGRATION SELESAI"
echo "============================================================"
echo "  Sekarang aman untuk ./deploy.sh"
echo ""
