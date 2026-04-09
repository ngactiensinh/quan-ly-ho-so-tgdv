import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Cấu hình trang
st.set_page_config(page_title="Hồ sơ CBCC - TGDV", page_icon="🗂️", layout="wide")

# ==========================================
# CẤU HÌNH SUPABASE (Dùng chung két sắt E-Cabinet)
# ==========================================
SUPABASE_URL = "https://qqzsdxhqrdfvxnlurnyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFxenNkeGhxcmRmdnhubHVybnliIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2MjY0NjAsImV4cCI6MjA5MTIwMjQ2MH0.H62F5zYEZ5l47fS4IdAE2JdRdI7inXQqWG0nvXhn2P8"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    pass

# CSS làm đẹp giao diện Thẻ hồ sơ
st.markdown("""
<style>
    .profile-card { background-color: #ffffff; padding: 25px; border-radius: 12px; border-left: 6px solid #C8102E; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-top:20px; }
    .profile-name { color: #004B87; font-size: 24px; font-weight: bold; margin-bottom: 5px; text-transform: uppercase;}
    .profile-title { color: #6c757d; font-size: 15px; font-style: italic; font-weight: bold; margin-bottom: 15px;}
    .profile-info { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 15px;}
    .info-label { color: #495057; font-weight: bold; }
    .header-box { background-color: #004B87; padding: 20px; border-radius: 10px; margin-bottom: 25px; text-align: center; color: white; box-shadow: 0 4px 10px rgba(0,0,0,0.1);}
    .header-box h1 { margin: 0; font-size: 28px; text-transform: uppercase; font-weight: 900;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>🗂️ QUẢN LÝ HỒ SƠ CÔNG CHỨC - TGDV</h1><p style="margin:0; opacity: 0.8;">Cơ sở dữ liệu nhân sự số hóa</p></div>', unsafe_allow_html=True)

menu = st.sidebar.radio("📌 CHỨC NĂNG:", ["🔍 Tra cứu & Xem Hồ sơ", "➕ Nhập mới / Cập nhật Hồ sơ"])
st.sidebar.write("---")

# Hàm tải dữ liệu
@st.cache_data(ttl=5)
def load_profiles():
    try:
        res = supabase.table("ho_so_cbcc").select("*").execute()
        return pd.DataFrame(res.data)
    except: return pd.DataFrame()

df_hoso = load_profiles()

if menu == "➕ Nhập mới / Cập nhật Hồ sơ":
    st.markdown("### 📝 FORM NHẬP THÔNG TIN CÁN BỘ")
    st.info("💡 Lưu ý: Nếu nhập 'Mã CBCC' đã tồn tại, hệ thống sẽ tự động cập nhật thông tin mới thay vì tạo thêm người.")
    
    with st.form("form_ho_so", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            ma_cb = st.text_input("Mã CBCC (VD: CV01)*", placeholder="Mã định danh duy nhất")
            ho_ten = st.text_input("Họ và tên*")
            ngay_sinh = st.text_input("Ngày sinh (DD/MM/YYYY)")
            gioi_tinh = st.selectbox("Giới tính", ["Nam", "Nữ"])
        with c2:
            que_quan = st.text_input("Quê quán")
            don_vi = st.selectbox("Đơn vị công tác*", ["Lãnh đạo Ban", "Văn phòng Ban", "Phòng LLCT - LSĐ", "Phòng Tuyên truyền, Báo chí", "Phòng Khoa giáo", "Phòng Dân vận", "Phòng Đoàn thể"])
            chuc_vu = st.selectbox("Chức vụ", ["Trưởng Ban", "Phó Trưởng Ban", "Chánh Văn phòng", "Trưởng phòng", "Phó Trưởng phòng", "Chuyên viên"])
            ngach = st.text_input("Ngạch công chức", placeholder="VD: Chuyên viên chính")
        with c3:
            chuyen_mon = st.text_input("Trình độ chuyên môn", placeholder="VD: Thạc sĩ QLNN")
            ly_luan = st.selectbox("Lý luận chính trị", ["Chưa qua đào tạo", "Sơ cấp", "Trung cấp", "Cao cấp", "Cử nhân"])
            ngay_vao_dang = st.text_input("Ngày vào Đảng (DD/MM/YYYY)")

        submit = st.form_submit_button("💾 LƯU HỒ SƠ", type="primary", use_container_width=True)
        if submit:
            if not ma_cb or not ho_ten:
                st.error("⚠️ Vui lòng nhập Mã CBCC và Họ tên!")
            else:
                data = {
                    "id": ma_cb.strip().upper(), "ho_ten": ho_ten.title(), "ngay_sinh": ngay_sinh, "gioi_tinh": gioi_tinh,
                    "que_quan": que_quan, "don_vi": don_vi, "chuc_vu": chuc_vu, "ngach_cong_chuc": ngach,
                    "trinh_do_chuyen_mon": chuyen_mon, "ly_luan_chinh_tri": ly_luan, "ngay_vao_dang": ngay_vao_dang
                }
                with st.spinner("Đang lưu dữ liệu..."):
                    try:
                        # Lệnh upsert: Có mã rồi thì đè lên sửa, chưa có thì tạo mới
                        supabase.table("ho_so_cbcc").upsert(data).execute()
                        st.success(f"✅ Đã lưu hồ sơ đồng chí **{ho_ten}** thành công!")
                        st.cache_data.clear()
                    except Exception as e:
                        st.error(f"⚠️ Có lỗi xảy ra: {e}")

elif menu == "🔍 Tra cứu & Xem Hồ sơ":
    st.markdown("### 🔍 TÌM KIẾM HỒ SƠ")
    if df_hoso.empty:
        st.warning("📭 Dữ liệu đang trống. Vui lòng sang mục Nhập mới để thêm hồ sơ.")
    else:
        tu_khoa = st.text_input("Nhập Tên, Mã CBCC hoặc Đơn vị để tìm kiếm:", placeholder="VD: Tuan, CV01, Văn phòng...")
        
        # Bộ lọc siêu tốc độ
        if tu_khoa:
            mask = df_hoso.apply(lambda row: row.astype(str).str.contains(tu_khoa, case=False).any(), axis=1)
            df_ket_qua = df_hoso[mask]
        else:
            df_ket_qua = df_hoso

        st.caption(f"Tìm thấy **{len(df_ket_qua)}** hồ sơ.")
        
        if not df_ket_qua.empty:
            # Chọn 1 người để xem Card chi tiết
            ds_hien_thi = df_ket_qua['ho_ten'] + " - " + df_ket_qua['chuc_vu'] + " (" + df_ket_qua['id'] + ")"
            chon_nguoi = st.selectbox("👉 Chọn một đồng chí để xem Chi tiết Hồ sơ:", ds_hien_thi.tolist())
            
            if chon_nguoi:
                ma_chon = chon_nguoi.split("(")[-1].replace(")", "")
                info = df_hoso[df_hoso['id'] == ma_chon].iloc[0]
                
                # Hiển thị Thẻ Hồ Sơ chuyên nghiệp
                st.markdown(f"""
                <div class="profile-card">
                    <div class="profile-name">{info['ho_ten']}</div>
                    <div class="profile-title">{info['chuc_vu']} | {info['don_vi']}</div>
                    <hr style="border-top: 1px dashed #dee2e6;">
                    <div class="profile-info">
                        <div>
                            <p><span class="info-label">Mã CBCC:</span> {info['id']}</p>
                            <p><span class="info-label">Ngày sinh:</span> {info.get('ngay_sinh', '---')}</p>
                            <p><span class="info-label">Giới tính:</span> {info.get('gioi_tinh', '---')}</p>
                            <p><span class="info-label">Quê quán:</span> {info.get('que_quan', '---')}</p>
                        </div>
                        <div>
                            <p><span class="info-label">Ngạch công chức:</span> {info.get('ngach_cong_chuc', '---')}</p>
                            <p><span class="info-label">Trình độ CM:</span> {info.get('trinh_do_chuyen_mon', '---')}</p>
                            <p><span class="info-label">Lý luận CT:</span> {info.get('ly_luan_chinh_tri', '---')}</p>
                            <p><span class="info-label">Ngày vào Đảng:</span> {info.get('ngay_vao_dang', '---')}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            st.write("---")
            with st.expander("👁️ Xem bảng dữ liệu tổng hợp (Excel view)"):
                # Đổi tên cột cho đẹp
                df_hien_thi = df_ket_qua.rename(columns={'id':'Mã CBCC', 'ho_ten':'Họ tên', 'don_vi':'Đơn vị', 'chuc_vu':'Chức vụ', 'trinh_do_chuyen_mon':'Chuyên môn', 'ly_luan_chinh_tri': 'Lý luận CT'})
                st.dataframe(df_hien_thi[['Mã CBCC', 'Họ tên', 'Đơn vị', 'Chức vụ', 'Chuyên môn', 'Lý luận CT']], hide_index=True)
