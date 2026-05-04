import os
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import credentials, auth, firestore
from pydantic import BaseModel

app = FastAPI(title="Note App API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- KHỞI TẠO FIREBASE & FIRESTORE ---
current_dir = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(current_dir, "firebase-service-account.json")

# Kiểm tra xem app đã khởi tạo chưa để tránh lỗi chạy lại của Uvicorn
if not firebase_admin._apps:
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

# Khởi tạo client kết nối với Firestore DB
db = firestore.client()

# --- DEPENDENCY XÁC THỰC ---
security = HTTPBearer()

def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
        )

# --- SCHEMA CHO DỮ LIỆU ĐẦU VÀO ---
class NoteRequest(BaseModel):
    content: str

# --- ENDPOINTS GHI CHÚ ---

# 1. API Lưu ghi chú mới (POST)
@app.post("/notes")
def create_note(note: NoteRequest, user_data: dict = Depends(verify_firebase_token)):
    # Lấy UID của user đang gọi API để lưu vào DB, đảm bảo ai xem ghi chú người nấy
    uid = user_data.get("uid")

    # Tạo document mới trong collection 'notes'
    note_data = {
        "uid": uid,
        "content": note.content,
        "created_at": datetime.now()
    }

    # Thêm vào Firestore
    doc_ref = db.collection('notes').document()
    doc_ref.set(note_data)

    return {"message": "Đã lưu ghi chú thành công", "note_id": doc_ref.id}

# 2. API Lấy danh sách ghi chú (GET)
@app.get("/notes")
def get_notes(user_data: dict = Depends(verify_firebase_token)):
    uid = user_data.get("uid")

    # Truy vấn DB: Chỉ lấy những ghi chú có uid bằng với uid của người đang đăng nhập
    notes_ref = db.collection('notes').where('uid', '==', uid).order_by('created_at', direction=firestore.Query.DESCENDING).stream()

    notes_list = []
    for note in notes_ref:
        doc_data = note.to_dict()
        notes_list.append({
            "id": note.id,
            "content": doc_data.get("content"),
            "created_at": doc_data.get("created_at")
        })

    return {"notes": notes_list}