import uuid
from pathlib import Path

from flask import current_app
from PIL import Image
from werkzeug.datastructures import FileStorage


class ImageService:
    @staticmethod
    def save_avatar(file: FileStorage, entity_type: str, entity_id: int) -> str:
        folder = current_app.config["AVATARS_FOLDER"]
        folder.mkdir(parents=True, exist_ok=True)
        ext = file.filename.rsplit(".", 1)[-1].lower()
        filename = f"{entity_type}_{entity_id}_{uuid.uuid4().hex[:8]}.{ext}"
        dest = folder / filename
        _save_resized(file, dest, size=(300, 300))
        return f"images/avatars/{filename}"

    @staticmethod
    def save_room_image(file: FileStorage, room_number: str, index: int) -> str:
        folder = current_app.config["ROOMS_FOLDER"]
        folder.mkdir(parents=True, exist_ok=True)
        ext = file.filename.rsplit(".", 1)[-1].lower()
        safe_num = room_number.replace("/", "_")
        filename = f"room_{safe_num}_{index}_{uuid.uuid4().hex[:8]}.{ext}"
        dest = folder / filename
        _save_resized(file, dest, size=(1000, 700))
        return f"images/rooms/{filename}"

    @staticmethod
    def save_room_type_image(file: FileStorage, type_name: str) -> str:
        folder = current_app.config["ROOM_TYPES_FOLDER"]
        folder.mkdir(parents=True, exist_ok=True)
        ext = file.filename.rsplit(".", 1)[-1].lower()
        safe = type_name.lower().replace(" ", "_")
        filename = f"type_{safe}_{uuid.uuid4().hex[:8]}.{ext}"
        dest = folder / filename
        _save_resized(file, dest, size=(800, 600))
        return f"images/room_types/{filename}"

    @staticmethod
    def delete(relative_path: str):
        if not relative_path:
            return
        static_dir = Path(current_app.root_path) / "static"
        full = (static_dir / relative_path).resolve()
        try:
            static_root = static_dir.resolve()
        except FileNotFoundError:
            return
        if static_root not in full.parents:
            return
        if full.exists() and full.is_file():
            full.unlink(missing_ok=True)


def _save_resized(file: FileStorage, dest: Path, size: tuple):
    img = Image.open(file.stream).convert("RGB")
    img.thumbnail(size, Image.LANCZOS)
    img.save(dest, quality=88, optimize=True)
