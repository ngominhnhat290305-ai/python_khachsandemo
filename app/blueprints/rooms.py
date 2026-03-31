from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.config import Config
from app.extensions import db
from app.models.booking import Booking
from app.models.room import Room
from app.models.room_type import RoomType
from app.services.image_service import ImageService
from app.utils.decorators import admin_required
from app.utils.validators import parse_money

bp = Blueprint("rooms", __name__, url_prefix="/rooms")


@bp.route("/")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", "").strip()
    floor = request.args.get("floor", type=int)
    status = request.args.get("status")
    bed_type = request.args.get("bed_type")
    rt_id = request.args.get("room_type_id", type=int)

    query = Room.query.filter_by(is_deleted=0).join(RoomType)
    if q:
        query = query.filter(Room.room_number.like(f"%{q}%"))
    if floor:
        query = query.filter(Room.floor == floor)
    if status:
        query = query.filter(Room.status == status)
    if bed_type:
        query = query.filter(Room.bed_type == bed_type)
    if rt_id:
        query = query.filter(Room.room_type_id == rt_id)

    rooms = query.order_by(Room.floor, Room.room_number).paginate(page=page, per_page=Config.PER_PAGE, error_out=False)
    room_types = RoomType.query.filter_by(is_deleted=0).all()
    floors = [f[0] for f in db.session.query(Room.floor).filter_by(is_deleted=0).distinct().order_by(Room.floor).all()]

    return render_template("rooms/index.html", rooms=rooms, room_types=room_types, floors=floors)


@bp.route("/floor-map")
@login_required
def floor_map():
    rooms = Room.query.filter_by(is_deleted=0).order_by(Room.floor, Room.room_number).all()
    floors = {}
    for r in rooms:
        floors.setdefault(r.floor, []).append(r)
    return render_template("rooms/floor_map.html", floors=floors)


@bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create():
    if request.method == "POST":
        room_number = request.form.get("room_number", "").strip()
        if not room_number:
            flash("Vui lòng nhập số phòng.", "error")
            return redirect(url_for("rooms.create"))
        if Room.query.filter_by(room_number=room_number).first():
            flash(f"Số phòng {room_number} đã tồn tại.", "error")
            return redirect(url_for("rooms.create"))

        room = Room(
            room_number=room_number,
            floor=int(request.form.get("floor") or 1),
            room_type_id=int(request.form.get("room_type_id") or 0),
            bed_type=request.form.get("bed_type") or "DOUBLE",
            price_override=parse_money(request.form.get("price_override")) if request.form.get("price_override") else None,
            description=request.form.get("description"),
        )
        db.session.add(room)
        db.session.flush()

        images = request.files.getlist("images")
        paths = []
        for i, f in enumerate(images[: Config.MAX_ROOM_IMAGES]):
            if f and f.filename:
                paths.append(ImageService.save_room_image(f, room_number, i + 1))
        room.image_paths = paths if paths else None

        db.session.commit()
        flash(f"Thêm phòng {room_number} thành công.", "success")
        return redirect(url_for("rooms.index"))

    room_types = RoomType.query.filter_by(is_deleted=0).all()
    return render_template("rooms/form.html", room=None, room_types=room_types)


@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit(id):
    room = Room.query.get_or_404(id)
    if room.is_deleted:
        flash("Phòng đã bị xóa.", "error")
        return redirect(url_for("rooms.index"))

    if request.method == "POST":
        room_number = request.form.get("room_number", "").strip()
        if not room_number:
            flash("Vui lòng nhập số phòng.", "error")
            return redirect(url_for("rooms.edit", id=id))
        exists = Room.query.filter(Room.room_number == room_number, Room.id != id).first()
        if exists:
            flash(f"Số phòng {room_number} đã tồn tại.", "error")
            return redirect(url_for("rooms.edit", id=id))

        room.room_number = room_number
        room.floor = int(request.form.get("floor") or 1)
        room.room_type_id = int(request.form.get("room_type_id") or room.room_type_id)
        room.bed_type = request.form.get("bed_type") or room.bed_type
        room.price_override = parse_money(request.form.get("price_override")) if request.form.get("price_override") else None
        room.description = request.form.get("description")

        current_paths = list(room.image_paths or [])
        remove_paths = request.form.getlist("remove_images")
        if remove_paths:
            remaining = [p for p in current_paths if p not in set(remove_paths)]
            for p in remove_paths:
                if p in current_paths:
                    ImageService.delete(p)
            current_paths = remaining

        uploads = request.files.getlist("images")
        allowed_slots = max(0, Config.MAX_ROOM_IMAGES - len(current_paths))
        next_index = len(current_paths) + 1
        for i, f in enumerate(uploads[:allowed_slots]):
            if f and f.filename:
                current_paths.append(ImageService.save_room_image(f, room.room_number, next_index + i))

        room.image_paths = current_paths if current_paths else None
        db.session.commit()
        flash("Cập nhật phòng thành công.", "success")
        return redirect(url_for("rooms.index"))

    room_types = RoomType.query.filter_by(is_deleted=0).all()
    return render_template("rooms/form.html", room=room, room_types=room_types)


@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
@admin_required
def delete(id):
    room = Room.query.get_or_404(id)
    has_active = (
        Booking.query.filter(
            Booking.room_id == id,
            Booking.is_deleted == 0,
            Booking.status.in_(["PENDING", "CONFIRMED", "CHECKED_IN"]),
        ).count()
        > 0
    )
    if has_active:
        return jsonify({"success": False, "message": "Không thể xóa: phòng đang có booking active."})
    room.soft_delete()
    db.session.commit()
    return jsonify({"success": True, "message": f"Đã xóa phòng {room.room_number}."})


@bp.route("/<int:id>/status", methods=["POST"])
@login_required
@admin_required
def update_status(id):
    room = Room.query.get_or_404(id)
    status = (request.json or {}).get("status")
    valid = ["AVAILABLE", "RESERVED", "OCCUPIED", "CLEANING", "MAINTENANCE"]
    if status not in valid:
        return jsonify({"success": False, "message": "Trạng thái không hợp lệ."})
    room.status = status
    db.session.commit()
    return jsonify({"success": True, "message": "Cập nhật trạng thái thành công."})
