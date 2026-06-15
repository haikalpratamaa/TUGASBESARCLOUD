from sqlalchemy.exc import IntegrityError
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.extensions import db
from app.models import PermissionCategory, User
from app.utils.decorators import role_required


bp = Blueprint("categories", __name__, url_prefix="/admin/categories")


@bp.get("")
@role_required(User.ROLE_ADMIN)
def index():
    categories = PermissionCategory.query.order_by(PermissionCategory.name.asc()).all()
    return render_template(
        "categories/index.html",
        title="Kategori Izin",
        categories=categories,
    )


@bp.post("")
@role_required(User.ROLE_ADMIN)
def create():
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    if not name:
        flash("Nama kategori wajib diisi.", "warning")
        return redirect(url_for("categories.index"))

    category = PermissionCategory(
        name=name,
        description=description or None,
        is_active=True,
    )
    db.session.add(category)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Nama kategori sudah digunakan.", "danger")
        return redirect(url_for("categories.index"))

    flash("Kategori izin berhasil ditambahkan.", "success")
    return redirect(url_for("categories.index"))


@bp.post("/<int:category_id>/update")
@role_required(User.ROLE_ADMIN)
def update(category_id):
    category = PermissionCategory.query.get_or_404(category_id)
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    if not name:
        flash("Nama kategori wajib diisi.", "warning")
        return redirect(url_for("categories.index"))

    category.name = name
    category.description = description or None
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Nama kategori sudah digunakan.", "danger")
        return redirect(url_for("categories.index"))

    flash("Kategori izin berhasil diperbarui.", "success")
    return redirect(url_for("categories.index"))


@bp.post("/<int:category_id>/toggle-active")
@role_required(User.ROLE_ADMIN)
def toggle_active(category_id):
    category = PermissionCategory.query.get_or_404(category_id)
    category.is_active = not category.is_active
    db.session.commit()

    status = "diaktifkan" if category.is_active else "dinonaktifkan"
    flash(f"Kategori izin berhasil {status}.", "success")
    return redirect(url_for("categories.index"))
