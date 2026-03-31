from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.config import Config
from app.extensions import db
from app.models.booking import Booking
from app.models.customer import Customer
from app.services.image_service import ImageService
from app.utils.decorators import admin_required

bp = Blueprint("customers", __name__, url_prefix="/customers")


@bp.route("/")
@login_required
def index():
    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)

    query = Customer.query.filter_by(is_deleted=0)
    if q:
        like = f"%{q}%"
        query = query.filter((Customer.full_name.like(like)) | (Customer.id_number.like(like)) | (Customer.phone.like(like)))

    customers = query.order_by(Customer.created_at.desc()).paginate(page=page, per_page=Config.PER_PAGE, error_out=False)
    return render_template("customers/index.html", customers=customers)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        id_number = request.form.get("id_number", "").strip()
        if not full_name or not id_number:
            flash("Vui lòng nhập họ tên và giấy tờ.", "error")
            return redirect(url_for("customers.create"))

        if Customer.query.filter_by(id_number=id_number).first():
            flash("Số giấy tờ đã tồn tại.", "error")
            return redirect(url_for("customers.create"))

        c = Customer(
            full_name=full_name,
            id_number=id_number,
            id_type=request.form.get("id_type") or "CCCD",
            gender=request.form.get("gender") or "MALE",
            date_of_birth=datetime.strptime(request.form.get("date_of_birth"), "%Y-%m-%d").date()
            if request.form.get("date_of_birth")
            else None,
            phone=request.form.get("phone") or None,
            email=request.form.get("email") or None,
            nationality=request.form.get("nationality") or "Việt Nam",
            address=request.form.get("address"),
            notes=request.form.get("notes"),
        )
        db.session.add(c)
        db.session.flush()

        avatar = request.files.get("avatar")
        if avatar and avatar.filename:
            c.avatar_path = ImageService.save_avatar(avatar, "customer", c.id)

        db.session.commit()
        flash("Thêm khách hàng thành công.", "success")
        return redirect(url_for("customers.index"))

    return render_template("customers/form.html", customer=None)


@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    c = Customer.query.get_or_404(id)
    if c.is_deleted:
        flash("Khách hàng đã bị xóa.", "error")
        return redirect(url_for("customers.index"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        id_number = request.form.get("id_number", "").strip()
        if not full_name or not id_number:
            flash("Vui lòng nhập họ tên và giấy tờ.", "error")
            return redirect(url_for("customers.edit", id=id))

        exists = Customer.query.filter(Customer.id_number == id_number, Customer.id != id).first()
        if exists:
            flash("Số giấy tờ đã tồn tại.", "error")
            return redirect(url_for("customers.edit", id=id))

        c.full_name = full_name
        c.id_number = id_number
        c.id_type = request.form.get("id_type") or c.id_type
        c.gender = request.form.get("gender") or c.gender
        c.date_of_birth = (
            datetime.strptime(request.form.get("date_of_birth"), "%Y-%m-%d").date()
            if request.form.get("date_of_birth")
            else None
        )
        c.phone = request.form.get("phone") or None
        c.email = request.form.get("email") or None
        c.nationality = request.form.get("nationality") or "Việt Nam"
        c.address = request.form.get("address")
        c.notes = request.form.get("notes")

        avatar = request.files.get("avatar")
        if avatar and avatar.filename:
            old = c.avatar_path
            c.avatar_path = ImageService.save_avatar(avatar, "customer", c.id)
            if old and old != c.avatar_path:
                ImageService.delete(old)

        db.session.commit()
        flash("Cập nhật khách hàng thành công.", "success")
        return redirect(url_for("customers.index"))

    return render_template("customers/form.html", customer=c)


@bp.route("/<int:id>")
@login_required
def detail(id):
    c = Customer.query.get_or_404(id)
    bookings = (
        Booking.query.filter_by(customer_id=id, is_deleted=0)
        .order_by(Booking.created_at.desc())
        .limit(50)
        .all()
    )
    return render_template("customers/detail.html", customer=c, bookings=bookings)


@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
@admin_required
def delete(id):
    c = Customer.query.get_or_404(id)
    has_active = (
        Booking.query.filter(
            Booking.customer_id == id,
            Booking.is_deleted == 0,
            Booking.status.in_(["PENDING", "CONFIRMED", "CHECKED_IN"]),
        ).count()
        > 0
    )
    if has_active:
        return jsonify({"success": False, "message": "Không thể xóa: khách có booking active."})
    c.soft_delete()
    db.session.commit()
    return jsonify({"success": True, "message": "Đã xóa khách hàng."})
