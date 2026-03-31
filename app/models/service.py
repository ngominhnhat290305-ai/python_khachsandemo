from datetime import datetime

from app.extensions import db
from app.models.mixins import SoftDeleteMixin, TimestampMixin


class Service(db.Model, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.Enum("FOOD", "LAUNDRY", "TRANSPORT", "SPA", "OTHER"), nullable=False, default="OTHER")
    unit_price = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    unit = db.Column(db.String(50), default="lần")
    description = db.Column(db.Text)


class BookingService(db.Model):
    __tablename__ = "booking_services"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(12, 2), nullable=False)
    total_price = db.Column(db.Numeric(12, 2), nullable=False)
    used_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text)

    booking = db.relationship("Booking", back_populates="booking_services")
    service = db.relationship("Service")
