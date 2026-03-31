from datetime import date

from flask import Blueprint, render_template
from flask_login import current_user, login_required
from sqlalchemy import func

from app.models.booking import Booking
from app.models.invoice import Invoice
from app.models.room import Room

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard")
@login_required
def index():
    today = date.today()

    total_rooms = Room.query.filter_by(is_deleted=0).count()
    available = Room.query.filter_by(is_deleted=0, status="AVAILABLE").count()
    occupied = Room.query.filter_by(is_deleted=0, status="OCCUPIED").count()
    maintenance = Room.query.filter_by(is_deleted=0, status="MAINTENANCE").count()

    checkins_today = Booking.query.filter(
        Booking.is_deleted == 0,
        Booking.check_in_date == today,
        Booking.status.in_(["CONFIRMED", "PENDING"]),
    ).all()

    checkouts_today = Booking.query.filter(
        Booking.is_deleted == 0,
        Booking.check_out_date == today,
        Booking.status == "CHECKED_IN",
    ).all()

    month_revenue = (
        Invoice.query.filter(
            Invoice.payment_status == "PAID",
            func.month(Invoice.paid_at) == today.month,
            func.year(Invoice.paid_at) == today.year,
        )
        .with_entities(func.sum(Invoice.total_amount))
        .scalar()
        or 0
    )

    chart_labels = []
    chart_data = []
    for m in range(1, 13):
        rev = (
            Invoice.query.filter(
                Invoice.payment_status == "PAID",
                func.month(Invoice.paid_at) == m,
                func.year(Invoice.paid_at) == today.year,
            )
            .with_entities(func.sum(Invoice.total_amount))
            .scalar()
            or 0
        )
        chart_labels.append(f"T{m}")
        chart_data.append(float(rev))

    recent_bookings = Booking.query.filter_by(is_deleted=0).order_by(Booking.created_at.desc()).limit(10).all()

    template = "dashboard/admin.html" if current_user.is_admin else "dashboard/receptionist.html"
    return render_template(
        template,
        total_rooms=total_rooms,
        available=available,
        occupied=occupied,
        maintenance=maintenance,
        checkins_today=checkins_today,
        checkouts_today=checkouts_today,
        month_revenue=month_revenue,
        chart_labels=chart_labels,
        chart_data=chart_data,
        recent_bookings=recent_bookings,
    )
