from app.extensions import db
from app.models.mixins import SoftDeleteMixin, TimestampMixin


class Customer(db.Model, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    id_number = db.Column(db.String(20), nullable=False, unique=True)
    id_type = db.Column(db.Enum("CCCD", "PASSPORT", "DRIVER_LICENSE"), nullable=False, default="CCCD")
    gender = db.Column(db.Enum("MALE", "FEMALE", "OTHER"), default="MALE")
    date_of_birth = db.Column(db.Date)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(200))
    nationality = db.Column(db.String(100), default="Việt Nam")
    address = db.Column(db.Text)
    avatar_path = db.Column(db.String(500))
    notes = db.Column(db.Text)

    bookings = db.relationship("Booking", back_populates="customer", lazy="dynamic")
