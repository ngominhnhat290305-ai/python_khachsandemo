import re

from flask import Blueprint, jsonify, render_template, request, session
from flask_login import current_user, login_required
from markdown import markdown

from app.services.chat_service import ChatService
from app.services.assistant_queries import answer_from_db

bp = Blueprint("assistant", __name__, url_prefix="/assistant")


def _md_to_html(md_text: str) -> str:
    html = markdown(md_text or "", extensions=["fenced_code", "tables", "sane_lists"])
    html = re.sub(r"(?is)<script.*?>.*?</script>", "", html)
    return html


@bp.route("/")
@login_required
def index():
    return render_template("assistant/index.html")


@bp.route("/api", methods=["POST"])
@login_required
def api():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"success": False, "message": "Vui lòng nhập nội dung."}), 400

    history = session.get("assistant_history") or []
    if not isinstance(history, list):
        history = []

    history.append({"role": "user", "content": message})
    history = history[-12:]

    handled, direct_md = answer_from_db(message, current_user)
    if handled and direct_md:
        assistant_md = direct_md
        history.append({"role": "assistant", "content": assistant_md})
        session["assistant_history"] = history[-12:]
        return jsonify({"success": True, "markdown": assistant_md, "html": _md_to_html(assistant_md)})

    system_prompt = ChatService.build_system_prompt(current_user.role)
    messages = [{"role": "system", "content": system_prompt}] + history

    ok, assistant_md = ChatService.call_openai(messages)
    if not ok:
        assistant_md = f"**Lỗi:** {assistant_md}"

    history.append({"role": "assistant", "content": assistant_md})
    session["assistant_history"] = history[-12:]

    return jsonify(
        {
            "success": True,
            "markdown": assistant_md,
            "html": _md_to_html(assistant_md),
        }
    )


@bp.route("/reset", methods=["POST"])
@login_required
def reset():
    session.pop("assistant_history", None)
    return jsonify({"success": True})
