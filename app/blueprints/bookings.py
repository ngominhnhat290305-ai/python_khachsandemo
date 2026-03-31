from datetime import date, datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models.booking import Booking
from app.models.customer import Customer
from app.models.room import Room
from app.models.service import BookingService, Service
from app.services.booking_service import cancel_booking, create_booking, do_check_in, do_check_out, do_confirm
from app.utils.decorators import admin_required
from app.utils.validators import parse_money

bp = Blueprint("bookings", __name__, url_prefix="/bookings")


def _can_view_booking(b: Booking) -> bool:
    if current_user.is_admin:
        return True
    today = date.today()
    return b.created_by == current_user.id or b.check_in_date == today or b.check_out_date == today


@bp.route("/")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    status = request.args.get("status")
    date_in = request.args.get("check_in")

    q = Booking.query.filter_by(is_deleted=0)
    if not current_user.is_admin:
        today = date.today()
        q = q.filter(
            (Booking.created_by == current_user.id)
            | (Booking.check_in_date == today)
            | (Booking.check_out_date == today)
        )
    if status:
        q = q.filter(Booking.status == status)
    if date_in:
        try:
            d = datetime.strptime(date_in, "%Y-%m-%d").date()
            q = q.filter(Booking.check_in_date == d)
        except ValueError:
            pass

    bookings = q.order_by(Booking.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template("bookings/index.html", bookings=bookings)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        try:
            check_in = datetime.strptime(request.form["check_in_date"], "%Y-%m-%d").date()
            check_out = datetime.strptime(request.form["check_out_date"], "%Y-%m-%d").date()
        except Exception:
            flash("Ngày nhận/trả phòng không hợp lệ.", "error")
            return redirect(url_for("bookings.create"))

        ok, msg, booking = create_booking(
            customer_id=int(request.form["customer_id"]),
            room_id=int(request.form["room_id"]),
            created_by=current_user.id,
            check_in=check_in,
            check_out=check_out,
            num_adults=int(request.form.get("num_adults", 1)),
            num_children=int(request.form.get("num_children", 0)),
            deposit=parse_money(request.form.get("deposit_amount")),
            special_requests=request.form.get("special_requests"),
            status="PENDING",
        )
        if ok and booking:
            flash(f"Đặt phòng thành công! Mã: {booking.booking_code}", "success")
            return redirect(url_for("bookings.detail", id=booking.id))
        flash(msg, "error")

    customers = Customer.query.filter_by(is_deleted=0).order_by(Customer.full_name).all()
    rooms = Room.query.filter_by(is_deleted=0, status="AVAILABLE").order_by(Room.floor, Room.room_number).all()
    return render_template("bookings/form.html", customers=customers, rooms=rooms)


@bp.route("/<int:id>")
@login_required
def detail(id):
    booking = Booking.query.get_or_404(id)
    if not _can_view_booking(booking):
        return redirect(url_for("bookings.index"))
    services = Service.query.filter_by(is_deleted=0).order_by(Service.name).all()
    return render_template("bookings/detail.html", booking=booking, services=services)


@bp.route("/<int:id>/confirm", methods=["POST"])
@login_required
@admin_required
def confirm(id):
    ok, msg = do_confirm(id)
    return jsonify({"success": ok, "message": msg})


@bp.route("/<int:id>/checkin", methods=["POST"])
@login_required
def checkin(id):
    booking = Booking.query.get_or_404(id)
    if not _can_view_booking(booking):
        return jsonify({"success": False, "message": "Không có quyền."})
    ok, msg = do_check_in(id)
    return jsonify({"success": ok, "message": msg})


@bp.route("/<int:id>/checkout", methods=["POST"])
@login_required
def checkout(id):
    booking = Booking.query.get_or_404(id)
    if not _can_view_booking(booking):
        return jsonify({"success": False, "message": "Không có quyền."})
    ok, msg, invoice = do_check_out(id)
    if ok and invoice:
        return jsonify({"success": True, "message": msg, "redirect": url_for("invoices.detail", id=invoice.id)})
    return jsonify({"success": False, "message": msg})


@bp.route("/<int:id>/cancel", methods=["POST"])
@login_required
def cancel(id):
    booking = Booking.query.get_or_404(id)
    if not current_user.is_admin and booking.created_by != current_user.id:
        return jsonify({"success": False, "message": "Bạn chỉ được huỷ booking của mình."})
    reason = (request.json or {}).get("reason", "")
    ok, msg = cancel_booking(id, reason)
    return jsonify({"success": ok, "message": msg})


@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
@admin_required
def delete(id):
    booking = Booking.query.get_or_404(id)
    booking.soft_delete()
    db.session.commit()
    return jsonify({"success": True, "message": "Đã xóa booking."})


@bp.route("/<int:id>/services/add", methods=["POST"])
@login_required
def add_service(id):
    booking = Booking.query.get_or_404(id)
    if not _can_view_booking(booking):
        flash("Không có quyền.", "error")
        return redirect(url_for("bookings.detail", id=id))
    if booking.status != "CHECKED_IN":
        flash("Chỉ thêm dịch vụ khi khách đang ở (CHECKED_IN).", "error")
        return redirect(url_for("bookings.detail", id=id))

    service_id = int(request.form["service_id"])
    quantity = int(request.form.get("quantity", 1))
    service = Service.query.get(service_id)
    if not service or service.is_deleted:
        flash("Dịch vụ không tồn tại.", "error")
        return redirect(url_for("bookings.detail", id=id))

    bs = BookingService(
        booking_id=id,
        service_id=service_id,
        quantity=quantity,
        unit_price=service.unit_price,
        total_price=float(service.unit_price) * quantity,
    )
    db.session.add(bs)
    db.session.commit()
    flash(f"Đã thêm dịch vụ: {service.name}", "success")
    return redirect(url_for("bookings.detail", id=id))


@bp.route("/<int:id>/services/<int:bs_id>/remove", methods=["POST"])
@login_required
def remove_service(id, bs_id):
    booking = Booking.query.get_or_404(id)
    if not _can_view_booking(booking):
        flash("Không có quyền.", "error")
        return redirect(url_for("bookings.detail", id=id))
    if booking.status != "CHECKED_IN":
        flash("Chỉ xóa dịch vụ khi khách đang ở (CHECKED_IN).", "error")
        return redirect(url_for("bookings.detail", id=id))
    bs = BookingService.query.get_or_404(bs_id)
    if bs.booking_id != id:
        flash("Dữ liệu không hợp lệ.", "error")
        return redirect(url_for("bookings.detail", id=id))
    db.session.delete(bs)
    db.session.commit()
    flash("Đã xóa dịch vụ.", "success")
    return redirect(url_for("bookings.detail", id=id))


@bp.route("/available-rooms")
@login_required
def available_rooms():
    check_in = request.args.get("check_in")
    check_out = request.args.get("check_out")
    try:
        d_in = datetime.strptime(check_in, "%Y-%m-%d").date()
        d_out = datetime.strptime(check_out, "%Y-%m-%d").date()
    except Exception:
        return jsonify([])

    booked_ids = [
        b.room_id
        for b in Booking.query.filter(
            Booking.is_deleted == 0,
            Booking.status.in_(["PENDING", "CONFIRMED", "CHECKED_IN"]),
            Booking.check_in_date < d_out,
            Booking.check_out_date > d_in,
        ).all()
    ]

    q = Room.query.filter(Room.is_deleted == 0, Room.status == "AVAILABLE")
    if booked_ids:
        q = q.filter(~Room.id.in_(booked_ids))
    rooms = q.order_by(Room.floor, Room.room_number).all()
    return jsonify(
        [
            {
                "id": r.id,
                "room_number": r.room_number,
                "floor": r.floor,
                "bed_type": r.bed_type,
                "room_type": r.room_type.name if r.room_type else "",
                "price": r.effective_price,
            }
            for r in rooms
        ]
    )


@bp.route("/calendar")
@login_required
def calendar():
    return render_template("bookings/calendar.html")
