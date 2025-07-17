import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title="Ứng dụng có Đăng nhập", layout="wide")

# --- LOAD CONFIGURATION ---
try:
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("Lỗi: Không tìm thấy file 'config.yaml'.")
    st.stop()

# --- CREATE AUTHENTICATOR OBJECT ---
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- RENDER LOGIN WIDGET AND HANDLE STATE ---
# ✨ Cách gọi hàm login mới ✨
authenticator.login()

if st.session_state["authentication_status"]:
    # --- LOGGED IN SUCCESFULLY ---
    # Lấy thông tin từ st.session_state
    name = st.session_state["name"]
    username = st.session_state["username"]

    st.sidebar.title(f'Xin chào, *{name}*')
    # Nút đăng xuất cũng được đặt bên trong authenticator
    authenticator.logout('Đăng xuất', 'sidebar')

    # --- NỘI DUNG CHÍNH CỦA APP ---
    st.header(f'Chào mừng đến với ứng dụng, {name}!')
    st.write(f'Bạn đã đăng nhập với vai trò **{username}**.')
    
    # ... Đặt code ứng dụng chính của bạn ở đây ...

elif st.session_state["authentication_status"] is False:
    st.error('Tên người dùng/mật khẩu không chính xác')

elif st.session_state["authentication_status"] is None:
    st.warning('Vui lòng nhập tên người dùng và mật khẩu của bạn')
