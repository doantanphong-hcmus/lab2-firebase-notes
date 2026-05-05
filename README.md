# Lab 2: Note App API & Firebase Studio

**Thông tin sinh viên:**
* Họ và tên: Đoàn Tấn Phong
* MSSV: 24120408
* Class: 24CTT3 

## 1. Giới thiệu tổng quan
Dự án ứng dụng ghi chú cá nhân được phát triển nhằm đáp ứng yêu cầu Bài thực hành số 2 - môn Tư Duy Tính Toán. Hệ thống áp dụng kiến trúc phân tách rạch ròi giữa Frontend và Backend, đồng thời tích hợp dịch vụ đám mây Firebase để xử lý xác thực người dùng và lưu trữ dữ liệu.

## 2. Tính năng cốt lõi
* **Xác thực người dùng:** Đăng ký và đăng nhập tài khoản qua Firebase Authentication (sử dụng Identity Toolkit REST API).
* **Quản lý Ghi chú:** Cho phép người dùng thêm mới và truy xuất danh sách ghi chú từ Firestore Database. Dữ liệu được bảo mật và phân tách độc lập theo UID của từng tài khoản.
* **Phân quyền:** Backend xác thực token Firebase (Bearer Token) để đảm bảo người dùng chỉ truy cập được dữ liệu của mình.

## 3. Cấu trúc thư mục
```text
lab2-firebase-notes/
│
├── backend/
│   ├── main.py                       # Chứa API Endpoints và logic xử lý Firebase Admin
│   └── firebase-service-account.json # File cấu hình Private Key của Firebase (Đã được ignore)
│
├── frontend/
│   └── app.py                        # Giao diện người dùng phát triển bằng Streamlit
│
├── requirements.txt                  # Danh sách các thư viện phụ thuộc
├── .gitignore                        # Cấu hình bỏ qua các file nhạy cảm và cache
└── README.md                         # Tài liệu hướng dẫn dự án (File này)
```

## 4. Hướng dẫn cài đặt môi trường

Yêu cầu máy tính đã cài đặt Python (khuyến nghị phiên bản 3.10 trở lên).

**Bước 1: Clone dự án về máy cục bộ**
```bash
git clone https://github.com/doantanphong-hcmus/lab2-firebase-notes.git
cd lab2-firebase-notes
```

**Bước 2: Tạo và kích hoạt môi trường ảo**
* Đối với hệ điều hành Windows (PowerShell):
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\activate
  ```
* Đối với hệ điều hành macOS/Linux:
  
```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

**Bước 3: Cài đặt các thư viện yêu cầu**
```bash
pip install -r requirements.txt
```

**Bước 4: Cấu hình khóa bảo mật Firebase**
1. Tải file Private Key từ Firebase Console (Project Settings -> Service Accounts), đổi tên thành `firebase-service-account.json` và lưu vào thư mục `backend/`.
2. Lấy chuỗi Web API Key từ Firebase Console (Project Settings -> General), mở file `frontend/app.py` và cập nhật vào biến `FIREBASE_WEB_API_KEY`.

## 5. Hướng dẫn khởi chạy hệ thống

**Chạy Backend (FastAPI)**
Mở terminal tại thư mục gốc, đảm bảo đã kích hoạt môi trường ảo và thực thi lệnh:
```bash
python -m uvicorn backend.main:app --reload
```
* Server Backend sẽ hoạt động tại: `[http://127.0.0.1:8000](http://127.0.0.1:8000)`
* Tài liệu API Swagger UI: `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`

**Chạy Frontend (Streamlit)**
Mở một terminal mới tại thư mục gốc, kích hoạt môi trường ảo và thực thi lệnh:
```bash
python -m streamlit run frontend/app.py
```
* Giao diện người dùng sẽ tự động hiển thị trên trình duyệt tại: `http://localhost:8501`

## 6. Video Demo Sản phẩm

👉 **[[LINK VIDEO DEMO YOUTUBE]([https://github.com/doantanphong-hcmus/lab2-firebase-notes.git](https://youtu.be/OvFXHwDP0vI))]**
