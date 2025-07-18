import streamlit as st
import pandas as pd
import io

# Thiết lập tiêu đề trang và layout
st.set_page_config(layout="wide", page_title="Công cụ Kết hợp Excel")

st.title("⚙️ Công cụ Kết hợp và Tải về File Excel")
st.write("Thực hiện theo 3 bước để kết hợp dữ liệu từ nhiều file Excel.")

# Khởi tạo session_state để lưu trữ các DataFrame
# Việc này giúp dữ liệu không bị mất sau mỗi lần người dùng tương tác
if 'master_df' not in st.session_state:
    st.session_state.master_df = None
if 'combined_df' not in st.session_state:
    st.session_state.combined_df = None

# --- BƯỚC 1: Tải lên File Dữ liệu Tổng (Master File) ---
st.header("Bước 1: Tải lên File Dữ liệu Tổng")
master_file = st.file_uploader(
    "Chọn file Excel gốc của bạn",
    type=['xlsx', 'xls'],
    key="master_uploader"
)

# Nếu người dùng đã tải lên file tổng
if master_file is not None:
    # Đọc file và lưu vào "bộ nhớ tạm" (session_state)
    st.session_state.master_df = pd.read_excel(master_file)
    st.success(f"✅ Đã tải lên và lưu trữ tạm thời file: **{master_file.name}**")
    st.write("Xem trước 5 dòng đầu của file tổng:")
    st.dataframe(st.session_state.master_df.head())


# --- BƯỚC 2: Tải lên File Dữ liệu cần Thêm ---
# Chỉ hiển thị bước này sau khi đã có file tổng
if st.session_state.master_df is not None:
    st.header("Bước 2: Tải lên File Dữ liệu cần Thêm")
    new_data_file = st.file_uploader(
        "Chọn file Excel chứa các dòng dữ liệu mới",
        type=['xlsx', 'xls'],
        key="new_data_uploader"
    )

    # --- BƯỚC 3: Kết hợp và Tải về ---
    # Chỉ hiển thị bước này sau khi đã có file dữ liệu mới
    if new_data_file is not None:
        st.header("Bước 3: Kết hợp và Tải về")
        
        # Tạo nút để thực hiện hành động kết hợp
        if st.button("Kết hợp dữ liệu"):
            # Đọc file dữ liệu mới
            new_data_df = pd.read_excel(new_data_file)
            st.write("Xem trước 5 dòng đầu của file dữ liệu mới:")
            st.dataframe(new_data_df.head())

            # Thực hiện kết hợp (nối) hai DataFrame lại với nhau
            combined_df = pd.concat([st.session_state.master_df, new_data_df], ignore_index=True)
            
            # Lưu kết quả vào session_state để có thể tải về
            st.session_state.combined_df = combined_df
            
            st.success("🎉 Đã kết hợp dữ liệu thành công!")
            st.write("Xem trước 5 dòng cuối của file tổng hợp:")
            st.dataframe(st.session_state.combined_df.tail())

# --- NÚT TẢI VỀ ---
# Chỉ hiển thị nút tải về sau khi đã nhấn nút "Kết hợp dữ liệu"
if st.session_state.combined_df is not None:
    st.markdown("---") # Thêm một đường kẻ ngang
    st.subheader("Tải về File Tổng hợp")

    # Chuyển đổi DataFrame thành một file Excel trong bộ nhớ
    # Đây là bước quan trọng để chuẩn bị dữ liệu cho nút download
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        st.session_state.combined_df.to_excel(writer, index=False, sheet_name='DuLieuTongHop')
    excel_data = output.getvalue()

    # Tạo nút download
    st.download_button(
        label="📥 Tải về File Excel Tổng hợp",
        data=excel_data,
        file_name='DuLieuTongHop.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
