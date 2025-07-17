import streamlit as st
import pandas as pd
import os

# --- CẤU HÌNH ---
MASTER_FILE = "DuLieuTongHop.xlsx"

# THÊM CỘT 'Người tạo' VÀO DANH SÁCH CỘT CỦA BẠN
# Ví dụ:
MASTER_COLUMNS = [
    'STT', 'Đối tượng được KT', 'Số văn bản', 'Người tạo', # <-- THÊM CỘT MỚI
    # ... VÀ TẤT CẢ CÁC CỘT KHÁC
]
UPLOAD_COLUMNS = [
    'STT', 'Đối tượng được KT', 'Số văn bản',
     # ... VÀ CÁC CỘT KHÁC CỦA FILE UPLOAD
]

# --- HỆ THỐNG XÁC THỰC NGƯỜI DÙNG ĐƠN GIẢN ---
st.set_page_config(page_title="Công Cụ Dữ Liệu Kiểm Toán", layout="wide")

# Kiểm tra nếu người dùng đã "đăng nhập" chưa (lưu trong session state)
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Giao diện đăng nhập
if st.session_state.user_id is None:
    st.title("🔐 Đăng nhập")
    user_id_input = st.text_input("Nhập Mã nhân viên hoặc Username của bạn:")
    if st.button("Đăng nhập"):
        if user_id_input:
            st.session_state.user_id = user_id_input
            st.rerun() # Chạy lại app sau khi đăng nhập thành công
        else:
            st.error("Vui lòng nhập Mã nhân viên.")
    st.stop() # Dừng app lại ở màn hình đăng nhập

# --- GIAO DIỆN CHÍNH SAU KHI ĐĂNG NHẬP ---
st.sidebar.title(f"Xin chào, {st.session_state.user_id}!")
if st.sidebar.button("Đăng xuất"):
    st.session_state.user_id = None
    st.rerun()

st.sidebar.divider()
st.sidebar.title("⚙️ Chức năng")
app_mode = st.sidebar.radio(
    "Chọn chế độ bạn muốn sử dụng:",
    ["Cập nhật từ File", "Chỉnh sửa Trực tiếp"]
)

st.title("Công Cụ Quản Lý Dữ Liệu Kiểm Toán")

# ==============================================================================
# CHẾ ĐỘ 1: CẬP NHẬT TỪ FILE (CÓ THÊM LOGIC GÁN NGƯỜI TẠO)
# ==============================================================================
if app_mode == "Cập nhật từ File":
    st.header("🚀 Chế độ 1: Cập nhật từ File Excel")
    uploaded_file = st.file_uploader("Chọn file Excel:", type=["xlsx", "xls"], key="uploader")

    if uploaded_file and st.button("✅ Bắt đầu Cập nhật", key="update_button"):
        try:
            uploaded_df = pd.read_excel(uploaded_file, engine='openpyxl')
            uploaded_df.columns = uploaded_df.columns.str.strip()
            
            # TỰ ĐỘNG THÊM CỘT 'Người tạo' VỚI MÃ CỦA NGƯỜI DÙNG ĐANG ĐĂNG NHẬP
            uploaded_df['Người tạo'] = st.session_state.user_id
            
            # Logic xử lý và ghép file như cũ...
            # ...
            st.success(f"Cập nhật thành công! Các dòng mới đã được gán cho bạn ({st.session_state.user_id}).")

        except Exception as e:
            st.error(f"Lỗi khi xử lý file: {e}")

# ==============================================================================
# CHẾ ĐỘ 2: CHỈNH SỬA TRỰC TIẾP (CÓ PHÂN QUYỀN)
# ==============================================================================
elif app_mode == "Chỉnh sửa Trực tiếp":
    st.header("✏️ Chế độ 2: Chỉnh sửa Trực tiếp trên Bảng")

    try:
        master_df = pd.read_excel(MASTER_FILE, engine='openpyxl')
        # Đảm bảo cột 'Người tạo' tồn tại
        if 'Người tạo' not in master_df.columns:
            st.error(f"Lỗi: File {MASTER_FILE} thiếu cột 'Người tạo'. Vui lòng thêm cột này.")
            st.stop()
    except FileNotFoundError:
        st.error(f"Không tìm thấy file {MASTER_FILE}. Vui lòng upload file để tạo trước.")
        st.stop()
    
    # --- LOGIC PHÂN QUYỀN ---
    # Tách DataFrame thành 2 phần: được sửa và chỉ xem
    user_id = st.session_state.user_id
    editable_df = master_df[master_df['Người tạo'] == user_id]
    readonly_df = master_df[master_df['Người tạo'] != user_id]

    st.subheader("✍️ Các dòng bạn được phép sửa")
    if not editable_df.empty:
        # Hiển thị bảng cho phép sửa
        edited_df = st.data_editor(
            editable_df,
            num_rows="dynamic",
            key="data_editor_editable",
            use_container_width=True
        )
    else:
        st.info("Bạn không có dòng nào để sửa.")
        edited_df = editable_df # Gán lại để không bị lỗi khi concat

    st.divider()

    st.subheader("🔒 Các dòng chỉ xem (do người khác tạo)")
    if not readonly_df.empty:
        # Hiển thị bảng chỉ để xem, không thể sửa
        st.dataframe(readonly_df, use_container_width=True)
    else:
        st.info("Không có dòng nào do người khác tạo.")
        
    st.divider()

    if st.button("💾 Lưu các thay đổi", key="save_button"):
        try:
            # Ghép lại 2 phần: phần đã sửa và phần chỉ xem (bản gốc)
            final_df = pd.concat([edited_df, readonly_df], ignore_index=True)
            
            # Sắp xếp lại nếu cần (ví dụ theo STT)
            if 'STT' in final_df.columns:
                final_df = final_df.sort_values(by='STT').reset_index(drop=True)
                
            final_df.to_excel(MASTER_FILE, index=False, engine='openpyxl')
            st.success(f"🎉 Đã lưu thành công các thay đổi!")
            st.balloons()
        except Exception as e:
            st.error(f"Đã có lỗi xảy ra khi lưu file: {e}")
