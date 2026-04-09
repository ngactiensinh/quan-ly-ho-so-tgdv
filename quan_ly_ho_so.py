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
    .auth-box { max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 5px solid #004B87;}
</style>
""", unsafe_allow_html=True)

# Khởi tạo Session State cho Đăng nhập
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "ma_cbcc" not in st.session_state: st.session_state["ma_cbcc"] = ""
if "ho_ten" not in st.session_state: st.session_state["ho_ten"] = ""
if "role" not in st.session_state: st.session_state["role"] = "User"

# ==========================================
# MÀN HÌNH XÁC THỰC (LOGIN / REGISTER)
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown('<div class="header-box"><h1>🗂️ HỆ THỐNG QUẢN LÝ HỒ SƠ TGDV</h1><p style="margin:0; opacity: 0.8;">Cổng thông tin nội bộ</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_register = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký Tài khoản"])
        
        with tab_login:
            # Đã xóa div rác ở đây
            with st.form("login_form"):
                log_ma = st.text_input("Mã CBCC (Tên đăng nhập):").strip().upper()
                log_pass = st.text_input("Mật khẩu:", type="password")
                if st.form_submit_button("🚀 ĐĂNG NHẬP", type="primary", use_container_width=True):
                    if not log_ma or not log_pass: st.error("⚠️ Vui lòng nhập đủ thông tin!")
                    else:
                        try:
                            user_data = supabase.table("tai_khoan").select("*").eq("ma_cbcc", log_ma).execute().data
                            if len(user_data) > 0:
                                user = user_data[0]
                                if user['mat_khau'] == log_pass:
                                    if user['trang_thai'] == 'Chờ duyệt': st.warning("⏳ Tài khoản của bạn đang chờ Admin phê duyệt!")
                                    else:
                                        st.session_state["logged_in"] = True
                                        st.session_state["ma_cbcc"] = user['ma_cbcc']
                                        st.session_state["ho_ten"] = user['ho_ten']
                                        st.session_state["role"] = user['phan_quyen']
                                        st.success("Đăng nhập thành công!"); st.rerun()
                                else: st.error("❌ Sai mật khẩu!")
                            else: st.error("❌ Không tìm thấy Mã CBCC này!")
                        except Exception as e: st.error(f"Lỗi kết nối: {e}")

        with tab_register:
            # Đã xóa div rác ở đây
            with st.form("register_form"):
                reg_ma = st.text_input("Mã CBCC (Sẽ dùng làm Tên đăng nhập)*").strip().upper()
                reg_name = st.text_input("Họ và tên*")
                reg_cv = st.selectbox("Chức vụ", ["Trưởng Ban", "Phó Trưởng Ban", "Chánh Văn phòng", "Trưởng phòng", "Phó Trưởng phòng", "Chuyên viên", "Khác"])
                reg_dv = st.selectbox("Đơn vị công tác", ["Lãnh đạo Ban", "Văn phòng Ban", "Phòng LLCT - LSĐ", "Phòng Tuyên truyền, Báo chí", "Phòng Khoa giáo", "Phòng Dân vận", "Phòng Đoàn thể"])
                reg_pass = st.text_input("Mật khẩu*", type="password")
                reg_pass2 = st.text_input("Nhập lại Mật khẩu*", type="password")
                
                if st.form_submit_button("📩 GỬI YÊU CẦU ĐĂNG KÝ", type="primary", use_container_width=True):
                    if not reg_ma or not reg_name or not reg_pass: st.error("⚠️ Vui lòng điền các trường bắt buộc (*)")
                    elif reg_pass != reg_pass2: st.error("⚠️ Mật khẩu xác nhận không khớp!")
                    else:
                        try:
                            check_exist = supabase.table("tai_khoan").select("ma_cbcc").eq("ma_cbcc", reg_ma).execute().data
                            if len(check_exist) > 0: st.error("⚠️ Mã CBCC này đã được đăng ký!")
                            else:
                                supabase.table("tai_khoan").insert({"ma_cbcc": reg_ma, "mat_khau": reg_pass, "ho_ten": reg_name.title(), "chuc_vu": reg_cv, "don_vi": reg_dv}).execute()
                                st.success("✅ Gửi yêu cầu thành công! Vui lòng chờ Admin phê duyệt.")
                        except Exception as e: st.error(f"Lỗi: {e}")
    st.stop()

# ==========================================
# GIAO DIỆN CHÍNH (KHI ĐÃ ĐĂNG NHẬP)
# ==========================================
st.sidebar.markdown(f"👋 Xin chào, **{st.session_state['ho_ten']}**")
st.sidebar.markdown(f"🔑 Quyền: **{st.session_state['role']}**")
if st.sidebar.button("🚪 Đăng xuất", type="primary", use_container_width=True):
    for key in ["logged_in", "ma_cbcc", "ho_ten", "role"]: st.session_state[key] = None
    st.rerun()

menu_options = ["🔍 Tra cứu & Xem Hồ sơ", "➕ Cập nhật Hồ sơ cá nhân"]
if st.session_state["role"] == "Admin": 
    menu_options = ["🛡️ Admin: Duyệt Tài khoản", "🔍 Tra cứu & Xem Hồ sơ", "➕ Admin: Cập nhật Hồ sơ (Tất cả)"]

menu = st.sidebar.radio("📌 CHỨC NĂNG:", menu_options)
st.sidebar.write("---")

st.markdown('<div class="header-box"><h1>🗂️ QUẢN LÝ HỒ SƠ CÁN BỘ BAN TUYÊN GIÁO VÀ DÂN VẬN TỈNH ỦY TUYÊN QUANG</h1></div>', unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_profiles():
    try: return pd.DataFrame(supabase.table("ho_so_cbcc").select("*").execute().data)
    except: return pd.DataFrame()

df_hoso = load_profiles()

# --- MODULE ADMIN: DUYỆT TÀI KHOẢN ---
if menu == "🛡️ Admin: Duyệt Tài khoản":
    st.markdown("### 🛡️ QUẢN TRỊ TÀI KHOẢN HỆ THỐNG")
    try:
        tk_data = supabase.table("tai_khoan").select("*").execute().data
        if not tk_data: st.info("Chưa có tài khoản nào.")
        else:
            df_tk = pd.DataFrame(tk_data)
            tab_cd, tab_hd = st.tabs(["⏳ Danh sách Chờ duyệt", "✅ Tài khoản đang Hoạt động"])
            
            with tab_cd:
                df_choduyet = df_tk[df_tk['trang_thai'] == 'Chờ duyệt']
                if df_choduyet.empty: st.success("🎉 Không có yêu cầu nào đang chờ duyệt!")
                else:
                    for idx, row in df_choduyet.iterrows():
                        with st.expander(f"👤 {row['ho_ten']} ({row['ma_cbcc']}) - {row['chuc_vu']}"):
                            st.write(f"**Đơn vị:** {row['don_vi']}")
                            if st.button("✅ DUYỆT TÀI KHOẢN NÀY", key=f"duyet_{row['ma_cbcc']}"):
                                supabase.table("tai_khoan").update({"trang_thai": "Hoạt động"}).eq("ma_cbcc", row['ma_cbcc']).execute()
                                st.success("Đã duyệt!"); st.rerun()
                                
            with tab_hd:
                df_hoatdong = df_tk[df_tk['trang_thai'] == 'Hoạt động']
                st.dataframe(df_hoatdong[['ma_cbcc', 'ho_ten', 'chuc_vu', 'don_vi', 'phan_quyen']], hide_index=True)
                st.markdown("#### 🔄 Chức năng Reset Mật khẩu")
                rs_ma = st.selectbox("Chọn tài khoản cần Reset về 'Chuyenvien@2026':", df_hoatdong['ma_cbcc'] + " - " + df_hoatdong['ho_ten'])
                if st.button("⚠️ XÁC NHẬN RESET", type="primary"):
                    ma_rs_chon = rs_ma.split(" - ")[0]
                    supabase.table("tai_khoan").update({"mat_khau": "Chuyenvien@2026"}).eq("ma_cbcc", ma_rs_chon).execute()
                    st.success(f"✅ Đã reset mật khẩu của {ma_rs_chon} về 'Chuyenvien@2026'")
    except Exception as e: st.error(f"Lỗi tải dữ liệu: {e}")

# --- MODULE NHẬP LIỆU (CHUNG CHO ADMIN & USER) ---
elif menu in ["➕ Cập nhật Hồ sơ cá nhân", "➕ Admin: Cập nhật Hồ sơ (Tất cả)"]:
    is_admin = st.session_state["role"] == "Admin"
    st.markdown("### 📝 TRUNG TÂM NHẬP LIỆU HỒ SƠ")
    
    # Nếu là User, ép buộc dùng mã của mình. Nếu là Admin, cho phép tự gõ.
    ma_mac_dinh = "" if is_admin else st.session_state["ma_cbcc"]
    
    tab_chinh, tab_congtac, tab_luong, tab_khenthuong = st.tabs(["👤 Hồ sơ chính", "🏢 Lịch sử công tác", "💰 Diễn biến lương", "🏆 Khen thưởng / Kỷ luật"])
    
    with tab_chinh:
        with st.form("form_ho_so", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                ma_cb = st.text_input("Mã CBCC*", value=ma_mac_dinh, disabled=not is_admin)
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
            ma_cb_ct = st.text_input("Mã CBCC*", value=ma_mac_dinh, disabled=not is_admin)
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
                    st.success("✅ Thành công!")

    with tab_luong:
        with st.form("form_luong", clear_on_submit=True):
            ma_cb_l = st.text_input("Mã CBCC*", value=ma_mac_dinh, disabled=not is_admin)
            ngay_qd_l = st.text_input("Ngày quyết định (DD/MM/YYYY)")
            c1, c2 = st.columns(2)
            bac_luong = c1.text_input("Bậc lương (VD: 3/9)")
            he_so = c2.text_input("Hệ số (VD: 3.00)")
            qd_l = st.text_input("Quyết định số")
            if st.form_submit_button("💾 LƯU DIỄN BIẾN LƯƠNG", type="primary", use_container_width=True):
                if not ma_cb_l: st.error("⚠️ Phải nhập Mã CBCC!")
                else:
                    supabase.table("dien_bien_luong").insert({"ma_cbcc": ma_cb_l.strip().upper(), "ngay_quyet_dinh": ngay_qd_l, "bac_luong": bac_luong, "he_so": he_so, "quyet_dinh_so": qd_l}).execute()
                    st.success("✅ Thành công!")

    with tab_khenthuong:
        with st.form("form_ktkl", clear_on_submit=True):
            ma_cb_kt = st.text_input("Mã CBCC*", value=ma_mac_dinh, disabled=not is_admin)
            ngay_qd_kt = st.text_input("Ngày quyết định (DD/MM/YYYY)")
            loai = st.selectbox("Loại", ["Khen thưởng", "Kỷ luật"])
            noi_dung = st.text_area("Nội dung")
            qd_kt = st.text_input("Quyết định số")
            if st.form_submit_button("💾 LƯU KHEN THƯỞNG / KỶ LUẬT", type="primary", use_container_width=True):
                if not ma_cb_kt: st.error("⚠️ Phải nhập Mã CBCC!")
                else:
                    supabase.table("khen_thuong_ky_luat").insert({"ma_cbcc": ma_cb_kt.strip().upper(), "ngay_quyet_dinh": ngay_qd_kt, "loai": loai, "noi_dung": noi_dung, "quyet_dinh_so": qd_kt}).execute()
                    st.success(f"✅ Thành công!")

# --- MODULE TRA CỨU ---
elif menu == "🔍 Tra cứu & Xem Hồ sơ":
    st.markdown("### 🔍 TÌM KIẾM HỒ SƠ")
    if df_hoso.empty: st.warning("📭 Dữ liệu đang trống.")
    else:
        tu_khoa = st.text_input("Nhập Tên hoặc Mã CBCC để tìm kiếm:")
        df_ket_qua = df_hoso[df_hoso.apply(lambda row: row.astype(str).str.contains(tu_khoa, case=False).any(), axis=1)] if tu_khoa else df_hoso
        
        if not df_ket_qua.empty:
            ds_hien_thi = df_ket_qua['ho_ten'] + " - " + df_ket_qua['chuc_vu'] + " (" + df_ket_qua['id'] + ")"
            chon_nguoi = st.selectbox("👉 Chọn một đồng chí để xem Chi tiết:", ds_hien_thi.tolist())
            
            if chon_nguoi:
                ma_chon = chon_nguoi.split("(")[-1].replace(")", "")
                info = df_hoso[df_hoso['id'] == ma_chon].iloc[0]
                
                st.markdown(f"""<div class="profile-card"><div class="profile-name">{info['ho_ten']}</div><div class="profile-title">{info['chuc_vu']} | {info['don_vi']}</div><hr style="border-top: 1px dashed #dee2e6;"><div class="profile-info"><div><p><span class="info-label">Mã CBCC:</span> {info['id']}</p><p><span class="info-label">Ngày sinh:</span> {info.get('ngay_sinh', '---')}</p><p><span class="info-label">Giới tính:</span> {info.get('gioi_tinh', '---')}</p><p><span class="info-label">Quê quán:</span> {info.get('que_quan', '---')}</p></div><div><p><span class="info-label">Ngạch:</span> {info.get('ngach_cong_chuc', '---')}</p><p><span class="info-label">Chuyên môn:</span> {info.get('trinh_do_chuyen_mon', '---')}</p><p><span class="info-label">Lý luận CT:</span> {info.get('ly_luan_chinh_tri', '---')}</p><p><span class="info-label">Ngày vào Đảng:</span> {info.get('ngay_vao_dang', '---')}</p></div></div></div>""", unsafe_allow_html=True)
                st.write("---")
                
                st.markdown("#### 📑 CÁC THÔNG TIN LIÊN QUAN")
                t_ct, t_l, t_kt = st.tabs(["🏢 Lịch sử công tác", "💰 Diễn biến lương", "🏆 Khen thưởng & Kỷ luật"])
                with t_ct:
                    df_ct = pd.DataFrame(supabase.table("lich_su_cong_tac").select("tu_ngay, den_ngay, vi_tri, don_vi, quyet_dinh_so").eq("ma_cbcc", ma_chon).execute().data)
                    if not df_ct.empty: st.table(df_ct.rename(columns={'tu_ngay':'Từ ngày', 'den_ngay':'Đến ngày', 'vi_tri':'Vị trí', 'don_vi':'Đơn vị', 'quyet_dinh_so':'Quyết định số'}))
                with t_l:
                    df_l = pd.DataFrame(supabase.table("dien_bien_luong").select("ngay_quyet_dinh, bac_luong, he_so, quyet_dinh_so").eq("ma_cbcc", ma_chon).execute().data)
                    if not df_l.empty: st.table(df_l.rename(columns={'ngay_quyet_dinh':'Ngày QĐ', 'bac_luong':'Bậc lương', 'he_so':'Hệ số', 'quyet_dinh_so':'Quyết định số'}))
                with t_kt:
                    df_kt = pd.DataFrame(supabase.table("khen_thuong_ky_luat").select("ngay_quyet_dinh, loai, noi_dung, quyet_dinh_so").eq("ma_cbcc", ma_chon).execute().data)
                    if not df_kt.empty: st.table(df_kt.rename(columns={'ngay_quyet_dinh':'Ngày QĐ', 'loai':'Loại', 'noi_dung':'Nội dung', 'quyet_dinh_so':'Quyết định số'}))
