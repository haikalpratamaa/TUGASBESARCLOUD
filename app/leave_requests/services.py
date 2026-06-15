from datetime import date, datetime, timezone
from secrets import token_urlsafe
import logging
from app.extensions import db
from app.models import LeaveRequest, ClassSchedule, PermissionCategory


def buat_token_verifikasi():
    return token_urlsafe(32)


def buat_nomor_izin():
    today = date.today()
    prefix = f"IZN-{today.strftime('%Y%m%d')}"

    last = (
        LeaveRequest.query
        .filter(LeaveRequest.request_number.like(f"{prefix}-%"))
        .order_by(LeaveRequest.request_number.desc())
        .first()
    )

    if last:
        try:
            last_seq = int(last.request_number.rsplit("-", 1)[-1])
        except (ValueError, IndexError):
            last_seq = 0
        seq = last_seq + 1
    else:
        seq = 1

    return f"{prefix}-{seq:04d}"


def kirim_notifikasi_pengajuan_baru(izin):
    """Send email notification to lecturer when student submits new request."""
    from app.notifications.email_service import kirim_dan_catat_email
    from app.notifications.templates import template_email_pengajuan_baru

    try:
        dosen = izin.schedule.lecturer
        if not dosen or not dosen.email:
            return
        subject, body = template_email_pengajuan_baru(
            izin.student.name, izin.schedule.course_name
        )
        kirim_dan_catat_email(izin.id, dosen.email, subject, body, "pengajuan_baru")
    except Exception:
        logging.getLogger(__name__).warning(
            "Gagal mengirim notifikasi pengajuan baru #%s", izin.id, exc_info=True
        )


def kirim_notifikasi_status(izin):
    """Send email notification to student after approval/rejection."""
    from app.notifications.email_service import kirim_dan_catat_email
    from app.notifications.templates import (
        template_email_izin_disetujui,
        template_email_izin_ditolak,
    )

    try:
        nama = izin.student.name
        matkul = izin.schedule.course_name
        nomor = izin.request_number
        email = izin.student.email

        if izin.status == LeaveRequest.STATUS_DISETUJUI:
            subject, body = template_email_izin_disetujui(nama, matkul, nomor)
            template_name = "izin_disetujui"
        elif izin.status == LeaveRequest.STATUS_DITOLAK:
            subject, body = template_email_izin_ditolak(
                nama, matkul, nomor, izin.admin_note
            )
            template_name = "izin_ditolak"
        else:
            return

        kirim_dan_catat_email(izin.id, email, subject, body, template_name)
    except Exception:
        logging.getLogger(__name__).warning(
            "Gagal mengirim notifikasi untuk izin #%s", izin.id, exc_info=True
        )


def validasi_pengajuan(schedule_id, category_id, permission_date, reason, current_user_id, leave_id=None):
    errors = []
    
    if not schedule_id:
        errors.append("Jadwal kelas wajib dipilih.")
    else:
        schedule = ClassSchedule.query.filter_by(id=schedule_id, is_active=True).first()
        if not schedule:
            errors.append("Jadwal kelas tidak valid atau sudah nonaktif.")
        elif permission_date:
            # Map permission_date weekday to Indonesian day names
            weekday_map = {0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"}
            current_day_name = weekday_map[permission_date.weekday()]
            if current_day_name != schedule.day:
                errors.append(f"Tanggal izin tidak sesuai dengan hari perkuliahan (Mata kuliah dijadwalkan pada hari {schedule.day}).")

    if not category_id:
        errors.append("Kategori izin wajib dipilih.")
    elif not PermissionCategory.query.filter_by(id=category_id, is_active=True).first():
        errors.append("Kategori izin tidak valid atau sudah nonaktif.")
        
    if not permission_date:
        errors.append("Tanggal izin wajib diisi.")
        
    if not reason or len(reason) < 10:
        errors.append("Alasan izin wajib diisi minimal 10 karakter.")
        
    # Check for duplicate active leave request (status not cancelled/dibatalkan)
    if schedule_id and permission_date:
        duplicate = LeaveRequest.query.filter(
            LeaveRequest.user_id == current_user_id,
            LeaveRequest.schedule_id == schedule_id,
            LeaveRequest.permission_date == permission_date,
            LeaveRequest.status != LeaveRequest.STATUS_DIBATALKAN
        )
        if leave_id:
            duplicate = duplicate.filter(LeaveRequest.id != leave_id)
        if duplicate.first():
            errors.append("Anda sudah memiliki pengajuan izin aktif untuk jadwal dan tanggal ini.")

    return errors


def parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_date(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None
