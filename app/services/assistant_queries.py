import re
from calendar import monthrange
from datetime import date, datetime, timedelta

from sqlalchemy import case, desc, func

from app.extensions import db
from app.models.booking import Booking
from app.models.customer import Customer
from app.models.invoice import Invoice
from app.models.room import Room
from app.models.room_type import RoomType
from app.models.service import BookingService, Service
from app.utils.formatters import format_currency
from app.utils.labels import booking_status_vi, invoice_status_vi, payment_method_vi, room_status_vi


def _extract_room_number(text: str) -> str | None:
    m = re.search(r"\bph[oò]ng\s*#?\s*(\d{1,6})\b", text.lower())
    if m:
        return m.group(1)
    m = re.search(r"\b(\d{3,4})\b", text)
    return m.group(1) if m else None


def _extract_top_n(text: str, default: int = 5, cap: int = 20) -> int:
    m = re.search(r"\btop\s*(\d{1,2})\b", text.lower())
    if not m:
        return default
    try:
        n = int(m.group(1))
    except Exception:
        return default
    return max(1, min(cap, n))


def _extract_booking_code(text: str) -> str | None:
    m = re.search(r"\bHMS-\d{8}-\d{6}\b", text, re.IGNORECASE)
    return m.group(0).upper() if m else None


def _extract_invoice_code(text: str) -> str | None:
    m = re.search(r"\bINV-\d{8}-\d{6}\b", text, re.IGNORECASE)
    return m.group(0).upper() if m else None


def _money_table(rows: list[list[str]], headers: list[str]) -> str:
    def esc(v: str) -> str:
        return str(v or "").replace("|", "\\|")

    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for r in rows:
        lines.append("| " + " | ".join(esc(c) for c in r) + " |")
    return "\n".join(lines)


def _normalize_text(s: str) -> str:
    return (s or "").strip().lower()


def _parse_vn_amount_token(token: str) -> int | None:
    t = token.strip().lower().replace(" ", "")
    if not t:
        return None
    m = re.fullmatch(r"(\d+)(k|ngan|ngàn|nghin|nghìn)", t)
    if m:
        return int(m.group(1)) * 1_000
    m = re.fullmatch(r"(\d+)(t|ty|tỷ)", t)
    if m:
        return int(m.group(1)) * 1_000_000_000
    m = re.fullmatch(r"(\d+)(tr|trieu|triệu)", t)
    if m:
        return int(m.group(1)) * 1_000_000
    m = re.fullmatch(r"(\d+)tr(\d+)", t)
    if m:
        a = int(m.group(1)) * 1_000_000
        b_raw = m.group(2)
        b = int(b_raw)
        if b <= 999:
            b *= 1_000
        return a + b
    m = re.fullmatch(r"(\d+)", t)
    if m:
        return int(m.group(1))
    return None


def _eval_vn_money_expression(text: str) -> int | None:
    s = (text or "").lower()
    if not any(x in s for x in ["k", "ngàn", "nghin", "nghìn", "tr", "triệu", "ty", "tỷ", "+", "-"]):
        return None
    s = s.replace("–", "-").replace("—", "-")
    parts = re.split(r"(\+|\-)", s)
    total = 0
    sign = 1
    consumed = False
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if p == "+":
            sign = 1
            continue
        if p == "-":
            sign = -1
            continue
        token = re.sub(r"[^\w\dàáạảãâầấậẩẫăằắặẳẵđêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹ]", "", p)
        val = _parse_vn_amount_token(token)
        if val is None:
            return None
        total += sign * val
        consumed = True
    return total if consumed else None


def _month_range(year: int, month: int) -> tuple[date, date]:
    last = monthrange(year, month)[1]
    start = date(year, month, 1)
    end = date(year, month, last)
    return start, end


def _extract_month_year(text: str) -> tuple[int, int] | None:
    m = re.search(r"\bth[aá]ng\s*(\d{1,2})\s*/\s*(\d{4})\b", text)
    if m:
        mm = int(m.group(1))
        yy = int(m.group(2))
        if 1 <= mm <= 12:
            return yy, mm
    m = re.search(r"\bth[aá]ng\s*(\d{1,2})\b", text)
    if m:
        mm = int(m.group(1))
        if 1 <= mm <= 12:
            return date.today().year, mm
    m = re.search(r"\bn[aă]m\s*(\d{4})\b", text)
    if m:
        yy = int(m.group(1))
        return yy, 0
    return None


def _extract_date_range(text: str) -> tuple[date, date] | None:
    today = date.today()
    t = _normalize_text(text)
    if "hôm nay" in t:
        return today, today
    if "tuần này" in t:
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start, end
    if "tháng này" in t:
        return _month_range(today.year, today.month)
    if "năm này" in t or "năm nay" in t:
        return date(today.year, 1, 1), date(today.year, 12, 31)

    m = re.search(r"\btừ\s*(\d{4})-(\d{2})-(\d{2})\s*đến\s*(\d{4})-(\d{2})-(\d{2})\b", t)
    if m:
        try:
            d1 = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            d2 = date(int(m.group(4)), int(m.group(5)), int(m.group(6)))
            if d2 < d1:
                d1, d2 = d2, d1
            return d1, d2
        except Exception:
            return None

    m = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", t)
    if m:
        try:
            d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            return d, d
        except Exception:
            return None

    my = _extract_month_year(t)
    if my:
        yy, mm = my
        if mm == 0:
            return date(yy, 1, 1), date(yy, 12, 31)
        return _month_range(yy, mm)
    return None


def _limit_role_booking_query(q, user):
    if getattr(user, "role", "") == "ADMIN":
        return q
    today = date.today()
    return q.filter(
        (Booking.created_by == user.id) | (Booking.check_in_date == today) | (Booking.check_out_date == today)
    )


def _limit_role_invoice_query(q, user):
    if getattr(user, "role", "") == "ADMIN":
        return q
    return q.filter(Invoice.created_by == user.id)


def answer_from_db(message: str, user) -> tuple[bool, str | None]:
    msg = (message or "").strip()
    if not msg:
        return False, None
    lower = _normalize_text(msg)

    try:
        if any(x in lower for x in ["=", "cộng", "trừ", "+", "-"]) and any(x in lower for x in ["k", "ngàn", "nghìn", "tr", "triệu", "ty", "tỷ"]):
            val = _eval_vn_money_expression(lower)
            if val is not None:
                if val < 0:
                    return True, f"## Kết quả\n- Tổng: **-{format_currency(abs(val))}**"
                return True, f"## Kết quả\n- Tổng: **{format_currency(val)}**"

        bcode = _extract_booking_code(msg)
        if bcode:
            q = Booking.query.join(Customer).join(Room).filter(Booking.is_deleted == 0, Booking.booking_code == bcode)
            q = _limit_role_booking_query(q, user)
            b = q.first()
            if not b:
                return True, f"Không tìm thấy booking **{bcode}** (hoặc bạn không có quyền xem)."
            md = "\n".join(
                [
                    f"## Booking {b.booking_code}",
                    _money_table(
                        [
                            [
                                b.booking_code,
                                b.customer.full_name,
                                b.room.room_number,
                                b.check_in_date.isoformat(),
                                b.check_out_date.isoformat(),
                                booking_status_vi(b.status),
                                format_currency(float(b.deposit_amount or 0)),
                            ]
                        ],
                        ["Mã", "Khách", "Phòng", "Nhận", "Trả", "Trạng thái", "Cọc"],
                    ),
                    "",
                    f"- Xem chi tiết: `/bookings/{b.id}`",
                ]
            )
            return True, md

        icode = _extract_invoice_code(msg)
        if icode:
            q = Invoice.query.join(Booking).join(Customer).join(Room).filter(Invoice.invoice_code == icode)
            q = _limit_role_invoice_query(q, user)
            inv = q.first()
            if not inv:
                return True, f"Không tìm thấy hóa đơn **{icode}** (hoặc bạn không có quyền xem)."
            md = "\n".join(
                [
                    f"## Hóa đơn {inv.invoice_code}",
                    _money_table(
                        [
                            [
                                inv.invoice_code,
                                inv.booking.booking_code,
                                inv.booking.customer.full_name,
                                inv.booking.room.room_number,
                                format_currency(float(inv.total_amount or 0)),
                                invoice_status_vi(inv.payment_status),
                            ]
                        ],
                        ["Mã HĐ", "Booking", "Khách", "Phòng", "Tổng", "Trạng thái"],
                    ),
                    "",
                    f"- Xem chi tiết: `/invoices/{inv.id}`",
                ]
            )
            return True, md

        if ("checkin" in lower or "check-in" in lower) and ("hôm nay" in lower or "today" in lower):
            today = date.today()
            q = Booking.query.join(Customer).join(Room).filter(
                Booking.is_deleted == 0,
                Booking.check_in_date == today,
                Booking.status.in_(["PENDING", "CONFIRMED"]),
            )
            q = _limit_role_booking_query(q, user)
            rows = q.order_by(Booking.created_at.desc()).limit(20).all()
            if not rows:
                return True, "Không có booking check-in hôm nay."
            table_rows = [
                [b.booking_code, b.customer.full_name, b.room.room_number, booking_status_vi(b.status)] for b in rows
            ]
            return True, "\n".join(
                ["## Check-in hôm nay", _money_table(table_rows, ["Mã", "Khách", "Phòng", "Trạng thái"])]
            )

        if ("checkout" in lower or "check-out" in lower) and ("hôm nay" in lower or "today" in lower):
            today = date.today()
            q = Booking.query.join(Customer).join(Room).filter(
                Booking.is_deleted == 0,
                Booking.check_out_date == today,
                Booking.status == "CHECKED_IN",
            )
            q = _limit_role_booking_query(q, user)
            rows = q.order_by(Booking.created_at.desc()).limit(20).all()
            if not rows:
                return True, "Không có booking check-out hôm nay."
            table_rows = [
                [b.booking_code, b.customer.full_name, b.room.room_number, booking_status_vi(b.status)] for b in rows
            ]
            return True, "\n".join(
                ["## Check-out hôm nay", _money_table(table_rows, ["Mã", "Khách", "Phòng", "Trạng thái"])]
            )

        if "hóa đơn" in lower and ("chưa thanh toán" in lower or "unpaid" in lower):
            top_n = _extract_top_n(lower, default=10)
            q = Invoice.query.join(Booking).join(Customer).join(Room).filter(Invoice.payment_status != "PAID")
            q = _limit_role_invoice_query(q, user)
            rows = q.order_by(Invoice.created_at.desc()).limit(top_n).all()
            if not rows:
                return True, "Không có hóa đơn chưa thanh toán."
            table_rows = [
                [
                    inv.invoice_code,
                    inv.booking.booking_code,
                    inv.booking.customer.full_name,
                    inv.booking.room.room_number,
                    format_currency(float(inv.amount_due or 0)),
                    invoice_status_vi(inv.payment_status),
                ]
                for inv in rows
            ]
            return True, "\n".join(
                [
                    f"## Top {top_n} hóa đơn chưa thanh toán",
                    _money_table(table_rows, ["Mã HĐ", "Booking", "Khách", "Phòng", "Còn lại", "Trạng thái"]),
                    "",
                    "- Xem chi tiết: `/invoices`",
                ]
            )

        if "phòng" in lower and ("trống" in lower or "available" in lower) and ("từ" in lower or "đến" in lower or "ngày" in lower or "tháng" in lower):
            dr = _extract_date_range(lower)
            if not dr:
                return True, "Bạn muốn kiểm tra phòng trống theo khoảng thời gian nào? Ví dụ: `từ 2026-03-20 đến 2026-03-22`."
            d1, d2 = dr
            if d2 <= d1:
                return True, "Khoảng ngày không hợp lệ (ngày kết thúc phải sau ngày bắt đầu)."

            booked_ids = [
                r[0]
                for r in (
                    db.session.query(Booking.room_id)
                    .filter(
                        Booking.is_deleted == 0,
                        Booking.status.in_(["PENDING", "CONFIRMED", "CHECKED_IN"]),
                        Booking.check_in_date < d2,
                        Booking.check_out_date > d1,
                    )
                    .all()
                )
            ]
            q = db.session.query(Room.room_number, Room.floor, RoomType.name.label("room_type"), Room.bed_type, Room.status).join(
                RoomType, Room.room_type_id == RoomType.id
            )
            q = q.filter(Room.is_deleted == 0, RoomType.is_deleted == 0)
            if booked_ids:
                q = q.filter(~Room.id.in_(booked_ids))
            q = q.order_by(Room.floor, Room.room_number).limit(30)
            rows = q.all()
            if not rows:
                return True, f"Không có phòng trống trong khoảng **{d1.isoformat()} → {d2.isoformat()}**."
            table_rows = [
                [r.room_number, f"Tầng {r.floor}", r.room_type, r.bed_type, room_status_vi(str(r.status))]
                for r in rows
            ]
            md = "\n".join(
                [
                    f"## Phòng trống ({d1.isoformat()} → {d2.isoformat()})",
                    _money_table(table_rows, ["Phòng", "Vị trí", "Hạng phòng", "Giường", "Trạng thái"]),
                    "",
                    "- Gợi ý: nếu muốn lọc chặt hơn, hỏi: `phòng trống top 10 từ ... đến ...`",
                ]
            )
            return True, md

        if "phòng" in lower and ("giá" in lower or "bao nhiêu" in lower or "đắt" in lower):
            room_no = _extract_room_number(lower)
            if room_no and ("cao nhất" not in lower and "đắt nhất" not in lower):
                r = (
                    Room.query.join(RoomType)
                    .filter(Room.is_deleted == 0, Room.room_number == room_no)
                    .with_entities(
                        Room.room_number,
                        Room.floor,
                        Room.status,
                        Room.bed_type,
                        Room.price_override,
                        RoomType.name.label("room_type"),
                        RoomType.base_price.label("base_price"),
                    )
                    .first()
                )
                if not r:
                    return True, f"Không tìm thấy phòng **{room_no}**."

                price_override = float(r.price_override) if r.price_override is not None else None
                base_price = float(r.base_price) if r.base_price is not None else 0.0
                effective = price_override if price_override is not None else base_price

                md = "\n".join(
                    [
                        f"## Giá phòng {r.room_number}",
                        _money_table(
                            [
                                [
                                    str(r.room_number),
                                    f"Tầng {r.floor}",
                                    str(r.room_type),
                                    str(r.bed_type),
                                    room_status_vi(str(r.status)),
                                    format_currency(effective),
                                ]
                            ],
                            ["Phòng", "Vị trí", "Hạng phòng", "Giường", "Trạng thái", "Giá/đêm"],
                        ),
                        "",
                        f"- Giá hạng phòng: {format_currency(base_price)}",
                        f"- Giá ghi đè: {format_currency(price_override) if price_override is not None else '—'}",
                    ]
                )
                return True, md

            top_n = _extract_top_n(lower, default=5)
            effective_expr = case((Room.price_override.isnot(None), Room.price_override), else_=RoomType.base_price)
            rows = (
                db.session.query(
                    Room.room_number,
                    Room.floor,
                    RoomType.name.label("room_type"),
                    Room.bed_type,
                    Room.status,
                    effective_expr.label("effective_price"),
                )
                .join(RoomType, Room.room_type_id == RoomType.id)
                .filter(Room.is_deleted == 0, RoomType.is_deleted == 0)
                .order_by(desc(effective_expr), Room.room_number)
                .limit(top_n)
                .all()
            )
            if not rows:
                return True, "Chưa có dữ liệu phòng để thống kê."
            table_rows = []
            for r in rows:
                table_rows.append(
                    [
                        str(r.room_number),
                        f"Tầng {r.floor}",
                        str(r.room_type),
                        str(r.bed_type),
                        room_status_vi(str(r.status)),
                        format_currency(float(r.effective_price or 0)),
                    ]
                )
            md = "\n".join(
                [
                    f"## Top {top_n} phòng có giá/đêm cao nhất",
                    _money_table(table_rows, ["Phòng", "Vị trí", "Hạng phòng", "Giường", "Trạng thái", "Giá/đêm"]),
                ]
            )
            return True, md

        if ("hạng phòng" in lower or "room type" in lower) and ("cao nhất" in lower or "đắt nhất" in lower or "top" in lower):
            top_n = _extract_top_n(lower, default=5)
            rows = (
                db.session.query(RoomType.name, RoomType.base_price, RoomType.max_adults, RoomType.max_children)
                .filter(RoomType.is_deleted == 0)
                .order_by(RoomType.base_price.desc())
                .limit(top_n)
                .all()
            )
            if not rows:
                return True, "Chưa có dữ liệu hạng phòng để thống kê."
            table_rows = [
                [r.name, format_currency(float(r.base_price or 0)), f"{r.max_adults} NL", f"{r.max_children} TE"] for r in rows
            ]
            md = "\n".join(
                [
                    f"## Top {top_n} hạng phòng có giá cao nhất",
                    _money_table(table_rows, ["Hạng phòng", "Giá cơ bản/đêm", "Max NL", "Max TE"]),
                    "",
                    "- Xem/điều chỉnh: `/room-types`",
                ]
            )
            return True, md

        if "hóa đơn" in lower and ("cao nhất" in lower or "lớn nhất" in lower or "đắt nhất" in lower):
            q = Invoice.query.join(Booking).join(Customer).join(Room)
            q = _limit_role_invoice_query(q, user)
            inv = q.order_by(Invoice.total_amount.desc()).first()
            if not inv:
                return True, "Chưa có hóa đơn phù hợp để thống kê."

            md = "\n".join(
                [
                    "## Hóa đơn có tổng tiền cao nhất",
                    _money_table(
                        [
                            [
                                inv.invoice_code,
                                inv.booking.booking_code,
                                inv.booking.customer.full_name,
                                inv.booking.room.room_number,
                                format_currency(float(inv.total_amount or 0)),
                                invoice_status_vi(inv.payment_status),
                            ]
                        ],
                        ["Mã HĐ", "Booking", "Khách", "Phòng", "Tổng", "Trạng thái"],
                    ),
                    "",
                    f"- Xem chi tiết: `/invoices/{inv.id}`",
                ]
            )
            return True, md

        if ("hóa đơn" in lower or "doanh thu" in lower) and ("tổng" in lower or "bao nhiêu" in lower or "tháng" in lower or "năm" in lower or "tuần" in lower or "hôm nay" in lower):
            dr = _extract_date_range(lower)
            if dr:
                d1, d2 = dr
                start_dt = datetime.combine(d1, datetime.min.time())
                end_dt = datetime.combine(d2, datetime.max.time())
                q = Invoice.query
                q = _limit_role_invoice_query(q, user)
                q = q.filter(Invoice.payment_status == "PAID", Invoice.paid_at.isnot(None), Invoice.paid_at >= start_dt, Invoice.paid_at <= end_dt)
                total = q.with_entities(func.sum(Invoice.total_amount)).scalar() or 0
                count = q.count()
                md = "\n".join(
                    [
                        "## Doanh thu (đã thanh toán)",
                        f"- Khoảng thời gian: **{d1.isoformat()} → {d2.isoformat()}**",
                        f"- Số hóa đơn PAID: **{count}**",
                        f"- Tổng doanh thu: **{format_currency(float(total))}**",
                        "",
                        "- Xem chi tiết hóa đơn: `/invoices` (lọc theo trạng thái PAID)",
                    ]
                )
                return True, md

        if ("khách" in lower or "khách hàng" in lower) and ("chi nhiều" in lower or "cao nhất" in lower or "top" in lower):
            top_n = _extract_top_n(lower, default=5)
            q = (
                db.session.query(
                    Customer.full_name,
                    Customer.phone,
                    func.sum(Invoice.total_amount).label("spent"),
                    func.count(Invoice.id).label("invoice_count"),
                )
                .join(Booking, Booking.customer_id == Customer.id)
                .join(Invoice, Invoice.booking_id == Booking.id)
            )
            if getattr(user, "role", "") != "ADMIN":
                q = q.filter(Invoice.created_by == user.id)
            q = q.filter(Invoice.payment_status == "PAID").group_by(Customer.id).order_by(desc("spent")).limit(top_n)
            rows = q.all()
            if not rows:
                return True, "Chưa có dữ liệu hóa đơn PAID để thống kê top khách."
            table_rows = [
                [r.full_name, r.phone or "—", str(int(r.invoice_count or 0)), format_currency(float(r.spent or 0))] for r in rows
            ]
            md = "\n".join(
                [
                    f"## Top {top_n} khách chi tiêu cao nhất (PAID)",
                    _money_table(table_rows, ["Khách", "SĐT", "Số HĐ", "Tổng chi"]),
                ]
            )
            return True, md

        if ("dịch vụ" in lower or "service" in lower) and ("phổ biến" in lower or "hay dùng" in lower or "top" in lower):
            top_n = _extract_top_n(lower, default=5)
            q = (
                db.session.query(
                    Service.name,
                    func.sum(BookingService.quantity).label("qty"),
                    func.sum(BookingService.total_price).label("rev"),
                )
                .join(BookingService, BookingService.service_id == Service.id)
                .join(Booking, BookingService.booking_id == Booking.id)
                .filter(Booking.is_deleted == 0)
            )
            if getattr(user, "role", "") != "ADMIN":
                today = date.today()
                q = q.filter((Booking.created_by == user.id) | (Booking.check_in_date == today) | (Booking.check_out_date == today))
            q = q.group_by(Service.id).order_by(desc("qty")).limit(top_n)
            rows = q.all()
            if not rows:
                return True, "Chưa có dữ liệu dịch vụ để thống kê."
            table_rows = [[r.name, str(int(r.qty or 0)), format_currency(float(r.rev or 0))] for r in rows]
            md = "\n".join(
                [
                    f"## Top {top_n} dịch vụ phổ biến",
                    _money_table(table_rows, ["Dịch vụ", "Số lượng", "Doanh thu"]),
                    "",
                    "- Quản lý dịch vụ: `/services`",
                ]
            )
            return True, md

        if "booking" in lower and ("tổng hợp" in lower or "thống kê" in lower):
            q = Booking.query.filter(Booking.is_deleted == 0)
            q = _limit_role_booking_query(q, user)
            counts = (
                q.with_entities(Booking.status, func.count(Booking.id))
                .group_by(Booking.status)
                .all()
            )
            map_counts = {s: int(c) for s, c in counts}
            rows = []
            for s in ["PENDING", "CONFIRMED", "CHECKED_IN", "CHECKED_OUT", "CANCELLED"]:
                rows.append([booking_status_vi(s), str(map_counts.get(s, 0))])
            md = "\n".join(
                [
                    "## Thống kê booking",
                    _money_table(rows, ["Trạng thái", "Số lượng"]),
                ]
            )
            return True, md

        return False, None
    except Exception:
        return True, "**Lỗi:** Không truy vấn được DB. Vui lòng kiểm tra MySQL/DB connection."
