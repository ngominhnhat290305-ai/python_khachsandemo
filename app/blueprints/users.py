import secrets
import string

from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify
from flask_login import current_user, login_required

from app.extensions import bcrypt, db
from app.models.booking import Booking
from app.models.user import User
from app.services.image_service import ImageService
from app.utils.decorators import admin_required
from app.utils.validators import validate_new_password

bp = Blueprint("users", __name__, url_prefix="/users")


def _generate_temp_password(length: int = 10) -> str:
    alphabet = string.ascii_letters + string.digits
    while True:
        pw = "".join(secrets.choice(alphabet) for _ in range(length))
        ok, _ = validate_new_password(pw)
        if ok:
            return pw


@bp.route("/")
@login_required
@admin_required
def index():
    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)

    query = User.query.filter_by(is_deleted=0)
    if q:
        like = f"%{q}%"
        query = query.filter((User.username.like(like)) | (User.full_name.like(like)))

    users = query.order_by(User.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template("users/index.html", users=users)


@bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        full_name = request.form.get("full_name", "").strip()
        role = request.form.get("role", "RECEPTIONIST")
        phone = request.form.get("phone", "").strip() or None
        email = request.form.get("email", "").strip() or None
        password = request.form.get("password", "")

        if not username or not full_name:
            flash("Vui lòng nhập username và họ tên.", "error")
            return redirect(url_for("users.create"))
        if role not in ("ADMIN", "RECEPTIONIST"):
            flash("Role không hợp lệ.", "error")
            return redirect(url_for("users.create"))
        if User.query.filter_by(username=username).first():
            flash("Username đã tồn tại.", "error")
            return redirect(url_for("users.create"))

        temp_pw = None
        if not password:
            temp_pw = _generate_temp_password()
            password = temp_pw
        ok, msg = validate_new_password(password)
        if not ok:
            flash(msg, "error")
            return redirect(url_for("users.create"))

        user = User(
            username=username,
            full_name=full_name,
            role=role,
            phone=phone,
            email=email,
            password_hash=bcrypt.generate_password_hash(password).decode(),
        )
        db.session.add(user)
        db.session.flush()

        avatar = request.files.get("avatar")
        if avatar and avatar.filename:
            user.avatar_path = ImageService.save_avatar(avatar, "user", user.id)

        db.session.commit()
        if temp_pw:
            flash(f"Tạo nhân viên thành công. Mật khẩu tạm: {temp_pw}", "success")
        else:
            flash("Tạo nhân viên thành công.", "success")
        return redirect(url_for("users.index"))

    return render_template("users/form.html", user=None)


@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit(id):
    user = User.query.get_or_404(id)
    if user.is_deleted:
        flash("Nhân viên đã bị xóa.", "error")
        return redirect(url_for("users.index"))

    if request.method == "POST":
        user.full_name = request.form.get("full_name", "").strip() or user.full_name
        user.phone = request.form.get("phone", "").strip() or None
        user.email = request.form.get("email", "").strip() or None

        if user.id != current_user.id:
            role = request.form.get("role", user.role)
            if role in ("ADMIN", "RECEPTIONIST"):
                user.role = role

        avatar = request.files.get("avatar")
        if avatar and avatar.filename:
            old = user.avatar_path
            user.avatar_path = ImageService.save_avatar(avatar, "user", user.id)
            if old and old != user.avatar_path:
                ImageService.delete(old)

        db.session.commit()
        flash("Cập nhật nhân viên thành công.", "success")
        return redirect(url_for("users.index"))

    return render_template("users/form.html", user=user)


@bp.route("/<int:id>/toggle-active", methods=["POST"])
@login_required
@admin_required
def toggle_active(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        return jsonify({"success": False, "message": "Không thể khóa/mở chính mình."})
    user.is_active = 0 if user.is_active else 1
    if user.is_active:
        user.login_attempts = 0
    db.session.commit()
    return jsonify({"success": True, "message": "Cập nhật trạng thái thành công."})


@bp.route("/<int:id>/reset-password", methods=["POST"])
@login_required
@admin_required
def reset_password(id):
    user = User.query.get_or_404(id)
    if user.is_deleted:
        return jsonify({"success": False, "message": "Nhân viên đã bị xóa."})
    temp_pw = _generate_temp_password()
    user.password_hash = bcrypt.generate_password_hash(temp_pw).decode()
    user.login_attempts = 0
    user.is_active = 1
    db.session.commit()
    return jsonify({"success": True, "message": f"Đã reset mật khẩu. Mật khẩu mới: {temp_pw}"})


@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
@admin_required
def delete(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        return jsonify({"success": False, "message": "Không thể xóa chính mình."})

    has_active = (
        Booking.query.filter(
            Booking.created_by == id,
            Booking.is_deleted == 0,
            Booking.status == "CHECKED_IN",
        ).count()
        > 0
    )
    if has_active:
        return jsonify({"success": False, "message": "Không thể xóa: có booking CHECKED_IN đang quản lý."})

    user.soft_delete()
    db.session.commit()
    return jsonify({"success": True, "message": "Đã xóa nhân viên."})
