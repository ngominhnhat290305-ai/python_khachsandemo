from datetime import datetime

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.config import Config
from app.extensions import db
from app.models.invoice import Invoice

bp = Blueprint("invoices", __name__, url_prefix="/invoices")


@bp.route("/")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    status = request.args.get("status")

    q = Invoice.query
    if not current_user.is_admin:
        q = q.filter(Invoice.created_by == current_user.id)
    if status:
        q = q.filter(Invoice.payment_status == status)

    invoices = q.order_by(Invoice.created_at.desc()).paginate(page=page, per_page=Config.PER_PAGE, error_out=False)
    return render_template("invoices/index.html", invoices=invoices)


@bp.route("/<int:id>")
@login_required
def detail(id):
    invoice = Invoice.query.get_or_404(id)
    if not current_user.is_admin and invoice.created_by != current_user.id:
        return redirect(url_for("invoices.index"))
    return render_template("invoices/detail.html", invoice=invoice)


@bp.route("/<int:id>/pay", methods=["POST"])
@login_required
def pay(id):
    invoice = Invoice.query.get_or_404(id)
    if not current_user.is_admin and invoice.created_by != current_user.id:
        return jsonify({"success": False, "message": "Không có quyền."})
    if invoice.payment_status == "PAID":
        return jsonify({"success": True, "message": "Hóa đơn đã thanh toán."})

    method = (request.json or {}).get("payment_method") or "CASH"
    if method not in ("CASH", "CARD", "TRANSFER", "MIXED"):
        return jsonify({"success": False, "message": "Phương thức không hợp lệ."})

    invoice.payment_method = method
    invoice.payment_status = "PAID"
    invoice.paid_at = datetime.utcnow()
    db.session.commit()
    return jsonify({"success": True, "message": "Đã xác nhận thanh toán."})
