from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import bcrypt, db
from app.models.user import User
from app.utils.validators import validate_new_password

bp = Blueprint("auth", __name__)


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    return redirect(url_for("auth.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        user = User.query.filter_by(username=username, is_deleted=0).first()
        if not user:
            flash("Tài khoản không tồn tại.", "error")
        elif not user.is_active:
            flash("Tài khoản đã bị khóa. Liên hệ quản trị viên.", "error")
        elif not bcrypt.check_password_hash(user.password_hash, password):
            user.login_attempts += 1
            if user.login_attempts >= 5:
                user.is_active = 0
                flash("Tài khoản bị khóa do đăng nhập sai nhiều lần.", "error")
            else:
                remaining = 5 - user.login_attempts
                flash(f"Sai mật khẩu. Còn {remaining} lần thử.", "error")
            db.session.commit()
        else:
            user.login_attempts = 0
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user, remember=remember)
            flash(f"Chào mừng, {user.full_name}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard.index"))

    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Đã đăng xuất.", "info")
    return redirect(url_for("auth.login"))


@bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old_pw = request.form.get("old_password", "")
        new_pw = request.form.get("new_password", "")
        confirm = request.form.get("confirm_password", "")

        if not bcrypt.check_password_hash(current_user.password_hash, old_pw):
            flash("Mật khẩu cũ không đúng.", "error")
        else:
            ok, msg = validate_new_password(new_pw)
            if not ok:
                flash(msg, "error")
            elif new_pw != confirm:
                flash("Xác nhận mật khẩu không khớp.", "error")
            else:
                current_user.password_hash = bcrypt.generate_password_hash(new_pw).decode()
                db.session.commit()
                flash("Đổi mật khẩu thành công.", "success")
                return redirect(url_for("dashboard.index"))

    return render_template("auth/change_password.html")
