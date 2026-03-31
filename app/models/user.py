from flask_login import UserMixin

from app.extensions import db
from app.models.mixins import SoftDeleteMixin, TimestampMixin


class User(UserMixin, db.Model, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Enum("ADMIN", "RECEPTIONIST"), nullable=False, default="RECEPTIONIST")
    phone = db.Column(db.String(15))
    email = db.Column(db.String(200))
    avatar_path = db.Column(db.String(500))
    is_active = db.Column(db.SmallInteger, nullable=False, default=1)
    last_login = db.Column(db.DateTime)
    login_attempts = db.Column(db.Integer, nullable=False, default=0)

    @property
    def is_admin(self):
        return self.role == "ADMIN"

    @property
    def role_display(self):
        return "Quản lý" if self.role == "ADMIN" else "Lễ tân"

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<User {self.username}>"
