import os

from dotenv import load_dotenv


load_dotenv()


# ---------------------------------------------------------------------------
# Lokasi database SQLite default untuk development lokal.
# Menggunakan path absolut agar tidak bergantung pada working directory.
# ---------------------------------------------------------------------------
_BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SQLITE_DEV = "sqlite:///" + os.path.join(_BASEDIR, "instance", "kelaskita.db")


def _env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class BaseConfig:
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    SECRET_KEY = os.getenv("SECRET_KEY")
    APP_URL = os.getenv("APP_URL", "http://localhost:5000")
    PORT = int(os.getenv("PORT", "5000"))
    
    # Upload Configurations
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB max file size
    UPLOAD_FOLDER = os.path.join(_BASEDIR, "app", "static", "uploads", "profiles")

    # Default ke SQLite lokal agar tidak pernah error saat DATABASE_URL kosong.
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", _SQLITE_DEV)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }

    CLOUD_SQL_CONNECTION_NAME = os.getenv("CLOUD_SQL_CONNECTION_NAME")

    MAIL_PROVIDER = os.getenv("MAIL_PROVIDER", "smtp")
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "KelasKita")
    MAIL_FROM_EMAIL = os.getenv("MAIL_FROM_EMAIL")
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_USE_TLS = _env_bool("SMTP_USE_TLS", True)


class DevelopmentConfig(BaseConfig):
    FLASK_ENV = "development"
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "local-development-secret")

    # ⚡ HARDCODE SQLite — tidak pernah membaca DATABASE_URL.
    # Jika ingin pakai MySQL lokal, set DEV_DATABASE_URL secara eksplisit.
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL", _SQLITE_DEV)


class ProductionConfig(BaseConfig):
    FLASK_ENV = "production"
    DEBUG = False


class TestingConfig(BaseConfig):
    FLASK_ENV = "testing"
    TESTING = True
    SECRET_KEY = os.getenv("SECRET_KEY", "testing-secret")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        _BASEDIR, "instance", "kelaskita_test.db"
    )


def get_config(config_name=None):
    selected = (config_name or os.getenv("FLASK_ENV", "production")).lower()
    configs = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    return configs.get(selected, ProductionConfig)
