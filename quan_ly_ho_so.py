import streamlit as st
import pandas as pd
from supabase import create_client, Client
import plotly.express as px
import base64
import os

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
# HÀM XỬ LÝ LOGO (TỰ ĐỘNG LẤY ẢNH LOCAL HOẶC WEB)
# ==========================================
def get_logo_html(height="80px"):
    # Tìm file logo.png trong thư mục, nếu không có thì lấy link mạng
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            return f'<img src="data:image/png;base64,{data}" style="height: {height};">'
    else:
        # Link Quốc huy dự phòng
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Qu%E1%BB%91c_huy_Vi%E1%BB%87t_Nam.svg/250px-Qu%E1%BB%91c_huy_Vi%E1%BB%87t_Nam.svg.png"
        return f'<img src="{url}" style="height: {height};">'

# ==========================================
# DANH MỤC CHUẨN HÓA
# ==========================================
DS_DON_VI = [
    "Lãnh đạo Ban", "Văn phòng Ban", "Phòng Lý luận chính trị, Lịch sử Đảng", 
    "Phòng Tuyên truyền, Báo chí - Xuất bản", "Phòng Khoa giáo, Văn hóa - Văn nghệ", 
    "Phòng Dân vận các cơ quan Nhà nước, dân tộc và tôn giáo", "Phòng Đoàn thể và các Hội"
]
DS_CHUC_VU = [
    "Trưởng Ban", "Phó Trưởng ban Thường trực", "Phó Trưởng Ban", "Chánh Văn phòng", 
    "Phó Chánh Văn phòng", "Trưởng phòng", "Phó Trưởng phòng", "Chuyên viên chính", 
    "Chuyên viên", "Văn thư viên", "Văn thư viên Trung cấp", "Kế toán viên", 
    "Kế toán viên trung cấp", "Nhân viên lái xe", "Nhân viên phục vụ"
]
DS_GIOI_TINH = ["Nam", "Nữ"]
DS_LY_LUAN = ["Chưa qua đào tạo", "Sơ cấp", "Trung cấp", "Cao cấp", "Cử nhân"]

# ==========================================
# CSS LÀM ĐẸP (NHUỘM XANH NAVY)
# ==========================================
st.markdown("""
<style>
    div[data-testid="stButton"] > button,
    div[data-testid="stFormSubmitButton"] > button,
    div[data-testid="stDownloadButton"] > button {
        background-color: #004B87 !important;
        color: white !important;
        border: 1px solid #004B87 !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        transition: all 0.3s ease;
    }
    div[data-testid="stButton"] > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover,
    div[data-testid="stDownloadButton"] > button:hover {
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
    
    /* Thiết kế Header chứa Logo mới */
    .header-box { 
        background-color: #004B87; 
        padding: 15px 30px; 
        border-radius: 10px; 
        margin-bottom: 25px; 
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        color: white; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .header-content { display: flex; flex-direction: column; align-items: flex-start;}
    .header-box h1 { margin: 0; font-size: 24px; text-transform: uppercase; font-weight: 900; line-height: 1.2;}
    .header-box p { margin: 0; font-size: 14px; opacity: 0.9;}
    
    div[data-testid="stForm"] { background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 20px;}
    .metric-container { background-color: #f8f9fa; border-left: 5px solid #C8102E; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .metric-title { font-size: 14px; font-weight: bold; color: #6c757d; text-transform: uppercase; margin-bottom: 5px;}
    .metric-value { font-size: 32px; font-weight: 900; color: #004B87; line-height: 1;}
</style>
""", unsafe_allow_html=True)

# Khởi tạo Session State
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "ma_cbcc" not in st.session_state: st.session_state["ma_cbcc"] = ""
if "ho_ten" not in st.session_state: st.session_state["ho_ten"] = ""
if "role" not in st.session_state: st.session_state["role"] = "User"
if "edit_target_id" not in st.session_state: st.session_state["edit_target_id"] = ""
if "menu_selection" not in st.session_state: st.session_state["menu_selection"] = ""

# ==========================================
# MÀN HÌNH XÁC THỰC
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown(f"""
    <div class="header-box">
        <div>{get_logo_html("70px")}</div>
        <div class="header-content">
            <h1>HỆ THỐNG QUẢN LÝ HỒ SƠ</h1>
            <p>BAN TUYÊN GIÁO VÀ DÂN VẬN TỈNH ỦY TUYÊN QUANG</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
                                    if user['trang_thai'] == 'Chờ duyệt': st.warning("⏳ Tài khoản đang chờ Admin phê duyệt!")
                                    else:
                                        st.session_state["logged_in"] = True; st.session_state["ma_cbcc"] = user['ma_cbcc']
                                        st.session_state["ho_ten"] = user['ho_ten']; st.session_state["role"] = user['phan_quyen']
                                        st.session_state["menu_selection"] = "📊 Dashboard" if user['phan_quyen'] == 'Admin' else "🔍 Hồ sơ của tôi"
                                        st.rerun()
                                else: st.error("❌ Sai mật khẩu!")
                            else: st.error("❌ Không tìm thấy Mã CBCC này!")
                        except Exception as e: st.error(f"Lỗi kết nối: {e}")
        with tab_register:
            with st.form("register_form"):
                reg_ma = st.text_input("Mã CBCC (Tên đăng nhập)*").strip().upper()
                reg_name = st.text_input("Họ và tên*")
                reg_cv = st.selectbox("Chức vụ", DS_CHUC_VU)
                reg_dv = st.selectbox("Đơn vị công tác", DS_DON_VI)
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
# Chèn Logo lên thanh Sidebar
st.sidebar.markdown(f"<div style='text-align: center; margin-bottom: 20px;'>{get_logo_html('100px')}</div>", unsafe_allow_html=True)

st.sidebar.markdown(f"👋 Xin chào, **{st.session_state['ho_ten']}**")
st.sidebar.markdown(f"🔑 Quyền: **{st.session_state['role']}**")

if st.sidebar.button("🚪 Đăng xuất", use_container_width=True):
    for key in ["logged_in", "ma_cbcc", "ho_ten", "role", "menu_selection"]: st.session_state[key] = None
    st.rerun()

is_admin = st.session_state["role"] == "Admin"
if is_admin:
    menu_options = ["📊 Dashboard", "🛡️ Admin: Duyệt Tài khoản", "🔍 Tra cứu & Xem Hồ sơ", "➕ Admin: Cập nhật Hồ sơ (Tất cả)"]
else:
    menu_options = ["🔍 Hồ sơ của tôi", "➕ Cập nhật Hồ sơ cá nhân"]

if st.session_state["menu_selection"] not in menu_options:
    st.session_state["menu_selection"] = menu_options[0]

current_idx = menu_options.index(st.session_state["menu_selection"])
menu = st.sidebar.radio("📌 CHỨC NĂNG:", menu_options, index=current_idx)

if menu != st.session_state["menu_selection"]:
    st.session_state["menu_selection"] = menu
    st.rerun()

st.sidebar.write("---")

# Header chính có gắn Logo
st.markdown(f"""
<div class="header-box">
    <div>{get_logo_html("60px")}</div>
    <div class="header-content">
        <h1>QUẢN LÝ HỒ SƠ CÁN BỘ</h1>
        <p>BAN TUYÊN GIÁO VÀ DÂN VẬN TỈNH ỦY TUYÊN QUANG</p>
    </div>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_profiles():
    try: return pd.DataFrame(supabase.table("ho_so_cbcc").select("*").execute().data)
    except: return pd.DataFrame()

df_hoso = load_profiles()

def get_idx(lst, val):
    try: return lst.index(val)
    except: return 0

# HÀM TẠO FILE XUẤT HTML BẢN IN ĐẸP
def create_html_export(info, df_ct, df_l, df_kt):
    tbl_ct = df_ct.rename(columns={'tu_ngay':'Từ ngày', 'den_ngay':'Đến ngày', 'vi_tri':'Vị trí', 'don_vi':'Đơn vị', 'quyet_dinh_so':'Quyết định số'}).drop(columns=['id', 'ma_cbcc'], errors='ignore').to_html(index=False, border=1) if not df_ct.empty else "<p>Chưa có dữ liệu.</p>"
    tbl_l = df_l.rename(columns={'ngay_quyet_dinh':'Ngày QĐ', 'bac_luong':'Bậc lương', 'he_so':'Hệ số', 'quyet_dinh_so':'Quyết định số'}).drop(columns=['id', 'ma_cbcc'], errors='ignore').to_html(index=False, border=1) if not df_l.empty else "<p>Chưa có dữ liệu.</p>"
    tbl_kt = df_kt.rename(columns={'ngay_quyet_dinh':'Ngày QĐ', 'loai':'Loại', 'noi_dung':'Nội dung', 'quyet_dinh_so':'Quyết định số'}).drop(columns=['id', 'ma_cbcc'], errors='ignore').to_html(index=False, border=1) if not df_kt.empty else "<p>Chưa có dữ liệu.</p>"
    
    html = f"""
    <html><head><meta charset="utf-8"><title>Hồ sơ {info['ho_ten']}</title>
    <style>
        body {{ font-family: 'Times New Roman', serif; line-height: 1.6; padding: 40px; max-width: 800px; margin: auto; color: black; font-size: 16px;}}
        h2 {{ text-align: center; margin-bottom: 5px; font-size: 22px; text-transform: uppercase;}}
        h3 {{ text-align: center; margin-top: 0; font-weight: normal; font-size: 18px; margin-bottom: 30px;}}
        h4 {{ color: #000; border-bottom: 1px solid #000; padding-bottom: 5px; text-transform: uppercase; margin-top:30px;}}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 20px; }}
        th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style></head><body>
        <h2>SƠ YẾU LÝ LỊCH CÁN BỘ, CÔNG CHỨC</h2>
        <h3>Đơn vị: {info.get('don_vi', '')}</h3>
        <h4>I. THÔNG TIN CHUNG</h4>
        <p><b>1. Họ và tên:</b> <span style="text-transform: uppercase;">{info['ho_ten']}</span></p>
        <p><b>2. Mã CBCC:</b> {info['id']}</p>
        <p><b>3. Ngày sinh:</b> {info.get('ngay_sinh', '')}</p>
        <p><b>4. Giới tính:</b> {info.get('gioi_tinh', '')}</p>
        <p><b>5. Quê quán:</b> {info.get('que_quan', '')}</p>
        <p><b>6. Chức vụ:</b> {info.get('chuc_vu', '')}</p>
        <p><b>7. Ngạch công chức:</b> {info.get('ngach_cong_chuc', '')}</p>
        <p><b>8. Trình độ chuyên môn:</b> {info.get('trinh_do_chuyen_mon', '')}</p>
        <p><b>9. Lý luận chính trị:</b> {info.get('ly_luan_chinh_tri', '')}</p>
        <p><b>10. Ngày vào Đảng:</b> Kết nạp: {info.get('ngay_vao_dang', '')} | Chính thức: {info.get('ngay_chinh_thuc', '')}</p>
        <h4>II. LỊCH SỬ CÔNG TÁC</h4>{tbl_ct}
        <h4>III. DIỄN BIẾN LƯƠNG</h4>{tbl_l}
        <h4>IV. KHEN THƯỞNG / KỶ LUẬT</h4>{tbl_kt}
    </body></html>
    """
    return html.encode('utf-8')

# --- MODULE 1: DASHBOARD ---
if menu == "📊 Dashboard":
    st.markdown("### 📊 DASHBOARD THỐNG KÊ NHÂN SỰ (Dành riêng cho Admin)")
    if df_hoso.empty: st.info("Chưa có dữ liệu để thống kê.")
    else:
        df_hoso.fillna("Chưa xác định", inplace=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="metric-container"><div class="metric-title">👥 Tổng số Cán bộ</div><div class="metric-value">{len(df_hoso)}</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-container" style="border-color: #004B87;"><div class="metric-title">👨 Nam</div><div class="metric-value">{len(df_hoso[df_hoso["gioi_tinh"] == "Nam"])}</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-container" style="border-color: #ff9900;"><div class="metric-title">👩 Nữ</div><div class="metric-value">{len(df_hoso[df_hoso["gioi_tinh"] == "Nữ"])}</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="metric-container" style="border-color: #28a745;"><div class="metric-title">🎓 Thạc sĩ trở lên</div><div class="metric-value">{len(df_hoso[df_hoso["trinh_do_chuyen_mon"].str.contains("Thạc|Tiến", case=False, na=False)])}</div></div>', unsafe_allow_html=True)
        st.write("---")
        
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            df_gt = df_hoso['gioi_tinh'].value_counts().reset_index()
            df_gt.columns = ['Giới tính', 'Số lượng']
            fig_gt = px.pie(df_gt, values='Số lượng', names='Giới tính', hole=0.5, title='Cơ cấu Giới tính', color='Giới tính', color_discrete_map={'Nam':'#004B87', 'Nữ':'#ff9900'})
            fig_gt.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_gt, use_container_width=True)
            
            df_ng = df_hoso['ngach_cong_chuc'].value_counts().reset_index()
            df_ng.columns = ['Ngạch công chức', 'Số lượng']
            fig_ng = px.bar(df_ng, x='Ngạch công chức', y='Số lượng', title='Ngạch hiện hưởng', color_discrete_sequence=['#17a2b8'], text_auto=True)
            st.plotly_chart(fig_ng, use_container_width=True)

        with col_chart2:
            df_ll = df_hoso['ly_luan_chinh_tri'].value_counts().reset_index()
            df_ll.columns = ['Lý luận chính trị', 'Số lượng']
            fig_ll = px.bar(df_ll, x='Lý luận chính trị', y='Số lượng', title='Trình độ Lý luận Chính trị', color_discrete_sequence=['#C8102E'], text_auto=True)
            st.plotly_chart(fig_ll, use_container_width=True)
            
            df_cm = df_hoso['trinh_do_chuyen_mon'].value_counts().reset_index()
            df_cm.columns = ['Trình độ', 'Số lượng']
            fig_cm = px.bar(df_cm, y='Trình độ', x='Số lượng', orientation='h', title='Trình độ Chuyên môn', color_discrete_sequence=['#28a745'], text_auto=True)
            fig_cm.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_cm, use_container_width=True)

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
                        c_duyet, c_xoa = st.columns(2)
                        if c_duyet.button("✅ DUYỆT TÀI KHOẢN", key=f"duyet_{row['ma_cbcc']}", use_container_width=True):
                            supabase.table("tai_khoan").update({"trang_thai": "Hoạt động"}).eq("ma_cbcc", row['ma_cbcc']).execute()
                            st.success("Đã duyệt!"); st.rerun()
                        if c_xoa.button("❌ TỪ CHỐI & XÓA", key=f"xoa_cd_{row['ma_cbcc']}", use_container_width=True):
                            supabase.table("tai_khoan").delete().eq("ma_cbcc", row['ma_cbcc']).execute()
                            st.success("Đã xóa yêu cầu!"); st.rerun()
        with tab_hd:
            df_hoatdong = df_tk[df_tk['trang_thai'] == 'Hoạt động']
            st.dataframe(df_hoatdong[['ma_cbcc', 'ho_ten', 'chuc_vu', 'don_vi', 'phan_quyen']], hide_index=True)
            c_rs, c_del = st.columns(2)
            ds_hd = (df_hoatdong['ma_cbcc'] + " - " + df_hoatdong['ho_ten']).tolist()
            with c_rs:
                st.markdown("#### 🔄 Reset Mật khẩu")
                rs_ma = st.selectbox("Chọn tài khoản cần Reset về 'Chuyenvien@2026':", ds_hd)
                if st.button("⚠️ XÁC NHẬN RESET", use_container_width=True):
                    supabase.table("tai_khoan").update({"mat_khau": "Chuyenvien@2026"}).eq("ma_cbcc", rs_ma.split(" - ")[0]).execute()
                    st.success("✅ Đã reset thành công!")
            with c_del:
                st.markdown("#### ❌ Xóa Tài khoản")
                del_ma = st.selectbox("Chọn tài khoản cần XÓA VĨNH VIỄN:", ["-- Chọn --"] + ds_hd)
                if st.button("🗑️ XÁC NHẬN XÓA TÀI KHOẢN", use_container_width=True):
                    if del_ma != "-- Chọn --":
                        ma_xoa = del_ma.split(" - ")[0]
                        if ma_xoa == "ADMIN": st.error("⚠️ Không thể xóa tài khoản Admin gốc!")
                        else:
                            supabase.table("tai_khoan").delete().eq("ma_cbcc", ma_xoa).execute()
                            st.success(f"✅ Đã xóa vĩnh viễn tài khoản {ma_xoa}!"); st.rerun()

# --- MODULE 3: TRA CỨU / HỒ SƠ CỦA TÔI ---
elif menu in ["🔍 Tra cứu & Xem Hồ sơ", "🔍 Hồ sơ của tôi"]:
    st.markdown("### 🔍 THÔNG TIN HỒ SƠ")
    if df_hoso.empty: 
        st.warning("📭 Dữ liệu hệ thống đang trống.")
    else:
        ma_chon = ""
        if is_admin:
            tu_khoa = st.text_input("Nhập Tên hoặc Mã CBCC để tìm kiếm (Ấn Enter để xem):", placeholder="VD: CV01, Tuan...")
            if not tu_khoa.strip():
                st.info("👆 Vui lòng nhập từ khóa và ấn Enter để tìm kiếm hồ sơ.")
            else:
                df_ket_qua = df_hoso[df_hoso.apply(lambda row: row.astype(str).str.contains(tu_khoa.strip(), case=False).any(), axis=1)]
                if df_ket_qua.empty: st.warning("❌ Không tìm thấy cán bộ nào khớp với từ khóa!")
                else:
                    ds_hien_thi = df_ket_qua['ho_ten'] + " - " + df_ket_qua['chuc_vu'] + " (" + df_ket_qua['id'] + ")"
                    chon_nguoi = st.selectbox("👉 Chọn một đồng chí để xem Chi tiết:", ds_hien_thi.tolist())
                    if chon_nguoi: ma_chon = chon_nguoi.split("(")[-1].replace(")", "")
        else:
            ma_chon = st.session_state["ma_cbcc"]
            match = df_hoso[df_hoso['id'] == ma_chon]
            if match.empty:
                st.warning("❌ Bạn chưa tạo hồ sơ. Vui lòng sang tab Cập nhật để điền thông tin!")
                ma_chon = ""

        if ma_chon:
            info = df_hoso[df_hoso['id'] == ma_chon].iloc[0].fillna("")
            
            if is_admin or info['id'] == st.session_state["ma_cbcc"]:
                if st.button("✏️ Chỉnh sửa Hồ sơ này"):
                    st.session_state["edit_target_id"] = info['id']
                    st.session_state["menu_selection"] = "➕ Admin: Cập nhật Hồ sơ (Tất cả)" if is_admin else "➕ Cập nhật Hồ sơ cá nhân"
                    st.rerun()

            st.markdown(f"""<div class="profile-card"><div class="profile-name">{info['ho_ten']}</div><div class="profile-title">{info['chuc_vu']} | {info['don_vi']}</div><hr style="border-top: 1px dashed #dee2e6;"><div class="profile-info"><div><p><span class="info-label">Mã CBCC:</span> {info['id']}</p><p><span class="info-label">Ngày sinh:</span> {info['ngay_sinh']}</p><p><span class="info-label">Giới tính:</span> {info['gioi_tinh']}</p><p><span class="info-label">Quê quán:</span> {info['que_quan']}</p></div><div><p><span class="info-label">Ngạch:</span> {info['ngach_cong_chuc']}</p><p><span class="info-label">Chuyên môn:</span> {info['trinh_do_chuyen_mon']}</p><p><span class="info-label">Lý luận CT:</span> {info['ly_luan_chinh_tri']}</p><p><span class="info-label">Ngày vào Đảng:</span> Kết nạp: {info.get('ngay_vao_dang','')} | Chính thức: {info.get('ngay_chinh_thuc','')}</p></div></div></div>""", unsafe_allow_html=True)
            
            df_ct = pd.DataFrame(supabase.table("lich_su_cong_tac").select("tu_ngay, den_ngay, vi_tri, don_vi, quyet_dinh_so").eq("ma_cbcc", ma_chon).order("id").execute().data)
            df_l = pd.DataFrame(supabase.table("dien_bien_luong").select("ngay_quyet_dinh, bac_luong, he_so, quyet_dinh_so").eq("ma_cbcc", ma_chon).order("id").execute().data)
            df_kt = pd.DataFrame(supabase.table("khen_thuong_ky_luat").select("ngay_quyet_dinh, loai, noi_dung, quyet_dinh_so").eq("ma_cbcc", ma_chon).order("id").execute().data)
            
            st.write("---")
            html_data = create_html_export(info, df_ct, df_l, df_kt)
            st.download_button(
                label="📥 TẢI SƠ YẾU LÝ LỊCH (BẢN IN TỐT)",
                data=html_data,
                file_name=f"So_yeu_ly_lich_{info['ho_ten'].replace(' ', '_')}.html",
                mime="text/html",
                type="primary",
                use_container_width=True
            )
            st.write("---")

            st.markdown("#### 📑 CÁC THÔNG TIN LIÊN QUAN")
            t_ct, t_l, t_kt = st.tabs(["🏢 Lịch sử công tác", "💰 Diễn biến lương", "🏆 Khen thưởng & Kỷ luật"])
            with t_ct:
                if not df_ct.empty: st.table(df_ct.rename(columns={'tu_ngay':'Từ ngày', 'den_ngay':'Đến ngày', 'vi_tri':'Vị trí', 'don_vi':'Đơn vị', 'quyet_dinh_so':'Quyết định số'}))
                else: st.info("Chưa có dữ liệu.")
            with t_l:
                if not df_l.empty: st.table(df_l.rename(columns={'ngay_quyet_dinh':'Ngày QĐ', 'bac_luong':'Bậc lương', 'he_so':'Hệ số', 'quyet_dinh_so':'Quyết định số'}))
                else: st.info("Chưa có dữ liệu.")
            with t_kt:
                if not df_kt.empty: st.table(df_kt.rename(columns={'ngay_quyet_dinh':'Ngày QĐ', 'loai':'Loại', 'noi_dung':'Nội dung', 'quyet_dinh_so':'Quyết định số'}))
                else: st.info("Chưa có dữ liệu.")

# --- MODULE 4: NHẬP LIỆU & CHỈNH SỬA TRỰC TIẾP ---
elif menu in ["➕ Cập nhật Hồ sơ cá nhân", "➕ Admin: Cập nhật Hồ sơ (Tất cả)"]:
    st.markdown("### 📝 TRUNG TÂM NHẬP LIỆU HỒ SƠ")
    
    if is_admin:
        kieu_nhap = st.radio("Chế độ:", ["Chỉnh sửa người có sẵn", "Thêm cán bộ mới"], horizontal=True)
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
    
    ex_data = {}
    if target_id and not df_hoso.empty:
        match = df_hoso[df_hoso['id'] == target_id]
        if not match.empty: ex_data = match.iloc[0].fillna("").to_dict()

    tab_chinh, tab_congtac, tab_luong, tab_khenthuong = st.tabs(["👤 Hồ sơ chính", "🏢 Lịch sử công tác", "💰 Diễn biến lương", "🏆 Khen thưởng / Kỷ luật"])
    
    with tab_chinh:
        with st.form("form_ho_so", clear_on_submit=False):
            c1, c2, c3 = st.columns(3)
            with c1:
                ho_ten = st.text_input("Họ và tên*", value=ex_data.get("ho_ten", ""))
                ngay_sinh = st.text_input("Ngày sinh (DD/MM/YYYY)", value=ex_data.get("ngay_sinh", ""))
                gioi_tinh = st.selectbox("Giới tính", DS_GIOI_TINH, index=get_idx(DS_GIOI_TINH, ex_data.get("gioi_tinh", "Nam")))
            with c2:
                que_quan = st.text_input("Quê quán", value=ex_data.get("que_quan", ""))
                don_vi = st.selectbox("Đơn vị công tác*", DS_DON_VI, index=get_idx(DS_DON_VI, ex_data.get("don_vi", "Lãnh đạo Ban")))
                chuc_vu = st.selectbox("Chức vụ", DS_CHUC_VU, index=get_idx(DS_CHUC_VU, ex_data.get("chuc_vu", "Chuyên viên")))
            with c3:
                ngach = st.text_input("Ngạch công chức", value=ex_data.get("ngach_cong_chuc", ""))
                chuyen_mon = st.text_input("Trình độ chuyên môn", value=ex_data.get("trinh_do_chuyen_mon", ""))
                ly_luan = st.selectbox("Lý luận chính trị", DS_LY_LUAN, index=get_idx(DS_LY_LUAN, ex_data.get("ly_luan_chinh_tri", "Chưa qua đào tạo")))
                
                c3_1, c3_2 = st.columns(2)
                ngay_ket_nap = c3_1.text_input("Ngày kết nạp", value=ex_data.get("ngay_vao_dang", ""))
                ngay_chinh_thuc = c3_2.text_input("Ngày chính thức", value=ex_data.get("ngay_chinh_thuc", ""))

            if st.form_submit_button("💾 LƯU HỒ SƠ CHÍNH", use_container_width=True):
                if not target_id or not ho_ten: st.error("⚠️ Phải có Mã CBCC và Họ tên!")
                else:
                    data = {
                        "id": target_id, "ho_ten": ho_ten.title(), "ngay_sinh": ngay_sinh, 
                        "gioi_tinh": gioi_tinh, "que_quan": que_quan, "don_vi": don_vi, 
                        "chuc_vu": chuc_vu, "ngach_cong_chuc": ngach, "trinh_do_chuyen_mon": chuyen_mon, 
                        "ly_luan_chinh_tri": ly_luan, "ngay_vao_dang": ngay_ket_nap, "ngay_chinh_thuc": ngay_chinh_thuc
                    }
                    supabase.table("ho_so_cbcc").upsert(data).execute()
                    st.session_state["edit_target_id"] = ""
                    st.success("✅ Đã cập nhật Hồ sơ chính!"); st.cache_data.clear(); st.rerun()

    with tab_congtac:
        with st.form("form_cong_tac"):
            c1, c2 = st.columns(2); tu_ngay = c1.text_input("Từ ngày"); den_ngay = c2.text_input("Đến ngày")
            vi_tri = st.text_input("Vị trí / Chức danh"); don_vi_ct = st.text_input("Đơn vị công tác"); qd_ct = st.text_input("Quyết định số")
            if st.form_submit_button("💾 THÊM MỚI LỊCH SỬ CÔNG TÁC", use_container_width=True):
                supabase.table("lich_su_cong_tac").insert({"ma_cbcc": target_id, "tu_ngay": tu_ngay, "den_ngay": den_ngay, "vi_tri": vi_tri, "don_vi": don_vi_ct, "quyet_dinh_so": qd_ct}).execute()
                st.success("✅ Đã thêm!"); st.rerun()
        
        st.markdown("#### 🔧 Nhấp đúp vào bảng để chỉnh sửa Dữ liệu cũ")
        df_ct = pd.DataFrame(supabase.table("lich_su_cong_tac").select("*").eq("ma_cbcc", target_id).order("id").execute().data)
        if not df_ct.empty:
            edited_ct = st.data_editor(df_ct.drop(columns=['ma_cbcc']), hide_index=True, use_container_width=True, disabled=["id"])
            col_save1, col_del1 = st.columns([3, 1])
            if col_save1.button("💾 LƯU CẬP NHẬT BẢNG CÔNG TÁC", use_container_width=True):
                update_data = edited_ct.copy()
                update_data['ma_cbcc'] = target_id
                supabase.table("lich_su_cong_tac").upsert(update_data.fillna("").to_dict(orient="records")).execute()
                st.success("✅ Đã cập nhật chỉnh sửa!"); st.rerun()
            del_ct = col_del1.selectbox("Hoặc chọn ID để xóa:", ["-- Chọn --"] + df_ct['id'].astype(str).tolist(), label_visibility="collapsed")
            if col_del1.button("🗑️ XÓA", key="btn_del1", use_container_width=True) and del_ct != "-- Chọn --":
                supabase.table("lich_su_cong_tac").delete().eq("id", del_ct).execute(); st.rerun()

    with tab_luong:
        with st.form("form_luong"):
            ngay_qd_l = st.text_input("Ngày quyết định"); c1, c2 = st.columns(2)
            bac_luong = c1.text_input("Bậc lương"); he_so = c2.text_input("Hệ số"); qd_l = st.text_input("Quyết định số")
            if st.form_submit_button("💾 THÊM MỚI DIỄN BIẾN LƯƠNG", use_container_width=True):
                supabase.table("dien_bien_luong").insert({"ma_cbcc": target_id, "ngay_quyet_dinh": ngay_qd_l, "bac_luong": bac_luong, "he_so": he_so, "quyet_dinh_so": qd_l}).execute()
                st.success("✅ Đã thêm!"); st.rerun()
        
        st.markdown("#### 🔧 Nhấp đúp vào bảng để chỉnh sửa Dữ liệu cũ")
        df_l = pd.DataFrame(supabase.table("dien_bien_luong").select("*").eq("ma_cbcc", target_id).order("id").execute().data)
        if not df_l.empty:
            edited_l = st.data_editor(df_l.drop(columns=['ma_cbcc']), hide_index=True, use_container_width=True, disabled=["id"])
            col_save2, col_del2 = st.columns([3, 1])
            if col_save2.button("💾 LƯU CẬP NHẬT BẢNG LƯƠNG", use_container_width=True):
                update_data = edited_l.copy()
                update_data['ma_cbcc'] = target_id
                supabase.table("dien_bien_luong").upsert(update_data.fillna("").to_dict(orient="records")).execute()
                st.success("✅ Đã cập nhật chỉnh sửa!"); st.rerun()
            del_l = col_del2.selectbox("Hoặc chọn ID để xóa:", ["-- Chọn --"] + df_l['id'].astype(str).tolist(), label_visibility="collapsed")
            if col_del2.button("🗑️ XÓA", key="btn_del2", use_container_width=True) and del_l != "-- Chọn --":
                supabase.table("dien_bien_luong").delete().eq("id", del_l).execute(); st.rerun()

    with tab_khenthuong:
        with st.form("form_ktkl"):
            ngay_qd_kt = st.text_input("Ngày quyết định"); loai = st.selectbox("Loại", ["Khen thưởng", "Kỷ luật"])
            noi_dung = st.text_area("Nội dung"); qd_kt = st.text_input("Quyết định số")
            if st.form_submit_button("💾 THÊM MỚI KHEN THƯỞNG / KỶ LUẬT", use_container_width=True):
                supabase.table("khen_thuong_ky_luat").insert({"ma_cbcc": target_id, "ngay_quyet_dinh": ngay_qd_kt, "loai": loai, "noi_dung": noi_dung, "quyet_dinh_so": qd_kt}).execute()
                st.success(f"✅ Đã thêm!"); st.rerun()
        
        st.markdown("#### 🔧 Nhấp đúp vào bảng để chỉnh sửa Dữ liệu cũ")
        df_kt = pd.DataFrame(supabase.table("khen_thuong_ky_luat").select("*").eq("ma_cbcc", target_id).order("id").execute().data)
        if not df_kt.empty:
            edited_kt = st.data_editor(df_kt.drop(columns=['ma_cbcc']), hide_index=True, use_container_width=True, disabled=["id"])
            col_save3, col_del3 = st.columns([3, 1])
            if col_save3.button("💾 LƯU CẬP NHẬT BẢNG KHEN THƯỞNG", use_container_width=True):
                update_data = edited_kt.copy()
                update_data['ma_cbcc'] = target_id
                supabase.table("khen_thuong_ky_luat").upsert(update_data.fillna("").to_dict(orient="records")).execute()
                st.success("✅ Đã cập nhật chỉnh sửa!"); st.rerun()
            del_kt = col_del3.selectbox("Hoặc chọn ID để xóa:", ["-- Chọn --"] + df_kt['id'].astype(str).tolist(), label_visibility="collapsed")
            if col_del3.button("🗑️ XÓA", key="btn_del3", use_container_width=True) and del_kt != "-- Chọn --":
                supabase.table("khen_thuong_ky_luat").delete().eq("id", del_kt).execute(); st.rerun()
