from flask import Blueprint, render_template, request

from app.models import EmailLog, User
from app.utils.decorators import role_required


bp = Blueprint("email_logs", __name__, url_prefix="")


@bp.get("/admin/email-logs")
@role_required(User.ROLE_ADMIN)
def index():
    status_filter = request.args.get("status")
    query = EmailLog.query

    if status_filter and status_filter in (
        EmailLog.STATUS_SENT,
        EmailLog.STATUS_FAILED,
        EmailLog.STATUS_PENDING,
    ):
        query = query.filter_by(status=status_filter)

    logs = query.order_by(EmailLog.created_at.desc()).limit(100).all()

    return render_template(
        "email_logs/index.html",
        title="Email Log",
        logs=logs,
        status_filter=status_filter,
    )
