import streamlit as st
import pandas as pd
import os

# --- CẤU HÌNH TÊN CỘT (Giữ nguyên không thay đổi) ---
MASTER_COLUMNS = [
    'STT', 'Đối tượng được KT', 'Số văn bản', 'Ngày, tháng, năm ban hành (mm/dd/yyyy)', 
    'Tên Đoàn kiểm toán', 'Số hiệu rủi ro', 'Số hiệu kiểm soát', 
    'Nghiệp vụ (R0) (nhập theo TVRR/Khung CTKT)', 'Quy trình/hoạt động con (R1)', 
    'Tên phát hiện (R2)', 'Chi tiết phát hiện (R3)', 'Dẫn chiếu', 
    'Mô tả chi tiết phát hiện', 'CIF Khách hàng/bút toán', 'Tên khách hàng', 
    'Loại KH (Nhập CN hoặc DN hoặc CN DN)', 'Số phát hiện/số mẫu chọn', 
    'Dư nợ sai phạm (trđ)', 'Số tiền tổn thất (trđ)', 'Số tiền cẩn thu hồi (trđ)', 
    'Trách nhiệm trực tiếp (Nhập Mã CBNV - Họ tên - Chức vụ - Đơn vị Phòng/Ban)', 
    'Trách nhiệm quản lý (Nhập Mã CBNV - Họ tên - Chức vụ - Đơn vị Phòng/Ban)', 
    'Xếp hạng rủi ro (Nhập theo định nghĩa ở Sheet DANHMUC)', 
    'Xếp hạng kiểm soát (Nhập theo định nghĩa ở Sheet DANHMUC)', 'Nguyên nhân', 
    'Ảnh hưởng', 'Kiến nghị', 'Loại/nhóm nguyên nhân (Nhập theo định nghĩa ở Sheet DANHMUC)', 
    'Loại/nhóm ảnh hưởng (Nhập theo định nghĩa ở Sheet DANHMUC)', 
    'Loại/nhóm kiến nghị (Nhập theo định nghĩa ở Sheet DANHMUC)', 
    'Chủ thể kiến nghị (Nhập CBKT hoặc Đoàn KT hoặc BKS)', 'Kế hoạch thực hiện', 
    'Trách nhiệm thực hiện', 
    'Đơn vị thực hiện KPCS (Nhập theo cột D của Sheet DTTHKPCS, mỗi dòng kiến nghị chỉ nhập 1 Đơn vị thực hiện KPCS)', 
    'ĐVKD, AMC, Hội sở (Nhập ĐVKD hoặc Hội sở hoặc AMC)', 'Người phê duyệt', 
    'Ý kiến của đơn vị', 'Mức độ ưu tiên hành động (Nhập theo định nghĩa ở Sheet DANHMUC)', 
    'Thời hạn hoàn thành (mm/dd/yyyy)', 'Đã khắc phục (Nếu đã khắc phục trong thời gian kiểm toán thì đánh dấu X)', 
    'Ngày đã KPCS (Ngày đã KPCS trong thời gian kiểm toán, mm/dd/yyyy)', 'CBKT (Mã CBKT-Họ tên)', 
    'Phòng CLVH', 'Thời hạn KPCS được gia hạn (mm/dd/yyyy)', 'TÌNH HÌNH KPCS', 
    'NGUYÊN NHÂN QUÁ HẠN', 'NGÀY HOÀN TẤT KPCS (mm/dd/yyyy)', 
    'TRÌNH TRANG KPCS (Đã KP, Đang KP; Chưa KP)', 'NGÀY CHUYỂN THEO DÕI RIÊNG (mm/dd/yyyy)', 
    'PHÂN CÔNG CÁN BỘ', 'GIÁM SÁT KPCS', 'PHÒNG GIÁM SÁT KPCS', 'NGƯỜI PHÊ DUYỆT', 
    'NGÀY PHÂN CÔNG', 'NGÀY CẬP NHẬT KPCS (tự động)', 'NGÀY PHÊ DUYỆT KPCS (tự động)', 
    'Đơn vị thực hiện KPCS đầu quý', 'Đơn vị thực hiện KPCS trong quý', 'Đoàn KT/GSTX', 
    'Ngày, tháng, năm ban hành (mm/dd/yyyy).1', 'Ngày phê duyệt gia hạn KPCS (mm/dd/yyyy)', 
    'SUM (THEO Khối, KV, ĐVKD, Hội sở, Ban Dự Án QLTS)', 'GHI CHÚ', 'Khối, Khu vực, AMC', 
    'Danh sach phan cong'
]

UPLOAD_COLUMNS = [
    'STT', 'Đối tượng được KT', 'Số văn bản', 'Ngày, tháng, năm ban hành (mm/dd/yyyy)', 
    'Tên Đoàn kiểm toán', 'Số hiệu rủi ro', 'Số hiệu kiểm soát', 
    'Nghiệp vụ (R0) (nhập theo TVRR/Khung CTKT)', 'Quy trình/hoạt động con (R1)', 
    'Tên phát hiện (R2)', 'Chi tiết phát hiện (R3)', 'Dẫn chiếu', 
    'Mô tả chi tiết phát hiện', 'CIF Khách hàng/bút toán', 'Tên khách hàng', 
    'Loại KH (Nhập CN hoặc DN hoặc CN DN)', 'Số phát hiện/số mẫu chọn', 
    'Dư nợ sai phạm (trđ)', 'Số tiền tổn thất (trđ)', 'Số tiền cẩn thu hồi (trđ)', 
    'Trách nhiệm trực tiếp (Nhập Mã CBNV - Họ tên - Chức vụ - Đơn vị Phòng/Ban)', 
    'Trách nhiệm quản lý (Nhập Mã CBNV - Họ tên - Chức vụ - Đơn vị Phòng/Ban)', 
    'Xếp hạng rủi ro (Nhập theo định nghĩa ở Sheet DANHMUC)', 
    'Xếp hạng kiểm soát (Nhập theo định nghĩa ở Sheet DANHMUC)', 'Nguyên nhân', 
    'Ảnh hưởng', 'Kiến nghị', 'Loại/nhóm nguyên nhân (Nhập theo định nghĩa ở Sheet DANHMUC)',
    'Loại/nhóm ảnh hưởng (Nhập theo định nghĩa ở Sheet DANHMUC)', 
    'Loại/nhóm kiến nghị (Nhập theo định nghĩa ở Sheet DANHMUC)', 
    'Chủ thể kiến nghị (Nhập CBKT hoặc Đoàn KT hoặc BKS)', 'Kế hoạch thực hiện', 
    'Trách nhiệm thực hiện', 
    'Đơn vị thực hiện KPCS (Nhập theo cột D của Sheet DTTHKPCS, mỗi dòng kiến nghị chỉ nhập 1 Đơn vị thực hiện KPCS)', 
    'ĐVKD, AMC, Hội sở (Nhập ĐVKD hoặc Hội sở hoặc AMC)', 'Người phê duyệt', 
    'Ý kiến của đơn vị', 'Mức độ ưu tiên hành động (Nhập theo định nghĩa ở Sheet DANHMUC)', 
    'Thời hạn hoàn thành (mm/dd/yyyy)', 
    'Đã khắc phục (Nếu đã khắc phục trong thời gian kiểm toán thì đánh dấu X)', 
    'Ngày đã KPCS (Ngày đã KPCS trong thời gian kiểm toán, mm/dd/yyyy)', 
    'CBKT (Mã CBKT-Họ tên)', 'Phòng CLVH', 'Thời hạn KPCS được gia hạn (mm/dd/yyyy)', 
    'TÌNH HÌNH KPCS', 'NGUYÊN NHÂN QUÁ HẠN', 'NGÀY HOÀN TẤT KPCS (mm/dd/yyyy)', 
    'TRÌNH TRANG KPCS (Đã KP, Đang KP; Chưa KP)', 'NGÀY CHUYỂN THEO DÕI RIÊNG (mm/dd/yyyy)', 
    'PHÂN CÔNG CÁN BỘ GIÁM SÁT KPCS', 'PHÒNG GIÁM SÁT KPCS', 'NGƯỜI PHÊ DUYỆT', 
    'NGÀY PHÂN CÔNG', 'NGÀY CẬP NHẬT KPCS (tự động)', 'NGÀY PHÊ DUYỆT KPCS (tự động)', 
    'Đơn vị thực hiện KPCS đầu quý', 'Đơn vị thực hiện KPCS trong quý', 'Đoàn KT/GSTX', 
    'Ngày, tháng, năm ban hành (mm/dd/yyyy).1', 'Ngày phê duyệt gia hạn KPCS (mm/dd/yyyy)', 
    'SUM (THEO Khối, KV, ĐVKD, Hội sở)', 'GHI CHÚ', 'Khối, Khu vực, AMC', 
    'Danh sach phan cong'
]

MASTER_FILE = "DuLieuTongHop.xlsx"


st.set_page_config(page_title="Công Cụ Nhập Liệu Kiểm Toán", layout="wide")
st.title("🚀 Ứng Dụng Cập Nhật Dữ Liệu Kiểm Toán")
st.write(f"**Lưu ý:** Vui lòng upload file Excel theo đúng mẫu. Dữ liệu sẽ được thêm vào file tổng: `{MASTER_FILE}`")

uploaded_file = st.file_uploader(
    "Chọn file Excel bạn muốn upload:",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:
    st.info(f"Đã tải lên file: `{uploaded_file.name}`. Nhấn nút bên dưới để xử lý.")
    
    if st.button("✅ Bắt đầu Cập nhật vào File Tổng"):
        try:
            uploaded_df = pd.read_excel(uploaded_file, engine='openpyxl')
            
            # =================================================================
            # ✨ ĐÂY LÀ THAY ĐỔI QUAN TRỌNG NHẤT: LÀM SẠCH TÊN CỘT ✨
            # Code sẽ tự động xóa các dấu cách thừa ở đầu và cuối mỗi tên cột
            uploaded_df.columns = uploaded_df.columns.str.strip()
            # =================================================================

            st.write("--- **Xem trước dữ liệu từ file bạn vừa upload (sau khi đã làm sạch tên cột):** ---")
            st.dataframe(uploaded_df.head())

            missing_cols = set(UPLOAD_COLUMNS) - set(uploaded_df.columns)
            if missing_cols:
                st.error(f"Lỗi: File upload vẫn bị thiếu hoặc sai tên các cột sau đây. Vui lòng kiểm tra lại file của bạn.")
                st.json(list(missing_cols)) # Hiển thị danh sách cột lỗi rõ ràng hơn
            else:
                if os.path.exists(MASTER_FILE):
                    master_df = pd.read_excel(MASTER_FILE, engine='openpyxl')
                else:
                    st.warning(f"Không tìm thấy file `{MASTER_FILE}`. Sẽ tạo một file mới.")
                    master_df = pd.DataFrame(columns=MASTER_COLUMNS)

                if not master_df.empty and 'STT' in master_df.columns:
                    last_stt = master_df['STT'].max()
                    if pd.isna(last_stt):
                        last_stt = 0
                else:
                    last_stt = 0
                
                uploaded_df['STT'] = range(int(last_stt) + 1, int(last_stt) + 1 + len(uploaded_df))

                data_to_add = uploaded_df[UPLOAD_COLUMNS]
                
                combined_df = pd.concat([master_df, data_to_add], ignore_index=True)
                
                combined_df.to_excel(MASTER_FILE, index=False, engine='openpyxl')
                
                st.success(f"🎉 Cập nhật thành công! Đã thêm {len(uploaded_df)} dòng mới vào file `{MASTER_FILE}`.")
                st.write("--- **Xem trước 5 dòng cuối của file tổng sau khi cập nhật:** ---")
                st.dataframe(combined_df.tail())

        except Exception as e:
            st.error(f"Đã có lỗi xảy ra trong quá trình xử lý: {e}")
