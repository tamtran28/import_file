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
    st.error("Lỗi: Không tìm thấy file 'config.yaml'. Vui lòng tạo file cấu hình.")
    st.stop()


# --- CREATE AUTHENTICATOR OBJECT ---
# ✨ Đã xóa tham số 'preauthorized' ở đây
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- RENDER LOGIN WIDGET ---
st.title("Ứng dụng có Đăng nhập")

name, authentication_status, username = authenticator.login('main')

# --- HANDLE LOGIN STATUS ---
if authentication_status is False:
    st.error('Tên người dùng/mật khẩu không chính xác')

elif authentication_status is None:
    st.warning('Vui lòng nhập tên người dùng và mật khẩu của bạn')

elif authentication_status:
    # --- LOGGED IN SUCCESFULLY ---
    st.sidebar.title(f'Xin chào, *{name}*')
    authenticator.logout('Đăng xuất', 'sidebar')

    # --- YOUR MAIN APP GOES HERE ---
    st.header('Trang chính của ứng dụng')
    st.write(f'Bạn đã đăng nhập với vai trò **{username}**.')

    if st.button('Hiển thị thông tin bí mật'):
        st.write('Đây là thông tin chỉ người dùng đã đăng nhập mới thấy được. 🤫')
