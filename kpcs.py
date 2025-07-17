import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# --- LOAD CONFIGURATION ---
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# --- CREATE AUTHENTICATOR OBJECT ---
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# --- RENDER LOGIN WIDGET ---
st.title("Ứng dụng có Đăng nhập")

# `login` is a method that renders the login form.
# It returns the user's name, authentication status, and username.
name, authentication_status, username = authenticator.login('main')

# --- HANDLE LOGIN STATUS ---

if authentication_status is False:
    st.error('Tên người dùng/mật khẩu không chính xác')

elif authentication_status is None:
    st.warning('Vui lòng nhập tên người dùng và mật khẩu của bạn')

elif authentication_status:
    # --- LOGGED IN SUCCESFULLY ---
    st.sidebar.title(f'Xin chào, *{name}*')
    
    # Add a logout button to the sidebar
    authenticator.logout('Đăng xuất', 'sidebar')

    # --- YOUR MAIN APP GOES HERE ---
    st.header('Trang chính của ứng dụng')
    st.write(f'Bạn đã đăng nhập với vai trò **{username}**.')
    st.write('Bây giờ bạn có thể thấy nội dung được bảo vệ.')

    # Ví dụ: Hiển thị dữ liệu hoặc chức năng chỉ dành cho người đã đăng nhập
    if st.button('Hiển thị thông tin bí mật'):
        st.write('Đây là thông tin chỉ người dùng đã đăng nhập mới thấy được. 🤫')
