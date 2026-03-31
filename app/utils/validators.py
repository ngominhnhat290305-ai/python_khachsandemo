import re


def validate_new_password(password: str) -> tuple[bool, str]:
    if password is None:
        return False, "Mật khẩu không hợp lệ."
    if len(password) < 8:
        return False, "Mật khẩu mới phải ít nhất 8 ký tự."
    if not re.search(r"[A-Z]", password):
        return False, "Mật khẩu mới phải có ít nhất 1 chữ hoa."
    if not re.search(r"\d", password):
        return False, "Mật khẩu mới phải có ít nhất 1 số."
    return True, "OK"


def parse_json_list(form, key: str) -> list[str]:
    raw = form.get(key, "").strip()
    if not raw:
        return []
    parts = [p.strip() for p in raw.split(",")]
    return [p for p in parts if p]


def parse_money(value) -> float:
    raw = str(value or "")
    digits = re.sub(r"[^\d]", "", raw)
    return float(digits) if digits else 0.0
