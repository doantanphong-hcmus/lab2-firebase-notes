import streamlit as st
import requests

# Cấu hình hằng số (Nhớ thay thế FIREBASE_WEB_API_KEY bằng key ông vừa copy)
BACKEND_URL = "http://127.0.0.1:8000"
FIREBASE_WEB_API_KEY = "AIzaSyAvMuGyFfZMA1zH_c_f1xHOWLOrD9n1GmE" 

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
        # Lấy được ID Token (rất quan trọng để gửi kèm Header xuống Backend)
        return response.json().get("idToken")
    else:
        st.error(f"Đăng nhập thất bại: {response.json().get('error', {}).get('message')}")
        return None

# Quản lý trạng thái Session (kiểm tra xem đã đăng nhập chưa)
if 'token' not in st.session_state:
    st.session_state.token = None

# GIAO DIỆN CHÍNH
st.title("📝 Ứng dụng Ghi chú Cá nhân")

# 1. KHI CHƯA ĐĂNG NHẬP (MÀN HÌNH LOGIN)
if not st.session_state.token:
    st.subheader("Đăng nhập")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        submit_btn = st.form_submit_button("Vào trong")
        
        if submit_btn:
            token = login_with_firebase(email, password)
            if token:
                st.session_state.token = token
                st.success("Đăng nhập thành công!")
                st.rerun() # Refresh lại trang
    st.info("💡 Ông nhớ vào Firebase Console -> Authentication -> Users để tạo trước một tài khoản Email/Pass để test nhé.")

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
    note_content = st.text_area("Hôm nay có gì mới?")
    if st.button("Lưu ghi chú"):
        if note_content.strip():
            # Bắn request POST xuống Backend FastAPI
            res = requests.post(f"{BACKEND_URL}/notes", json={"content": note_content}, headers=headers)
            if res.status_code == 200:
                st.success("Đã lưu!")
            else:
                st.error("Lỗi khi lưu ghi chú.")
        else:
            st.warning("Vui lòng nhập nội dung.")

    st.divider()

    # Hiển thị danh sách ghi chú
    st.subheader("Danh sách của tôi")
    # Bắn request GET xuống Backend FastAPI để lấy data
    res = requests.get(f"{BACKEND_URL}/notes", headers=headers)
    
    if res.status_code == 200:
        notes = res.json().get("notes", [])
        if not notes:
            st.info("Chưa có ghi chú nào.")
        for note in notes:
            with st.container(border=True):
                st.markdown(f"**Nội dung:** {note['content']}")
    else:
        st.error("Phiên đăng nhập hết hạn hoặc lỗi Server. Vui lòng đăng nhập lại.")