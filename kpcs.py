import streamlit as st
import pandas as pd
import os

# --- CẤU HÌNH TÊN CỘT ---
# Đây là bước quan trọng nhất, định nghĩa cấu trúc của file tổng và file upload
# Lưu ý: Tên cột phải chính xác tuyệt đối, bao gồm cả dấu cách, ký tự đặc biệt.

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

# Tên file Excel tổng
MASTER_FILE = "DuLieuTongHop.xlsx"


# --- GIAO DIỆN ỨNG DỤNG ---
st.set_page_config(page_title="Công Cụ Nhập Liệu Kiểm Toán", layout="wide")
st.title("🚀 Ứng Dụng Cập Nhật Dữ Liệu Kiểm Toán")
st.write(f"**Lưu ý:** Vui lòng upload file Excel theo đúng mẫu. Dữ liệu sẽ được thêm vào file tổng: `{MASTER_FILE}`")

# 1. Khu vực upload file
uploaded_file = st.file_uploader(
    "Chọn file Excel bạn muốn upload:",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:
    st.info(f"Đã tải lên file: `{uploaded_file.name}`. Nhấn nút bên dưới để xử lý.")
    
    # Nút bấm để thực hiện
    if st.button("✅ Bắt đầu Cập nhật vào File Tổng"):
        try:
            # 2. Đọc dữ liệu từ file upload
            uploaded_df = pd.read_excel(uploaded_file, engine='openpyxl')
            st.write("--- **Xem trước dữ liệu từ file bạn vừa upload:** ---")
            st.dataframe(uploaded_df.head())

            # 3. KIỂM TRA CẤU TRÚC CỘT CỦA FILE UPLOAD
            # Kiểm tra xem tất cả các cột cần thiết có trong file upload không
            missing_cols = set(UPLOAD_COLUMNS) - set(uploaded_df.columns)
            if missing_cols:
                st.error(f"Lỗi: File upload bị thiếu các cột sau đây: {list(missing_cols)}. Vui lòng kiểm tra lại file mẫu.")
            else:
                # 4. Đọc file tổng (hoặc tạo mới nếu chưa có)
                if os.path.exists(MASTER_FILE):
                    master_df = pd.read_excel(MASTER_FILE, engine='openpyxl')
                else:
                    st.warning(f"Không tìm thấy file `{MASTER_FILE}`. Sẽ tạo một file mới.")
                    master_df = pd.DataFrame(columns=MASTER_COLUMNS)

                # 5. XỬ LÝ CỘT STT (SỐ THỨ TỰ)
                if not master_df.empty and 'STT' in master_df.columns:
                    last_stt = master_df['STT'].max()
                    # Kiểm tra nếu last_stt là NaN (trường hợp cột STT toàn rỗng)
                    if pd.isna(last_stt):
                        last_stt = 0
                else:
                    last_stt = 0
                
                # Tạo STT mới cho dữ liệu upload, bắt đầu từ số lớn nhất + 1
                uploaded_df['STT'] = range(int(last_stt) + 1, int(last_stt) + 1 + len(uploaded_df))

                # 6. ÁNH XẠ CỘT VÀ KẾT HỢP DỮ LIỆU
                # Chỉ lấy các cột theo đúng mẫu từ file upload để đảm bảo thứ tự
                data_to_add = uploaded_df[UPLOAD_COLUMNS]
                
                # Dùng concat để nối 2 DataFrame, pandas sẽ tự động căn chỉnh cột theo tên
                # Các cột trong file tổng mà file upload không có sẽ tự điền giá trị rỗng (NaN)
                combined_df = pd.concat([master_df, data_to_add], ignore_index=True)
                
                # 7. LƯU LẠI FILE TỔNG
                combined_df.to_excel(MASTER_FILE, index=False, engine='openpyxl')
                
                st.success(f"🎉 Cập nhật thành công! Đã thêm {len(uploaded_df)} dòng mới vào file `{MASTER_FILE}`.")
                st.write("--- **Xem trước 5 dòng cuối của file tổng sau khi cập nhật:** ---")
                st.dataframe(combined_df.tail())

        except Exception as e:
            st.error(f"Đã có lỗi xảy ra trong quá trình xử lý: {e}")