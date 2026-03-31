from datetime import datetime


def generate_booking_code() -> str:
    from app.models.booking import Booking

    today = datetime.now().strftime("%Y%m%d")
    prefix = f"HMS-{today}-"
    last = Booking.query.filter(Booking.booking_code.like(f"{prefix}%")).order_by(Booking.id.desc()).first()
    seq = (int(last.booking_code.split("-")[-1]) + 1) if last else 1
    return f"{prefix}{seq:06d}"


def generate_invoice_code() -> str:
    from app.models.invoice import Invoice

    today = datetime.now().strftime("%Y%m%d")
    prefix = f"INV-{today}-"
    last = Invoice.query.filter(Invoice.invoice_code.like(f"{prefix}%")).order_by(Invoice.id.desc()).first()
    seq = (int(last.invoice_code.split("-")[-1]) + 1) if last else 1
    return f"{prefix}{seq:06d}"


def allowed_file(filename: str, allowed_ext: set) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_ext
