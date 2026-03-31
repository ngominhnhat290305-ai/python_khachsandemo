from app.extensions import db
from app.models.mixins import SoftDeleteMixin, TimestampMixin


class Booking(db.Model, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    booking_code = db.Column(db.String(20), nullable=False, unique=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    actual_check_in = db.Column(db.DateTime)
    actual_check_out = db.Column(db.DateTime)
    num_adults = db.Column(db.Integer, nullable=False, default=1)
    num_children = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(
        db.Enum("PENDING", "CONFIRMED", "CHECKED_IN", "CHECKED_OUT", "CANCELLED"),
        nullable=False,
        default="PENDING",
    )
    deposit_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    total_amount = db.Column(db.Numeric(12, 2))
    special_requests = db.Column(db.Text)
    notes = db.Column(db.Text)
    cancelled_at = db.Column(db.DateTime)
    cancel_reason = db.Column(db.Text)

    customer = db.relationship("Customer", back_populates="bookings")
    room = db.relationship("Room", back_populates="bookings")
    creator = db.relationship("User", foreign_keys=[created_by])
    booking_services = db.relationship(
        "BookingService",
        back_populates="booking",
        cascade="all, delete-orphan",
    )
    invoice = db.relationship("Invoice", back_populates="booking", uselist=False)

    @property
    def num_nights(self):
        return (self.check_out_date - self.check_in_date).days

