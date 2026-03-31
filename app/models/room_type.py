from app.extensions import db
from app.models.mixins import SoftDeleteMixin, TimestampMixin


class RoomType(db.Model, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "room_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    base_price = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    max_adults = db.Column(db.Integer, nullable=False, default=2)
    max_children = db.Column(db.Integer, nullable=False, default=1)
    amenities = db.Column(db.JSON)
    image_path = db.Column(db.String(500))

    rooms = db.relationship("Room", back_populates="room_type", lazy="dynamic")
