from sqlalchemy.exc import IntegrityError
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.auth.services import buat_hash_password
from app.extensions import db
from app.models import User
from app.utils.decorators import role_required


bp = Blueprint("users", __name__, url_prefix="/admin/users")


@bp.get("")
@role_required(User.ROLE_ADMIN)
def index():
    users = User.query.order_by(User.role.asc(), User.name.asc()).all()
    return render_template(
        "users/index.html",
        title="Manajemen User",
        users=users,
        roles=User.ROLES,
    )


@bp.post("")
@role_required(User.ROLE_ADMIN)
def create():
    errors = _validasi_form_user(request.form, is_create=True)
    if errors:
        for error in errors:
            flash(error, "warning")
        return redirect(url_for("users.index"))

    student_number, lecturer_code = _normalisasi_identitas_role(
        request.form["role"],
        request.form.get("student_number"),
        request.form.get("lecturer_code"),
    )
    user = User(
        name=request.form["name"].strip(),
        email=request.form["email"].strip().lower(),
        password_hash=buat_hash_password(request.form["password"]),
        role=request.form["role"],
        student_number=student_number,
        lecturer_code=lecturer_code,
        phone=_nilai_opsional(request.form.get("phone")),
        is_active=True,
    )

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Email, NIM, atau kode dosen sudah digunakan.", "danger")
        return redirect(url_for("users.index"))

    flash("User berhasil ditambahkan.", "success")
    return redirect(url_for("users.index"))


@bp.post("/<int:user_id>/update")
@role_required(User.ROLE_ADMIN)
def update(user_id):
    user = User.query.get_or_404(user_id)
    errors = _validasi_form_user(request.form, is_create=False)
    if errors:
        for error in errors:
            flash(error, "warning")
        return redirect(url_for("users.index"))

    user.name = request.form["name"].strip()
    user.email = request.form["email"].strip().lower()
    user.role = request.form["role"]
    user.student_number, user.lecturer_code = _normalisasi_identitas_role(
        request.form["role"],
        request.form.get("student_number"),
        request.form.get("lecturer_code"),
    )
    user.phone = _nilai_opsional(request.form.get("phone"))

    password = request.form.get("password", "")
    if password:
        user.password_hash = buat_hash_password(password)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Email, NIM, atau kode dosen sudah digunakan.", "danger")
        return redirect(url_for("users.index"))

    flash("User berhasil diperbarui.", "success")
    return redirect(url_for("users.index"))


@bp.post("/<int:user_id>/toggle-active")
@role_required(User.ROLE_ADMIN)
def toggle_active(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("Admin tidak dapat menonaktifkan akunnya sendiri.", "warning")
        return redirect(url_for("users.index"))

    user.is_active = not user.is_active
    db.session.commit()

    status = "diaktifkan" if user.is_active else "dinonaktifkan"
    flash(f"User berhasil {status}.", "success")
    return redirect(url_for("users.index"))


def _validasi_form_user(form, is_create):
    errors = []
    role = form.get("role")
    password = form.get("password", "")

    if not form.get("name", "").strip():
        errors.append("Nama user wajib diisi.")
    if not form.get("email", "").strip():
        errors.append("Email user wajib diisi.")
    if role not in User.ROLES:
        errors.append("Role user tidak valid.")
    if is_create and len(password) < 6:
        errors.append("Password minimal 6 karakter.")
    if not is_create and password and len(password) < 6:
        errors.append("Password baru minimal 6 karakter.")
    if role == User.ROLE_MAHASISWA and not form.get("student_number", "").strip():
        errors.append("NIM wajib diisi untuk mahasiswa.")
    if role == User.ROLE_DOSEN and not form.get("lecturer_code", "").strip():
        errors.append("Kode dosen wajib diisi untuk dosen.")

    return errors


def _nilai_opsional(value):
    value = (value or "").strip()
    return value or None


def _normalisasi_identitas_role(role, student_number, lecturer_code):
    if role == User.ROLE_MAHASISWA:
        return _nilai_opsional(student_number), None
    if role == User.ROLE_DOSEN:
        return None, _nilai_opsional(lecturer_code)
    return None, None
