from datetime import datetime

from flask import Flask

from app.config import Config
from app.extensions import bcrypt, db, login_manager, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    for folder in [
        app.config["AVATARS_FOLDER"],
        app.config["ROOMS_FOLDER"],
        app.config["ROOM_TYPES_FOLDER"],
        app.config["DEFAULT_FOLDER"],
    ]:
        folder.mkdir(parents=True, exist_ok=True)

    from app.blueprints.auth import bp as auth_bp
    from app.blueprints.dashboard import bp as dashboard_bp
    from app.blueprints.profile import bp as profile_bp
    from app.blueprints.users import bp as users_bp
    from app.blueprints.room_types import bp as room_types_bp
    from app.blueprints.rooms import bp as rooms_bp
    from app.blueprints.customers import bp as customers_bp
    from app.blueprints.bookings import bp as bookings_bp
    from app.blueprints.invoices import bp as invoices_bp
    from app.blueprints.services import bp as services_bp
    from app.blueprints.reports import bp as reports_bp
    from app.blueprints.assistant import bp as assistant_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(room_types_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(assistant_bp)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.utils.formatters import format_currency, format_date, format_datetime
    from app.utils.labels import bed_type_vi, booking_status_vi, invoice_status_vi, payment_method_vi, room_status_vi

    app.jinja_env.filters["currency"] = format_currency
    app.jinja_env.filters["fdate"] = format_date
    app.jinja_env.filters["fdatetime"] = format_datetime
    app.jinja_env.filters["booking_status_vi"] = booking_status_vi
    app.jinja_env.filters["invoice_status_vi"] = invoice_status_vi
    app.jinja_env.filters["room_status_vi"] = room_status_vi
    app.jinja_env.filters["payment_method_vi"] = payment_method_vi
    app.jinja_env.filters["bed_type_vi"] = bed_type_vi

    @app.context_processor
    def inject_now():
        return {"now": datetime.now()}

    return app
