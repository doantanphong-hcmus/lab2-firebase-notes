import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load các biến môi trường từ file .env lên hệ thống
load_dotenv()

# Cấu hình hằng số 
BACKEND_URL = "http://127.0.0.1:8000"
# Lấy Key từ file .env, nếu không có thì trả về chuỗi rỗng
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY", "") 

st.set_page_config(page_title="Note App - Lab 2", page_icon="📝")

def login_with_firebase(email, password):
    """Sử dụng Firebase Identity Toolkit REST API để đăng nhập lấy Token"""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("idToken")
    else:
        st.error(f"Đăng nhập thất bại: {response.json().get('error', {}).get('message')}")
        return None

def register_with_firebase(email, password):
    """Sử dụng Firebase Identity Toolkit REST API để đăng ký tài khoản mới"""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return True, "Đăng ký thành công! Xin mời ông chuyển sang tab Đăng nhập."
    else:
        error_msg = response.json().get('error', {}).get('message')
        return False, f"Đăng ký thất bại: {error_msg}"

# Quản lý trạng thái Session
if 'token' not in st.session_state:
    st.session_state.token = None

# GIAO DIỆN CHÍNH
st.title("📝 Ứng dụng Ghi chú Cá nhân")

# 1. KHI CHƯA ĐĂNG NHẬP (MÀN HÌNH LOGIN / REGISTER)
if not st.session_state.token:
    # Chia giao diện thành 2 Tab 
    tab_login, tab_register = st.tabs(["🔑 Đăng nhập", "📝 Đăng ký mới"])
    
    with tab_login:
        st.subheader("Đăng nhập vào hệ thống")
        with st.form("login_form"):
            email_login = st.text_input("Email")
            password_login = st.text_input("Mật khẩu", type="password")
            submit_login = st.form_submit_button("Vào trong")
            
            if submit_login:
                token = login_with_firebase(email_login, password_login)
                if token:
                    st.session_state.token = token
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                    
    with tab_register:
        st.subheader("Tạo tài khoản mới")
        with st.form("register_form"):
            email_reg = st.text_input("Nhập Email mới")
            password_reg = st.text_input("Nhập Mật khẩu (tối thiểu 6 ký tự)", type="password")
            submit_reg = st.form_submit_button("Đăng ký")
            
            if submit_reg:
                if len(password_reg) < 6:
                    st.warning("Mật khẩu phải có ít nhất 6 ký tự ông ơi!")
                else:
                    success, msg = register_with_firebase(email_reg, password_reg)
                    if success:
                        st.success(msg)
                        st.balloons() 
                    else:
                        st.error(msg)

# 2. KHI ĐÃ ĐĂNG NHẬP (TÍNH NĂNG GHI CHÚ)
else:
    # Header gọi API luôn phải đính kèm Token này
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # Nút Đăng xuất
    if st.button("Đăng xuất"):
        st.session_state.token = None
        st.rerun()
        
    st.divider()

    # Form Thêm ghi chú mới
    st.subheader("Thêm ghi chú")
    
    with st.form("add_note_form", clear_on_submit=True):
        note_content = st.text_area("Hôm nay có gì mới?")
        submit_note = st.form_submit_button("Lưu ghi chú")
        
        if submit_note:
            if note_content.strip():
                try:
                    res = requests.post(f"{BACKEND_URL}/notes", json={"content": note_content}, headers=headers)
                    if res.status_code == 200:
                        st.success("Đã lưu!")
                        st.rerun() 
                    else:
                        st.error("Lỗi khi lưu ghi chú.")
                except requests.exceptions.ConnectionError:
                    st.error("🚨 Không thể kết nối tới Backend. Xin hãy kiểm tra lại lệnh chạy Uvicorn!")
            else:
                st.warning("Vui lòng nhập nội dung.")
                
    # Hiển thị danh sách ghi chú
    st.subheader("Danh sách của tôi")
    try:
        res = requests.get(f"{BACKEND_URL}/notes", headers=headers)
        if res.status_code == 200:
            notes = res.json().get("notes", [])
            if not notes:
                st.info("Chưa có ghi chú nào.")
            for note in notes:
                with st.container(border=True):
                    time_str = note.get('created_at', '')[:16] 
                    st.caption(f"🕒 {time_str}")
                    st.markdown(f"**Nội dung:** {note['content']}")
        else:
            st.error("Phiên đăng nhập hết hạn hoặc lỗi Server. Vui lòng đăng nhập lại.")
    except requests.exceptions.ConnectionError:
        st.error("🚨 Không thể lấy danh sách. Backend đang không phản hồi!")