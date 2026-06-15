import logging
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage

from flask import current_app

from app.extensions import db
from app.models import EmailLog

logger = logging.getLogger(__name__)


def kirim_email_notifikasi(recipient_email, subject, body):
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = _format_pengirim()
    message["To"] = recipient_email
    message.set_content(body)

    with smtplib.SMTP(
        current_app.config["SMTP_HOST"],
        current_app.config["SMTP_PORT"],
        timeout=10,
    ) as smtp:
        if current_app.config["SMTP_USE_TLS"]:
            smtp.starttls()
        if current_app.config["SMTP_USERNAME"]:
            smtp.login(
                current_app.config["SMTP_USERNAME"],
                current_app.config["SMTP_PASSWORD"],
            )
        smtp.send_message(message)


def kirim_dan_catat_email(leave_request_id, recipient_email, subject, body, template_name):
    log = EmailLog(
        leave_request_id=leave_request_id,
        recipient_email=recipient_email,
        subject=subject,
        template_name=template_name,
        status=EmailLog.STATUS_PENDING,
    )
    db.session.add(log)
    db.session.flush()

    try:
        kirim_email_notifikasi(recipient_email, subject, body)
        log.status = EmailLog.STATUS_SENT
        log.sent_at = datetime.now(timezone.utc)
    except Exception as e:
        log.status = EmailLog.STATUS_FAILED
        log.error_message = str(e)[:500]
        logger.warning("Gagal mengirim email ke %s: %s", recipient_email, e)

    db.session.commit()
    return log


def _format_pengirim():
    name = current_app.config["MAIL_FROM_NAME"]
    email = current_app.config["MAIL_FROM_EMAIL"]
    if name and email:
        return f"{name} <{email}>"
    return email or "noreply@kelaskita.local"
