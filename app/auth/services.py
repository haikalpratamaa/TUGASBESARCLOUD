from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_

from app.models import User


def buat_hash_password(password):
    return generate_password_hash(password)


def cek_password(password_hash, password):
    return check_password_hash(password_hash, password)


def cari_user_untuk_login(identifier):
    identifier = (identifier or "").strip()
    if not identifier:
        return None
    return User.query.filter(
        or_(User.email == identifier, User.student_number == identifier),
        User.is_active.is_(True),
    ).first()


def autentikasi_user(identifier, password):
    user = cari_user_untuk_login(identifier)
    if not user:
        return None
    if not cek_password(user.password_hash, password or ""):
        return None
    return user
