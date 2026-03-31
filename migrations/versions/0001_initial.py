from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    ts_now = sa.text("CURRENT_TIMESTAMP")
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(50), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("role", sa.Enum("ADMIN", "RECEPTIONIST"), nullable=False, server_default="RECEPTIONIST"),
        sa.Column("phone", sa.String(15)),
        sa.Column("email", sa.String(200)),
        sa.Column("avatar_path", sa.String(500)),
        sa.Column("is_active", sa.SmallInteger, nullable=False, server_default="1"),
        sa.Column("last_login", sa.DateTime),
        sa.Column("login_attempts", sa.Integer, nullable=False, server_default="0"),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0", index=True),
        sa.Column("deleted_at", sa.DateTime),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=ts_now),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=ts_now, server_onupdate=ts_now),
        mysql_engine="InnoDB",
    )
    op.create_index("idx_username", "users", ["username"])
    op.create_index("idx_role", "users", ["role"])
    op.create_index("idx_users_deleted", "users", ["is_deleted"])

    op.create_table(
        "room_types",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("base_price", sa.Numeric(12, 2), nullable=False, server_default="0.00"),
        sa.Column("max_adults", sa.Integer, nullable=False, server_default="2"),
        sa.Column("max_children", sa.Integer, nullable=False, server_default="1"),
        sa.Column("amenities", sa.JSON),
        sa.Column("image_path", sa.String(500)),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0", index=True),
        sa.Column("deleted_at", sa.DateTime),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=ts_now),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=ts_now, server_onupdate=ts_now),
        mysql_engine="InnoDB",
    )
    op.create_index("idx_room_types_deleted", "room_types", ["is_deleted"])

    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("room_number", sa.String(10), nullable=False, unique=True),
        sa.Column("floor", sa.Integer, nullable=False, server_default="1"),
        sa.Column("room_type_id", sa.Integer, sa.ForeignKey("room_types.id", onupdate="CASCADE"), nullable=False),
        sa.Column(
            "bed_type",
            sa.Enum("SINGLE", "DOUBLE", "TWIN", "TRIPLE", "SUITE", "PRESIDENTIAL", "FAMILY"),
            nullable=False,
            server_default="DOUBLE",
        ),
        sa.Column(
            "status",
            sa.Enum("AVAILABLE", "RESERVED", "OCCUPIED", "CLEANING", "MAINTENANCE"),
            nullable=False,
            server_default="AVAILABLE",
        ),
        sa.Column("price_override", sa.Numeric(12, 2)),
        sa.Column("description", sa.Text),
        sa.Column("image_paths", sa.JSON),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0", index=True),
        sa.Column("deleted_at", sa.DateTime),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=ts_now),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=ts_now, server_onupdate=ts_now),
        mysql_engine="InnoDB",
    )
    op.create_index("idx_rooms_status", "rooms", ["status"])
    op.create_index("idx_rooms_floor", "rooms", ["floor"])
    op.create_index("idx_rooms_deleted", "rooms", ["is_deleted"])

    op.create_table(
        "customers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("id_number", sa.String(20), nullable=False, unique=True),
        sa.Column("id_type", sa.Enum("CCCD", "PASSPORT", "DRIVER_LICENSE"), nullable=False, server_default="CCCD"),
        sa.Column("gender", sa.Enum("MALE", "FEMALE", "OTHER"), server_default="MALE"),
        sa.Column("date_of_birth", sa.Date),
        sa.Column("phone", sa.String(15)),
        sa.Column("email", sa.String(200)),
        sa.Column("nationality", sa.String(100), server_default="Việt Nam"),
        sa.Column("address", sa.Text),
        sa.Column("avatar_path", sa.String(500)),
        sa.Column("notes", sa.Text),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0", index=True),
        sa.Column("deleted_at", sa.DateTime),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=ts_now),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=ts_now, server_onupdate=ts_now),
        mysql_engine="InnoDB",
    )
    op.create_index("idx_customers_id_number", "customers", ["id_number"])
    op.create_index("idx_customers_phone", "customers", ["phone"])
    op.create_index("idx_customers_full_name", "customers", ["full_name"])
    op.create_index("idx_customers_deleted", "customers", ["is_deleted"])

    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("booking_code", sa.String(20), nullable=False, unique=True),
        sa.Column("customer_id", sa.Integer, sa.ForeignKey("customers.id", onupdate="CASCADE"), nullable=False),
        sa.Column("room_id", sa.Integer, sa.ForeignKey("rooms.id", onupdate="CASCADE"), nullable=False),
        sa.Column("created_by", sa.Integer, sa.ForeignKey("users.id", onupdate="CASCADE"), nullable=False),
        sa.Column("check_in_date", sa.Date, nullable=False),
        sa.Column("check_out_date", sa.Date, nullable=False),
        sa.Column("actual_check_in", sa.DateTime),
        sa.Column("actual_check_out", sa.DateTime),
        sa.Column("num_adults", sa.Integer, nullable=False, server_default="1"),
        sa.Column("num_children", sa.Integer, nullable=False, server_default="0"),
        sa.Column(
            "status",
            sa.Enum("PENDING", "CONFIRMED", "CHECKED_IN", "CHECKED_OUT", "CANCELLED"),
            nullable=False,
            server_default="PENDING",
        ),
        sa.Column("deposit_amount", sa.Numeric(12, 2), nullable=False, server_default="0.00"),
        sa.Column("total_amount", sa.Numeric(12, 2)),
        sa.Column("special_requests", sa.Text),
        sa.Column("notes", sa.Text),
        sa.Column("cancelled_at", sa.DateTime),
        sa.Column("cancel_reason", sa.Text),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0", index=True),
        sa.Column("deleted_at", sa.DateTime),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=ts_now),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=ts_now, server_onupdate=ts_now),
        mysql_engine="InnoDB",
    )
    op.create_index("idx_bookings_code", "bookings", ["booking_code"])
    op.create_index("idx_bookings_status", "bookings", ["status"])
    op.create_index("idx_bookings_checkin", "bookings", ["check_in_date"])
    op.create_index("idx_bookings_checkout", "bookings", ["check_out_date"])
    op.create_index("idx_bookings_customer", "bookings", ["customer_id"])
    op.create_index("idx_bookings_room", "bookings", ["room_id"])
    op.create_index("idx_bookings_deleted", "bookings", ["is_deleted"])

    op.create_table(
        "services",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("category", sa.Enum("FOOD", "LAUNDRY", "TRANSPORT", "SPA", "OTHER"), nullable=False, server_default="OTHER"),
        sa.Column("unit_price", sa.Numeric(12, 2), nullable=False, server_default="0.00"),
        sa.Column("unit", sa.String(50), server_default="lần"),
        sa.Column("description", sa.Text),
        sa.Column("is_deleted", sa.SmallInteger, nullable=False, server_default="0", index=True),
        sa.Column("deleted_at", sa.DateTime),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=ts_now),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=ts_now, server_onupdate=ts_now),
        mysql_engine="InnoDB",
    )
    op.create_index("idx_services_category", "services", ["category"])
    op.create_index("idx_services_deleted", "services", ["is_deleted"])

    op.create_table(
        "booking_services",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("booking_id", sa.Integer, sa.ForeignKey("bookings.id", onupdate="CASCADE"), nullable=False),
        sa.Column("service_id", sa.Integer, sa.ForeignKey("services.id", onupdate="CASCADE"), nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False, server_default="1"),
        sa.Column("unit_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("total_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("used_at", sa.DateTime, nullable=False, server_default=ts_now),
        sa.Column("notes", sa.Text),
        mysql_engine="InnoDB",
    )
    op.create_index("idx_booking_services_booking", "booking_services", ["booking_id"])

    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("invoice_code", sa.String(20), nullable=False, unique=True),
        sa.Column("booking_id", sa.Integer, sa.ForeignKey("bookings.id", onupdate="CASCADE"), nullable=False, unique=True),
        sa.Column("created_by", sa.Integer, sa.ForeignKey("users.id", onupdate="CASCADE"), nullable=False),
        sa.Column("room_charge", sa.Numeric(12, 2), nullable=False, server_default="0.00"),
        sa.Column("service_charge", sa.Numeric(12, 2), nullable=False, server_default="0.00"),
        sa.Column("discount_amount", sa.Numeric(12, 2), nullable=False, server_default="0.00"),
        sa.Column("tax_rate", sa.Numeric(5, 2), nullable=False, server_default="10.00"),
        sa.Column("tax_amount", sa.Numeric(12, 2), nullable=False, server_default="0.00"),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=False, server_default="0.00"),
        sa.Column("deposit_amount", sa.Numeric(12, 2), nullable=False, server_default="0.00"),
        sa.Column("amount_due", sa.Numeric(12, 2), nullable=False, server_default="0.00"),
        sa.Column("payment_method", sa.Enum("CASH", "CARD", "TRANSFER", "MIXED"), nullable=False, server_default="CASH"),
        sa.Column("payment_status", sa.Enum("UNPAID", "PARTIAL", "PAID"), nullable=False, server_default="UNPAID"),
        sa.Column("paid_at", sa.DateTime),
        sa.Column("notes", sa.Text),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=ts_now),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=ts_now, server_onupdate=ts_now),
        mysql_engine="InnoDB",
    )
    op.create_index("idx_invoices_code", "invoices", ["invoice_code"])
    op.create_index("idx_invoices_status", "invoices", ["payment_status"])
    op.create_index("idx_invoices_date", "invoices", ["created_at"])


def downgrade():
    op.drop_index("idx_invoices_date", table_name="invoices")
    op.drop_index("idx_invoices_status", table_name="invoices")
    op.drop_index("idx_invoices_code", table_name="invoices")
    op.drop_table("invoices")

    op.drop_index("idx_booking_services_booking", table_name="booking_services")
    op.drop_table("booking_services")

    op.drop_index("idx_services_deleted", table_name="services")
    op.drop_index("idx_services_category", table_name="services")
    op.drop_table("services")

    op.drop_index("idx_bookings_deleted", table_name="bookings")
    op.drop_index("idx_bookings_room", table_name="bookings")
    op.drop_index("idx_bookings_customer", table_name="bookings")
    op.drop_index("idx_bookings_checkout", table_name="bookings")
    op.drop_index("idx_bookings_checkin", table_name="bookings")
    op.drop_index("idx_bookings_status", table_name="bookings")
    op.drop_index("idx_bookings_code", table_name="bookings")
    op.drop_table("bookings")

    op.drop_index("idx_customers_deleted", table_name="customers")
    op.drop_index("idx_customers_full_name", table_name="customers")
    op.drop_index("idx_customers_phone", table_name="customers")
    op.drop_index("idx_customers_id_number", table_name="customers")
    op.drop_table("customers")

    op.drop_index("idx_rooms_deleted", table_name="rooms")
    op.drop_index("idx_rooms_floor", table_name="rooms")
    op.drop_index("idx_rooms_status", table_name="rooms")
    op.drop_table("rooms")

    op.drop_index("idx_room_types_deleted", table_name="room_types")
    op.drop_table("room_types")

    op.drop_index("idx_users_deleted", table_name="users")
    op.drop_index("idx_role", table_name="users")
    op.drop_index("idx_username", table_name="users")
    op.drop_table("users")
