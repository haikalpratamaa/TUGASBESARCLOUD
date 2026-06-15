from datetime import date, datetime, timezone

from flask import Blueprint, abort, flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user

from app.extensions import db
from app.models import ClassSchedule, LeaveRequest, PermissionCategory, User
from app.utils.decorators import role_required

from .services import (
    buat_nomor_izin,
    buat_token_verifikasi,
    parse_int,
    parse_date,
    validasi_pengajuan,
    kirim_notifikasi_pengajuan_baru,
    kirim_notifikasi_status,
)


bp = Blueprint("leave_requests", __name__, url_prefix="")


# =========================================================================
# MAHASISWA ROUTES
# =========================================================================

@bp.get("/student/leave-requests/create")
@role_required(User.ROLE_MAHASISWA)
def mahasiswa_create():
    schedules = (
        ClassSchedule.query
        .filter_by(is_active=True)
        .order_by(ClassSchedule.course_name.asc())
        .all()
    )
    categories = (
        PermissionCategory.query
        .filter_by(is_active=True)
        .order_by(PermissionCategory.name.asc())
        .all()
    )
    return render_template(
        "leave_requests/create.html",
        title="Ajukan Izin",
        schedules=schedules,
        categories=categories,
    )


@bp.post("/student/leave-requests")
@role_required(User.ROLE_MAHASISWA)
def mahasiswa_store():
    schedule_id = parse_int(request.form.get("schedule_id"))
    category_id = parse_int(request.form.get("category_id"))
    permission_date = parse_date(request.form.get("permission_date"))
    reason = (request.form.get("reason") or "").strip()

    errors = validasi_pengajuan(schedule_id, category_id, permission_date, reason, current_user.id)
    if errors:
        for error in errors:
            flash(error, "warning")
        return redirect(url_for("leave_requests.mahasiswa_create"))

    izin = LeaveRequest(
        request_number=buat_nomor_izin(),
        user_id=current_user.id,
        schedule_id=schedule_id,
        category_id=category_id,
        permission_date=permission_date,
        reason=reason,
        status=LeaveRequest.STATUS_DIAJUKAN,
        verification_token=buat_token_verifikasi(),
    )
    db.session.add(izin)
    db.session.commit()

    kirim_notifikasi_pengajuan_baru(izin)

    flash("Pengajuan izin berhasil dikirim.", "success")
    return redirect(url_for("leave_requests.mahasiswa_index"))


@bp.get("/student/leave-requests")
@role_required(User.ROLE_MAHASISWA)
def mahasiswa_index():
    status_filter = request.args.get("status")
    query = LeaveRequest.query.filter_by(user_id=current_user.id)

    if status_filter and status_filter in LeaveRequest.STATUSES:
        query = query.filter_by(status=status_filter)

    izin_list = query.order_by(LeaveRequest.created_at.desc()).all()

    return render_template(
        "leave_requests/index.html",
        title="Riwayat Izin",
        izin_list=izin_list,
        status_filter=status_filter,
    )


@bp.get("/student/leave-requests/<int:leave_id>")
@role_required(User.ROLE_MAHASISWA)
def mahasiswa_detail(leave_id):
    izin = LeaveRequest.query.get_or_404(leave_id)
    if izin.user_id != current_user.id:
        abort(403)
    return render_template(
        "leave_requests/detail.html",
        title="Detail Izin",
        izin=izin,
    )


@bp.get("/student/leave-requests/<int:leave_id>/edit")
@role_required(User.ROLE_MAHASISWA)
def mahasiswa_edit(leave_id):
    izin = LeaveRequest.query.get_or_404(leave_id)
    if izin.user_id != current_user.id:
        abort(403)
    if not izin.bisa_diedit():
        flash("Izin tidak dapat diedit karena sudah diproses.", "warning")
        return redirect(url_for("leave_requests.mahasiswa_detail", leave_id=leave_id))

    schedules = ClassSchedule.query.filter_by(is_active=True).order_by(ClassSchedule.course_name.asc()).all()
    categories = PermissionCategory.query.filter_by(is_active=True).order_by(PermissionCategory.name.asc()).all()

    return render_template(
        "leave_requests/edit.html",
        title="Edit Izin",
        izin=izin,
        schedules=schedules,
        categories=categories,
    )


@bp.post("/student/leave-requests/<int:leave_id>/update")
@role_required(User.ROLE_MAHASISWA)
def mahasiswa_update(leave_id):
    izin = LeaveRequest.query.get_or_404(leave_id)
    if izin.user_id != current_user.id:
        abort(403)
    if not izin.bisa_diedit():
        flash("Izin tidak dapat diedit karena sudah diproses.", "warning")
        return redirect(url_for("leave_requests.mahasiswa_detail", leave_id=leave_id))

    schedule_id = parse_int(request.form.get("schedule_id"))
    category_id = parse_int(request.form.get("category_id"))
    permission_date = parse_date(request.form.get("permission_date"))
    reason = (request.form.get("reason") or "").strip()

    errors = validasi_pengajuan(schedule_id, category_id, permission_date, reason, current_user.id, leave_id=leave_id)
    if errors:
        for error in errors:
            flash(error, "warning")
        return redirect(url_for("leave_requests.mahasiswa_edit", leave_id=leave_id))

    izin.schedule_id = schedule_id
    izin.category_id = category_id
    izin.permission_date = permission_date
    izin.reason = reason
    db.session.commit()

    flash("Pengajuan izin berhasil diperbarui.", "success")
    return redirect(url_for("leave_requests.mahasiswa_detail", leave_id=leave_id))


@bp.post("/student/leave-requests/<int:leave_id>/cancel")
@role_required(User.ROLE_MAHASISWA)
def mahasiswa_cancel(leave_id):
    izin = LeaveRequest.query.get_or_404(leave_id)
    if izin.user_id != current_user.id:
        abort(403)
    if not izin.bisa_dibatalkan():
        flash("Izin tidak dapat dibatalkan karena sudah diproses.", "warning")
        return redirect(url_for("leave_requests.mahasiswa_detail", leave_id=leave_id))

    izin.status = LeaveRequest.STATUS_DIBATALKAN
    db.session.commit()

    flash("Pengajuan izin berhasil dibatalkan.", "success")
    return redirect(url_for("leave_requests.mahasiswa_index"))


@bp.get("/student/leave-requests/<int:leave_id>/print")
@role_required(User.ROLE_MAHASISWA)
def mahasiswa_print(leave_id):
    izin = LeaveRequest.query.get_or_404(leave_id)
    if izin.user_id != current_user.id:
        abort(403)
    if not izin.bisa_dicetak():
        flash("Surat izin hanya bisa dicetak jika status sudah disetujui.", "warning")
        return redirect(url_for("leave_requests.mahasiswa_detail", leave_id=leave_id))

    from flask import current_app
    verification_url = f"{current_app.config['APP_URL']}/verify/{izin.verification_token}"

    return render_template(
        "leave_requests/print.html",
        title="Surat Izin",
        izin=izin,
        verification_url=verification_url,
    )


@bp.get("/student/leave-requests/<int:leave_id>/qr")
@role_required(User.ROLE_MAHASISWA)
def qr_image(leave_id):
    izin = LeaveRequest.query.get_or_404(leave_id)
    if izin.user_id != current_user.id:
        abort(403)
    if not izin.bisa_dicetak():
        abort(404)

    from flask import current_app
    from .qr_service import buat_qr_code_png

    verification_url = f"{current_app.config['APP_URL']}/verify/{izin.verification_token}"
    buffer = buat_qr_code_png(verification_url)
    return send_file(buffer, mimetype="image/png")


# =========================================================================
# DOSEN ROUTES
# =========================================================================

@bp.get("/lecturer/leave-requests")
@role_required(User.ROLE_DOSEN)
def dosen_index():
    jadwal_ids = [
        s.id for s in ClassSchedule.query.filter_by(
            lecturer_id=current_user.id, is_active=True
        ).all()
    ]

    status_filter = request.args.get("status")

    if jadwal_ids:
        query = LeaveRequest.query.filter(LeaveRequest.schedule_id.in_(jadwal_ids))
        if status_filter and status_filter in LeaveRequest.STATUSES:
            query = query.filter_by(status=status_filter)
        izin_list = query.order_by(LeaveRequest.created_at.desc()).all()
    else:
        izin_list = []

    return render_template(
        "leave_requests/lecturer_list.html",
        title="Pengajuan Masuk",
        izin_list=izin_list,
        status_filter=status_filter,
    )


@bp.get("/lecturer/leave-requests/<int:leave_id>")
@role_required(User.ROLE_DOSEN)
def dosen_detail(leave_id):
    izin = LeaveRequest.query.get_or_404(leave_id)
    jadwal = ClassSchedule.query.get(izin.schedule_id)
    if not jadwal or jadwal.lecturer_id != current_user.id:
        abort(403)

    return render_template(
        "leave_requests/lecturer_detail.html",
        title="Detail Pengajuan",
        izin=izin,
    )


@bp.post("/lecturer/leave-requests/<int:leave_id>/approve")
@role_required(User.ROLE_DOSEN)
def dosen_approve(leave_id):
    izin = LeaveRequest.query.get_or_404(leave_id)
    jadwal = ClassSchedule.query.get(izin.schedule_id)
    if not jadwal or jadwal.lecturer_id != current_user.id:
        abort(403)

    if not izin.bisa_diproses():
        flash("Izin sudah diproses sebelumnya.", "warning")
        return redirect(url_for("leave_requests.dosen_detail", leave_id=leave_id))

    izin.status = LeaveRequest.STATUS_DISETUJUI
    izin.admin_note = (request.form.get("admin_note") or "").strip() or None
    izin.reviewed_by = current_user.id
    izin.reviewed_at = datetime.now(timezone.utc)
    db.session.commit()

    kirim_notifikasi_status(izin)

    flash("Izin berhasil disetujui.", "success")
    return redirect(url_for("leave_requests.dosen_detail", leave_id=leave_id))


@bp.post("/lecturer/leave-requests/<int:leave_id>/reject")
@role_required(User.ROLE_DOSEN)
def dosen_reject(leave_id):
    izin = LeaveRequest.query.get_or_404(leave_id)
    jadwal = ClassSchedule.query.get(izin.schedule_id)
    if not jadwal or jadwal.lecturer_id != current_user.id:
        abort(403)

    if not izin.bisa_diproses():
        flash("Izin sudah diproses sebelumnya.", "warning")
        return redirect(url_for("leave_requests.dosen_detail", leave_id=leave_id))

    izin.status = LeaveRequest.STATUS_DITOLAK
    izin.admin_note = (request.form.get("admin_note") or "").strip() or None
    izin.reviewed_by = current_user.id
    izin.reviewed_at = datetime.now(timezone.utc)
    db.session.commit()

    kirim_notifikasi_status(izin)

    flash("Izin berhasil ditolak.", "success")
    return redirect(url_for("leave_requests.dosen_detail", leave_id=leave_id))
