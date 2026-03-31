from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.services.image_service import ImageService

bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        current_user.full_name = request.form.get("full_name", "").strip() or current_user.full_name
        current_user.phone = request.form.get("phone", "").strip() or None
        current_user.email = request.form.get("email", "").strip() or None

        avatar = request.files.get("avatar")
        if avatar and avatar.filename:
            old = current_user.avatar_path
            path = ImageService.save_avatar(avatar, "user", current_user.id)
            current_user.avatar_path = path
            if old and old != path:
                ImageService.delete(old)

        db.session.commit()
        flash("Cập nhật thông tin cá nhân thành công.", "success")
        return redirect(url_for("profile.index"))

    return render_template("profile/index.html")
