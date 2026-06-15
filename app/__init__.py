from datetime import datetime

from flask import Flask, jsonify, redirect, render_template, url_for
from flask_login import current_user

from .config import get_config
from .extensions import db, login_manager, migrate


def create_app(config_name=None):
    app = Flask(__name__)
    config_obj = get_config(config_name)
    app.config.from_object(config_obj)

    # Print configuration info on startup to verify environment and database
    print(f" * Loaded Configuration: {config_obj.__name__}")
    print(f" * Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    print(f" * Flask Environment: {app.config.get('FLASK_ENV')}")

    _validasi_konfigurasi_wajib(app)
    _inisialisasi_extensions(app)
    _daftarkan_blueprint(app)
    _daftarkan_cli_command(app)
    _daftarkan_route_teknis(app)
    _daftarkan_error_handler(app)
    _daftarkan_context_processor(app)

    return app


def _daftarkan_context_processor(app):
    @app.context_processor
    def inject_greeting():
        hour = datetime.now().hour
        if hour < 11:
            greeting = "Selamat pagi"
        elif hour < 15:
            greeting = "Selamat siang"
        elif hour < 18:
            greeting = "Selamat sore"
        else:
            greeting = "Selamat malam"
        return {"greeting": greeting}


def _inisialisasi_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Silakan login terlebih dahulu."
    login_manager.login_message_category = "warning"


def _daftarkan_blueprint(app):
    from .auth.routes import bp as auth_bp
    from .categories.routes import bp as categories_bp
    from .dashboard.routes import bp as dashboard_bp
    from .email_logs.routes import bp as email_logs_bp
    from .leave_requests.routes import bp as leave_requests_bp
    from .schedules.routes import bp as schedules_bp
    from .users.routes import bp as users_bp
    from .verification.routes import bp as verification_bp
    from .profile.routes import bp as profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(leave_requests_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(schedules_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(verification_bp)
    app.register_blueprint(email_logs_bp)
    app.register_blueprint(profile_bp)


def _daftarkan_route_teknis(app):
    @app.get("/healthz")
    def healthz():
        return jsonify({"status": "ok", "service": "kelaskita"})

    @app.get("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for(current_user.dashboard_endpoint()))
        return render_template("index.html")


def _daftarkan_cli_command(app):
    from .commands import register_commands

    register_commands(app)


def _daftarkan_error_handler(app):
    @app.errorhandler(403)
    def forbidden(error):
        return (
            render_template(
                "errors/error.html",
                title="Akses Ditolak",
                status_code=403,
                message="Anda tidak memiliki akses ke halaman ini.",
            ),
            403,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            render_template(
                "errors/error.html",
                title="Halaman Tidak Ditemukan",
                status_code=404,
                message="Halaman yang Anda cari tidak ditemukan.",
            ),
            404,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            render_template(
                "errors/error.html",
                title="Terjadi Kesalahan",
                status_code=500,
                message="Sistem sedang mengalami gangguan. Silakan coba lagi nanti.",
            ),
            500,
        )


def _validasi_konfigurasi_wajib(app):
    if app.config["FLASK_ENV"] == "production":
        konfigurasi_kosong = [
            nama
            for nama in ("SECRET_KEY", "SQLALCHEMY_DATABASE_URI")
            if not app.config.get(nama)
        ]
        if konfigurasi_kosong:
            daftar = ", ".join(konfigurasi_kosong)
            raise RuntimeError(f"Konfigurasi production wajib diisi: {daftar}")
