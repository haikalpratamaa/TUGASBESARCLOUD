#!/bin/bash
# ============================================================
# KelasKita - Deploy ke Google Cloud Run (Cloud Shell / Linux)
# ============================================================
# Pemakaian (di Cloud Shell):
#   ./deploy.sh
#
# Prasyarat:
#   1. gcloud sudah authenticated (Cloud Shell otomatis sudah)
#   2. .env.production di-upload ke folder yang sama dengan script ini
#   3. Project GCP sudah di-set: gcloud config set project [NAMA_PROJECT]
#   4. Artifact Registry "kelaskita-repo" sudah dibuat
# ============================================================

set -e  # Stop kalau ada error

# ---------- KONFIGURASI ----------
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
REGION="asia-southeast1"
SERVICE="kelaskita-app"
REPO="kelaskita-repo"
TAG="v$(date +%Y%m%d%H%M%S)"
IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/kelaskita:${TAG}"

echo ""
echo "============================================================"
echo "  KelasKita - Deploy ke Cloud Run"
echo "============================================================"
echo "  Project : ${PROJECT_ID}"
echo "  Region  : ${REGION}"
echo "  Service : ${SERVICE}"
echo "  Image   : ${IMAGE}"
echo ""

# Validasi project
if [ -z "${PROJECT_ID}" ]; then
    echo "ERROR: gcloud project belum di-set."
    echo "  Jalankan: gcloud config set project [NAMA_PROJECT]"
    exit 1
fi

# Validasi .env.production
if [ ! -f .env.production ]; then
    echo "ERROR: .env.production tidak ditemukan di folder ini."
    echo "  Upload file .env.production dari laptop ke Cloud Shell dulu."
    exit 1
fi

# ---------- WARNING MIGRATION ----------
echo ""
echo "==> [0/3] Cek migration database..."
LATEST_MIGRATION=$(ls -t migrations/versions/*.py 2>/dev/null | head -n1)
if [ -n "${LATEST_MIGRATION}" ]; then
    echo "    Migration terbaru: $(basename "${LATEST_MIGRATION}")"
    echo "    Pastikan sudah jalankan: ./migrate.sh"
    read -p "    Sudah migrate? (y/N): " -n 1 -r REPLY
    echo ""
    if [[ ! ${REPLY} =~ ^[Yy]$ ]]; then
        echo "    Batalkan deploy. Jalankan: ./migrate.sh dulu."
        exit 1
    fi
fi

# ---------- BUILD ----------
echo "==> [1/3] Build image via Cloud Build (~3-5 menit)..."
gcloud builds submit --tag "${IMAGE}" --region="${REGION}"

# ---------- BANGUN ENV VARS FILE (format JSON-valid YAML) ----------
echo ""
echo "==> [2/3] Bangun env vars dari .env.production..."

ENV_FILE=$(mktemp)
python3 - <<'PYEOF' > "${ENV_FILE}"
import json
env = {}
with open('.env.production') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        # Strip inline comments
        v_clean = v.split('#', 1)[0].strip()
        # Strip surrounding quotes if any
        if (v_clean.startswith('"') and v_clean.endswith('"')) or (v_clean.startswith("'") and v_clean.endswith("'")):
            v_clean = v_clean[1:-1]
        env[k.strip()] = v_clean
print(json.dumps(env))
PYEOF

# ---------- DEPLOY ----------
echo "==> [3/3] Deploy ke Cloud Run..."
gcloud run deploy "${SERVICE}" \
    --image "${IMAGE}" \
    --region "${REGION}" \
    --platform managed \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 1 \
    --timeout 600 \
    --port 8080 \
    --concurrency 80 \
    --env-vars-file "${ENV_FILE}"

DEPLOY_EXIT=$?
rm -f "${ENV_FILE}"

if [ ${DEPLOY_EXIT} -ne 0 ]; then
    echo "ERROR: Deploy gagal."
    exit 1
fi

# ---------- INFO ----------
URL=$(gcloud run services describe "${SERVICE}" --region="${REGION}" --format="value(status.url)")

echo ""
echo "============================================================"
echo "  DEPLOY BERHASIL"
echo "============================================================"
echo "  Service URL : ${URL}"
echo "  Health      : ${URL}/healthz"
echo "  Login       : ${URL}/login"
echo ""
echo "Cek log realtime:"
echo "  gcloud run services logs tail ${SERVICE} --region=${REGION}"
echo ""
