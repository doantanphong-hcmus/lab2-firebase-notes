import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import credentials, auth

# 1. Khởi tạo FastAPI App
app = FastAPI(title="Note App API", version="1.0.0")

# 2. Cấu hình CORS Middleware
# Cho phép Frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong thực tế nên sửa thành domain cụ thể của frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Khởi tạo Firebase Admin SDK
current_dir = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(current_dir, "firebase-service-account.json")
cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred)

# 4. Endpoints Cơ bản
@app.get("/")
def read_root():
    return {"message": "Welcome to Note App API"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "running"}

# 5. Endpoint Xác thực (Xác minh Firebase Token)
security = HTTPBearer()

def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Hàm này đóng vai trò như một Dependency. 
    Nó trích xuất Token JWT từ header Authorization: Bearer <token>,
    sau đó dùng Firebase Admin SDK để verify token đó.
    """
    token = credentials.credentials
    try:
        # Giải mã và xác thực token với Firebase
        decoded_token = auth.verify_id_token(token)
        return decoded_token # Trả về payload chứa thông tin user (uid, email...)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/auth/me")
def get_current_user(user_data: dict = Depends(verify_firebase_token)):
    """
    Endpoint test xác thực. Chỉ trả về thông tin khi token hợp lệ.
    """
    return {
        "message": "Authentication successful",
        "uid": user_data.get("uid"),
        "email": user_data.get("email")
    }