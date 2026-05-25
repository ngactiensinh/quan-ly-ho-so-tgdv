"""
HỆ THỐNG QUẢN LÝ HỒ SƠ CÁN BỘ, CÔNG CHỨC - PHIÊN BẢN V6.4 (PRO MAX)
Tối ưu: Giao diện Mobile, Biểu đồ ngang Plotly, Bảng chỉ tiêu HTML, Lọc dữ liệu rác.
"""

import streamlit as st
import pandas as pd
from supabase import create_client, Client
import plotly.express as px
import plotly.graph_objects as go
import base64
import os
from datetime import datetime
import re

# ==========================================
# 1. CẤU HÌNH TRANG (BẮT BUỘC Ở ĐẦU)
# ==========================================
st.set_page_config(
    page_title="Hồ sơ CBCC - Ban Tuyên giáo & Dân vận Tuyên Quang",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. CSS PHONG CÁCH CHÍNH TRỊ & FIX MOBILE
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700;900&family=Source+Sans+3:wght@400;500;600;700&display=swap');

    :root {
        --red-primary: #C8102E; --red-dark: #A00C23; --red-light: #E8203F;
        --gold: #D4AF37; --gold-light: #F0D060; --navy: #0A1628;
        --navy-mid: #1A2E4A; --navy-light: #2A4A70; --cream: #FDF8F0;
        --off-white: #F5F1E8; --text-dark: #1A1A2E; --text-mid: #3D3D5C;
        --text-light: #6B7280;
        --shadow-sm: 0 2px 8px rgba(0,0,0,0.08); --shadow-md: 0 4px 20px rgba(0,0,0,0.12); --shadow-lg: 0 8px 40px rgba(0,0,0,0.16);
    }
    html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; color: var(--text-dark); }
    .stApp { background: linear-gradient(160deg, #f8f4ef 0%, #ede8e0 50%, #f5f0e8 100%); }

    /* ---- FIXED MOBILE MENU BUTTON ---- */
    [data-testid="collapsedControl"] {
        position: fixed !important;
        top: 15px !important;
        left: 15px !important;
        z-index: 999999 !important;
        background-color: #0A1628 !important; /* Navy */
        width: 45px !important; height: 45px !important;
        border-radius: 8px !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        visibility: visible !important;
    }
    [data-testid="collapsedControl"] svg {
        fill: #D4AF37 !important; /* Gold */
        width: 25px !important; height: 25px !important;
    }

    /* ---- SIDEBAR ---- */
    [data-testid="stSidebar"] { background: linear-gradient(180deg, var(--navy) 0%, var(--navy-mid) 60%, #0D1E35 100%) !important; border-right: 3px solid var(--gold) !important; z-index: 9999999 !important; }
    [data-testid="stSidebar"] * { color: #e8dfc8 !important; }
    [data-testid="stSidebar"] .stRadio label { color: #c8bfa8 !important; padding: 10px 14px; border-radius: 6px; display: block; transition: all 0.2s; font-weight: 500; font-size: 14px; border-left: 3px solid transparent; }
    [data-testid="stSidebar"] .stRadio label:hover { background: rgba(212,175,55,0.12) !important; border-left-color: var(--gold) !important; color: var(--gold-light) !important; }
    [data-testid="stSidebar"] [aria-checked="true"] + label, [data-testid="stSidebar"] .stRadio [data-checked="true"] label { background: rgba(200,16,46,0.25) !important; border-left-color: var(--red-primary) !important; color: #fff !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(212,175,55,0.25) !important; }

    /* ---- HEADER CHÍNH ---- */
    .gov-header { background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 40%, var(--red-dark) 100%); border-bottom: 4px solid var(--gold); padding: 20px 32px; border-radius: 12px; margin-bottom: 28px; display: flex; align-items: center; gap: 24px; position: relative; overflow: hidden; box-shadow: var(--shadow-lg); padding-left: 70px !important; }
    .gov-header::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: repeating-linear-gradient(45deg, transparent, transparent 40px, rgba(212,175,55,0.03) 40px, rgba(212,175,55,0.03) 41px); }
    .gov-header-text h1 { font-family: 'Merriweather', serif; font-size: 20px; font-weight: 900; color: #fff; margin: 0 0 4px 0; letter-spacing: 1.5px; text-transform: uppercase; text-shadow: 0 2px 8px rgba(0,0,0,0.3); }
    .gov-header-text .subtitle { font-size: 13px; color: var(--gold-light); margin: 0; letter-spacing: 0.5px; opacity: 0.9; }
    .gold-bar { width: 3px; height: 60px; background: linear-gradient(180deg, var(--gold-light), var(--gold), transparent); border-radius: 2px; flex-shrink: 0; }

    /* ---- METRIC CARDS ---- */
    .metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }
    .metric-card { background: #fff; border-radius: 10px; padding: 20px 22px; border-top: 4px solid var(--red-primary); box-shadow: var(--shadow-sm); position: relative; overflow: hidden; transition: transform 0.2s, box-shadow 0.2s; }
    .metric-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
    .metric-card.gold { border-top-color: var(--gold); }
    .metric-card.navy { border-top-color: var(--navy); }
    .metric-card.green { border-top-color: #2E7D32; }
    .metric-card::after { content: ''; position: absolute; bottom: -20px; right: -20px; width: 80px; height: 80px; border-radius: 50%; background: rgba(200,16,46,0.04); }
    .metric-card .m-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--text-light); margin-bottom: 8px; }
    .metric-card .m-value { font-family: 'Merriweather', serif; font-size: 38px; font-weight: 900; color: var(--red-primary); line-height: 1; }
    .metric-card.gold .m-value { color: #B8860B; }
    .metric-card.navy .m-value { color: var(--navy-mid); }
    .metric-card.green .m-value { color: #2E7D32; }
    .metric-card .m-sub { font-size: 12px; color: var(--text-light); margin-top: 5px; }

    /* ---- PROFILE CARD ---- */
    .profile-card { background: #fff; border-radius: 12px; padding: 28px 32px; margin: 20px 0; box-shadow: var(--shadow-md); border-left: 6px solid var(--red-primary); position: relative; overflow: hidden; }
    .profile-card::before { content: ''; position: absolute; top: 0; right: 0; width: 120px; height: 120px; background: linear-gradient(135deg, rgba(200,16,46,0.04), rgba(212,175,55,0.06)); border-radius: 0 0 0 120px; }
    .profile-badge { display: inline-block; background: var(--red-primary); color: #fff; font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; padding: 3px 10px; border-radius: 12px; margin-bottom: 10px; }
    .profile-name { font-family: 'Merriweather', serif; font-size: 24px; font-weight: 900; color: var(--navy); letter-spacing: 0.5px; margin-bottom: 4px; text-transform: uppercase; }
    .profile-title { color: var(--red-primary); font-size: 15px; font-weight: 600; margin-bottom: 18px; }
    .profile-divider { border: none; border-top: 1px dashed rgba(200,16,46,0.2); margin: 16px 0; }
    .profile-info-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; }
    .info-item { display: flex; flex-direction: column; gap: 2px; background: #FAF7F2; padding: 8px 12px; border-radius: 6px; border: 1px solid #EFEAE2; }
    .info-item .lbl { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; color: var(--text-light); }
    .info-item .val { font-size: 14px; font-weight: 600; color: var(--text-dark); }

    /* ---- FORMS & BUTTONS ---- */
    div[data-testid="stForm"] { background: #fff; border: 1px solid rgba(212,175,55,0.25); border-top: 3px solid var(--gold); border-radius: 10px; padding: 24px !important; box-shadow: var(--shadow-sm); }
    div[data-testid="stButton"] > button, div[data-testid="stFormSubmitButton"] > button, div[data-testid="stDownloadButton"] > button { background: linear-gradient(135deg, var(--red-primary), var(--red-dark)) !important; color: #fff !important; border: none !important; font-weight: 700 !important; font-size: 13px !important; letter-spacing: 0.8px !important; text-transform: uppercase !important; padding: 10px 20px !important; border-radius: 6px !important; box-shadow: 0 3px 12px rgba(200,16,46,0.3) !important; transition: all 0.25s ease !important; }
    div[data-testid="stButton"] > button:hover { background: linear-gradient(135deg, var(--red-light), var(--red-primary)) !important; transform: translateY(-1px) !important; }

    /* Ẩn các thành phần thừa */
    #MainMenu, footer { visibility: hidden !important; }
    header { background-color: transparent !important; }
    .block-container { padding-top: 24px !important; padding-bottom: 40px !important; }

    /* ---- MOBILE RESPONSIVE ---- */
    @media screen and (max-width: 768px) {
        header[data-testid="stHeader"] { visibility: visible !important; background-color: #0A1628 !important; border-bottom: 2px solid #D4AF37 !important; }
        header[data-testid="stHeader"] svg { fill: #D4AF37 !important; width: 25px !important; height: 25px !important; }
        .gov-header { margin-top: 3.5rem !important; flex-direction: column !important; text-align: center !important; padding: 15px !important; padding-left: 15px !important; gap: 10px !important; }
        .gold-bar { width: 80px !important; height: 3px !important; background: linear-gradient(90deg, #F0D060, #D4AF37, transparent) !important; margin: 0 auto !important; }
        .metric-grid { grid-template-columns: 1fr 1fr; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. KẾT NỐI SUPABASE & LOG TRUY CẬP
# ==========================================
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("⚠️ Lỗi kết nối cơ sở dữ liệu. Vui lòng kiểm tra cấu hình Secrets.")
    st.stop()

def log_access(app_name):
    key_name = f"da_dem_truy_cap_{app_name}"
    if key_name not in st.session_state:
        try:
            supabase.table("thong_ke_truy_cap").insert({"ten_app": app_name}).execute()
            st.session_state[key_name] = True
        except: pass
log_access("Quản lý Hồ sơ CBCC")

def get_logo_html(height="80px"):
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            return f'<img src="data:image/png;base64,{data}" style="height: {height}; filter: drop-shadow(0 2px 8px rgba(0,0,0,0.3));">'
    return f'<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Qu%E1%BB%91c_huy_Vi%E1%BB%87t_Nam.svg/250px-Qu%E1%BB%91c_huy_Vi%E1%BB%87t_Nam.svg.png" style="height: {height}; filter: drop-shadow(0 2px 8px rgba(0,0,0,0.3));">'

# ==========================================
# 4. DANH MỤC CHUẨN HÓA
# ==========================================
DS_DON_VI = ["Lãnh đạo Ban", "Văn phòng Ban", "Phòng Lý luận chính trị, Lịch sử Đảng", "Phòng Tuyên truyền, Báo chí - Xuất bản", "Phòng Khoa giáo, Văn hóa - Văn nghệ", "Phòng Dân vận các cơ quan Nhà nước, dân tộc và tôn giáo", "Phòng Đoàn thể và các Hội"]
DS_CHUC_VU = ["Trưởng Ban", "Phó Trưởng ban Thường trực", "Phó Trưởng Ban", "Chánh Văn phòng", "Phó Chánh Văn phòng", "Trưởng phòng", "Phó Trưởng phòng", "Chuyên viên chính", "Chuyên viên", "Văn thư viên", "Văn thư viên Trung cấp", "Kế toán viên", "Kế toán viên trung cấp", "Nhân viên lái xe", "Nhân viên phục vụ"]
DS_GIOI_TINH = ["Nam", "Nữ"]
DS_LY_LUAN = ["Chưa qua đào tạo", "Sơ cấp", "Trung cấp", "Cao cấp", "Cử nhân"]

# ==========================================
# 5. SESSION STATE & ĐĂNG NHẬP
# ==========================================
defaults = {"logged_in": False, "ma_cbcc": "", "ho_ten": "", "role": "User", "edit_target_id": "", "menu_selection": ""}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state["logged_in"]:
    st.markdown(f"""
    <div style="max-width:900px; margin: 0 auto 32px auto;">
        <div style="background: linear-gradient(135deg, var(--navy, #0A1628) 0%, #1A2E4A 50%, #C8102E 100%);
            padding: 28px 36px; border-radius: 14px; display:flex; align-items:center;
            gap: 24px; box-shadow: 0 8px 40px rgba(0,0,0,0.18); border-bottom: 4px solid #D4AF37;
            position:relative; overflow:hidden;">
            <div style="position:relative;">{get_logo_html("90px")}</div>
            <div style="width:3px;height:70px;background:linear-gradient(180deg,#F0D060,#D4AF37,transparent);border-radius:2px;flex-shrink:0;"></div>
            <div style="position:relative;">
                <div style="font-size:11px;color:#D4AF37;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;">Tỉnh ủy Tuyên Quang</div>
                <div style="font-family:'Georgia',serif;font-size:22px;font-weight:900;color:#fff;letter-spacing:1.5px;text-transform:uppercase;line-height:1.2;margin-bottom:6px;">Hệ thống Quản lý Hồ sơ</div>
                <div style="font-size:15px;color:#e8dfc8;font-weight:600;">Ban Tuyên giáo và Dân vận</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        tab_login, tab_register = st.tabs(["🔐  Đăng nhập hệ thống", "📝  Đăng ký tài khoản"])
        with tab_login:
            with st.form("login_form"):
                st.markdown("##### Mã cán bộ")
                log_ma = st.text_input("Mã CBCC", label_visibility="collapsed", placeholder="VD: CV01").strip().upper()
                st.markdown("##### Mật khẩu")
                log_pass = st.text_input("Mật khẩu", type="password", label_visibility="collapsed", placeholder="••••••••")
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                if st.form_submit_button("🚀  ĐĂNG NHẬP VÀO HỆ THỐNG", use_container_width=True):
                    if not log_ma or not log_pass:
                        st.error("⚠️ Vui lòng nhập đầy đủ Mã CBCC và Mật khẩu.")
                    else:
                        try:
                            user_data = supabase.table("tai_khoan").select("*").eq("ma_cbcc", log_ma).execute().data
                            if user_data:
                                user = user_data[0]
                                if user['mat_khau'] == log_pass:
                                    if user['trang_thai'] == 'Chờ duyệt':
                                        st.warning("⏳ Tài khoản đang chờ duyệt.")
                                    else:
                                        st.session_state.update({
                                            "logged_in": True, "ma_cbcc": user['ma_cbcc'],
                                            "ho_ten": user['ho_ten'], "role": user['phan_quyen'],
                                            "menu_selection": "📊 Dashboard" if user['phan_quyen'] == 'Admin' else "🔍 Hồ sơ của tôi"
                                        })
                                        st.rerun()
                                else: st.error("❌ Sai mật khẩu.")
                            else: st.error("❌ Không tìm thấy Mã CBCC.")
                        except Exception as e: st.error(f"Lỗi kết nối: {e}")

        with tab_register:
            with st.form("register_form"):
                c1, c2 = st.columns(2)
                reg_ma = c1.text_input("Mã CBCC *").strip().upper()
                reg_name = c2.text_input("Họ và tên *")
                reg_cv = st.selectbox("Chức vụ", DS_CHUC_VU)
                reg_dv = st.selectbox("Đơn vị công tác", DS_DON_VI)
                cp1, cp2 = st.columns(2)
                reg_pass = cp1.text_input("Mật khẩu *", type="password")
                reg_pass2 = cp2.text_input("Xác nhận Mật khẩu *", type="password")
                if st.form_submit_button("📩  GỬI YÊU CẦU ĐĂNG KÝ", use_container_width=True):
                    if not reg_ma or not reg_name or not reg_pass: st.error("⚠️ Điền đủ các trường bắt buộc (*).")
                    elif reg_pass != reg_pass2: st.error("⚠️ Mật khẩu không khớp.")
                    else:
                        try:
                            if supabase.table("tai_khoan").select("ma_cbcc").eq("ma_cbcc", reg_ma).execute().data:
                                st.error("⚠️ Mã CBCC đã tồn tại.")
                            else:
                                supabase.table("tai_khoan").insert({
                                    "ma_cbcc": reg_ma, "mat_khau": reg_pass,
                                    "ho_ten": reg_name.title(), "chuc_vu": reg_cv, "don_vi": reg_dv
                                }).execute()
                                st.success("✅ Đã gửi yêu cầu đăng ký.")
                        except Exception as e: st.error(f"Lỗi: {e}")
    st.stop()

# ==========================================
# 6. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown(f"<div style='text-align:center;padding:20px 0 16px;'>{get_logo_html('90px')}</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="user-chip" style="background:rgba(255,255,255,0.1); padding:10px; border-radius:8px; text-align:center; margin-bottom:15px;">
        <div style="font-weight:bold; color:#fff; font-size:16px;">👤 {st.session_state['ho_ten']}</div>
        <div style="color:#D4AF37; font-size:12px; margin-top:5px;">{'QUẢN TRỊ VIÊN' if st.session_state['role']=='Admin' else 'CÁN BỘ'}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪  Đăng xuất", use_container_width=True):
        for key in list(defaults.keys()): st.session_state[key] = defaults[key]
        st.rerun()

    st.markdown("---")
    is_admin = st.session_state["role"] == "Admin"
    menu_opts = ["📊 Dashboard", "🛡️ Admin: Duyệt Tài khoản", "🔍 Tra cứu & Xem Hồ sơ", "➕ Admin: Cập nhật Hồ sơ (Tất cả)"] if is_admin else ["🔍 Hồ sơ của tôi", "➕ Cập nhật Hồ sơ cá nhân"]
    
    if st.session_state["menu_selection"] not in menu_opts: st.session_state["menu_selection"] = menu_opts[0]
    menu = st.radio("Chức năng", menu_opts, index=menu_opts.index(st.session_state["menu_selection"]), label_visibility="collapsed")
    if menu != st.session_state["menu_selection"]:
        st.session_state["menu_selection"] = menu
        st.rerun()

# ==========================================
# 7. HEADER CHÍNH & HÀM TIỆN ÍCH
# ==========================================
st.markdown(f"""
<div class="gov-header">
    <div style="position:relative;">{get_logo_html("65px")}</div>
    <div class="gold-bar"></div>
    <div class="gov-header-text">
        <h1>Hệ thống Quản lý Hồ sơ Cán bộ, Công chức</h1>
        <p class="subtitle">Ban Tuyên giáo và Dân vận — Tỉnh ủy Tuyên Quang</p>
    </div>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_profiles():
    try: return pd.DataFrame(supabase.table("ho_so_cbcc").select("*").execute().data)
    except: return pd.DataFrame()

df_hoso = load_profiles()
def get_idx(lst, val): return lst.index(val) if val in lst else 0
def section_title(icon, text): st.markdown(f'<div class="section-title">{icon} {text}</div>', unsafe_allow_html=True)

# (Hàm tạo HTML bản in 2C-TW giữ nguyên)
def create_html_export(info, df_ct, df_l, df_kt, df_gd):
    def tbl(df, rename_map):
        if df.empty: return "<tr><td colspan='10' style='text-align:center;color:#888;padding:16px;'>Chưa có dữ liệu.</td></tr>"
        df2 = df.rename(columns=rename_map).drop(columns=['id', 'ma_cbcc'], errors='ignore')
        rows = "".join("<tr>" + "".join(f"<td>{v}</td>" for v in row) + "</tr>" for _, row in df2.iterrows())
        return "<tr>" + "".join(f"<th>{c}</th>" for c in df2.columns) + "</tr>" + rows
    
    ct_rows = tbl(df_ct, {'tu_ngay':'Từ ngày','den_ngay':'Đến ngày','vi_tri':'Vị trí','don_vi':'Đơn vị','quyet_dinh_so':'Quyết định số'})
    l_rows = tbl(df_l, {'ngay_quyet_dinh':'Ngày QĐ','bac_luong':'Bậc lương','he_so':'Hệ số','quyet_dinh_so':'Quyết định số'})
    kt_rows = tbl(df_kt, {'ngay_quyet_dinh':'Ngày QĐ','loai':'Loại','noi_dung':'Nội dung','quyet_dinh_so':'Quyết định số'})

    gd_html = "<tr><td colspan='7' style='text-align:center;color:#888;padding:16px;'>Chưa có dữ liệu.</td></tr>"
    if not df_gd.empty:
        df_gd2 = df_gd.drop(columns=['id','ma_cbcc','created_at','thong_tin_khac'], errors='ignore').rename(columns={'loai_quan_he':'Phân loại','quan_he':'Quan hệ','ho_ten':'Họ tên','nam_sinh':'Năm sinh','que_quan_gd':'Quê quán','nghe_nghiep_gd':'Nghề nghiệp','noi_o_gd':'Nơi ở'})
        rows = "".join("<tr>" + "".join(f"<td>{v}</td>" for v in row) + "</tr>" for _, row in df_gd2.iterrows())
        gd_html = "<tr>" + "".join(f"<th>{c}</th>" for c in df_gd2.columns) + "</tr>" + rows

    html = f"""<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8"><title>Sơ yếu lý lịch — {info.get('ho_ten','—')}</title>
<style>body {{ font-family: 'Times New Roman', serif; line-height: 1.6; padding: 30px; font-size: 14px; }}
table.data-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
table.data-table th, table.data-table td {{ border: 1px solid #000; padding: 6px; }}
</style></head><body>
<h2 style="text-align:center;">SƠ YẾU LÝ LỊCH CÁN BỘ, CÔNG CHỨC</h2>
<p><strong>Họ và tên:</strong> {info.get('ho_ten','—')} &nbsp;&nbsp; <strong>Mã CBCC:</strong> {info.get('id','—')}</p>
<p><strong>Ngày sinh:</strong> {info.get('ngay_sinh','—')} &nbsp;&nbsp; <strong>Giới tính:</strong> {info.get('gioi_tinh','—')}</p>
<p><strong>Quốc tịch:</strong> {info.get('quoc_tich','Việt Nam')} &nbsp;&nbsp; <strong>Dân tộc:</strong> {info.get('dan_toc','—')}</p>
<p><strong>Chức vụ:</strong> {info.get('chuc_vu','—')} &nbsp;&nbsp; <strong>Đơn vị:</strong> {info.get('don_vi','—')}</p>
<h3>1. Lịch sử công tác</h3><table class="data-table">{ct_rows}</table>
<h3>2. Diễn biến lương</h3><table class="data-table">{l_rows}</table>
<h3>3. Khen thưởng / Kỷ luật</h3><table class="data-table">{kt_rows}</table>
<h3>4. Quan hệ gia đình</h3><table class="data-table">{gd_html}</table>
</body></html>"""
    return html.encode('utf-8')

# ==========================================
# MODULE 1: DASHBOARD (HOÀN HẢO)
# ==========================================
if menu == "📊 Dashboard":
    # 🤖 CHỖ NÀY ĐỂ DÀNH CHO CODE CHATBOT TRỢ LÝ NHÂN SỰ CỦA SẾP
    # Sếp dán code chatbot vào dưới dòng này nếu cần nhé!
    # st.subheader("🤖 Trợ lý Nhân sự")
    # ... code chatbot ...

    section_title("📊", "THỐNG KÊ NHÂN SỰ TỔNG QUAN")

    if df_hoso.empty:
        st.info("📭 Chưa có dữ liệu để thống kê. Vui lòng nhập hồ sơ cán bộ trước.")
    else:
        # BƯỚC QUAN TRỌNG: Làm sạch dữ liệu, xử lý các ô chỉ toàn dấu cách
        df = df_hoso.fillna("Chưa xác định").copy()
        df = df.replace(r'^\s*$', 'Chưa xác định', regex=True)

        total  = len(df)
        nam    = len(df[df["gioi_tinh"] == "Nam"])
        nu     = len(df[df["gioi_tinh"] == "Nữ"])
        dang   = len(df[df["ngay_vao_dang"].notna() & (df["ngay_vao_dang"] != "Chưa xác định")])
        thac_si= len(df[df["trinh_do_chuyen_mon"].str.contains("Thạc|Tiến", case=False, na=False)])
        tyle_nu = round(nu / total * 100) if total else 0

        # ---- METRIC CARDS ----
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="m-label">👥 Tổng Cán bộ</div>
                <div class="m-value">{total}</div>
                <div class="m-sub">Biên chế chính thức toàn Ban</div>
            </div>
            <div class="metric-card gold">
                <div class="m-label">👨 Cán bộ Nam</div>
                <div class="m-value">{nam}</div>
                <div class="m-sub">{round(nam/total*100) if total else 0}% tổng số</div>
            </div>
            <div class="metric-card navy">
                <div class="m-label">👩 Cán bộ Nữ</div>
                <div class="m-value">{nu}</div>
                <div class="m-sub">{tyle_nu}% tổng số</div>
            </div>
            <div class="metric-card green">
                <div class="m-label">🎓 Thạc sĩ trở lên</div>
                <div class="m-value">{thac_si}</div>
                <div class="m-sub">{round(thac_si/total*100) if total else 0}% tổng số</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ---- BIỂU ĐỒ HÀNG 1 ----
        col_a, col_b = st.columns([1, 2])
        with col_a:
            df_gt = df[df['gioi_tinh'].isin(["Nam", "Nữ"])]['gioi_tinh'].value_counts().reset_index()
            df_gt.columns = ['Giới tính', 'Số lượng']
            if not df_gt.empty:
                fig_gt = px.pie(df_gt, values='Số lượng', names='Giới tính', hole=0.60, color='Giới tính', color_discrete_map={'Nam': '#1A2E4A', 'Nữ': '#C8102E'}, title='<b>Cơ cấu Giới tính</b>')
                fig_gt.update_traces(textposition='outside', textinfo='label+percent+value', marker=dict(line=dict(color='#ffffff', width=3)), pull=[0.04, 0.04])
                fig_gt.add_annotation(text=f"<b>{total}</b><br>CB", x=0.5, y=0.5, showarrow=False, font=dict(size=20, color='#1A2E4A', family='Merriweather'))
                fig_gt.update_layout(font_family="Source Sans 3", title_font=dict(size=14, color='#1A2E4A'), title_x=0.5, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5), margin=dict(t=50, b=30, l=20, r=20), height=320)
                st.plotly_chart(fig_gt, use_container_width=True)

        with col_b:
            df_cm = df[df['trinh_do_chuyen_mon'] != 'Chưa xác định']['trinh_do_chuyen_mon'].value_counts().reset_index()
            df_cm.columns = ['Trình độ', 'Số lượng']
            df_cm = df_cm.sort_values('Số lượng', ascending=False)
            if not df_cm.empty:
                fig_cm = px.bar(df_cm, x='Trình độ', y='Số lượng', text_auto=True, title='<b>Trình độ Chuyên môn</b>', color_discrete_sequence=['#C8102E'])
                fig_cm.update_layout(font_family="Source Sans 3", title_font_size=14, title_x=0.5, plot_bgcolor='rgba(248,244,239,0.6)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=55, b=20, l=40, r=20), height=320)
                st.plotly_chart(fig_cm, use_container_width=True)

        # ---- BIỂU ĐỒ HÀNG 2 (NGẠCH & LÝ LUẬN - CỘT NGANG) ----
        col_c, col_d = st.columns(2)
        with col_c:
            df_ng = df[df['ngach_cong_chuc'] != 'Chưa xác định']['ngach_cong_chuc'].value_counts().reset_index()
            df_ng.columns = ['Ngạch', 'Số lượng']
            if not df_ng.empty:
                fig_ng = px.bar(df_ng, y='Ngạch', x='Số lượng', orientation='h', title='<b>Ngạch Công chức hiện hưởng</b>', color_discrete_sequence=['#1A2E4A'], text_auto=True)
                fig_ng.update_layout(font_family="Source Sans 3", title_font_size=14, title_x=0.5, plot_bgcolor='rgba(248,244,239,0.6)', paper_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder': 'total ascending'}, margin=dict(t=55, b=20, l=10, r=50), height=340)
                st.plotly_chart(fig_ng, use_container_width=True)

        with col_d:
            thu_tu_ll = ["Chưa qua đào tạo", "Sơ cấp", "Trung cấp", "Cao cấp", "Cử nhân"]
            df_ll_raw = df[df['ly_luan_chinh_tri'] != 'Chưa xác định']['ly_luan_chinh_tri'].value_counts().reset_index()
            df_ll_raw.columns = ['Lý luận CT', 'Số lượng']
            df_ll_raw['Lý luận CT'] = pd.Categorical(df_ll_raw['Lý luận CT'], categories=thu_tu_ll, ordered=True)
            df_ll = df_ll_raw.sort_values('Lý luận CT', ascending=True).dropna()
            if not df_ll.empty:
                fig_ll = px.bar(df_ll, y='Lý luận CT', x='Số lượng', orientation='h', title='<b>Trình độ Lý luận Chính trị</b>', color_discrete_sequence=['#D4AF37'], text_auto=True)
                fig_ll.update_layout(font_family="Source Sans 3", title_font_size=14, title_x=0.5, plot_bgcolor='rgba(248,244,239,0.6)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=55, b=20, l=10, r=50), height=340)
                st.plotly_chart(fig_ll, use_container_width=True)

        # ---- BẢNG TÓM TẮT & HỌC VỊ ----
        section_title("🎓", "CƠ CẤU HỌC VỊ VÀ ĐẢNG VỤ")
        col_e, col_f = st.columns([1.4, 1])
        with col_e:
            df_hv = df[(df['hoc_vi'] != 'Chưa xác định')]['hoc_vi'].value_counts().reset_index()
            df_hv.columns = ['Học vị', 'Số lượng']
            chua_hoc_vi = total - df_hv['Số lượng'].sum()
            if chua_hoc_vi > 0:
                df_hv = pd.concat([df_hv, pd.DataFrame([{'Học vị': 'Đại học / Chưa xác định', 'Số lượng': chua_hoc_vi}])], ignore_index=True)
            
            fig_hv = px.pie(df_hv, values='Số lượng', names='Học vị', hole=0.55, title='<b>Cơ cấu Học vị cán bộ</b>', color_discrete_sequence=px.colors.sequential.RdBu)
            fig_hv.update_traces(textposition='outside', textinfo='label+percent')
            fig_hv.update_layout(font_family="Source Sans 3", title_font_size=14, title_x=0.5, margin=dict(t=55, b=20, l=20, r=160), height=360)
            st.plotly_chart(fig_hv, use_container_width=True)

        with col_f:
            tyle_dang = round(dang / total * 100) if total else 0
            st.markdown(f"""
            <div style="background:#fff;border-radius:12px;padding:22px 24px;border-left:5px solid #D4AF37;box-shadow:0 4px 20px rgba(0,0,0,0.08);margin-top:8px;">
                <div style="font-family:'Merriweather',serif;font-size:13px;font-weight:700;color:#0A1628;letter-spacing:1px;text-transform:uppercase;border-bottom:1px dashed rgba(212,175,55,0.4);padding-bottom:10px;margin-bottom:14px;">📋 Bảng Tổng hợp Chỉ tiêu</div>
                <table style="width:100%;border-collapse:collapse;font-size:13px;">
                    <tr style="background:rgba(200,16,46,0.06);"><td style="padding:9px 10px;color:#6B7280;font-weight:600;">👥 Tổng biên chế</td><td style="padding:9px 10px;text-align:right;font-weight:900;color:#C8102E;font-size:16px;">{total}</td></tr>
                    <tr><td style="padding:9px 10px;color:#6B7280;font-weight:600;">👨 Cán bộ Nam</td><td style="padding:9px 10px;text-align:right;font-weight:700;color:#1A2E4A;">{nam} ({round(nam/total*100) if total else 0}%)</td></tr>
                    <tr style="background:rgba(212,175,55,0.05);"><td style="padding:9px 10px;color:#6B7280;font-weight:600;">👩 Cán bộ Nữ</td><td style="padding:9px 10px;text-align:right;font-weight:700;color:#C8102E;">{nu} ({tyle_nu}%)</td></tr>
                    <tr><td style="padding:9px 10px;color:#6B7280;font-weight:600;">☭ Đảng viên</td><td style="padding:9px 10px;text-align:right;font-weight:700;color:#1A2E4A;">{dang} ({tyle_dang}%)</td></tr>
                    <tr style="background:rgba(200,16,46,0.06);"><td style="padding:9px 10px;color:#6B7280;font-weight:600;">🎓 Thạc sĩ trở lên</td><td style="padding:9px 10px;text-align:right;font-weight:700;color:#2E7D32;">{thac_si} ({round(thac_si/total*100) if total else 0}%)</td></tr>
                    <tr><td style="padding:9px 10px;color:#6B7280;font-weight:600;">🏛️ Lý luận Cao cấp/CN</td><td style="padding:9px 10px;text-align:right;font-weight:700;color:#B8860B;">{len(df[df['ly_luan_chinh_tri'].isin(['Cao cấp','Cử nhân'])])} người</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

        # ---- DANH SÁCH & XUẤT FILE ----
        section_title("📋", "DANH SÁCH CÁN BỘ, CÔNG CHỨC")
        cols_show = ['id', 'ho_ten', 'chuc_vu', 'don_vi', 'ngay_sinh', 'gioi_tinh', 'hoc_vi', 'trinh_do_chuyen_mon', 'ly_luan_chinh_tri', 'ngach_cong_chuc']
        df_show = df[[c for c in cols_show if c in df.columns]].rename(columns={
            'id': 'Mã CB', 'ho_ten': 'Họ và tên', 'chuc_vu': 'Chức vụ', 'don_vi': 'Đơn vị',
            'ngay_sinh': 'Ngày sinh', 'gioi_tinh': 'Giới tính', 'hoc_vi': 'Học vị', 
            'trinh_do_chuyen_mon': 'Chuyên môn', 'ly_luan_chinh_tri': 'Lý luận CT', 'ngach_cong_chuc': 'Ngạch CC'
        })
        st.dataframe(df_show, hide_index=True, use_container_width=True)

        st.download_button("📥  XUẤT DANH SÁCH (.CSV)", data=df_show.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'), file_name=f"DanhSach_CBCC_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

# ==========================================
# MODULE 2: ADMIN DUYỆT TÀI KHOẢN
# ==========================================
elif menu == "🛡️ Admin: Duyệt Tài khoản":
    section_title("🛡️", "QUẢN TRỊ TÀI KHOẢN HỆ THỐNG")
    tk_data = supabase.table("tai_khoan").select("*").execute().data
    if not tk_data: st.info("Chưa có tài khoản nào.")
    else:
        df_tk = pd.DataFrame(tk_data)
        tab_cd, tab_hd = st.tabs(["⏳  Chờ phê duyệt", "✅  Tài khoản hoạt động"])
        with tab_cd:
            df_choduyet = df_tk[df_tk['trang_thai'] == 'Chờ duyệt']
            if df_choduyet.empty: st.success("🎉 Không có yêu cầu nào chờ duyệt.")
            else:
                for _, row in df_choduyet.iterrows():
                    with st.expander(f"👤  {row['ho_ten']} ({row['ma_cbcc']}) — {row['chuc_vu']}"):
                        st.markdown(f"<b>Đơn vị:</b> {row['don_vi']}<br><b>Chức vụ:</b> {row['chuc_vu']}", unsafe_allow_html=True)
                        c1, c2 = st.columns(2)
                        if c1.button("✅ DUYỆT", key=f"d_{row['ma_cbcc']}", use_container_width=True):
                            supabase.table("tai_khoan").update({"trang_thai": "Hoạt động"}).eq("ma_cbcc", row['ma_cbcc']).execute()
                            if not supabase.table("ho_so_cbcc").select("id").eq("id", row['ma_cbcc']).execute().data:
                                supabase.table("ho_so_cbcc").insert({"id": row['ma_cbcc'], "ho_ten": row['ho_ten'], "chuc_vu": row['chuc_vu'], "don_vi": row['don_vi'], "quoc_tich": "Việt Nam", "dan_toc": "Kinh"}).execute()
                            st.success("Đã duyệt!"); st.rerun()
                        if c2.button("❌ TỪ CHỐI", key=f"x_{row['ma_cbcc']}", use_container_width=True):
                            supabase.table("tai_khoan").delete().eq("ma_cbcc", row['ma_cbcc']).execute()
                            st.success("Đã xóa."); st.rerun()

        with tab_hd:
            df_hd = df_tk[df_tk['trang_thai'] == 'Hoạt động']
            st.dataframe(df_hd[['ma_cbcc', 'ho_ten', 'chuc_vu', 'don_vi', 'phan_quyen']], hide_index=True, use_container_width=True)
            st.markdown("---")
            c_rs, c_del = st.columns(2)
            ds_hd = (df_hd['ma_cbcc'] + " — " + df_hd['ho_ten']).tolist()
            with c_rs:
                rs_ma = st.selectbox("🔑 Xem Mật khẩu:", ds_hd)
                if st.button("👁️ XEM MẬT KHẨU", use_container_width=True):
                    ma_xem = rs_ma.split(" — ")[0]
                    mk = supabase.table("tai_khoan").select("mat_khau").eq("ma_cbcc", ma_xem).execute().data
                    if mk: st.info(f"Mật khẩu: `{mk[0]['mat_khau']}`")
            with c_del:
                del_ma = st.selectbox("❌ Xóa Tài khoản:", ["— Chọn —"] + ds_hd)
                if st.button("🗑️ XÓA VĨNH VIỄN", use_container_width=True) and del_ma != "— Chọn —":
                    ma_xoa = del_ma.split(" — ")[0]
                    if ma_xoa.upper() == "ADMIN": st.error("⚠️ Không thể xóa Admin!")
                    else:
                        supabase.table("tai_khoan").delete().eq("ma_cbcc", ma_xoa).execute()
                        supabase.table("ho_so_cbcc").delete().eq("id", ma_xoa).execute()
                        st.success("Đã xóa hoàn toàn."); st.rerun()

# ==========================================
# MODULE 3: XEM HỒ SƠ
# ==========================================
elif menu in ["🔍 Tra cứu & Xem Hồ sơ", "🔍 Hồ sơ của tôi"]:
    section_title("🔍", "TRA CỨU & XEM HỒ SƠ CÁN BỘ")
    if df_hoso.empty: st.warning("📭 Hệ thống chưa có hồ sơ.")
    else:
        ma_chon = ""
        if is_admin:
            tu_khoa = st.text_input("🔎 Tìm kiếm (Tên/Mã):", placeholder="Nhập từ khóa...")
            if tu_khoa:
                df_kq = df_hoso[df_hoso.apply(lambda r: r.astype(str).str.contains(tu_khoa, case=False).any(), axis=1)]
                if not df_kq.empty:
                    chon = st.selectbox("👉 Chọn cán bộ:", (df_kq['ho_ten'] + " (" + df_kq['id'] + ")").tolist())
                    ma_chon = chon.split("(")[-1].replace(")", "")
                else: st.warning("Không tìm thấy.")
        else:
            ma_chon = st.session_state["ma_cbcc"]
            if df_hoso[df_hoso['id'] == ma_chon].empty:
                st.warning("❌ Bạn chưa có hồ sơ. Chuyển sang Cập nhật Hồ sơ."); ma_chon = ""

        if ma_chon:
            info = df_hoso[df_hoso['id'] == ma_chon].iloc[0].fillna("—")
            c1, c2 = st.columns(2)
            if c1.button("✏️ Chỉnh sửa hồ sơ", use_container_width=True):
                st.session_state["edit_target_id"] = info['id']
                st.session_state["menu_selection"] = "➕ Admin: Cập nhật Hồ sơ (Tất cả)" if is_admin else "➕ Cập nhật Hồ sơ cá nhân"
                st.rerun()

            df_ct = pd.DataFrame(supabase.table("lich_su_cong_tac").select("*").eq("ma_cbcc", ma_chon).execute().data)
            df_l = pd.DataFrame(supabase.table("dien_bien_luong").select("*").eq("ma_cbcc", ma_chon).execute().data)
            df_kt = pd.DataFrame(supabase.table("khen_thuong_ky_luat").select("*").eq("ma_cbcc", ma_chon).execute().data)
            try: df_gd = pd.DataFrame(supabase.table("quan_he_gia_dinh").select("*").eq("ma_cbcc", ma_chon).execute().data)
            except: df_gd = pd.DataFrame()

            c2.download_button("📥 TẢI SYLL 2C-TW", data=create_html_export(info, df_ct, df_l, df_kt, df_gd), file_name=f"SYLL_2C_{info['ho_ten']}.html", mime="text/html", use_container_width=True)

            st.markdown(f"""
            <div class="profile-card">
                <div class="profile-badge">MẪU SƠ YẾU LÝ LỊCH CÁN BỘ 2C-TW</div>
                <div class="profile-name">{info['ho_ten']}</div>
                <div class="profile-title">🏛️ {info.get('chuc_vu','—')} &nbsp;|&nbsp; {info.get('don_vi','—')}</div><hr class="profile-divider">
                <div class="profile-info-grid">
                    <div class="info-item"><span class="lbl">Mã cán bộ</span><span class="val">{info.get('id','—')}</span></div>
                    <div class="info-item"><span class="lbl">Ngày sinh</span><span class="val">{info.get('ngay_sinh','—')}</span></div>
                    <div class="info-item"><span class="lbl">Giới tính</span><span class="val">{info.get('gioi_tinh','—')}</span></div>
                    <div class="info-item"><span class="lbl">Quê quán</span><span class="val">{info.get('que_quan','—')}</span></div>
                    <div class="info-item"><span class="lbl">Nơi ở hiện nay</span><span class="val">{info.get('noi_o_hien_nay','—')}</span></div>
                    <div class="info-item"><span class="lbl">Chức vụ Đảng</span><span class="val">{info.get('chuc_vu_dang','—')}</span></div>
                    <div class="info-item"><span class="lbl">Trình độ chuyên môn</span><span class="val">{info.get('trinh_do_chuyen_mon','—')}</span></div>
                    <div class="info-item"><span class="lbl">Lý luận chính trị</span><span class="val">{info.get('ly_luan_chinh_tri','—')}</span></div>
                    <div class="info-item"><span class="lbl">Ngày vào Đảng</span><span class="val">{info.get('ngay_vao_dang','—')}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            t_ct, t_l, t_kt, t_gd = st.tabs(["🏢 Lịch sử công tác", "💰 Diễn biến lương", "🏆 Khen thưởng & Kỷ luật", "👨‍👩‍👧‍👦 Quan hệ gia đình"])
            with t_ct: st.dataframe(df_ct.drop(columns=['ma_cbcc','id','created_at'], errors='ignore'), use_container_width=True) if not df_ct.empty else st.info("Trống")
            with t_l: st.dataframe(df_l.drop(columns=['ma_cbcc','id','created_at'], errors='ignore'), use_container_width=True) if not df_l.empty else st.info("Trống")
            with t_kt: st.dataframe(df_kt.drop(columns=['ma_cbcc','id','created_at'], errors='ignore'), use_container_width=True) if not df_kt.empty else st.info("Trống")
            with t_gd: st.dataframe(df_gd.drop(columns=['ma_cbcc','id','created_at'], errors='ignore'), use_container_width=True) if not df_gd.empty else st.info("Trống")

# ==========================================
# MODULE 4: NHẬP LIỆU & CHỈNH SỬA
# ==========================================
elif menu in ["➕ Cập nhật Hồ sơ cá nhân", "➕ Admin: Cập nhật Hồ sơ (Tất cả)"]:
    section_title("📝", "TRUNG TÂM NHẬP LIỆU HỒ SƠ HỆ THỐNG")
    
    if is_admin:
        kieu_nhap = st.radio("Chế độ:", ["Sửa hồ sơ hiện có", "Thêm cán bộ mới"], horizontal=True)
        if kieu_nhap == "Sửa hồ sơ hiện có":
            ds_cbcc = (df_hoso['id'] + " — " + df_hoso['ho_ten']).tolist() if not df_hoso.empty else []
            target_id = st.selectbox("Chọn cán bộ:", ds_cbcc).split(" — ")[0] if ds_cbcc else ""
        else: target_id = st.text_input("Mã CBCC mới:").strip().upper()
    else:
        target_id = st.session_state["ma_cbcc"]
        st.info(f"📋 Cập nhật hồ sơ cá nhân — Mã: **{target_id}**")

    ex_data = df_hoso[df_hoso['id'] == target_id].iloc[0].fillna("").to_dict() if target_id and not df_hoso.empty and target_id in df_hoso['id'].values else {}

    tab_chinh, tab_ct, tab_luong, tab_kt, tab_gd = st.tabs(["👤 Hồ sơ chính", "🏢 Quá trình CT", "💰 Lương", "🏆 Khen thưởng", "👨‍👩‍👧‍👦 Gia đình"])

    with tab_chinh:
        with st.form("form_ho_so"):
            c1, c2, c3 = st.columns(3)
            with c1:
                ho_ten = st.text_input("Họ và tên *", ex_data.get("ho_ten", ""))
                ngay_sinh = st.text_input("Ngày sinh", ex_data.get("ngay_sinh", ""))
                gioi_tinh = st.selectbox("Giới tính", DS_GIOI_TINH, get_idx(DS_GIOI_TINH, ex_data.get("gioi_tinh", "Nam")))
                quoc_tich = st.text_input("Quốc tịch", ex_data.get("quoc_tich", "Việt Nam"))
                dan_toc = st.text_input("Dân tộc", ex_data.get("dan_toc", "Kinh"))
            with c2:
                que_quan = st.text_input("Quê quán", ex_data.get("que_quan", ""))
                noi_khai_sinh = st.text_input("Nơi sinh", ex_data.get("noi_khai_sinh", ""))
                thuong_tru = st.text_input("Thường trú", ex_data.get("thuong_tru", ""))
                noi_o_hien_nay = st.text_input("Nơi ở hiện nay", ex_data.get("noi_o_hien_nay", ""))
            with c3:
                don_vi = st.selectbox("Đơn vị *", DS_DON_VI, get_idx(DS_DON_VI, ex_data.get("don_vi", "Lãnh đạo Ban")))
                chuc_vu = st.selectbox("Chức vụ", DS_CHUC_VU, get_idx(DS_CHUC_VU, ex_data.get("chuc_vu", "Chuyên viên")))
                chuc_vu_dang = st.text_input("Chức vụ Đảng", ex_data.get("chuc_vu_dang", ""))
                nghe_nghiep_ht = st.text_input("Nghề nghiệp", ex_data.get("nghe_nghiep_ht", ""))
                ngach = st.text_input("Ngạch công chức", ex_data.get("ngach_cong_chuc", ""))

            cx1, cx2, cx3, cx4, cx5 = st.columns(5)
            giao_duc_pt = cx1.text_input("GD Phổ thông", ex_data.get("giao_duc_pt", ""))
            chuyen_mon = cx2.text_input("Chuyên môn", ex_data.get("trinh_do_chuyen_mon", ""))
            hoc_vi = cx3.text_input("Học vị", ex_data.get("hoc_vi", ""))
            ngoai_ngu = cx4.text_input("Ngoại ngữ", ex_data.get("ngoai_ngu", ""))
            tin_hoc = cx5.text_input("Tin học", ex_data.get("tin_hoc", ""))

            cl1, cl2, cl3 = st.columns(3)
            ly_luan = cl1.selectbox("Lý luận CT", DS_LY_LUAN, get_idx(DS_LY_LUAN, ex_data.get("ly_luan_chinh_tri", "Chưa qua đào tạo")))
            ngay_ket_nap = cl2.text_input("Ngày vào Đảng", ex_data.get("ngay_vao_dang", ""))
            ngay_chinh_thuc = cl3.text_input("Ngày chính thức", ex_data.get("ngay_chinh_thuc", ""))

            if st.form_submit_button("💾 LƯU HỒ SƠ CHÍNH", use_container_width=True):
                if not target_id or not ho_ten: st.error("⚠️ Mã CBCC và Họ tên là bắt buộc.")
                else:
                    data = {"id": target_id, "ho_ten": ho_ten.title(), "ngay_sinh": ngay_sinh, "gioi_tinh": gioi_tinh, "quoc_tich": quoc_tich, "dan_toc": dan_toc, "que_quan": que_quan, "noi_khai_sinh": noi_khai_sinh, "thuong_tru": thuong_tru, "noi_o_hien_nay": noi_o_hien_nay, "don_vi": don_vi, "chuc_vu": chuc_vu, "chuc_vu_dang": chuc_vu_dang, "nghe_nghiep_ht": nghe_nghiep_ht, "ngach_cong_chuc": ngach, "giao_duc_pt": giao_duc_pt, "trinh_do_chuyen_mon": chuyen_mon, "hoc_vi": hoc_vi, "ngoai_ngu": ngoai_ngu, "tin_hoc": tin_hoc, "ly_luan_chinh_tri": ly_luan, "ngay_vao_dang": ngay_ket_nap, "ngay_chinh_thuc": ngay_chinh_thuc}
                    supabase.table("ho_so_cbcc").upsert(data).execute(); st.cache_data.clear(); st.success("✅ Đã lưu thành công!"); st.rerun()

    def crud_tab(table, f_key, title, cols):
        with st.form(f"f_{f_key}"):
            st.write(f"**Thêm {title}**")
            vals = {fname: st.text_input(flabel) for fname, flabel in cols}
            if st.form_submit_button(f"➕ THÊM", use_container_width=True):
                supabase.table(table).insert({"ma_cbcc": target_id, **vals}).execute(); st.rerun()

        try: 
            raw_data = supabase.table(table).select("*").eq("ma_cbcc", target_id).order("id").execute().data
            df_sub = pd.DataFrame(raw_data)
        except: df_sub = pd.DataFrame()

        if not df_sub.empty:
            # GIỮ LẠI CỘT 'id' ĐỂ KHÔNG BỊ LỖI, CHỈ BỎ CÁC CỘT HỆ THỐNG
            df_show = df_sub.drop(columns=['ma_cbcc', 'created_at'], errors='ignore')
            
            # Đưa id ra cột đầu tiên cho dễ nhìn
            cols_order = ['id'] + [c for c in df_show.columns if c != 'id']
            df_show = df_show[cols_order]
            
            # Bỏ disabled=["id"] vì giờ 'id' đã nằm trong bảng, không lo lỗi nữa
            ed = st.data_editor(df_show, hide_index=True, use_container_width=True)
            
            c1, c2 = st.columns([3,1])
            if c1.button("💾 LƯU THAY ĐỔI", key=f"s_{f_key}", use_container_width=True):
                # Update từng dòng dựa vào 'id'
                for i in range(len(ed)):
                    row_data = ed.iloc[i].to_dict()
                    row_id = row_data.pop('id') # Lấy id ra để làm điều kiện update
                    supabase.table(table).update(row_data).eq("id", row_id).execute()
                st.success("✅ Đã cập nhật!"); st.rerun()
            
            del_id = c2.selectbox("Xóa ID:", ["—"] + df_sub['id'].astype(str).tolist(), label_visibility="collapsed", key=f"d_{f_key}")
            if c2.button("🗑️ XÓA", key=f"b_{f_key}", use_container_width=True) and del_id != "—":
                supabase.table(table).delete().eq("id", del_id).execute(); st.rerun()
        else: st.info("Chưa có dữ liệu.")
    with tab_ct: crud_tab("lich_su_cong_tac", "ct", "Công tác", [("tu_ngay","Từ"), ("den_ngay","Đến"), ("vi_tri","Vị trí"), ("don_vi","Đơn vị"), ("quyet_dinh_so","Số QĐ")])
    with tab_luong: crud_tab("dien_bien_luong", "l", "Lương", [("ngay_quyet_dinh","Ngày QĐ"), ("bac_luong","Bậc"), ("he_so","Hệ số"), ("quyet_dinh_so","Số QĐ")])
    with tab_kt: crud_tab("khen_thuong_ky_luat", "kt", "KT/KL", [("ngay_quyet_dinh","Ngày QĐ"), ("loai","Loại (Khen thưởng/Kỷ luật)"), ("noi_dung","Nội dung"), ("quyet_dinh_so","Số QĐ")])
    with tab_gd:
        st.info("📌 Kê khai gia đình (bản thân & bên vợ/chồng). Lưu ý: Nếu đã mất, ghi 'Đã từ trần (năm...)' vào mục Nghề nghiệp.")
        crud_tab("quan_he_gia_dinh", "gd", "Người thân", [("loai_quan_he","Bản thân hay Vợ/Chồng"), ("quan_he","Quan hệ (Bố/Mẹ/Vợ...)"), ("ho_ten","Họ tên"), ("nam_sinh","Năm sinh"), ("que_quan_gd","Quê quán"), ("nghe_nghiep_gd","Nghề nghiệp"), ("noi_o_gd","Nơi ở")])
