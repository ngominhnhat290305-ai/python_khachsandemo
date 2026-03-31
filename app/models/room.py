from app.extensions import db
from app.models.mixins import SoftDeleteMixin, TimestampMixin


class Room(db.Model, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), nullable=False, unique=True)
    floor = db.Column(db.Integer, nullable=False, default=1)
    room_type_id = db.Column(db.Integer, db.ForeignKey("room_types.id"), nullable=False)
    bed_type = db.Column(
        db.Enum("SINGLE", "DOUBLE", "TWIN", "TRIPLE", "SUITE", "PRESIDENTIAL", "FAMILY"),
        nullable=False,
        default="DOUBLE",
    )
    status = db.Column(
        db.Enum("AVAILABLE", "RESERVED", "OCCUPIED", "CLEANING", "MAINTENANCE"),
        nullable=False,
        default="AVAILABLE",
    )
    price_override = db.Column(db.Numeric(12, 2))
    description = db.Column(db.Text)
    image_paths = db.Column(db.JSON)

    room_type = db.relationship("RoomType", back_populates="rooms")
    bookings = db.relationship("Booking", back_populates="room", lazy="dynamic")

    @property
    def effective_price(self):
        if self.price_override is not None:
            return float(self.price_override)
        return float(self.room_type.base_price) if self.room_type else 0.0

    @property
    def status_color(self):
        colors = {
            "AVAILABLE": "sage",
            "RESERVED": "amber",
            "OCCUPIED": "rust",
            "CLEANING": "gold",
            "MAINTENANCE": "slate",
        }
        return colors.get(self.status, "slate")
