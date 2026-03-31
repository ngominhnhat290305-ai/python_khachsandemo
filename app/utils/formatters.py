from datetime import datetime


def format_currency(amount, suffix=" VNĐ") -> str:
    if amount is None:
        return "0" + suffix
    return f"{int(float(amount)):,}".replace(",", ".") + suffix


def format_date(d, fmt="%d/%m/%Y") -> str:
    if d is None:
        return "—"
    if isinstance(d, datetime):
        d = d.date()
    return d.strftime(fmt)


def format_datetime(dt, fmt="%d/%m/%Y %H:%M") -> str:
    if dt is None:
        return "—"
    return dt.strftime(fmt)
