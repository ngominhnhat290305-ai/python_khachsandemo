from datetime import date
from io import BytesIO

from flask import Blueprint, Response, render_template, request
from flask_login import login_required
from openpyxl import Workbook
from sqlalchemy import func

from app.extensions import db
from app.models.invoice import Invoice
from app.utils.decorators import admin_required

bp = Blueprint("reports", __name__, url_prefix="/reports")


@bp.route("/")
@login_required
@admin_required
def index():
    today = date.today()
    month = request.args.get("month", today.month, type=int)
    year = request.args.get("year", today.year, type=int)

    rows = (
        db.session.query(func.date(Invoice.paid_at).label("d"), func.sum(Invoice.total_amount).label("rev"))
        .filter(
            Invoice.payment_status == "PAID",
            func.month(Invoice.paid_at) == month,
            func.year(Invoice.paid_at) == year,
        )
        .group_by(func.date(Invoice.paid_at))
        .order_by(func.date(Invoice.paid_at))
        .all()
    )
    labels = [r.d.strftime("%d/%m") for r in rows]
    data = [float(r.rev or 0) for r in rows]
    total = sum(data)

    return render_template("reports/index.html", month=month, year=year, labels=labels, data=data, total=total)


@bp.route("/export")
@login_required
@admin_required
def export():
    today = date.today()
    report_type = request.args.get("type", "revenue")
    month = request.args.get("month", today.month, type=int)
    year = request.args.get("year", today.year, type=int)

    if report_type != "revenue":
        return Response("Unsupported report type", status=400)

    rows = (
        db.session.query(func.date(Invoice.paid_at).label("d"), func.sum(Invoice.total_amount).label("rev"))
        .filter(
            Invoice.payment_status == "PAID",
            func.month(Invoice.paid_at) == month,
            func.year(Invoice.paid_at) == year,
        )
        .group_by(func.date(Invoice.paid_at))
        .order_by(func.date(Invoice.paid_at))
        .all()
    )

    wb = Workbook()
    ws = wb.active
    ws.title = "Revenue"
    ws.append(["Ngày", "Doanh thu (VNĐ)"])
    total = 0
    for r in rows:
        rev = float(r.rev or 0)
        total += rev
        ws.append([r.d.strftime("%d/%m/%Y"), rev])
    ws.append([])
    ws.append(["Tổng", total])

    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)

    filename = f"revenue_{year}_{month:02d}.xlsx"
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }
    return Response(buf.getvalue(), headers=headers)
