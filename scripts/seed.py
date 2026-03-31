import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from app.extensions import bcrypt, db
from app.models.booking import Booking
from app.models.customer import Customer
from app.models.invoice import Invoice
from app.models.room import Room
from app.models.room_type import RoomType
from app.models.service import BookingService, Service
from app.models.user import User


def seed_users():
    users = [
        User(
            username="admin",
            full_name="Nguyễn Quản Lý",
            role="ADMIN",
            password_hash=bcrypt.generate_password_hash("Admin@123").decode(),
            phone="0901234567",
            email="admin@hotel.com",
            avatar_path="images/avatars/user_admin.jpg",
        ),
        User(
            username="letan1",
            full_name="Trần Thị Lễ Tân",
            role="RECEPTIONIST",
            password_hash=bcrypt.generate_password_hash("Letan@123").decode(),
            phone="0912345678",
            email="letan1@hotel.com",
            avatar_path="images/avatars/user_recept1.jpg",
        ),
        User(
            username="letan2",
            full_name="Phạm Văn Tiếp Đón",
            role="RECEPTIONIST",
            password_hash=bcrypt.generate_password_hash("Letan@123").decode(),
            phone="0923456789",
            avatar_path="images/avatars/user_recept2.jpg",
        ),
    ]
    for u in users:
        db.session.add(u)
    db.session.flush()
    return users


def seed_room_types():
    types = [
        RoomType(
            name="Standard",
            base_price=500_000,
            max_adults=2,
            max_children=1,
            description="Phòng tiêu chuẩn thoải mái, đầy đủ tiện nghi cơ bản.",
            amenities=["WiFi", "Điều hoà", "TV", "Minibar"],
            image_path="images/room_types/standard.jpg",
        ),
        RoomType(
            name="Deluxe",
            base_price=900_000,
            max_adults=2,
            max_children=2,
            description="Không gian cao cấp hơn, view đẹp, tiện nghi nâng cấp.",
            amenities=["WiFi", "Điều hoà", "Smart TV", "Minibar", "Ban công"],
            image_path="images/room_types/deluxe.jpg",
        ),
        RoomType(
            name="Suite",
            base_price=1_800_000,
            max_adults=3,
            max_children=2,
            description="Phòng Suite sang trọng với phòng khách và phòng ngủ riêng biệt.",
            amenities=["WiFi", "Điều hoà", "Smart TV", "Jacuzzi"],
            image_path="images/room_types/suite.jpg",
        ),
        RoomType(
            name="Presidential Suite",
            base_price=5_000_000,
            max_adults=4,
            max_children=2,
            description="Hạng cao nhất, dịch vụ cá nhân hoàn hảo.",
            amenities=["WiFi", "Butler", "Jacuzzi", "Xe đưa đón"],
            image_path="images/room_types/presidential.jpg",
        ),
        RoomType(
            name="Family",
            base_price=1_200_000,
            max_adults=4,
            max_children=3,
            description="Phòng gia đình rộng rãi, phù hợp gia đình.",
            amenities=["WiFi", "Điều hoà", "2 phòng ngủ"],
            image_path="images/room_types/family.jpg",
        ),
    ]
    for t in types:
        db.session.add(t)
    db.session.flush()
    return types


def seed_rooms(rts):
    std, dlx, suite, pres, fam = rts
    rooms = [
        Room(
            room_number="101",
            floor=1,
            room_type_id=std.id,
            bed_type="SINGLE",
            status="AVAILABLE",
            description="Phòng đơn, view sân vườn",
            image_paths=["images/rooms/room_101_1.jpg", "images/rooms/room_101_2.jpg"],
        ),
        Room(
            room_number="102",
            floor=1,
            room_type_id=std.id,
            bed_type="DOUBLE",
            status="OCCUPIED",
            image_paths=["images/rooms/room_102_1.jpg"],
        ),
        Room(
            room_number="103",
            floor=1,
            room_type_id=std.id,
            bed_type="TWIN",
            status="AVAILABLE",
            image_paths=["images/rooms/room_103_1.jpg"],
        ),
        Room(room_number="201", floor=2, room_type_id=dlx.id, bed_type="DOUBLE", status="AVAILABLE",
             image_paths=["images/rooms/room_201_1.jpg", "images/rooms/room_201_2.jpg"]),
        Room(room_number="202", floor=2, room_type_id=dlx.id, bed_type="SUITE", status="RESERVED",
             image_paths=["images/rooms/room_202_1.jpg", "images/rooms/room_202_2.jpg"]),
        Room(room_number="301", floor=3, room_type_id=suite.id, bed_type="SUITE", status="AVAILABLE",
             image_paths=["images/rooms/room_301_1.jpg", "images/rooms/room_301_2.jpg"]),
        Room(room_number="401", floor=4, room_type_id=pres.id, bed_type="PRESIDENTIAL", status="AVAILABLE",
             image_paths=["images/rooms/room_401_1.jpg", "images/rooms/room_401_2.jpg", "images/rooms/room_401_3.jpg"]),
        Room(room_number="204", floor=2, room_type_id=fam.id, bed_type="FAMILY", status="AVAILABLE"),
    ]
    for r in rooms:
        if r.image_paths:
            r.image_paths = [p for p in r.image_paths if p]
        db.session.add(r)
    db.session.flush()
    return rooms


def seed_customers():
    customers = [
        Customer(
            full_name="Nguyễn Văn Anh",
            id_number="079123456001",
            id_type="CCCD",
            gender="MALE",
            date_of_birth=date(1990, 5, 15),
            phone="0901111001",
            email="vananh@email.com",
            address="123 Lê Lợi, Q1, TP.HCM",
            avatar_path="images/avatars/customer_1.jpg",
        ),
        Customer(
            full_name="Trần Thị Bình",
            id_number="079123456002",
            id_type="CCCD",
            gender="FEMALE",
            date_of_birth=date(1988, 3, 22),
            phone="0902222002",
            email="thibinh@email.com",
            address="45 Nguyễn Huệ, Q1, TP.HCM",
            avatar_path="images/avatars/customer_2.jpg",
        ),
        Customer(
            full_name="John Smith",
            id_number="US98765432",
            id_type="PASSPORT",
            gender="MALE",
            nationality="Mỹ",
            phone="+1-555-0101",
            email="jsmith@corp.com",
            notes="Business traveler",
            avatar_path="images/avatars/customer_8.jpg",
        ),
    ]
    for c in customers:
        db.session.add(c)
    db.session.flush()
    return customers


def seed_services():
    services = [
        Service(name="Ăn sáng", category="FOOD", unit_price=100_000, unit="người"),
        Service(name="Giặt ủi", category="LAUNDRY", unit_price=80_000, unit="kg"),
        Service(name="Đặt xe", category="TRANSPORT", unit_price=200_000, unit="chuyến"),
        Service(name="Spa", category="SPA", unit_price=600_000, unit="lần"),
    ]
    for s in services:
        db.session.add(s)
    db.session.flush()
    return services


def seed_bookings(users, rooms, customers, services):
    today = date.today()
    admin = users[0]
    recept = users[1]

    b1 = Booking(
        booking_code=f"HMS-{(today - timedelta(7)).strftime('%Y%m%d')}-000001",
        customer_id=customers[0].id,
        room_id=rooms[0].id,
        created_by=recept.id,
        check_in_date=today - timedelta(7),
        check_out_date=today - timedelta(5),
        actual_check_in=datetime.combine(today - timedelta(7), datetime.min.time().replace(hour=14)),
        actual_check_out=datetime.combine(today - timedelta(5), datetime.min.time().replace(hour=12)),
        num_adults=1,
        status="CHECKED_OUT",
        deposit_amount=200_000,
        total_amount=1_320_000,
    )
    db.session.add(b1)
    db.session.flush()

    bs1 = BookingService(
        booking_id=b1.id,
        service_id=services[0].id,
        quantity=2,
        unit_price=100_000,
        total_price=200_000,
        used_at=datetime.combine(today - timedelta(6), datetime.min.time().replace(hour=8)),
    )
    db.session.add(bs1)

    inv1 = Invoice(
        invoice_code=f"INV-{(today - timedelta(5)).strftime('%Y%m%d')}-000001",
        booking_id=b1.id,
        created_by=recept.id,
        room_charge=1_000_000,
        service_charge=200_000,
        discount_amount=0,
        tax_rate=10,
        tax_amount=120_000,
        total_amount=1_320_000,
        deposit_amount=200_000,
        amount_due=1_120_000,
        payment_method="CASH",
        payment_status="PAID",
        paid_at=datetime.combine(today - timedelta(5), datetime.min.time().replace(hour=12)),
    )
    db.session.add(inv1)

    b2 = Booking(
        booking_code=f"HMS-{today.strftime('%Y%m%d')}-000002",
        customer_id=customers[1].id,
        room_id=rooms[3].id,
        created_by=admin.id,
        check_in_date=today,
        check_out_date=today + timedelta(2),
        num_adults=2,
        num_children=0,
        status="CONFIRMED",
        deposit_amount=500_000,
    )
    db.session.add(b2)


def run_seed():
    try:
        import subprocess

        subprocess.run([sys.executable, "scripts/download_images.py"], check=False)
    except Exception:
        pass

    app = create_app()
    with app.app_context():
        from flask_migrate import upgrade

        upgrade()
        if User.query.filter_by(username="admin").first():
            return

        users = seed_users()
        rts = seed_room_types()
        rooms = seed_rooms(rts)
        customers = seed_customers()
        services = seed_services()
        seed_bookings(users, rooms, customers, services)
        db.session.commit()


if __name__ == "__main__":
    run_seed()
