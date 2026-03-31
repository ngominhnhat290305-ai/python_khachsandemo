<h1 align="center">🏨 Hotel Management System (HMS)</h1>
<h3 align="center">Hệ Thống Quản Lý Khách Sạn Toàn Diện</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-3.1.x-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL"/>
  <img src="https://img.shields.io/badge/TailwindCSS-CDN-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="TailwindCSS"/>
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI"/>
</p>


<p align="center">
  <b>HMS</b> là hệ thống quản lý khách sạn chuyên nghiệp, tích hợp <b>AI Chatbot</b> (OpenAI GPT) hỗ trợ nghiệp vụ, được xây dựng trên nền tảng <b>Flask + MySQL</b> với giao diện Dashboard hiện đại sử dụng <b>TailwindCSS</b>. Hệ thống phân quyền rõ ràng giữa <b>Admin</b> và <b>Lễ tân</b>, đáp ứng đầy đủ quy trình vận hành khách sạn từ đặt phòng, check-in/out, quản lý dịch vụ đến xuất hóa đơn & báo cáo doanh thu.
</p>

---

## 🌟 TÍNH NĂNG NỔI BẬT (Key Features)

### 1. 📊 Dashboard Thông Minh
- Tổng quan trạng thái phòng theo thời gian thực (Trống / Đang ở / Bảo trì)
- Danh sách Check-in / Check-out trong ngày
- Biểu đồ doanh thu 12 tháng (Chart.js)
- Giao diện riêng cho **Admin** và **Lễ tân**

### 2. 🤖 Trợ Lý AI (AI Assistant)
- Tích hợp **OpenAI GPT-4o-mini** (hoặc model tuỳ chỉnh)
- Trả lời câu hỏi nghiệp vụ bằng **Tiếng Việt**
- Tự động truy vấn DB: tra cứu giá phòng, doanh thu, hóa đơn, top khách hàng...
- Hiểu đơn vị tiền Việt rút gọn: `500k`, `1tr2`, `2ty3tr`
- Hỗ trợ tính toán biểu thức tiền tệ: `500k + 1tr - 200k`
- Phân quyền trả lời theo role (Admin / Lễ tân)

### 3. 🛏️ Quản Lý Phòng & Hạng Phòng
- CRUD hạng phòng: Standard, Deluxe, Suite, Presidential, Family
- CRUD phòng: số phòng, tầng, loại giường, ảnh phòng (tối đa 5 ảnh)
- Trạng thái phòng: `Trống` · `Đã đặt` · `Đang có khách` · `Đang dọn` · `Bảo trì`
- Hỗ trợ ghi đè giá riêng từng phòng (`price_override`)

### 4. 📅 Đặt Phòng (Booking)
- Tạo / Sửa / Huỷ booking với mã tự động (`HMS-YYYYMMDD-XXXXXX`)
- Kiểm tra trùng lịch trên cùng phòng
- Quy trình: `Chờ xác nhận` → `Đã xác nhận` → `Check-in` → `Check-out` → `Đã huỷ`
- Check-in chuẩn sau 14:00, Check-out chuẩn trước 12:00 (cảnh báo sớm/muộn)
- Quản lý đặt cọc, yêu cầu đặc biệt, ghi chú

### 5. 👥 Quản Lý Khách Hàng
- Thông tin: Họ tên, CCCD/Passport/GPLX, giới tính, ngày sinh, SĐT, email
- Hỗ trợ khách quốc tế (nationality)
- Upload ảnh đại diện khách hàng
- Xoá mềm (soft delete)

### 6. 🧾 Hóa Đơn (Invoice)
- Tự động tính: `Tiền phòng + Dịch vụ - Giảm giá + VAT 10%`
- Mã hóa đơn tự sinh (`INV-YYYYMMDD-XXXXXX`)
- Phương thức thanh toán: Tiền mặt / Thẻ / Chuyển khoản / Kết hợp
- Trạng thái: Chưa thanh toán / Thanh toán một phần / Đã thanh toán

### 7. 🍽️ Quản Lý Dịch Vụ
- Danh mục: Ăn uống, Giặt ủi, Đặt xe, Spa, Khác
- Thêm dịch vụ vào booking (chỉ khi đang ở - `CHECKED_IN`)
- Tính giá theo số lượng × đơn giá

### 8. 📈 Báo Cáo & Xuất Excel
- Báo cáo doanh thu theo tháng/năm (biểu đồ)
- Xuất file `.xlsx` chi tiết doanh thu (openpyxl)
- Chỉ Admin mới có quyền truy cập

### 9. 👤 Quản Lý Nhân Viên & Phân Quyền
- 2 role: **Admin** (toàn quyền) và **Receptionist** (lễ tân)
- Quản lý tài khoản: tạo / khoá / xoá mềm
- Đổi mật khẩu, cập nhật profile, avatar
- Theo dõi lần đăng nhập cuối, số lần thử đăng nhập sai

---

## 🏗️ KIẾN TRÚC DỰ ÁN (Project Architecture)

```
python_khachsan/
├── app/
│   ├── blueprints/          # 📌 Các route/controller (12 blueprints)
│   │   ├── assistant.py     #     AI Chatbot API
│   │   ├── auth.py          #     Đăng nhập, đăng xuất, đổi mật khẩu
│   │   ├── bookings.py      #     CRUD đặt phòng, check-in/out
│   │   ├── customers.py     #     CRUD khách hàng
│   │   ├── dashboard.py     #     Trang tổng quan
│   │   ├── invoices.py      #     CRUD hóa đơn
│   │   ├── profile.py       #     Cập nhật thông tin cá nhân
│   │   ├── reports.py       #     Báo cáo + xuất Excel
│   │   ├── room_types.py    #     CRUD hạng phòng
│   │   ├── rooms.py         #     CRUD phòng
│   │   ├── services.py      #     CRUD dịch vụ
│   │   └── users.py         #     Quản lý nhân viên (Admin)
│   ├── models/              # 📦 ORM Models (SQLAlchemy)
│   │   ├── booking.py       #     Booking + BookingService
│   │   ├── customer.py      #     Khách hàng
│   │   ├── invoice.py       #     Hóa đơn
│   │   ├── room.py          #     Phòng
│   │   ├── room_type.py     #     Hạng phòng
│   │   ├── service.py       #     Dịch vụ
│   │   ├── user.py          #     Tài khoản nhân viên
│   │   └── mixins.py        #     Soft delete mixin
│   ├── services/            # ⚙️ Business Logic Layer
│   │   ├── assistant_queries.py  # Truy vấn DB cho AI
│   │   ├── booking_service.py    # Logic đặt phòng
│   │   ├── chat_service.py       # Gọi OpenAI API
│   │   ├── image_service.py      # Upload/xử lý ảnh
│   │   └── invoice_service.py    # Logic hóa đơn
│   ├── templates/           # 🎨 Jinja2 Templates
│   │   ├── base.html        #     Layout chính (sidebar + topbar)
│   │   ├── assistant/       #     Giao diện chatbot
│   │   ├── auth/            #     Đăng nhập / đổi mật khẩu
│   │   ├── bookings/        #     Đặt phòng
│   │   ├── customers/       #     Khách hàng
│   │   ├── dashboard/       #     Dashboard (admin / receptionist)
│   │   ├── invoices/        #     Hóa đơn
│   │   ├── profile/         #     Hồ sơ cá nhân
│   │   ├── reports/         #     Báo cáo
│   │   ├── room_types/      #     Hạng phòng
│   │   ├── rooms/           #     Phòng
│   │   ├── services/        #     Dịch vụ
│   │   └── users/           #     Nhân viên
│   ├── static/              # 🖼️ Static Files
│   │   ├── css/custom.css   #     CSS tuỳ chỉnh
│   │   ├── js/main.js       #     JavaScript chính
│   │   ├── js/image-preview.js   # Preview upload ảnh
│   │   └── images/          #     Ảnh upload (avatars, rooms,...)
│   ├── utils/               # 🔧 Tiện ích
│   │   ├── decorators.py    #     @admin_required,...
│   │   ├── formatters.py    #     format_currency, format_date
│   │   ├── helpers.py       #     Hàm helper chung
│   │   ├── labels.py        #     Mapping enum → tiếng Việt
│   │   └── validators.py    #     Validate dữ liệu đầu vào
│   ├── __init__.py          # 🏭 App Factory (create_app)
│   ├── config.py            # ⚙️ Cấu hình (DB, upload, session,...)
│   └── extensions.py        # 🔌 Flask Extensions (SQLAlchemy, Login,...)
├── migrations/              # 🔄 Alembic migrations
├── scripts/
│   ├── seed.py              # 🌱 Seed dữ liệu mẫu
│   └── download_images.py   # 📥 Tải ảnh mẫu
├── .env.example             # 📋 Mẫu biến môi trường
├── hotel_db.sql             # 💾 SQL dump cơ sở dữ liệu
├── manage.py                # 🖥️ Flask CLI
├── run.py                   # 🚀 Entry point chạy server
├── requirements.txt         # 📦 Dependencies
├── prompt.md                # 🤖 System prompt cho AI
└── rules.md                 # 📜 Rules inject cho AI
```

---

## 🛠️ CÔNG NGHỆ SỬ DỤNG (Tech Stack)

| Thành phần | Công nghệ |
|---|---|
| **Backend** | Python 3.11+, Flask 3.1.x |
| **ORM / Migration** | Flask-SQLAlchemy , Flask-Migrate (Alembic) |
| **Database** | MySQL 8.0 |
| **Authentication** | Flask-Login , Flask-Bcrypt |
| **Frontend** | TailwindCSS (CDN), Jinja2, Vanilla JavaScript |
| **UI Components** | Font Awesome 6.5, Google Fonts (Playfair Display + Inter) |
| **Charts** | Chart.js  |
| **AI Chatbot** | OpenAI API (GPT-4o-mini) |
| **Image Processing** | Pillow  |
| **Excel Export** | openpyxl |
| **PDF/Screenshot** | Playwright  |
| **HTTP Client** | Requests |
| **Environment** | python-dotenv|

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT & SỬ DỤNG

### 📋 Yêu cầu hệ thống

- **Python** >= 3.11
- **MySQL** >= 8.0
- **Git**
- (Tuỳ chọn) **OpenAI API Key** — nếu muốn dùng tính năng AI Chatbot

### 1️⃣ Clone dự án

```bash
git clone <repository-url>
cd python_khachsan
```

### 2️⃣ Tạo môi trường ảo & cài thư viện

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3️⃣ Cấu hình biến môi trường

```bash
cp .env.example .env
```

Mở file `.env` và điền thông tin:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=hotel_db
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
SECRET_KEY=your-super-secret-key-change-me
DEBUG=True

# (Tuỳ chọn) AI Chatbot
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 4️⃣ Tạo Database & Import dữ liệu mẫu

```bash
# Tạo database trong MySQL
mysql -u root -p -e "CREATE DATABASE hotel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"

# Import SQL dump (có sẵn dữ liệu mẫu)
mysql -u root -p hotel_db < hotel_db.sql
```

### 5️⃣ Chạy ứng dụng

```bash
python run.py
```

Truy cập: **http://localhost:5000**

### 6️⃣ Tài khoản mặc định

| Vai trò | Username | Password | Mô tả |
|---|---|---|---|
| 🔑 Admin | `admin` | `admin@123` | Toàn quyền quản trị |
| 👤 Lễ tân | `letan1` | `letan@123` | Quyền lễ tân |
| 👤 Lễ tân | `letan2` | `letan@123` | Quyền lễ tân |

> ⚠️ **Lưu ý:** Hãy đổi mật khẩu mặc định ngay sau khi đăng nhập lần đầu!

---

## 🔐 PHÂN QUYỀN HỆ THỐNG

| Chức năng | Admin | Lễ tân |
|---|:---:|:---:|
| Dashboard | ✅ (đầy đủ) | ✅ (rút gọn) |
| Trợ lý AI | ✅ | ✅ |
| Quản lý nhân viên | ✅ | ❌ |
| Hạng phòng (CRUD) | ✅ | 👁️ Xem |
| Quản lý phòng | ✅ | 👁️ Xem |
| Khách hàng (CRUD) | ✅ | ✅ |
| Đặt phòng | ✅ | ✅ (giới hạn) |
| Check-in / Check-out | ✅ | ✅ |
| Hóa đơn | ✅ | ✅ (của mình) |
| Dịch vụ (CRUD) | ✅ | ❌ |
| Báo cáo & Xuất Excel | ✅ | ❌ |


## 🤖 TÍNH NĂNG AI CHATBOT

Hệ thống tích hợp **AI Assistant** có khả năng:

| Loại câu hỏi | Ví dụ |
|---|---|
| 💰 Tra giá phòng | *"Phòng 203 giá bao nhiêu?"* |
| 📊 Doanh thu | *"Tổng doanh thu tháng 3?"* |
| 🔍 Tra booking | *"Tra HMS-20260308-000001"* |
| 🏆 Top khách hàng | *"Top 5 khách chi nhiều nhất?"* |
| 🛏️ Phòng trống | *"Phòng trống hôm nay?"* |
| 🧮 Tính tiền VN | *"500k + 1tr2 - 200k = ?"* |
| 📋 Thống kê booking | *"Thống kê booking tổng hợp"* |
| 🍽️ Top dịch vụ | *"Top dịch vụ phổ biến nhất?"* |

---

## 🌐 DEMO & DEPLOY

> 🔗 **Link Demo:** [http://103.75.184.108:5000/](http://103.75.184.108:5000/)

---


