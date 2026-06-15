from datetime import time
import click
from flask.cli import with_appcontext

from .auth.services import buat_hash_password
from .extensions import db
from .models import User, ClassSchedule, PermissionCategory


def register_commands(app):
    app.cli.add_command(seed_users)
    app.cli.add_command(seed_schedules)
    app.cli.add_command(seed_categories)


@click.command("seed-users")
@with_appcontext
def seed_users():
    users = [
        {
            "name": "Admin KelasKita",
            "email": "admin@kelaskita.local",
            "password": "admin123",
            "role": User.ROLE_ADMIN,
        },
        {
            "name": "Dosen Demo",
            "email": "dosen@kelaskita.local",
            "password": "dosen123",
            "role": User.ROLE_DOSEN,
            "lecturer_code": "DSN001",
        },
        {
            "name": "Mahasiswa Demo",
            "email": "mahasiswa@kelaskita.local",
            "password": "mhs12345",
            "role": User.ROLE_MAHASISWA,
            "student_number": "20260001",
        },
    ]

    created_count = 0
    for data in users:
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            continue

        password = data.pop("password")
        user = User(**data)
        user.password_hash = buat_hash_password(password)
        db.session.add(user)
        created_count += 1

    db.session.commit()
    click.echo(f"Seed user selesai. User baru: {created_count}")


@click.command("seed-schedules")
@with_appcontext
def seed_schedules():
    dosen = User.query.filter_by(role=User.ROLE_DOSEN).first()
    if not dosen:
        click.echo("Dosen belum ada. Silakan jalankan 'flask seed-users' dulu.")
        return

    schedules = [
        # Senin
        {
            "course_name": "APLIKASI PERANGKAT BERGERAK",
            "class_name": "Reguler A",
            "lecturer_id": dosen.id,
            "day": "Senin",
            "start_time": time(9, 30),
            "end_time": time(12, 30),
            "room": "APDEV LAB."
        },
        {
            "course_name": "METODOLOGI PENELITIAN DAN TATA TULIS ILMIAH",
            "class_name": "Reguler A",
            "lecturer_id": dosen.id,
            "day": "Senin",
            "start_time": time(12, 30),
            "end_time": time(14, 30),
            "room": "KTT1.22"
        },
        # Selasa
        {
            "course_name": "KOMPUTASI AWAN DAN VIRTUALISASI",
            "class_name": "Reguler A",
            "lecturer_id": dosen.id,
            "day": "Selasa",
            "start_time": time(9, 30),
            "end_time": time(12, 30),
            "room": "KTT2.17"
        },
        {
            "course_name": "PENGUJIAN PENETRASI DAN ETIKA PERETASAN",
            "class_name": "Reguler A",
            "lecturer_id": dosen.id,
            "day": "Selasa",
            "start_time": time(13, 30),
            "end_time": time(16, 30),
            "room": "KTT2.17"
        },
        # Rabu
        {
            "course_name": "PENGOLAHAN CITRA DIGITAL",
            "class_name": "Reguler A",
            "lecturer_id": dosen.id,
            "day": "Rabu",
            "start_time": time(9, 30),
            "end_time": time(12, 30),
            "room": "KTT2.16"
        },
        # Kamis
        {
            "course_name": "MANAJEMEN PROYEK",
            "class_name": "Reguler A",
            "lecturer_id": dosen.id,
            "day": "Kamis",
            "start_time": time(12, 30),
            "end_time": time(15, 30),
            "room": "KTT B-1.05"
        },
        # Jumat
        {
            "course_name": "KEWARGANEGARAAN",
            "class_name": "Reguler A",
            "lecturer_id": dosen.id,
            "day": "Jumat",
            "start_time": time(7, 30),
            "end_time": time(9, 30),
            "room": "KTT1.07"
        },
        {
            "course_name": "ARSITEKTUR INTEGRASI SISTEM",
            "class_name": "Reguler A",
            "lecturer_id": dosen.id,
            "day": "Jumat",
            "start_time": time(13, 30),
            "end_time": time(16, 30),
            "room": "KTT2.17"
        }
    ]

    created_count = 0
    for data in schedules:
        existing = ClassSchedule.query.filter_by(
            course_name=data["course_name"],
            day=data["day"],
            start_time=data["start_time"]
        ).first()
        if not existing:
            schedule = ClassSchedule(**data)
            db.session.add(schedule)
            created_count += 1
            
    db.session.commit()
    click.echo(f"Seed jadwal selesai. Jadwal baru: {created_count}")


@click.command("seed-categories")
@with_appcontext
def seed_categories():
    categories = [
        {"name": "Sakit", "description": "Izin tidak masuk karena alasan kesehatan dan memiliki surat dokter atau bukti pendukung lainnya."},
        {"name": "Izin", "description": "Izin karena keperluan mendesak atau halangan keluarga yang tidak bisa ditinggalkan."},
        {"name": "Kegiatan Kampus", "description": "Dispensasi karena mewakili kampus dalam lomba, organisasi, atau acara resmi kemahasiswaan."},
        {"name": "Lainnya", "description": "Alasan izin lain yang tidak termasuk dalam kategori di atas."}
    ]

    created_count = 0
    for data in categories:
        existing = PermissionCategory.query.filter_by(name=data["name"]).first()
        if not existing:
            category = PermissionCategory(**data)
            db.session.add(category)
            created_count += 1
            
    db.session.commit()
    click.echo(f"Seed kategori selesai. Kategori baru: {created_count}")
