from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required

from app.config import Config
from app.extensions import db
from app.models.booking import Booking
from app.models.service import BookingService, Service
from app.utils.decorators import admin_required
from app.utils.validators import parse_money

bp = Blueprint("services", __name__, url_prefix="/services")


@bp.route("/")
@login_required
@admin_required
def index():
    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    query = Service.query.filter_by(is_deleted=0)
    if q:
        query = query.filter(Service.name.like(f"%{q}%"))
    services = query.order_by(Service.created_at.desc()).paginate(page=page, per_page=Config.PER_PAGE, error_out=False)
    return render_template("services/index.html", services=services)


@bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Vui lòng nhập tên dịch vụ.", "error")
            return redirect(url_for("services.create"))

        s = Service(
            name=name,
            category=request.form.get("category") or "OTHER",
            unit_price=parse_money(request.form.get("unit_price")),
            unit=request.form.get("unit") or "lần",
            description=request.form.get("description"),
        )
        db.session.add(s)
        db.session.commit()
        flash("Thêm dịch vụ thành công.", "success")
        return redirect(url_for("services.index"))
    return render_template("services/form.html", service=None)


@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit(id):
    s = Service.query.get_or_404(id)
    if s.is_deleted:
        flash("Dịch vụ đã bị xóa.", "error")
        return redirect(url_for("services.index"))

    if request.method == "POST":
        s.name = request.form.get("name", "").strip() or s.name
        s.category = request.form.get("category") or s.category
        s.unit_price = parse_money(request.form.get("unit_price"))
        s.unit = request.form.get("unit") or s.unit
        s.description = request.form.get("description")
        db.session.commit()
        flash("Cập nhật dịch vụ thành công.", "success")
        return redirect(url_for("services.index"))

    return render_template("services/form.html", service=s)


@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
@admin_required
def delete(id):
    s = Service.query.get_or_404(id)
    active_bs = (
        db.session.query(BookingService.id)
        .join(Booking, BookingService.booking_id == Booking.id)
        .filter(
            BookingService.service_id == id,
            Booking.is_deleted == 0,
            Booking.status.in_(["PENDING", "CONFIRMED", "CHECKED_IN"]),
        )
        .first()
        is not None
    )
    if active_bs:
        return jsonify({"success": False, "message": "Không thể xóa: dịch vụ đang dùng trong booking active."})
    s.soft_delete()
    db.session.commit()
    return jsonify({"success": True, "message": "Đã xóa dịch vụ."})
