from flask import Blueprint, render_template

from app.models import LeaveRequest


bp = Blueprint("verification", __name__, url_prefix="")


@bp.get("/verify/<string:token>")
def verify(token):
    izin = LeaveRequest.query.filter_by(verification_token=token).first()

    if not izin:
        return render_template(
            "verification/verify.html",
            title="Verifikasi Gagal",
            valid=False,
            izin=None,
        ), 404

    return render_template(
        "verification/verify.html",
        title="Verifikasi Surat Izin",
        valid=True,
        izin=izin,
    )
