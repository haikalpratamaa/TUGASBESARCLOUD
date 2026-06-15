from flask_login import UserMixin

from .extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )


class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "users"

    ROLE_MAHASISWA = "mahasiswa"
    ROLE_DOSEN = "dosen"
    ROLE_ADMIN = "admin"
    ROLES = (ROLE_MAHASISWA, ROLE_DOSEN, ROLE_ADMIN)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(*ROLES, name="user_role"), nullable=False, index=True)
    student_number = db.Column(db.String(40), unique=True, nullable=True, index=True)
    lecturer_code = db.Column(db.String(40), unique=True, nullable=True, index=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True, index=True)

    def punya_role(self, role):
        return self.role == role

    def dashboard_endpoint(self):
        mapping = {
            self.ROLE_MAHASISWA: "dashboard.mahasiswa",
            self.ROLE_DOSEN: "dashboard.dosen",
            self.ROLE_ADMIN: "dashboard.admin",
        }
        return mapping.get(self.role, "auth.login")


class PermissionCategory(TimestampMixin, db.Model):
    __tablename__ = "permission_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True, index=True)


class ClassSchedule(TimestampMixin, db.Model):
    __tablename__ = "class_schedules"

    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(150), nullable=False, index=True)
    class_name = db.Column(db.String(80), nullable=False, index=True)
    lecturer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    day = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    room = db.Column(db.String(80), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True, index=True)

    lecturer = db.relationship("User", backref=db.backref("class_schedules", lazy=True))


class LeaveRequest(TimestampMixin, db.Model):
    __tablename__ = "leave_requests"

    STATUS_DIAJUKAN = "diajukan"
    STATUS_DISETUJUI = "disetujui"
    STATUS_DITOLAK = "ditolak"
    STATUS_DIBATALKAN = "dibatalkan"
    STATUSES = (STATUS_DIAJUKAN, STATUS_DISETUJUI, STATUS_DITOLAK, STATUS_DIBATALKAN)

    id = db.Column(db.Integer, primary_key=True)
    request_number = db.Column(db.String(30), nullable=False, unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey("class_schedules.id"), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("permission_categories.id"), nullable=False, index=True)
    permission_date = db.Column(db.Date, nullable=False, index=True)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum(*STATUSES, name="leave_status"),
        nullable=False,
        default=STATUS_DIAJUKAN,
        index=True,
    )
    admin_note = db.Column(db.Text, nullable=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    verification_token = db.Column(db.String(64), nullable=False, unique=True, index=True)
    email_notified_at = db.Column(db.DateTime, nullable=True)

    student = db.relationship("User", foreign_keys=[user_id], backref=db.backref("leave_requests", lazy=True))
    reviewer = db.relationship("User", foreign_keys=[reviewed_by])
    schedule = db.relationship("ClassSchedule", backref=db.backref("leave_requests", lazy=True))
    category = db.relationship("PermissionCategory", backref=db.backref("leave_requests", lazy=True))

    def bisa_diedit(self):
        return self.status == self.STATUS_DIAJUKAN

    def bisa_dibatalkan(self):
        return self.status == self.STATUS_DIAJUKAN

    def bisa_diproses(self):
        return self.status == self.STATUS_DIAJUKAN

    def bisa_dicetak(self):
        return self.status == self.STATUS_DISETUJUI

    def label_status(self):
        mapping = {
            self.STATUS_DIAJUKAN: "Diajukan",
            self.STATUS_DISETUJUI: "Disetujui",
            self.STATUS_DITOLAK: "Ditolak",
            self.STATUS_DIBATALKAN: "Dibatalkan",
        }
        return mapping.get(self.status, self.status)

    def css_status(self):
        mapping = {
            self.STATUS_DIAJUKAN: "warning",
            self.STATUS_DISETUJUI: "success",
            self.STATUS_DITOLAK: "danger",
            self.STATUS_DIBATALKAN: "muted",
        }
        return mapping.get(self.status, "muted")


class EmailLog(db.Model):
    __tablename__ = "email_logs"

    STATUS_PENDING = "pending"
    STATUS_SENT = "sent"
    STATUS_FAILED = "failed"

    id = db.Column(db.Integer, primary_key=True)
    leave_request_id = db.Column(db.Integer, db.ForeignKey("leave_requests.id"), nullable=False, index=True)
    recipient_email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    template_name = db.Column(db.String(80), nullable=False)
    status = db.Column(
        db.Enum(STATUS_PENDING, STATUS_SENT, STATUS_FAILED, name="email_status"),
        nullable=False,
        default=STATUS_PENDING,
    )
    error_message = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    leave_request = db.relationship("LeaveRequest", backref=db.backref("email_logs", lazy=True))


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    action = db.Column(db.String(80), nullable=False)
    entity_type = db.Column(db.String(80), nullable=False)
    entity_id = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    user = db.relationship("User", backref=db.backref("audit_logs", lazy=True))
