from datetime import date, datetime

from app.extensions import db
from app.models.booking import Booking
from app.models.room import Room
from app.utils.helpers import generate_booking_code


def check_room_availability(room_id: int, check_in: date, check_out: date, exclude_id: int | None = None) -> bool:
    q = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.is_deleted == 0,
        Booking.status.in_(["PENDING", "CONFIRMED", "CHECKED_IN"]),
        Booking.check_in_date < check_out,
        Booking.check_out_date > check_in,
    )
    if exclude_id:
        q = q.filter(Booking.id != exclude_id)
    return q.count() == 0


def create_booking(
    customer_id: int,
    room_id: int,
    created_by: int,
    check_in: date,
    check_out: date,
    num_adults: int = 1,
    num_children: int = 0,
    deposit: float = 0,
    special_requests: str | None = None,
    status: str = "PENDING",
) -> tuple[bool, str, Booking | None]:
    if check_out <= check_in:
        return False, "Ngày trả phòng phải sau ngày nhận phòng.", None
    if not check_room_availability(room_id, check_in, check_out):
        return False, "Phòng đã được đặt trong khoảng thời gian này.", None

    room = Room.query.get(room_id)
    if not room or room.is_deleted:
        return False, "Phòng không tồn tại.", None

    booking = Booking(
        booking_code=generate_booking_code(),
        customer_id=customer_id,
        room_id=room_id,
        created_by=created_by,
        check_in_date=check_in,
        check_out_date=check_out,
        num_adults=num_adults,
        num_children=num_children,
        deposit_amount=deposit,
        special_requests=special_requests,
        status=status,
    )
    if status in ("CONFIRMED",):
        room.status = "RESERVED"
    db.session.add(booking)
    db.session.commit()
    return True, "Đặt phòng thành công.", booking


def do_confirm(booking_id: int) -> tuple[bool, str]:
    booking = Booking.query.get(booking_id)
    if not booking:
        return False, "Booking không tồn tại."
    if booking.status != "PENDING":
        return False, "Chỉ xác nhận booking trạng thái PENDING."
    booking.status = "CONFIRMED"
    booking.room.status = "RESERVED"
    db.session.commit()
    return True, "Xác nhận booking thành công."


def do_check_in(booking_id: int) -> tuple[bool, str]:
    booking = Booking.query.get(booking_id)
    if not booking:
        return False, "Booking không tồn tại."
    if booking.status not in ("CONFIRMED",):
        return False, f"Không thể check-in trạng thái {booking.status}."
    booking.status = "CHECKED_IN"
    booking.actual_check_in = datetime.utcnow()
    booking.room.status = "OCCUPIED"
    db.session.commit()
    return True, "Check-in thành công."


def do_check_out(booking_id: int) -> tuple[bool, str, object | None]:
    from app.services.invoice_service import create_invoice

    booking = Booking.query.get(booking_id)
    if not booking:
        return False, "Booking không tồn tại.", None
    if booking.status != "CHECKED_IN":
        return False, "Booking chưa check-in.", None

    booking.status = "CHECKED_OUT"
    booking.actual_check_out = datetime.utcnow()
    booking.room.status = "CLEANING"

    ok, msg, invoice = create_invoice(booking)
    if not ok:
        db.session.rollback()
        return False, msg, None

    db.session.commit()
    return True, "Check-out thành công.", invoice


def cancel_booking(booking_id: int, reason: str | None = None) -> tuple[bool, str]:
    booking = Booking.query.get(booking_id)
    if not booking:
        return False, "Booking không tồn tại."
    if booking.status in ("CHECKED_OUT", "CANCELLED"):
        return False, "Không thể huỷ booking này."
    if booking.status == "CHECKED_IN":
        return False, "Khách đang ở. Hãy check-out trước."

    booking.status = "CANCELLED"
    booking.cancelled_at = datetime.utcnow()
    booking.cancel_reason = reason
    booking.room.status = "AVAILABLE"
    db.session.commit()
    return True, "Huỷ booking thành công."
