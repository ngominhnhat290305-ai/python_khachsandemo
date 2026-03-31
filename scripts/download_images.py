import urllib.request
from pathlib import Path

STATIC = Path(__file__).resolve().parent.parent / "app" / "static" / "images"
for d in ["avatars", "rooms", "room_types", "default"]:
    (STATIC / d).mkdir(parents=True, exist_ok=True)

AVATARS = {
    "user_admin.jpg": "https://randomuser.me/api/portraits/men/32.jpg",
    "user_recept1.jpg": "https://randomuser.me/api/portraits/women/44.jpg",
    "user_recept2.jpg": "https://randomuser.me/api/portraits/men/55.jpg",
    "customer_1.jpg": "https://randomuser.me/api/portraits/men/11.jpg",
    "customer_2.jpg": "https://randomuser.me/api/portraits/women/12.jpg",
    "customer_3.jpg": "https://randomuser.me/api/portraits/men/23.jpg",
    "customer_4.jpg": "https://randomuser.me/api/portraits/women/34.jpg",
    "customer_5.jpg": "https://randomuser.me/api/portraits/women/45.jpg",
    "customer_6.jpg": "https://randomuser.me/api/portraits/men/45.jpg",
    "customer_7.jpg": "https://randomuser.me/api/portraits/women/56.jpg",
    "customer_8.jpg": "https://randomuser.me/api/portraits/men/67.jpg",
}

ROOM_TYPES_IMGS = {
    "standard.jpg": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=700&q=80",
    "deluxe.jpg": "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=700&q=80",
    "suite.jpg": "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=700&q=80",
    "presidential.jpg": "https://images.unsplash.com/photo-1541971875076-8f970d573be6?w=700&q=80",
    "family.jpg": "https://images.unsplash.com/photo-1595576508898-0ad5c879a061?w=700&q=80",
}

ROOMS_IMGS = {
    "room_101_1.jpg": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80",
    "room_101_2.jpg": "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800&q=80",
    "room_102_1.jpg": "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800&q=80",
    "room_103_1.jpg": "https://images.unsplash.com/photo-1595576508898-0ad5c879a061?w=800&q=80",
    "room_201_1.jpg": "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800&q=80",
    "room_201_2.jpg": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&q=80",
    "room_202_1.jpg": "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    "room_202_2.jpg": "https://images.unsplash.com/photo-1560185007-c5ca9d2c014d?w=800&q=80",
    "room_301_1.jpg": "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=800&q=80",
    "room_301_2.jpg": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800&q=80",
    "room_401_1.jpg": "https://images.unsplash.com/photo-1541971875076-8f970d573be6?w=800&q=80",
    "room_401_2.jpg": "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800&q=80",
    "room_401_3.jpg": "https://images.unsplash.com/photo-1602595624657-7af5a89c5bc4?w=800&q=80",
}

DEFAULTS = {
    "avatar.png": "https://ui-avatars.com/api/?name=User&background=8B6F47&color=fff&size=200&bold=true",
    "room.png": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=60",
}


def download(url: str, dest: Path):
    if dest.exists():
        return
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            dest.write_bytes(r.read())
    except Exception:
        _placeholder(dest)


def _placeholder(dest: Path):
    try:
        from PIL import Image, ImageDraw, ImageFont

        is_avatar = dest.parent.name == "avatars" or dest.name.startswith(("user_", "customer_")) or dest.name == "avatar.png"
        size = (220, 220) if is_avatar else (900, 650)
        img = Image.new("RGB", size, "#F5F0E8")
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, size[0], size[1]], outline="#EDE8DF", width=12)
        text = "No Image"
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None
        bbox = draw.textbbox((0, 0), text, font=font)
        x = (size[0] - (bbox[2] - bbox[0])) // 2
        y = (size[1] - (bbox[3] - bbox[1])) // 2
        draw.text((x, y), text, fill="#7D6355", font=font)
        img.save(dest)
    except Exception:
        dest.write_bytes(b"")


if __name__ == "__main__":
    for f, u in AVATARS.items():
        download(u, STATIC / "avatars" / f)
    for f, u in ROOM_TYPES_IMGS.items():
        download(u, STATIC / "room_types" / f)
    for f, u in ROOMS_IMGS.items():
        download(u, STATIC / "rooms" / f)
    for f, u in DEFAULTS.items():
        download(u, STATIC / "default" / f)
