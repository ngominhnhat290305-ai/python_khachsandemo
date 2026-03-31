import os
from datetime import datetime
from pathlib import Path

import requests
from sqlalchemy import inspect

from app.extensions import db


class ChatService:
    @staticmethod
    def _read_inject_file(filename: str) -> str:
        root = Path(__file__).resolve().parents[2]
        path = root / filename
        try:
            return path.read_text(encoding="utf-8").strip()
        except Exception:
            return ""

    @staticmethod
    def build_schema_context() -> str:
        try:
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            lines = ["## Schema DB (tóm tắt)"]
            for t in sorted(tables):
                cols = inspector.get_columns(t)
                col_parts = []
                for c in cols:
                    col_parts.append(f"{c['name']}:{str(c['type'])}")
                lines.append(f"- {t}: " + ", ".join(col_parts))
            return "\n".join(lines)
        except Exception:
            return "## Schema DB (tóm tắt)\n- Không truy cập được DB để lấy schema (vui lòng kiểm tra MySQL)."

    @staticmethod
    def build_system_prompt(role: str) -> str:
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        injected_prompt = ChatService._read_inject_file("prompt.md")
        injected_rules = ChatService._read_inject_file("rules.md")
        schema_md = ChatService.build_schema_context()
        perms = (
            "Admin: full quyền theo đặc tả (users, room_types, rooms, customers, bookings, invoices, services, reports)."
            if role == "ADMIN"
            else "Receptionist: xem phòng, CRUD customers, tạo/sửa/huỷ booking của mình + hôm nay, check-in/out, xem hoá đơn do mình tạo."
        )
        parts = [
            f"Thời gian hiện tại: {now}",
            f"Vai trò người dùng hiện tại: {role}",
            f"Quyền: {perms}",
        ]
        if injected_prompt:
            parts.append("\n# Inject: prompt.md\n" + injected_prompt)
        if injected_rules:
            parts.append("\n# Inject: rules.md\n" + injected_rules)
        parts.append("\n" + schema_md)
        return "\n".join(parts).strip()

    @staticmethod
    def call_openai(messages: list[dict]) -> tuple[bool, str]:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            return False, "Thiếu OPENAI_API_KEY. Vui lòng set trong file .env rồi restart server."

        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"

        url = f"{base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 900,
        }
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
        except Exception:
            return False, "Không gọi được OpenAI API. Kiểm tra mạng hoặc OPENAI_BASE_URL."

        if resp.status_code >= 400:
            return False, f"OpenAI API lỗi ({resp.status_code}). Vui lòng kiểm tra token/model."

        data = resp.json()
        content = (((data.get("choices") or [{}])[0].get("message") or {}).get("content") or "").strip()
        if not content:
            return False, "OpenAI không trả nội dung."
        return True, content
