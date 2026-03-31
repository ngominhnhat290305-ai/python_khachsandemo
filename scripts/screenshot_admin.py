import argparse
import os
import re
import time
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright


def _safe_name(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\-_/]+", "-", s)
    s = s.strip("-")
    s = s.replace("/", "_")
    return s or "page"


def _wait_ready(page, timeout_ms: int = 20000):
    try:
        page.wait_for_load_state("domcontentloaded", timeout=timeout_ms)
    except Exception:
        pass
    try:
        page.wait_for_load_state("networkidle", timeout=timeout_ms)
    except Exception:
        pass
    page.wait_for_timeout(300)


def _ensure_logged_in(page, base_url: str, username: str, password: str):
    page.goto(urljoin(base_url, "/dashboard"), wait_until="domcontentloaded")
    if "/login" not in page.url:
        return
    page.goto(urljoin(base_url, "/login"), wait_until="domcontentloaded")
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    _wait_ready(page)
    if "/login" in page.url:
        raise RuntimeError("Đăng nhập thất bại (vẫn ở /login). Kiểm tra username/password.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=os.getenv("BASE_URL", "http://127.0.0.1:5000"))
    ap.add_argument("--out", default="screenshots/admin")
    ap.add_argument("--username", default=os.getenv("HMS_ADMIN_USER", "admin"))
    ap.add_argument("--password", default=os.getenv("HMS_ADMIN_PASS", "Admin@123"))
    ap.add_argument("--headless", action="store_true", default=True)
    ap.add_argument("--no-headless", action="store_false", dest="headless")
    ap.add_argument("--delay-ms", type=int, default=250)
    args = ap.parse_args()

    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    routes = [
        ("/dashboard", "01_dashboard"),
        ("/assistant", "02_assistant"),
        ("/users", "03_users"),
        ("/room-types", "04_room_types"),
        ("/rooms", "05_rooms"),
        ("/rooms/floor-map", "06_floor_map"),
        ("/customers", "07_customers"),
        ("/bookings", "08_bookings"),
        ("/bookings/calendar", "09_calendar"),
        ("/invoices", "10_invoices"),
        ("/services", "11_services"),
        ("/reports", "12_reports"),
        ("/profile", "13_profile"),
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        _ensure_logged_in(page, args.base_url, args.username, args.password)

        for route, label in routes:
            url = urljoin(args.base_url, route)
            page.goto(url, wait_until="domcontentloaded")
            _wait_ready(page)
            time.sleep(max(0, args.delay_ms) / 1000)
            name = _safe_name(label)
            path = out_dir / f"{name}.png"
            page.screenshot(path=str(path), full_page=True)

        browser.close()

    print(f"OK: saved {len(routes)} screenshots to {out_dir}")


if __name__ == "__main__":
    main()
