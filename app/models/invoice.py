from app.extensions import db
from app.models.mixins import TimestampMixin


class Invoice(db.Model, TimestampMixin):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    invoice_code = db.Column(db.String(20), nullable=False, unique=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False, unique=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    room_charge = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    service_charge = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    discount_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    tax_rate = db.Column(db.Numeric(5, 2), nullable=False, default=10)
    tax_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    deposit_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    amount_due = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    payment_method = db.Column(db.Enum("CASH", "CARD", "TRANSFER", "MIXED"), nullable=False, default="CASH")
    payment_status = db.Column(db.Enum("UNPAID", "PARTIAL", "PAID"), nullable=False, default="UNPAID")
    paid_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    booking = db.relationship("Booking", back_populates="invoice")
    creator = db.relationship("User", foreign_keys=[created_by])
