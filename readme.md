
# \<p align="center"\>🏨 Hotel Management System (HMS)\</p\>

\<p align="center"\>\<b\>Hệ Thống Quản Lý Khách Sạn Toàn Diện Tích Hợp AI\</b\>\</p\>

\<p align="center"\>
\<img src="[https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge\&logo=python\&logoColor=white](https://www.google.com/search?q=https://img.shields.io/badge/Python-3.11%2B-3776AB%3Fstyle%3Dfor-the-badge%26logo%3Dpython%26logoColor%3Dwhite)" alt="Python"/\>
\<img src="[https://img.shields.io/badge/Flask-3.1.x-000000?style=for-the-badge\&logo=flask\&logoColor=white](https://www.google.com/search?q=https://img.shields.io/badge/Flask-3.1.x-000000%3Fstyle%3Dfor-the-badge%26logo%3Dflask%26logoColor%3Dwhite)" alt="Flask"/\>
\<img src="[https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge\&logo=mysql\&logoColor=white](https://www.google.com/search?q=https://img.shields.io/badge/MySQL-8.0-4479A1%3Fstyle%3Dfor-the-badge%26logo%3Dmysql%26logoColor%3Dwhite)" alt="MySQL"/\>
\<img src="[https://img.shields.io/badge/TailwindCSS-CDN-06B6D4?style=for-the-badge\&logo=tailwindcss\&logoColor=white](https://www.google.com/search?q=https://img.shields.io/badge/TailwindCSS-CDN-06B6D4%3Fstyle%3Dfor-the-badge%26logo%3Dtailwindcss%26logoColor%3Dwhite)" alt="TailwindCSS"/\>
\<img src="[https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=for-the-badge\&logo=openai\&logoColor=white](https://www.google.com/search?q=https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991%3Fstyle%3Dfor-the-badge%26logo%3Dopenai%26logoColor%3Dwhite)" alt="OpenAI"/\>
\</p\>

**HMS** là hệ thống quản lý khách sạn chuyên nghiệp, tích hợp **AI Chatbot** (OpenAI GPT) hỗ trợ nghiệp vụ. Được xây dựng trên nền tảng **Flask + MySQL** với giao diện Dashboard hiện đại từ **TailwindCSS**, hệ thống đáp ứng đầy đủ quy trình vận hành từ đặt phòng, check-in/out đến báo cáo doanh thu.

-----

## 🌟 Tính Năng Nổi Bật

### 1\. 📊 Dashboard Thông Minh

  * Theo dõi trạng thái phòng thời gian thực (Trống / Đang ở / Bảo trì).
  * Thống kê nhanh danh sách Check-in / Check-out trong ngày.
  * Biểu đồ doanh thu trực quan với **Chart.js**.

### 2\. 🤖 Trợ Lý AI (AI Assistant)

  * **Model:** OpenAI GPT-4o-mini hỗ trợ Tiếng Việt.
  * **Nghiệp vụ:** Tra cứu trực tiếp Database (giá phòng, doanh thu, hóa đơn...).
  * **Thông minh:** Hiểu đơn vị tiền tệ rút gọn (`500k`, `1tr2`) và tính toán biểu thức phức tạp.

### 3\. 🛏️ Quản Lý Lưu Trú

  * **Phòng & Hạng phòng:** Quản lý đa dạng hạng phòng (Suite, Deluxe...), hỗ trợ upload 5 ảnh/phòng và ghi đè giá (`price_override`).
  * **Đặt phòng (Booking):** Mã booking tự động, kiểm tra trùng lịch, quy trình chuẩn hóa từ *Chờ xác nhận* đến *Check-out*.

### 4\. 🧾 Tài Chính & Dịch Vụ

  * **Hóa đơn:** Tự động tính toán bao gồm Thuế VAT 10% và giảm giá.
  * **Dịch vụ:** Tích hợp các dịch vụ đi kèm (Ăn uống, Spa, Giặt ủi) trực tiếp vào hóa đơn phòng.
  * **Báo cáo:** Xuất dữ liệu doanh thu chi tiết ra file `.xlsx` (Excel).

-----

## 🏗️ Kiến Trúc Dự Án

```text
python_khachsan/
├── app/
│   ├── blueprints/          # Điều hướng & Logic (12 modules: AI, Auth, Booking...)
│   ├── models/              # Cấu trúc Database (SQLAlchemy Models)
│   ├── services/            # Tầng xử lý nghiệp vụ & AI Service
│   ├── templates/           # Giao diện Jinja2 (TailwindCSS)
│   ├── static/              # Assets (CSS, JS, Images)
│   └── utils/               # Tiện ích bổ trợ (Validators, Formatters)
├── scripts/                 # Script khởi tạo dữ liệu (Seed)
├── .env.example             # Cấu hình biến môi trường mẫu
├── hotel_db.sql             # Database dump
├── run.py                   # Entry point
└── requirements.txt         # Danh sách thư viện
```

-----

## 🚀 Hướng Dẫn Cài Đặt

### 1\. Chuẩn bị môi trường

```bash
# Clone dự án
git clone <repository-url>
cd python_khachsan

# Tạo và kích hoạt môi trường ảo
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Cài đặt thư viện
pip install -r requirements.txt
```

### 2\. Cấu hình Database & Environment

1.  Tạo Database `hotel_db` trong MySQL.
2.  Import dữ liệu: `mysql -u root -p hotel_db < hotel_db.sql`.
3.  Copy `.env.example` thành `.env` và điền các thông số:
      * `MYSQL_PASSWORD`, `SECRET_KEY`.
      * `OPENAI_API_KEY` (nếu dùng AI).

### 3\. Khởi chạy

```bash
python run.py
```

Truy cập: **http://localhost:5000**

-----

## 🔐 Phân Quyền & Tài Khoản

| Vai trò | Username | Password | Quyền hạn |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` | Toàn quyền hệ thống, xem báo cáo, quản lý nhân viên. |
| **Lễ tân** | `letan1` | `letan123` | Thực hiện nghiệp vụ đặt phòng, check-in/out, khách hàng. |

-----

## 🤖 Khả Năng Của AI Assistant

Bạn có thể hỏi Chatbot các câu như:

  * *"Phòng 203 giá bao nhiêu?"*
  * *"Tổng doanh thu tháng này là bao nhiêu?"*
  * *"Liệt kê các phòng còn trống trong hôm nay."*
  * *"Tính giúp tôi: 500k + 1tr2 - 200k."*

-----

> [\!IMPORTANT]
> **Lưu ý:** Hãy đổi mật khẩu mặc định ngay sau khi đăng nhập lần đầu để đảm bảo an toàn hệ thống.

🔗 **Link Demo:** [http://103.75.184.108:5000/](http://103.75.184.108:5000/)
