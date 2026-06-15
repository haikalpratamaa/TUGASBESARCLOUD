from urllib.parse import urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .services import autentikasi_user


bp = Blueprint("auth", __name__, url_prefix="")


@bp.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for(current_user.dashboard_endpoint()))
    return render_template("auth/login.html", title="Login")


@bp.post("/login")
def proses_login():
    if current_user.is_authenticated:
        return redirect(url_for(current_user.dashboard_endpoint()))

    identifier = request.form.get("identifier")
    password = request.form.get("password")
    remember = request.form.get("remember") == "on"

    if not identifier or not password:
        flash("Email/NIM dan password wajib diisi.", "warning")
        return render_template("auth/login.html", title="Login", identifier=identifier), 400

    user = autentikasi_user(identifier, password)
    if not user:
        flash("Login gagal. Periksa kembali Email/NIM dan password.", "danger")
        return render_template("auth/login.html", title="Login", identifier=identifier), 401

    login_user(user, remember=remember)
    flash("Login berhasil.", "success")

    next_url = request.args.get("next")
    if _next_url_aman(next_url):
        return redirect(next_url)
    return redirect(url_for(user.dashboard_endpoint()))


@bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Anda sudah logout.", "success")
    return redirect(url_for("auth.login"))


def _next_url_aman(next_url):
    if not next_url:
        return False
    parsed = urlparse(next_url)
    return parsed.scheme == "" and parsed.netloc == "" and next_url.startswith("/")
