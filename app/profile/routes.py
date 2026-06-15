import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.profile import bp


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")

        if not name:
            flash("Nama tidak boleh kosong.", "error")
            return redirect(url_for("profile.index"))

        current_user.name = name
        current_user.phone = phone

        # Handle profile picture upload
        if "profile_picture" in request.files:
            file = request.files["profile_picture"]
            if file and file.filename != "":
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    ext = filename.rsplit(".", 1)[1].lower()
                    
                    # Generate unique filename
                    unique_filename = f"{current_user.id}_{uuid.uuid4().hex[:8]}.{ext}"
                    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_filename)
                    
                    # Ensure directory exists
                    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
                    
                    # Save new file
                    file.save(filepath)

                    # Delete old file if exists
                    if current_user.profile_picture:
                        old_filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], current_user.profile_picture)
                        if os.path.exists(old_filepath):
                            try:
                                os.remove(old_filepath)
                            except OSError:
                                pass

                    current_user.profile_picture = unique_filename
                else:
                    flash("Format file tidak didukung. Gunakan JPG atau PNG.", "error")
                    return redirect(url_for("profile.index"))

        try:
            db.session.commit()
            flash("Profil berhasil diperbarui.", "success")
        except Exception as e:
            db.session.rollback()
            flash("Terjadi kesalahan saat menyimpan profil.", "error")
            
        return redirect(url_for("profile.index"))

    return render_template("profile/index.html", title="Profil Saya")
