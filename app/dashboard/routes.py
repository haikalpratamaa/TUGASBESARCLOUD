from flask import Blueprint, render_template
from flask_login import current_user

from app.models import ClassSchedule, EmailLog, LeaveRequest, PermissionCategory, User
from app.utils.decorators import role_required


bp = Blueprint("dashboard", __name__, url_prefix="")


@bp.get("/student/dashboard")
@role_required(User.ROLE_MAHASISWA)
def mahasiswa():
    user_id = current_user.id
    total = LeaveRequest.query.filter_by(user_id=user_id).count()
    diajukan = LeaveRequest.query.filter_by(user_id=user_id, status=LeaveRequest.STATUS_DIAJUKAN).count()
    disetujui = LeaveRequest.query.filter_by(user_id=user_id, status=LeaveRequest.STATUS_DISETUJUI).count()
    ditolak = LeaveRequest.query.filter_by(user_id=user_id, status=LeaveRequest.STATUS_DITOLAK).count()

    terbaru = (
        LeaveRequest.query
        .filter_by(user_id=user_id)
        .order_by(LeaveRequest.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard/mahasiswa.html",
        title="Dashboard Mahasiswa",
        total=total,
        diajukan=diajukan,
        disetujui=disetujui,
        ditolak=ditolak,
        terbaru=terbaru,
    )


@bp.get("/lecturer/dashboard")
@role_required(User.ROLE_DOSEN)
def dosen():
    jadwal_ids = [
        s.id for s in ClassSchedule.query.filter_by(
            lecturer_id=current_user.id, is_active=True
        ).all()
    ]

    if jadwal_ids:
        base = LeaveRequest.query.filter(LeaveRequest.schedule_id.in_(jadwal_ids))
        total = base.count()
        menunggu = base.filter_by(status=LeaveRequest.STATUS_DIAJUKAN).count()
        disetujui = base.filter_by(status=LeaveRequest.STATUS_DISETUJUI).count()
        ditolak = base.filter_by(status=LeaveRequest.STATUS_DITOLAK).count()
        terbaru = (
            base.filter_by(status=LeaveRequest.STATUS_DIAJUKAN)
            .order_by(LeaveRequest.created_at.desc())
            .limit(5)
            .all()
        )
    else:
        total = menunggu = disetujui = ditolak = 0
        terbaru = []

    return render_template(
        "dashboard/dosen.html",
        title="Dashboard Dosen",
        total=total,
        menunggu=menunggu,
        disetujui=disetujui,
        ditolak=ditolak,
        terbaru=terbaru,
    )


@bp.get("/admin/dashboard")
@role_required(User.ROLE_ADMIN)
def admin():
    total_user = User.query.filter_by(is_active=True).count()
    total_jadwal = ClassSchedule.query.filter_by(is_active=True).count()
    total_kategori = PermissionCategory.query.filter_by(is_active=True).count()
    total_izin = LeaveRequest.query.count()
    email_terkirim = EmailLog.query.filter_by(status=EmailLog.STATUS_SENT).count()
    email_gagal = EmailLog.query.filter_by(status=EmailLog.STATUS_FAILED).count()

    return render_template(
        "dashboard/admin.html",
        title="Dashboard Admin",
        total_user=total_user,
        total_jadwal=total_jadwal,
        total_kategori=total_kategori,
        total_izin=total_izin,
        email_terkirim=email_terkirim,
        email_gagal=email_gagal,
    )
