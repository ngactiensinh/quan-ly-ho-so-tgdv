import streamlit as st
import pandas as pd
from supabase import create_client, Client

st.set_page_config(page_title="Hồ sơ CBCC - TGDV", page_icon="🗂️", layout="wide")

# ==========================================
# CẤU HÌNH SUPABASE
# ==========================================
SUPABASE_URL = "https://qqzsdxhqrdfvxnlurnyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFxenNkeGhxcmRmdnhubHVybnliIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2MjY0NjAsImV4cCI6MjA5MTIwMjQ2MH0.H62F5zYEZ5l47fS4IdAE2JdRdI7inXQqWG0nvXhn2P8"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    pass

st.markdown("""
<style>
    .profile-card { background-color: #ffffff; padding: 25px; border-radius: 12px; border-left: 6px solid #C8102E; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-top:20px; }
    .profile-name { color: #004B87; font-size: 24px; font-weight: bold; margin-bottom: 5px; text-transform: uppercase;}
    .profile-title { color: #6c757d; font-size: 15px; font-style: italic; font-weight: bold; margin-bottom: 15px;}
    .profile-info { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 15px;}
    .info-label { color: #495057; font-weight: bold; }
    .header-box { background-color: #004B87; padding: 20px; border-radius: 10px; margin-bottom: 25px; text-align: center; color: white; box-shadow: 0 4px 10px rgba(0,0,0,0.1);}
    .header-box h1 { margin: 0; font-size: 28px; text-transform: uppercase; font-weight: 900;}
    div[data-testid="stForm"] { background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 20px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>🗂️ QUẢN LÝ HỒ SƠ CÔNG CHỨC - TGDV</h1><p style="margin:0; opacity: 0.8;">Cơ sở dữ liệu nhân sự số hóa</p></div>', unsafe_allow_html=True)

menu = st.sidebar.radio("📌 CHỨC NĂNG:", ["🔍 Tra cứu & Xem Hồ sơ", "➕ Nhập liệu Đa nhiệm"])
st.sidebar.write("---")

@st.cache_data(ttl=5)
def load_profiles():
    try: return pd.DataFrame(supabase.table("ho_so_cbcc").select("*").execute().data)
    except: return pd.DataFrame()

df_hoso = load_profiles()

# ==========================================
# CHỨC NĂNG NHẬP LIỆU
# ==========================================
if menu == "➕ Nhập liệu Đa nhiệm":
    st.markdown("### 📝 TRUNG TÂM NHẬP LIỆU HỒ SƠ")
    st.info("💡 Hệ thống liên kết dữ liệu thông qua **Mã CBCC**. Hãy đảm bảo nhập đúng Mã CBCC của cán bộ ở tất cả các tab.")
    
    # CHIA 4 TAB Y HỆT THIẾT KẾ CỦA SẾP
    tab_chinh, tab_congtac, tab_luong, tab_khenthuong = st.tabs(["👤 Hồ sơ chính", "🏢 Lịch sử công tác", "💰 Diễn biến lương", "🏆 Khen thưởng / Kỷ luật"])
    
    with tab_chinh:
        with st.form("form_ho_so", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                ma_cb = st.text_input("Mã CBCC (VD: CV01)*")
                ho_ten = st.text_input("Họ và tên*")
                ngay_sinh = st.text_input("Ngày sinh (DD/MM/YYYY)")
                gioi_tinh = st.selectbox("Giới tính", ["Nam", "Nữ"])
            with c2:
                que_quan = st.text_input("Quê quán")
                don_vi = st.selectbox("Đơn vị công tác*", ["Lãnh đạo Ban", "Văn phòng Ban", "Phòng LLCT - LSĐ", "Phòng Tuyên truyền, Báo chí", "Phòng Khoa giáo", "Phòng Dân vận", "Phòng Đoàn thể"])
                chuc_vu = st.selectbox("Chức vụ", ["Trưởng Ban", "Phó Trưởng Ban", "Chánh Văn phòng", "Phó Chánh Văn phòng", "Trưởng phòng", "Phó Trưởng phòng", "Chuyên viên", "Khác"])
                ngach = st.text_input("Ngạch công chức")
            with c3:
                chuyen_mon = st.text_input("Trình độ chuyên môn")
                ly_luan = st.selectbox("Lý luận chính trị", ["Chưa qua đào tạo", "Sơ cấp", "Trung cấp", "Cao cấp", "Cử nhân"])
                ngay_vao_dang = st.text_input("Ngày vào Đảng (DD/MM/YYYY)")

            if st.form_submit_button("💾 LƯU HỒ SƠ CHÍNH", type="primary", use_container_width=True):
                if not ma_cb or not ho_ten: st.error("⚠️ Nhập thiếu Mã CBCC hoặc Họ tên!")
                else:
                    data = {"id": ma_cb.strip().upper(), "ho_ten": ho_ten.title(), "ngay_sinh": ngay_sinh, "gioi_tinh": gioi_tinh, "que_quan": que_quan, "don_vi": don_vi, "chuc_vu": chuc_vu, "ngach_cong_chuc": ngach, "trinh_do_chuyen_mon": chuyen_mon, "ly_luan_chinh_tri": ly_luan, "ngay_vao_dang": ngay_vao_dang}
                    supabase.table("ho_so_cbcc").upsert(data).execute()
                    st.success("✅ Đã lưu Hồ sơ chính!"); st.cache_data.clear()

    with tab_congtac:
        with st.form("form_cong_tac", clear_on_submit=True):
            ma_cb_ct = st.text_input("🔑 Nhập Mã CBCC cần thêm lịch sử (VD: CV01)*")
            c1, c2 = st.columns(2)
            tu_ngay = c1.text_input("Từ ngày (DD/MM/YYYY)")
            den_ngay = c2.text_input("Đến ngày (DD/MM/YYYY)")
            vi_tri = st.text_input("Vị trí / Chức danh")
            don_vi_ct = st.text_input("Đơn vị công tác")
            qd_ct = st.text_input("Quyết định số")
            
            if st.form_submit_button("💾 LƯU LỊCH SỬ CÔNG TÁC", type="primary", use_container_width=True):
                if not ma_cb_ct: st.error("⚠️ Phải nhập Mã CBCC!")
                else:
                    supabase.table("lich_su_cong_tac").insert({"ma_cbcc": ma_cb_ct.strip().upper(), "tu_ngay": tu_ngay, "den_ngay": den_ngay, "vi_tri": vi_tri, "don_vi": don_vi_ct, "quyet_dinh_so": qd_ct}).execute()
                    st.success("✅ Đã lưu Lịch sử công tác!")

    with tab_luong:
        with st.form("form_luong", clear_on_submit=True):
            ma_cb_l = st.text_input("🔑 Nhập Mã CBCC cần cập nhật lương (VD: CV01)*")
            ngay_qd_l = st.text_input("Ngày quyết định (DD/MM/YYYY)")
            c1, c2 = st.columns(2)
            bac_luong = c1.text_input("Bậc lương (VD: 3/9)")
            he_so = c2.text_input("Hệ số (VD: 3.00)")
            qd_l = st.text_input("Quyết định số")
            
            if st.form_submit_button("💾 LƯU DIỄN BIẾN LƯƠNG", type="primary", use_container_width=True):
                if not ma_cb_l: st.error("⚠️ Phải nhập Mã CBCC!")
                else:
                    supabase.table("dien_bien_luong").insert({"ma_cbcc": ma_cb_l.strip().upper(), "ngay_quyet_dinh": ngay_qd_l, "bac_luong": bac_luong, "he_so": he_so, "quyet_dinh_so": qd_l}).execute()
                    st.success("✅ Đã lưu Diễn biến lương!")

    with tab_khenthuong:
        with st.form("form_ktkl", clear_on_submit=True):
            ma_cb_kt = st.text_input("🔑 Nhập Mã CBCC cần thêm khen thưởng/kỷ luật (VD: CV01)*")
            ngay_qd_kt = st.text_input("Ngày quyết định (DD/MM/YYYY)")
            loai = st.selectbox("Loại", ["Khen thưởng", "Kỷ luật"])
            noi_dung = st.text_area("Nội dung Khen thưởng / Kỷ luật")
            qd_kt = st.text_input("Quyết định số")
            
            if st.form_submit_button("💾 LƯU KHEN THƯỞNG / KỶ LUẬT", type="primary", use_container_width=True):
                if not ma_cb_kt: st.error("⚠️ Phải nhập Mã CBCC!")
                else:
                    supabase.table("khen_thuong_ky_luat").insert({"ma_cbcc": ma_cb_kt.strip().upper(), "ngay_quyet_dinh": ngay_qd_kt, "loai": loai, "noi_dung": noi_dung, "quyet_dinh_so": qd_kt}).execute()
                    st.success(f"✅ Đã lưu {loai}!")

# ==========================================
# CHỨC NĂNG TRA CỨU
# ==========================================
elif menu == "🔍 Tra cứu & Xem Hồ sơ":
    st.markdown("### 🔍 TÌM KIẾM HỒ SƠ")
    if df_hoso.empty: st.warning("📭 Dữ liệu đang trống.")
    else:
        tu_khoa = st.text_input("Nhập Tên hoặc Mã CBCC để tìm kiếm:", placeholder="VD: CV01, Tuan...")
        df_ket_qua = df_hoso[df_hoso.apply(lambda row: row.astype(str).str.contains(tu_khoa, case=False).any(), axis=1)] if tu_khoa else df_hoso
        st.caption(f"Tìm thấy **{len(df_ket_qua)}** hồ sơ.")
        
        if not df_ket_qua.empty:
            ds_hien_thi = df_ket_qua['ho_ten'] + " - " + df_ket_qua['chuc_vu'] + " (" + df_ket_qua['id'] + ")"
            chon_nguoi = st.selectbox("👉 Chọn một đồng chí để xem Chi tiết Hồ sơ:", ds_hien_thi.tolist())
            
            if chon_nguoi:
                ma_chon = chon_nguoi.split("(")[-1].replace(")", "")
                info = df_hoso[df_hoso['id'] == ma_chon].iloc[0]
                
                # Render Thẻ Hồ sơ
                st.markdown(f"""
                <div class="profile-card">
                    <div class="profile-name">{info['ho_ten']}</div>
                    <div class="profile-title">{info['chuc_vu']} | {info['don_vi']}</div>
                    <hr style="border-top: 1px dashed #dee2e6;">
                    <div class="profile-info">
                        <div><p><span class="info-label">Mã CBCC:</span> {info['id']}</p><p><span class="info-label">Ngày sinh:</span> {info.get('ngay_sinh', '---')}</p><p><span class="info-label">Giới tính:</span> {info.get('gioi_tinh', '---')}</p><p><span class="info-label">Quê quán:</span> {info.get('que_quan', '---')}</p></div>
                        <div><p><span class="info-label">Ngạch:</span> {info.get('ngach_cong_chuc', '---')}</p><p><span class="info-label">Chuyên môn:</span> {info.get('trinh_do_chuyen_mon', '---')}</p><p><span class="info-label">Lý luận CT:</span> {info.get('ly_luan_chinh_tri', '---')}</p><p><span class="info-label">Ngày vào Đảng:</span> {info.get('ngay_vao_dang', '---')}</p></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("---")
                
                # --- TRÍCH XUẤT THÔNG TIN LIÊN QUAN ---
                st.markdown("#### 📑 CÁC THÔNG TIN LIÊN QUAN")
                t_ct, t_l, t_kt = st.tabs(["🏢 Lịch sử công tác", "💰 Diễn biến lương", "🏆 Khen thưởng & Kỷ luật"])
                
                with t_ct:
                    try: 
                        df_ct = pd.DataFrame(supabase.table("lich_su_cong_tac").select("tu_ngay, den_ngay, vi_tri, don_vi, quyet_dinh_so").eq("ma_cbcc", ma_chon).execute().data)
                        if not df_ct.empty: st.table(df_ct.rename(columns={'tu_ngay':'Từ ngày', 'den_ngay':'Đến ngày', 'vi_tri':'Vị trí', 'don_vi':'Đơn vị', 'quyet_dinh_so':'Quyết định số'}))
                        else: st.info("Chưa có dữ liệu.")
                    except: st.info("Chưa có dữ liệu.")
                        
                with t_l:
                    try:
                        df_l = pd.DataFrame(supabase.table("dien_bien_luong").select("ngay_quyet_dinh, bac_luong, he_so, quyet_dinh_so").eq("ma_cbcc", ma_chon).execute().data)
                        if not df_l.empty: st.table(df_l.rename(columns={'ngay_quyet_dinh':'Ngày QĐ', 'bac_luong':'Bậc lương', 'he_so':'Hệ số', 'quyet_dinh_so':'Quyết định số'}))
                        else: st.info("Chưa có dữ liệu.")
                    except: st.info("Chưa có dữ liệu.")
                        
                with t_kt:
                    try:
                        df_kt = pd.DataFrame(supabase.table("khen_thuong_ky_luat").select("ngay_quyet_dinh, loai, noi_dung, quyet_dinh_so").eq("ma_cbcc", ma_chon).execute().data)
                        if not df_kt.empty: st.table(df_kt.rename(columns={'ngay_quyet_dinh':'Ngày QĐ', 'loai':'Loại', 'noi_dung':'Nội dung', 'quyet_dinh_so':'Quyết định số'}))
                        else: st.info("Chưa có dữ liệu.")
                    except: st.info("Chưa có dữ liệu.")
