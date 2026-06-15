from datetime import time

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.extensions import db
from app.models import ClassSchedule, User
from app.utils.decorators import role_required


bp = Blueprint("schedules", __name__, url_prefix="/admin/schedules")


@bp.get("")
@role_required(User.ROLE_ADMIN)
def index():
    schedules = (
        ClassSchedule.query.join(User)
        .order_by(ClassSchedule.class_name.asc(), ClassSchedule.course_name.asc())
        .all()
    )
    lecturers = (
        User.query.filter_by(role=User.ROLE_DOSEN, is_active=True)
        .order_by(User.name.asc())
        .all()
    )
    return render_template(
        "schedules/index.html",
        title="Jadwal Kelas",
        schedules=schedules,
        lecturers=lecturers,
        days=_daftar_hari(),
    )


@bp.post("")
@role_required(User.ROLE_ADMIN)
def create():
    data, errors = _ambil_data_jadwal(request.form)
    if errors:
        for error in errors:
            flash(error, "warning")
        return redirect(url_for("schedules.index"))

    schedule = ClassSchedule(**data, is_active=True)
    db.session.add(schedule)
    db.session.commit()

    flash("Jadwal kelas berhasil ditambahkan.", "success")
    return redirect(url_for("schedules.index"))


@bp.post("/<int:schedule_id>/update")
@role_required(User.ROLE_ADMIN)
def update(schedule_id):
    schedule = ClassSchedule.query.get_or_404(schedule_id)
    data, errors = _ambil_data_jadwal(request.form)
    if errors:
        for error in errors:
            flash(error, "warning")
        return redirect(url_for("schedules.index"))

    for field, value in data.items():
        setattr(schedule, field, value)
    db.session.commit()

    flash("Jadwal kelas berhasil diperbarui.", "success")
    return redirect(url_for("schedules.index"))


@bp.post("/<int:schedule_id>/toggle-active")
@role_required(User.ROLE_ADMIN)
def toggle_active(schedule_id):
    schedule = ClassSchedule.query.get_or_404(schedule_id)
    schedule.is_active = not schedule.is_active
    db.session.commit()

    status = "diaktifkan" if schedule.is_active else "dinonaktifkan"
    flash(f"Jadwal kelas berhasil {status}.", "success")
    return redirect(url_for("schedules.index"))


def _ambil_data_jadwal(form):
    errors = []
    course_name = form.get("course_name", "").strip()
    class_name = form.get("class_name", "").strip()
    day = form.get("day", "").strip()
    room = form.get("room", "").strip() or None
    lecturer_id = _parse_int(form.get("lecturer_id"))
    start_time = _parse_time(form.get("start_time"))
    end_time = _parse_time(form.get("end_time"))

    if not course_name:
        errors.append("Nama mata kuliah wajib diisi.")
    if not class_name:
        errors.append("Nama kelas wajib diisi.")
    if day not in _daftar_hari():
        errors.append("Hari kuliah tidak valid.")
    if not lecturer_id:
        errors.append("Dosen wajib dipilih.")
    elif not User.query.filter_by(id=lecturer_id, role=User.ROLE_DOSEN, is_active=True).first():
        errors.append("Dosen yang dipilih tidak valid atau tidak aktif.")
    if not start_time or not end_time:
        errors.append("Jam mulai dan jam selesai wajib diisi.")
    elif end_time <= start_time:
        errors.append("Jam selesai harus lebih besar dari jam mulai.")

    data = {
        "course_name": course_name,
        "class_name": class_name,
        "lecturer_id": lecturer_id,
        "day": day,
        "start_time": start_time,
        "end_time": end_time,
        "room": room,
    }
    return data, errors


def _parse_time(value):
    try:
        hour, minute = (value or "").split(":")
        return time(hour=int(hour), minute=int(minute))
    except (TypeError, ValueError):
        return None


def _parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _daftar_hari():
    return ("Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu")
