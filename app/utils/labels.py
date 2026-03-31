BOOKING_STATUS_VI = {
    "PENDING": "Chờ xác nhận",
    "CONFIRMED": "Đã xác nhận",
    "CHECKED_IN": "Đang ở",
    "CHECKED_OUT": "Đã trả phòng",
    "CANCELLED": "Đã huỷ",
}

ROOM_STATUS_VI = {
    "AVAILABLE": "Trống",
    "RESERVED": "Đã đặt",
    "OCCUPIED": "Đang có khách",
    "CLEANING": "Đang dọn",
    "MAINTENANCE": "Bảo trì",
}

INVOICE_STATUS_VI = {
    "UNPAID": "Chưa thanh toán",
    "PARTIAL": "Thanh toán một phần",
    "PAID": "Đã thanh toán",
}

PAYMENT_METHOD_VI = {
    "CASH": "Tiền mặt",
    "CARD": "Thẻ",
    "TRANSFER": "Chuyển khoản",
    "MIXED": "Kết hợp",
}

BED_TYPE_VI = {
    "SINGLE": "Phòng đơn",
    "DOUBLE": "Phòng đôi",
    "TWIN": "Twin (2 giường)",
    "TRIPLE": "Triple",
    "SUITE": "Suite",
    "PRESIDENTIAL": "Tổng thống",
    "FAMILY": "Gia đình",
}


def booking_status_vi(code: str | None) -> str:
    return BOOKING_STATUS_VI.get(code or "", code or "—")


def room_status_vi(code: str | None) -> str:
    return ROOM_STATUS_VI.get(code or "", code or "—")


def invoice_status_vi(code: str | None) -> str:
    return INVOICE_STATUS_VI.get(code or "", code or "—")


def payment_method_vi(code: str | None) -> str:
    return PAYMENT_METHOD_VI.get(code or "", code or "—")


def bed_type_vi(code: str | None) -> str:
    return BED_TYPE_VI.get(code or "", code or "—")

