from app.extensions import db
from app.models.invoice import Invoice
from app.utils.helpers import generate_invoice_code


def create_invoice(booking, discount=0, tax_rate=10) -> tuple[bool, str, Invoice | None]:
    if booking.invoice:
        return True, "Invoice đã tồn tại.", booking.invoice

    room_charge = booking.room.effective_price * booking.num_nights
    service_charge = sum(float(bs.total_price) for bs in booking.booking_services)
    subtotal = room_charge + service_charge - discount
    tax_amount = subtotal * (float(tax_rate) / 100)
    total = subtotal + tax_amount
    amount_due = max(0, total - float(booking.deposit_amount))

    invoice = Invoice(
        invoice_code=generate_invoice_code(),
        booking_id=booking.id,
        created_by=booking.created_by,
        room_charge=room_charge,
        service_charge=service_charge,
        discount_amount=discount,
        tax_rate=tax_rate,
        tax_amount=tax_amount,
        total_amount=total,
        deposit_amount=float(booking.deposit_amount),
        amount_due=amount_due,
    )
    booking.total_amount = total
    db.session.add(invoice)
    return True, "OK", invoice
