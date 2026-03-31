from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify
from flask_login import login_required

from app.extensions import db
from app.models.room import Room
from app.models.room_type import RoomType
from app.services.image_service import ImageService
from app.utils.decorators import admin_required
from app.utils.validators import parse_json_list, parse_money

bp = Blueprint("room_types", __name__, url_prefix="/room-types")


@bp.route("/")
@login_required
@admin_required
def index():
    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)

    query = RoomType.query.filter_by(is_deleted=0)
    if q:
        query = query.filter(RoomType.name.like(f"%{q}%"))

    room_types = query.order_by(RoomType.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template("room_types/index.html", room_types=room_types)


@bp.route("/deleted")
@login_required
@admin_required
def deleted():
    page = request.args.get("page", 1, type=int)
    room_types = RoomType.query.filter_by(is_deleted=1).order_by(RoomType.deleted_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template("room_types/deleted.html", room_types=room_types)


@bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Vui lòng nhập tên hạng phòng.", "error")
            return redirect(url_for("room_types.create"))

        rt = RoomType(
            name=name,
            description=request.form.get("description"),
            base_price=parse_money(request.form.get("base_price")),
            max_adults=int(request.form.get("max_adults") or 2),
            max_children=int(request.form.get("max_children") or 1),
            amenities=parse_json_list(request.form, "amenities"),
        )
        db.session.add(rt)
        db.session.flush()

        img = request.files.get("image")
        if img and img.filename:
            rt.image_path = ImageService.save_room_type_image(img, name)

        db.session.commit()
        flash("Thêm hạng phòng thành công.", "success")
        return redirect(url_for("room_types.index"))

    return render_template("room_types/form.html", room_type=None)


@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit(id):
    rt = RoomType.query.get_or_404(id)
    if rt.is_deleted:
        flash("Hạng phòng đã bị xóa.", "error")
        return redirect(url_for("room_types.index"))

    if request.method == "POST":
        rt.name = request.form.get("name", "").strip() or rt.name
        rt.description = request.form.get("description")
        rt.base_price = parse_money(request.form.get("base_price"))
        rt.max_adults = int(request.form.get("max_adults") or 2)
        rt.max_children = int(request.form.get("max_children") or 1)
        rt.amenities = parse_json_list(request.form, "amenities")

        img = request.files.get("image")
        if img and img.filename:
            old = rt.image_path
            rt.image_path = ImageService.save_room_type_image(img, rt.name)
            if old and old != rt.image_path:
                ImageService.delete(old)

        db.session.commit()
        flash("Cập nhật hạng phòng thành công.", "success")
        return redirect(url_for("room_types.index"))

    return render_template("room_types/form.html", room_type=rt)


@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
@admin_required
def delete(id):
    rt = RoomType.query.get_or_404(id)
    has_rooms = Room.query.filter_by(room_type_id=id, is_deleted=0).count() > 0
    if has_rooms:
        return jsonify({"success": False, "message": "Không thể xóa: có phòng đang dùng hạng này."})
    rt.soft_delete()
    db.session.commit()
    return jsonify({"success": True, "message": "Đã xóa hạng phòng."})


@bp.route("/<int:id>/restore", methods=["POST"])
@login_required
@admin_required
def restore(id):
    rt = RoomType.query.get_or_404(id)
    rt.restore()
    db.session.commit()
    return jsonify({"success": True, "message": "Đã khôi phục hạng phòng."})
