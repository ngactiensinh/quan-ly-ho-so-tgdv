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

# ==========================================
# CSS LÀM ĐẸP (NHUỘM XANH NAVY TẤT CẢ CÁC NÚT)
# ==========================================
st.markdown("""
<style>
    /* Biến TẤT CẢ các nút thành Xanh Navy uy tín */
    div[data-testid="stButton"] > button,
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #004B87 !important;
        color: white !important;
        border: 1px solid #004B87 !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        transition: all 0.3s ease;
    }
    div[data-testid="stButton"] > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #003366 !important;
        border: 1px solid #003366 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    .profile-card { background-color: #ffffff; padding: 25px; border-radius: 12px; border-left: 6px solid #004B87; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-top:20px; margin-bottom: 20px;}
    .profile-name { color: #004B87; font-size: 24px; font-weight: bold; margin-bottom: 5px; text-transform: uppercase;}
    .profile-title { color: #6c757d; font-size: 15px; font-style: italic; font-weight: bold; margin-bottom: 15px;}
    .profile-info { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 15px;}
    .info-label { color: #495057; font-weight: bold; }
    .header-box { background-color: #004B87; padding: 20px; border-radius: 10px; margin-bottom: 25px; text-align: center; color: white; box-shadow: 0 4px 10px rgba(0,0,0,0.1);}
    .header-box h1 { margin: 0; font-size: 28px; text-transform: uppercase; font-weight: 900;}
    div[data-testid="stForm"] { background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 20px;}
</style>
""", unsafe_allow_html=True)

# Khởi tạo Session State
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "ma_cbcc" not in st.session_state: st.session_state["ma_cbcc"] = ""
if "ho_ten" not in st.session_state: st.session_state["ho_ten"] = ""
if "role" not in st.session_state: st.session_state["role"] = "User"
if "menu_selection" not in st.session_state: st.session_state["menu_selection"] = "📊 Bảng Điều khiển"
if "edit_target_id" not in st.session_state: st.session_state["edit_target_id"] = ""

# ==========================================
# MÀN HÌNH XÁC THỰC
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown('<div class="header-box"><h1>🗂️ HỆ THỐNG QUẢN LÝ HỒ SƠ TGDV</h1><p style="margin:0; opacity: 0.8;">Cổng thông tin nội bộ</p></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_register = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký Tài khoản"])
        with tab_login:
            with st.form("login_form"):
                log_ma = st.text_input("Mã CBCC (Tên đăng nhập):").strip().upper()
                log_pass = st.text_input("Mật khẩu:", type="password")
                if st.form_submit_button("🚀 ĐĂNG NHẬP", use_container_width=True):
                    if not log_ma or not log_pass: st.error("⚠️ Vui lòng nhập đủ thông tin!")
                    else:
                        try:
                            user_data = supabase.table("tai_khoan").select("*").eq("ma_cbcc", log_ma).execute().data
                            if len(user_data) > 0:
                                user = user_data[0]
                                if user['mat_khau'] == log_pass:
                                    if user['trang_thai'] == 'Chờ duyệt': st.warning("⏳ Tài khoản của bạn đang chờ Admin phê duyệt!")
                                    else:
                                        st.session_state["logged_in"] = True; st.session_state["ma_cbcc"] = user['ma_cbcc']
                                        st.session_state["ho_ten"] = user['ho_ten']; st.session_state["role"] = user['phan_quyen']
                                        st.session_state["menu_selection"] = "📊 Bảng Điều khiển"
                                        st.rerun()
                                else: st.error("❌ Sai mật khẩu!")
                            else: st.error("❌ Không tìm thấy Mã CBCC này!")
                        except Exception as e: st.error(f"Lỗi kết nối: {e}")
        with tab_register:
            with st.form("register_form"):
                reg_ma = st.text_input("Mã CBCC (Sẽ dùng làm Tên đăng nhập)*").strip().upper()
                reg_name = st.text_input("Họ và tên*")
                reg_cv = st.selectbox("Chức vụ", ["Trưởng Ban", "Phó Trưởng Ban", "Chánh Văn phòng", "Trưởng phòng", "Phó Trưởng phòng", "Chuyên viên", "Khác"])
                reg_dv = st.selectbox("Đơn vị công tác", ["Lãnh đạo Ban", "Văn phòng Ban", "Phòng LLCT - LSĐ", "Phòng Tuyên truyền, Báo chí", "Phòng Khoa giáo", "Phòng Dân vận", "Phòng Đoàn thể"])
                reg_pass = st.text_input("Mật khẩu*", type="password")
                reg_pass2 = st.text_input("Nhập lại Mật khẩu*", type="password")
                if st.form_submit_button("📩 GỬI YÊU CẦU ĐĂNG KÝ", use_container_width=True):
                    if not reg_ma or not reg_name or not reg_pass: st.error("⚠️ Vui lòng điền các trường bắt buộc (*)")
                    elif reg_pass != reg_pass2: st.error("⚠️ Mật khẩu xác nhận không khớp!")
                    else:
                        try:
                            if len(supabase.table("tai_khoan").select("ma_cbcc").eq("ma_cbcc", reg_ma).execute().data) > 0: st.error("⚠️ Mã CBCC này đã được đăng ký!")
                            else:
                                supabase.table("tai_khoan").insert({"ma_cbcc": reg_ma, "mat_khau": reg_pass, "ho_ten": reg_name.title(), "chuc_vu": reg_cv, "don_vi": reg_dv}).execute()
                                st.success("✅ Gửi yêu cầu thành công! Vui lòng chờ Admin phê duyệt.")
                        except Exception as e: st.error(f"Lỗi: {e}")
    st.stop()

# ==========================================
# GIAO DIỆN CHÍNH
# ==========================================
st.sidebar.markdown(f"👋 Xin chào, **{st.session_state['ho_ten']}**")
st.sidebar.markdown(f"🔑 Quyền: **{st.session_state['role']}**")

if st.sidebar.button("🚪 Đăng xuất", use_container_width=True):
    for key in ["logged_in", "ma_cbcc", "ho_ten", "role"]: st.session_state[key] = None
    st.rerun()

is_admin = st.session_state["role"] == "Admin"
menu_options = ["📊 Bảng Điều khiển", "🔍 Tra cứu & Xem Hồ sơ", "➕ Cập nhật Hồ sơ cá nhân"]
if is_admin: 
    menu_options = ["📊 Bảng Điều khiển", "🛡️ Admin: Duyệt Tài khoản", "🔍 Tra cứu & Xem Hồ sơ", "➕ Admin: Cập nhật Hồ sơ (Tất cả)"]

idx = menu_options.index(st.session_state["menu_selection"]) if st.session_state["menu_selection"] in menu_options else 0
menu = st.sidebar.radio("📌 CHỨC NĂNG:", menu_options, index=idx)
st.session_state["menu_selection"] = menu
st.sidebar.write("---")

st.markdown('<div class="header-box"><h1>🗂️ QUẢN LÝ HỒ SƠ CÁN BỘ BAN TUYÊN GIÁO VÀ DÂN VẬN TỈNH ỦY TUYÊN QUANG</h1></div>', unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_profiles():
    try: return pd.DataFrame(supabase.table("ho_so_cbcc").select("*").execute().data)
    except: return pd.DataFrame()

df_hoso = load_profiles()

def get_idx(lst, val):
    try: return lst.index(val)
    except: return 0

# --- MODULE 1: DASHBOARD ---
if menu == "📊 Bảng Điều khiển":
    st.markdown("### 📊 DASHBOARD THỐNG KÊ NHÂN SỰ")
    if df_hoso.empty: st.info("Chưa có dữ liệu để thống kê.")
    else:
        df_hoso.fillna("Chưa cập nhật", inplace=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("👥 Tổng số CBCC", len(df_hoso))
        c2.metric("👨 Nam", len(df_hoso[df_hoso['gioi_tinh'] == 'Nam']))
        c3.metric("👩 Nữ", len(df_hoso[df_hoso['gioi_tinh'] == 'Nữ']))
        c4.metric("🎓 Trình độ Thạc sĩ", len(df_hoso[df_hoso['trinh_do_chuyen_mon'].str.contains("Thạc", case=False, na=False)]))
        st.write("---")
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.markdown("#### 1. Trình độ Chuyên môn")
            st.bar_chart(df_hoso['trinh_do_chuyen_mon'].value_counts())
            st.markdown("#### 3. Ngạch Công chức")
            st.bar_chart(df_hoso['ngach_cong_chuc'].value_counts())
        with col_chart2:
            st.markdown("#### 2. Trình độ Lý luận Chính trị")
            st.bar_chart(df_hoso['ly_luan_chinh_tri'].value_counts())
            st.markdown("#### 4. Cơ cấu Giới tính")
            st.bar_chart(df_hoso['gioi_tinh'].value_counts())

# --- MODULE 2: ADMIN DUYỆT TÀI KHOẢN ---
elif menu == "🛡️ Admin: Duyệt Tài khoản":
    st.markdown("### 🛡️ QUẢN TRỊ TÀI KHOẢN HỆ THỐNG")
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
                    with st.expander(f"👤 {row['ho_ten']} ({row['ma_cbcc']})"):
                        st.write(f"**Chức vụ:** {row['chuc_vu']} | **Đơn vị:** {row['don_vi']}")
                        if st.button("✅ DUYỆT TÀI KHOẢN NÀY", key=f"duyet_{row['ma_cbcc']}"):
                            supabase.table("tai_khoan").update({"trang_thai": "Hoạt động"}).eq("ma_cbcc", row['ma_cbcc']).execute()
                            st.success("Đã duyệt!"); st.rerun()
        with tab_hd:
            df_hoatdong = df_tk[df_tk['trang_thai'] == 'Hoạt động']
            st.dataframe(df_hoatdong[['ma_cbcc', 'ho_ten', 'chuc_vu', 'don_vi', 'phan_quyen']], hide_index=True)
            st.markdown("#### 🔄 Chức năng Reset Mật khẩu")
            rs_ma = st.selectbox("Chọn tài khoản cần Reset về 'Chuyenvien@2026':", df_hoatdong['ma_cbcc'] + " - " + df_hoatdong['ho_ten'])
            if st.button("⚠️ XÁC NHẬN RESET"):
                supabase.table("tai_khoan").update({"mat_khau": "Chuyenvien@2026"}).eq("ma_cbcc", rs_ma.split(" - ")[0]).execute()
                st.success("✅ Đã reset thành công!")

# --- MODULE 3: TRA CỨU HỒ SƠ ---
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
                info = df_hoso[df_hoso['id'] == ma_chon].iloc[0].fillna("")
                
                # NÚT CHỈNH SỬA NHANH MÀU XANH
                if is_admin or info['id'] == st.session_state["ma_cbcc"]:
                    if st.button("✏️ Chỉnh sửa Hồ sơ này"):
                        st.session_state["edit_target_id"] = info['id']
                        st.session_state["menu_selection"] = "➕ Admin: Cập nhật Hồ sơ (Tất cả)" if is_admin else "➕ Cập nhật Hồ sơ cá nhân"
                        st.rerun()

                st.markdown(f"""<div class="profile-card"><div class="profile-name">{info['ho_ten']}</div><div class="profile-title">{info['chuc_vu']} | {info['don_vi']}</div><hr style="border-top: 1px dashed #dee2e6;"><div class="profile-info"><div><p><span class="info-label">Mã CBCC:</span> {info['id']}</p><p><span class="info-label">Ngày sinh:</span> {info['ngay_sinh']}</p><p><span class="info-label">Giới tính:</span> {info['gioi_tinh']}</p><p><span class="info-label">Quê quán:</span> {info['que_quan']}</p></div><div><p><span class="info-label">Ngạch:</span> {info['ngach_cong_chuc']}</p><p><span class="info-label">Chuyên môn:</span> {info['trinh_do_chuyen_mon']}</p><p><span class="info-label">Lý luận CT:</span> {info['ly_luan_chinh_tri']}</p><p><span class="info-label">Ngày vào Đảng:</span> {info['ngay_vao_dang']}</p></div></div></div>""", unsafe_allow_html=True)
                
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

# --- MODULE 4: NHẬP LIỆU (ADMIN TỰ DO SỬA - NHÂN VIÊN TỰ SỬA MÌNH) ---
elif menu in ["➕ Cập nhật Hồ sơ cá nhân", "➕ Admin: Cập nhật Hồ sơ (Tất cả)"]:
    st.markdown("### 📝 TRUNG TÂM NHẬP LIỆU HỒ SƠ")
    
    # Chế độ chọn Mã CBCC
    if is_admin:
        kieu_nhap = st.radio("Chế độ:", ["Chỉnh sửa người có sẵn", "Thêm cán bộ mới tinh"], horizontal=True)
        if kieu_nhap == "Chỉnh sửa người có sẵn":
            ds_cbcc = (df_hoso['id'] + " - " + df_hoso['ho_ten']).tolist() if not df_hoso.empty else []
            idx_def = 0
            if st.session_state["edit_target_id"] and ds_cbcc:
                for i, val in enumerate(ds_cbcc):
                    if val.startswith(st.session_state["edit_target_id"]):
                        idx_def = i; break
            chon_cb = st.selectbox("Lựa chọn Cán bộ cần sửa:", ds_cbcc, index=idx_def) if ds_cbcc else ""
            target_id = chon_cb.split(" - ")[0] if chon_cb else ""
        else:
            target_id = st.text_input("Nhập Mã CBCC mới (VD: CV999):").strip().upper()
    else:
        target_id = st.session_state["ma_cbcc"]
        st.info(f"Đang cập nhật hồ sơ cho mã của bạn: **{target_id}**")
    
    # Lấy data cũ để điền sẵn vào Form
    ex_data = {}
    if target_id and not df_hoso.empty:
        match = df_hoso[df_hoso['id'] == target_id]
        if not match.empty: ex_data = match.iloc[0].fillna("").to_dict()

    ds_gt = ["Nam", "Nữ"]; ds_dv = ["Lãnh đạo Ban", "Văn phòng Ban", "Phòng LLCT - LSĐ", "Phòng Tuyên truyền, Báo chí", "Phòng Khoa giáo", "Phòng Dân vận", "Phòng Đoàn thể"]
    ds_cv = ["Trưởng Ban", "Phó Trưởng Ban", "Chánh Văn phòng", "Phó Chánh Văn phòng", "Trưởng phòng", "Phó Trưởng phòng", "Chuyên viên", "Khác"]
    ds_ll = ["Chưa qua đào tạo", "Sơ cấp", "Trung cấp", "Cao cấp", "Cử nhân"]

    tab_chinh, tab_congtac, tab_luong, tab_khenthuong = st.tabs(["👤 Hồ sơ chính", "🏢 Lịch sử công tác", "💰 Diễn biến lương", "🏆 Khen thưởng / Kỷ luật"])
    
    with tab_chinh:
        with st.form("form_ho_so", clear_on_submit=False):
            c1, c2, c3 = st.columns(3)
            with c1:
                ho_ten = st.text_input("Họ và tên*", value=ex_data.get("ho_ten", ""))
                ngay_sinh = st.text_input("Ngày sinh (DD/MM/YYYY)", value=ex_data.get("ngay_sinh", ""))
                gioi_tinh = st.selectbox("Giới tính", ds_gt, index=get_idx(ds_gt, ex_data.get("gioi_tinh", "Nam")))
            with c2:
                que_quan = st.text_input("Quê quán", value=ex_data.get("que_quan", ""))
                don_vi = st.selectbox("Đơn vị công tác*", ds_dv, index=get_idx(ds_dv, ex_data.get("don_vi", "Lãnh đạo Ban")))
                chuc_vu = st.selectbox("Chức vụ", ds_cv, index=get_idx(ds_cv, ex_data.get("chuc_vu", "Chuyên viên")))
            with c3:
                ngach = st.text_input("Ngạch công chức", value=ex_data.get("ngach_cong_chuc", ""))
                chuyen_mon = st.text_input("Trình độ chuyên môn", value=ex_data.get("trinh_do_chuyen_mon", ""))
                ly_luan = st.selectbox("Lý luận chính trị", ds_ll, index=get_idx(ds_ll, ex_data.get("ly_luan_chinh_tri", "Chưa qua đào tạo")))
                ngay_vao_dang = st.text_input("Ngày vào Đảng", value=ex_data.get("ngay_vao_dang", ""))

            if st.form_submit_button("💾 LƯU HỒ SƠ CHÍNH", use_container_width=True):
                if not target_id or not ho_ten: st.error("⚠️ Phải có Mã CBCC và Họ tên!")
                else:
                    data = {"id": target_id, "ho_ten": ho_ten.title(), "ngay_sinh": ngay_sinh, "gioi_tinh": gioi_tinh, "que_quan": que_quan, "don_vi": don_vi, "chuc_vu": chuc_vu, "ngach_cong_chuc": ngach, "trinh_do_chuyen_mon": chuyen_mon, "ly_luan_chinh_tri": ly_luan, "ngay_vao_dang": ngay_vao_dang}
                    supabase.table("ho_so_cbcc").upsert(data).execute()
                    st.success("✅ Đã cập nhật Hồ sơ chính!"); st.cache_data.clear(); st.rerun()

    with tab_congtac:
        with st.form("form_cong_tac"):
            c1, c2 = st.columns(2); tu_ngay = c1.text_input("Từ ngày"); den_ngay = c2.text_input("Đến ngày")
            vi_tri = st.text_input("Vị trí / Chức danh"); don_vi_ct = st.text_input("Đơn vị công tác"); qd_ct = st.text_input("Quyết định số")
            if st.form_submit_button("💾 THÊM MỚI LỊCH SỬ CÔNG TÁC", use_container_width=True):
                supabase.table("lich_su_cong_tac").insert({"ma_cbcc": target_id, "tu_ngay": tu_ngay, "den_ngay": den_ngay, "vi_tri": vi_tri, "don_vi": don_vi_ct, "quyet_dinh_so": qd_ct}).execute()
                st.success("✅ Đã thêm!"); st.rerun()
        st.markdown("#### 🔧 Quản lý Dữ liệu đã nhập (Xóa nếu sai)")
        df_ct = pd.DataFrame(supabase.table("lich_su_cong_tac").select("*").eq("ma_cbcc", target_id).execute().data)
        if not df_ct.empty:
            st.dataframe(df_ct.drop(columns=['ma_cbcc']), hide_index=True)
            del_ct = st.selectbox("Chọn ID bản ghi cần xóa (Lịch sử CT):", ["-- Chọn --"] + df_ct['id'].astype(str).tolist())
            if st.button("🗑️ XÓA BẢN GHI NÀY", key="del1"):
                if del_ct != "-- Chọn --": supabase.table("lich_su_cong_tac").delete().eq("id", del_ct).execute(); st.success("Đã xóa!"); st.rerun()
        else: st.info("Chưa có dữ liệu")

    with tab_luong:
        with st.form("form_luong"):
            ngay_qd_l = st.text_input("Ngày quyết định"); c1, c2 = st.columns(2)
            bac_luong = c1.text_input("Bậc lương"); he_so = c2.text_input("Hệ số"); qd_l = st.text_input("Quyết định số")
            if st.form_submit_button("💾 THÊM MỚI DIỄN BIẾN LƯƠNG", use_container_width=True):
                supabase.table("dien_bien_luong").insert({"ma_cbcc": target_id, "ngay_quyet_dinh": ngay_qd_l, "bac_luong": bac_luong, "he_so": he_so, "quyet_dinh_so": qd_l}).execute()
                st.success("✅ Đã thêm!"); st.rerun()
        st.markdown("#### 🔧 Quản lý Dữ liệu đã nhập")
        df_l = pd.DataFrame(supabase.table("dien_bien_luong").select("*").eq("ma_cbcc", target_id).execute().data)
        if not df_l.empty:
            st.dataframe(df_l.drop(columns=['ma_cbcc']), hide_index=True)
            del_l = st.selectbox("Chọn ID bản ghi cần xóa (Lương):", ["-- Chọn --"] + df_l['id'].astype(str).tolist())
            if st.button("🗑️ XÓA BẢN GHI NÀY", key="del2"):
                if del_l != "-- Chọn --": supabase.table("dien_bien_luong").delete().eq("id", del_l).execute(); st.success("Đã xóa!"); st.rerun()
        else: st.info("Chưa có dữ liệu")

    with tab_khenthuong:
        with st.form("form_ktkl"):
            ngay_qd_kt = st.text_input("Ngày quyết định"); loai = st.selectbox("Loại", ["Khen thưởng", "Kỷ luật"])
            noi_dung = st.text_area("Nội dung"); qd_kt = st.text_input("Quyết định số")
            if st.form_submit_button("💾 THÊM MỚI KHEN THƯỞNG / KỶ LUẬT", use_container_width=True):
                supabase.table("khen_thuong_ky_luat").insert({"ma_cbcc": target_id, "ngay_quyet_dinh": ngay_qd_kt, "loai": loai, "noi_dung": noi_dung, "quyet_dinh_so": qd_kt}).execute()
                st.success(f"✅ Đã thêm!"); st.rerun()
        st.markdown("#### 🔧 Quản lý Dữ liệu đã nhập")
        df_kt = pd.DataFrame(supabase.table("khen_thuong_ky_luat").select("*").eq("ma_cbcc", target_id).execute().data)
        if not df_kt.empty:
            st.dataframe(df_kt.drop(columns=['ma_cbcc']), hide_index=True)
            del_kt = st.selectbox("Chọn ID bản ghi cần xóa (KT/KL):", ["-- Chọn --"] + df_kt['id'].astype(str).tolist())
            if st.button("🗑️ XÓA BẢN GHI NÀY", key="del3"):
                if del_kt != "-- Chọn --": supabase.table("khen_thuong_ky_luat").delete().eq("id", del_kt).execute(); st.success("Đã xóa!"); st.rerun()
        else: st.info("Chưa có dữ liệu")
