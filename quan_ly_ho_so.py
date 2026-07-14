"""
HỆ THỐNG QUẢN LÝ HỒ SƠ CÁN BỘ, CÔNG CHỨC - PHIÊN BẢN V7.0 (DASHBOARD TỐI ƯU)
Đã cập nhật: Dashboard đầy đủ biểu đồ Giới tính, Chuyên môn, Ngạch CC, Lý luận CT, Học vị
"""

import streamlit as st
import pandas as pd
from supabase import create_client, Client
import plotly.express as px
import plotly.graph_objects as go
import base64
import os
from datetime import datetime

# ==========================================
# 1. CẤU HÌNH TRANG
# ==========================================
st.set_page_config(
    page_title="Hồ sơ CBCC - Ban Tuyên giáo & Dân vận Tuyên Quang",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700;900&family=Source+Sans+3:wght@400;500;600;700&display=swap');

    :root {
        --red-primary: #C8102E; --red-dark: #A00C23; --red-light: #E8203F;
        --gold: #D4AF37; --gold-light: #F0D060; --navy: #0A1628;
        --navy-mid: #1A2E4A; --navy-light: #2A4A70; --cream: #FDF8F0;
        --off-white: #F5F1E8; --text-dark: #1A1A2E; --text-mid: #3D3D5C;
        --text-light: #6B7280; --border: #D4AF3740;
        --shadow-sm: 0 2px 8px rgba(0,0,0,0.08);
        --shadow-md: 0 4px 20px rgba(0,0,0,0.12);
        --shadow-lg: 0 8px 40px rgba(0,0,0,0.16);
    }
    html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; color: var(--text-dark); }
    .stApp { background: linear-gradient(160deg, #f8f4ef 0%, #ede8e0 50%, #f5f0e8 100%); }

    /* ---- SIDEBAR ---- */
    [data-testid="stSidebar"] { background: linear-gradient(180deg, var(--navy) 0%, var(--navy-mid) 60%, #0D1E35 100%) !important; border-right: 3px solid var(--gold) !important; z-index: 999999 !important; }
    [data-testid="stSidebar"] * { color: #e8dfc8 !important; }
    [data-testid="stSidebar"] .stRadio label { color: #c8bfa8 !important; padding: 10px 14px; border-radius: 6px; display: block; transition: all 0.2s; font-weight: 500; font-size: 14px; border-left: 3px solid transparent; }
    [data-testid="stSidebar"] .stRadio label:hover { background: rgba(212,175,55,0.12) !important; border-left-color: var(--gold) !important; color: var(--gold-light) !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(212,175,55,0.25) !important; }

    /* ---- HEADER CHÍNH ---- */
    .gov-header { background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 40%, var(--red-dark) 100%); border-bottom: 4px solid var(--gold); padding: 20px 32px; border-radius: 12px; margin-bottom: 28px; display: flex; align-items: center; gap: 24px; position: relative; overflow: hidden; box-shadow: var(--shadow-lg); }
    .gov-header::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: repeating-linear-gradient(45deg, transparent, transparent 40px, rgba(212,175,55,0.03) 40px, rgba(212,175,55,0.03) 41px); }
    .gov-header-text h1 { font-family: 'Merriweather', serif; font-size: 20px; font-weight: 900; color: #fff; margin: 0 0 4px 0; letter-spacing: 1.5px; text-transform: uppercase; text-shadow: 0 2px 8px rgba(0,0,0,0.3); }
    .gov-header-text .subtitle { font-size: 13px; color: var(--gold-light); margin: 0; letter-spacing: 0.5px; opacity: 0.9; }
    .gold-bar { width: 3px; height: 60px; background: linear-gradient(180deg, var(--gold-light), var(--gold), transparent); border-radius: 2px; flex-shrink: 0; }

    /* ---- SECTION TITLE ---- */
    .section-title { font-family: 'Merriweather', serif; font-size: 17px; font-weight: 700; color: var(--navy); display: flex; align-items: center; gap: 10px; margin: 24px 0 16px 0; padding-bottom: 10px; border-bottom: 2px solid var(--red-primary); }
    .section-title::before { content: ''; display: block; width: 5px; height: 22px; background: var(--gold); border-radius: 3px; }

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

    /* ---- DATA TABLE ---- */
    [data-testid="stDataFrame"] thead th { background-color: var(--navy) !important; color: #fff !important; font-weight: 700 !important; font-size: 13px !important; letter-spacing: 0.5px !important; }
    [data-testid="stDataFrame"] tbody tr:hover { background: rgba(200,16,46,0.04) !important; }

    /* ---- FORMS ---- */
    div[data-testid="stForm"] { background: #fff; border: 1px solid rgba(212,175,55,0.25); border-top: 3px solid var(--gold); border-radius: 10px; padding: 24px !important; box-shadow: var(--shadow-sm); }
    .stTextInput input, .stTextArea textarea { border: 1.5px solid #e0d8cc !important; border-radius: 6px !important; background: var(--cream) !important; font-family: 'Source Sans 3', sans-serif !important; transition: border-color 0.2s !important; }
    .stTextInput input:focus, .stTextArea textarea:focus { border-color: var(--red-primary) !important; box-shadow: 0 0 0 3px rgba(200,16,46,0.08) !important; }
    .stSelectbox div[data-baseweb="select"] > div { border: 1.5px solid #e0d8cc !important; border-radius: 6px !important; background: var(--cream) !important; font-family: 'Source Sans 3', sans-serif !important; transition: border-color 0.2s !important; }
    .stSelectbox div[data-baseweb="select"] > div:hover { border-color: var(--red-primary) !important; }
    .stSelectbox div[data-baseweb="select"] input { background: transparent !important; }
    .stSelectbox ul[data-baseweb="menu"] { background: var(--cream) !important; }

    /* ---- BUTTONS ---- */
    div[data-testid="stButton"] > button,
    div[data-testid="stFormSubmitButton"] > button,
    div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, var(--red-primary), var(--red-dark)) !important;
        color: #fff !important; border: none !important;
        font-family: 'Source Sans 3', sans-serif !important; font-weight: 700 !important;
        font-size: 13px !important; letter-spacing: 0.8px !important; text-transform: uppercase !important;
        padding: 10px 20px !important; border-radius: 6px !important;
        box-shadow: 0 3px 12px rgba(200,16,46,0.3) !important; transition: all 0.25s ease !important;
    }
    div[data-testid="stButton"] > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover,
    div[data-testid="stDownloadButton"] > button:hover {
        background: linear-gradient(135deg, var(--red-light), var(--red-primary)) !important;
        box-shadow: 0 5px 18px rgba(200,16,46,0.4) !important; transform: translateY(-1px) !important;
    }

    /* ---- TABS ---- */
    .stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 2px solid rgba(200,16,46,0.15) !important; gap: 4px !important; }
    .stTabs [data-baseweb="tab"] { font-family: 'Source Sans 3', sans-serif !important; font-weight: 600 !important; font-size: 13px !important; color: var(--text-mid) !important; padding: 10px 18px !important; border-radius: 6px 6px 0 0 !important; border: none !important; background: transparent !important; transition: all 0.2s !important; }
    .stTabs [aria-selected="true"] { color: var(--red-primary) !important; background: rgba(200,16,46,0.06) !important; border-bottom: 3px solid var(--red-primary) !important; }

    /* ---- EXPANDER ---- */
    [data-testid="stExpander"] summary { font-weight: 600 !important; color: var(--navy-mid) !important; background: var(--off-white) !important; border-left: 4px solid var(--gold) !important; border-radius: 6px !important; padding: 12px 16px !important; }

    #MainMenu, footer { visibility: hidden !important; }
    .block-container { padding-top: 24px !important; padding-bottom: 40px !important; }

    /* ---- MOBILE FIX ---- */
    @media screen and (max-width: 768px) {
        header[data-testid="stHeader"] { visibility: visible !important; background-color: #0A1628 !important; border-bottom: 2px solid #D4AF37 !important; }
        header[data-testid="stHeader"] svg { fill: #D4AF37 !important; width: 25px !important; height: 25px !important; }
        .gov-header { margin-top: 3.5rem !important; flex-direction: column !important; text-align: center !important; padding: 15px !important; gap: 10px !important; }
        .gold-bar { width: 80px !important; height: 3px !important; background: linear-gradient(90deg, #F0D060, #D4AF37, transparent) !important; margin: 0 auto !important; }
        .metric-grid { grid-template-columns: repeat(2, 1fr) !important; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SUPABASE
# ==========================================
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("⚠️ Lỗi kết nối cơ sở dữ liệu. Vui lòng kiểm tra lại cấu hình Secrets!")
    st.stop()

def log_access(app_name):
    key_name = f"da_dem_truy_cap_{app_name}"
    if key_name not in st.session_state:
        try:
            supabase.table("thong_ke_truy_cap").insert({"ten_app": app_name}).execute()
            st.session_state[key_name] = True
        except:
            pass

log_access("Quản lý Hồ sơ CBCC")

def get_logo_html(height="80px"):
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            return f'<img src="data:image/png;base64,{data}" style="height: {height}; filter: drop-shadow(0 2px 8px rgba(0,0,0,0.3));">'
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Qu%E1%BB%91c_huy_Vi%E1%BB%87t_Nam.svg/250px-Qu%E1%BB%91c_huy_Vi%E1%BB%87t_Nam.svg.png"
    return f'<img src="{url}" style="height: {height}; filter: drop-shadow(0 2px 8px rgba(0,0,0,0.3));">'

# ==========================================
# 3. DANH MỤC CHUẨN HÓA
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
# 4. SESSION STATE
# ==========================================
defaults = {
    "logged_in": False, "ma_cbcc": "", "ho_ten": "",
    "role": "User", "edit_target_id": "", "menu_selection": ""
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==========================================
# 5. ĐĂNG NHẬP
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown(f"""
    <div style="max-width:900px; margin: 0 auto 32px auto;">
        <div style="background: linear-gradient(135deg, #0A1628 0%, #1A2E4A 50%, #C8102E 100%);
            padding: 28px 36px; border-radius: 14px; display:flex; align-items:center;
            gap: 24px; box-shadow: 0 8px 40px rgba(0,0,0,0.18); border-bottom: 4px solid #D4AF37; position:relative; overflow:hidden;">
            <div style="position:relative;">{get_logo_html("90px")}</div>
            <div style="width:3px;height:70px;background:linear-gradient(180deg,#F0D060,#D4AF37,transparent);border-radius:2px;flex-shrink:0;"></div>
            <div>
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
                            if len(user_data) > 0:
                                user = user_data[0]
                                if user['mat_khau'] == log_pass:
                                    if user['trang_thai'] == 'Chờ duyệt':
                                        st.warning("⏳ Tài khoản đang chờ quản trị viên phê duyệt.")
                                    else:
                                        st.session_state.update({
                                            "logged_in": True, "ma_cbcc": user['ma_cbcc'],
                                            "ho_ten": user['ho_ten'], "role": user['phan_quyen'],
                                            "menu_selection": "📊 Dashboard" if user['phan_quyen'] == 'Admin' else "🔍 Hồ sơ của tôi"
                                        })
                                        st.rerun()
                                else:
                                    st.error("❌ Sai mật khẩu.")
                            else:
                                st.error("❌ Không tìm thấy Mã CBCC này trong hệ thống.")
                        except Exception as e:
                            st.error(f"Lỗi kết nối: {e}")

        with tab_register:
            with st.form("register_form"):
                c1, c2 = st.columns(2)
                reg_ma = c1.text_input("Mã CBCC *", placeholder="VD: CV099").strip().upper()
                reg_name = c2.text_input("Họ và tên *")
                reg_cv = st.selectbox("Chức vụ", DS_CHUC_VU)
                reg_dv = st.selectbox("Đơn vị công tác", DS_DON_VI)
                cp1, cp2 = st.columns(2)
                reg_pass = cp1.text_input("Mật khẩu *", type="password")
                reg_pass2 = cp2.text_input("Xác nhận Mật khẩu *", type="password")
                if st.form_submit_button("📩  GỬI YÊU CẦU ĐĂNG KÝ", use_container_width=True):
                    if not reg_ma or not reg_name or not reg_pass:
                        st.error("⚠️ Vui lòng điền đầy đủ các trường bắt buộc (*).")
                    elif reg_pass != reg_pass2:
                        st.error("⚠️ Mật khẩu xác nhận không khớp.")
                    else:
                        try:
                            if len(supabase.table("tai_khoan").select("ma_cbcc").eq("ma_cbcc", reg_ma).execute().data) > 0:
                                st.error("⚠️ Mã CBCC này đã được đăng ký.")
                            else:
                                supabase.table("tai_khoan").insert({
                                    "ma_cbcc": reg_ma, "mat_khau": reg_pass,
                                    "ho_ten": reg_name.title(), "chuc_vu": reg_cv, "don_vi": reg_dv
                                }).execute()
                                st.success("✅ Đã gửi yêu cầu. Vui lòng chờ phê duyệt.")
                        except Exception as e:
                            st.error(f"Lỗi: {e}")
    st.stop()

# ==========================================
# 6. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown(f"<div style='text-align:center;padding:20px 0 16px;'>{get_logo_html('90px')}</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.25);
        border-radius:8px;padding:12px 14px;margin-bottom:12px;">
        <div style="font-weight:700;font-size:14px;">👤 {st.session_state['ho_ten']}</div>
        <div style="margin-top:4px;">
            <span style="background:{'#C8102E' if st.session_state['role']=='Admin' else '#1A2E4A'};
                color:#fff;font-size:10px;font-weight:700;letter-spacing:1px;
                text-transform:uppercase;padding:2px 8px;border-radius:10px;">
                {'QUẢN TRỊ VIÊN' if st.session_state['role']=='Admin' else 'CÁN BỘ'}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪  Đăng xuất", use_container_width=True):
        for key in list(defaults.keys()):
            st.session_state[key] = defaults[key]
        st.rerun()

    st.markdown("---")
    st.markdown("<div style='font-size:10px;color:rgba(212,175,55,0.5);letter-spacing:1.5px;text-transform:uppercase;padding:0 4px;margin-bottom:8px;'>Chức năng</div>", unsafe_allow_html=True)

    is_admin = st.session_state["role"] == "Admin"
    if is_admin:
        menu_options = ["📊 Dashboard", "🛡️ Admin: Duyệt Tài khoản", "🔍 Tra cứu & Xem Hồ sơ", "➕ Admin: Cập nhật Hồ sơ (Tất cả)"]
    else:
        menu_options = ["🔍 Hồ sơ của tôi", "➕ Cập nhật Hồ sơ cá nhân"]

    if st.session_state["menu_selection"] not in menu_options:
        st.session_state["menu_selection"] = menu_options[0]

    current_idx = menu_options.index(st.session_state["menu_selection"])
    menu = st.radio("", menu_options, index=current_idx, label_visibility="collapsed")

    if menu != st.session_state["menu_selection"]:
        st.session_state["menu_selection"] = menu
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px;color:rgba(212,175,55,0.4);text-align:center;line-height:1.8;padding-bottom:10px;'>
        Ban Tuyên giáo & Dân vận<br>Tỉnh ủy Tuyên Quang<br>
        <span style='font-size:10px;opacity:0.6;'>© Hệ thống quản lý CBCC v7.0</span>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 7. HEADER CHÍNH
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

# ==========================================
# 8. HÀM TIỆN ÍCH
# ==========================================
@st.cache_data(ttl=5)
def load_profiles():
    try:
        return pd.DataFrame(supabase.table("ho_so_cbcc").select("*").execute().data)
    except Exception:
        return pd.DataFrame()

df_hoso = load_profiles()

def get_idx(lst, val):
    try: return lst.index(val)
    except Exception: return 0

def section_title(icon, text):
    st.markdown(f'<div class="section-title">{icon} {text}</div>', unsafe_allow_html=True)

def create_html_export(info, df_ct, df_l, df_kt):
    def tbl(df, rename_map):
        if df.empty:
            return "<tr><td colspan='10' style='text-align:center;color:#888;padding:16px;'>Chưa có dữ liệu.</td></tr>"
        df2 = df.rename(columns=rename_map).drop(columns=['id', 'ma_cbcc'], errors='ignore')
        rows = "".join("<tr>" + "".join(f"<td>{v}</td>" for v in row) + "</tr>" for _, row in df2.iterrows())
        header = "<tr>" + "".join(f"<th>{c}</th>" for c in df2.columns) + "</tr>"
        return header + rows

    ct_rows = tbl(df_ct, {'tu_ngay':'Từ ngày','den_ngay':'Đến ngày','vi_tri':'Vị trí','don_vi':'Đơn vị','quyet_dinh_so':'Quyết định số'})
    l_rows  = tbl(df_l,  {'ngay_quyet_dinh':'Ngày QĐ','bac_luong':'Bậc lương','he_so':'Hệ số','quyet_dinh_so':'Quyết định số'})
    kt_rows = tbl(df_kt, {'ngay_quyet_dinh':'Ngày QĐ','loai':'Loại','noi_dung':'Nội dung','quyet_dinh_so':'Quyết định số'})

    html = f"""<!DOCTYPE html>
<html lang="vi"><head><meta charset="utf-8">
<title>Sơ yếu lý lịch — {info['ho_ten']}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Source+Sans+3:wght@400;600&display=swap');
  body{{font-family:'Source Sans 3','Times New Roman',serif;line-height:1.7;padding:48px 56px;max-width:860px;margin:auto;color:#1a1a2e;font-size:14px;}}
  .header{{text-align:center;border-bottom:3px double #C8102E;padding-bottom:16px;margin-bottom:25px;}}
  .header h1{{font-family:'Merriweather',serif;font-size:20px;text-transform:uppercase;letter-spacing:2px;color:#0A1628;margin-bottom:4px;}}
  .header .org{{color:#C8102E;font-size:13px;font-weight:600;}}
  .info-table{{width:100%;border-collapse:collapse;margin-bottom:20px;}}
  .info-table td{{border:none;padding:6px 10px;border-bottom:1px dotted #ddd;width:50%;}}
  h3{{font-family:'Merriweather',serif;color:#0A1628;background:linear-gradient(90deg,#f5e8e8,#fff);padding:6px 12px;border-left:5px solid #C8102E;margin:24px 0 12px;font-size:13px;text-transform:uppercase;letter-spacing:1px;}}
  table.data-table{{width:100%;border-collapse:collapse;font-size:12px;}}
  table.data-table th{{background:#0A1628;color:#fff;padding:8px 10px;text-align:left;}}
  table.data-table td{{padding:7px 10px;border-bottom:1px solid #e8e0d4;vertical-align:top;}}
  table.data-table tr:nth-child(even) td{{background:#fdf8f0;}}
  .footer{{margin-top:40px;text-align:right;font-size:12px;color:#888;border-top:1px solid #ddd;padding-top:12px;}}
</style></head><body>
<div class="header">
  <p class="org">TỈNH ỦY TUYÊN QUANG — BAN TUYÊN GIÁO VÀ DÂN VẬN</p>
  <h1>Sơ yếu lý lịch cán bộ, công chức</h1>
</div>
<h3>I. Thông tin cá nhân</h3>
<table class="info-table">
  <tr><td><strong>Họ và tên:</strong> {str(info.get('ho_ten','')).upper()}</td><td><strong>Mã CBCC:</strong> {info.get('id','—')}</td></tr>
  <tr><td><strong>Ngày sinh:</strong> {info.get('ngay_sinh','—')}</td><td><strong>Giới tính:</strong> {info.get('gioi_tinh','—')}</td></tr>
  <tr><td><strong>Quốc tịch:</strong> {info.get('quoc_tich','Việt Nam')}</td><td><strong>Dân tộc:</strong> {info.get('dan_toc','—')}</td></tr>
  <tr><td><strong>Nơi đăng ký khai sinh:</strong> {info.get('noi_khai_sinh','—')}</td><td><strong>Nơi đăng ký thường trú:</strong> {info.get('thuong_tru','—')}</td></tr>
  <tr><td colspan="2"><strong>Nơi ở hiện nay:</strong> {info.get('noi_o_hien_nay','—')}</td></tr>
  <tr><td><strong>Quê quán:</strong> {info.get('que_quan','—')}</td><td><strong>Đơn vị công tác:</strong> {info.get('don_vi','—')}</td></tr>
  <tr><td><strong>Chức vụ hiện tại:</strong> {info.get('chuc_vu','—')}</td><td><strong>Chức vụ trong Đảng:</strong> {info.get('chuc_vu_dang','—')}</td></tr>
  <tr><td><strong>Nghề nghiệp hiện nay:</strong> {info.get('nghe_nghiep_ht','—')}</td><td><strong>Ngạch công chức:</strong> {info.get('ngach_cong_chuc','—')}</td></tr>
  <tr><td><strong>Giáo dục phổ thông:</strong> {info.get('giao_duc_pt','—')}</td><td><strong>Trình độ chuyên môn:</strong> {info.get('trinh_do_chuyen_mon','—')}</td></tr>
  <tr><td><strong>Học vị:</strong> {info.get('hoc_vi','—')}</td><td><strong>Lý luận chính trị:</strong> {info.get('ly_luan_chinh_tri','—')}</td></tr>
  <tr><td><strong>Ngoại ngữ:</strong> {info.get('ngoai_ngu','—')}</td><td><strong>Tin học:</strong> {info.get('tin_hoc','—')}</td></tr>
  <tr><td colspan="2"><strong>Đảng vụ:</strong> Kết nạp: {info.get('ngay_vao_dang','—')} &nbsp;|&nbsp; Chính thức: {info.get('ngay_chinh_thuc','—')}</td></tr>
</table>
<h3>II. Lịch sử công tác</h3>
<table class="data-table">{ct_rows}</table>
<h3>III. Diễn biến lương</h3>
<table class="data-table">{l_rows}</table>
<h3>IV. Khen thưởng & kỷ luật</h3>
<table class="data-table">{kt_rows}</table>
<div class="footer">Xuất từ Hệ thống Quản lý Hồ sơ CBCC — Ban Tuyên giáo và Dân vận Tỉnh ủy Tuyên Quang</div>
</body></html>"""
    return html.encode('utf-8')


# ==========================================
# MODULE 1: DASHBOARD (ĐÃ TỐI ƯU HÓA)
# ==========================================
if menu == "📊 Dashboard":
    section_title("📊", "THỐNG KÊ NHÂN SỰ TỔNG QUAN")

    if df_hoso.empty:
        st.info("📭 Chưa có dữ liệu để thống kê. Vui lòng nhập hồ sơ cán bộ trước.")
    else:
        df = df_hoso.fillna("Chưa xác định").copy()
        total   = len(df)
        nam     = len(df[df["gioi_tinh"] == "Nam"])
        nu      = len(df[df["gioi_tinh"] == "Nữ"])
        dang    = len(df[df["ngay_vao_dang"].notna() & (df["ngay_vao_dang"] != "Chưa xác định") & (df["ngay_vao_dang"] != "")])
        thac_si = len(df[df["trinh_do_chuyen_mon"].str.contains("Thạc|Tiến", case=False, na=False)])
        tyle_nu = round(nu / total * 100) if total else 0

        # ── METRIC CARDS ──
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="m-label">👥 Tổng Cán bộ</div>
                <div class="m-value">{total}</div>
                <div class="m-sub">Biên chế chính thức</div>
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

        # ── HÀNG 2: GIỚI TÍNH + TRÌNH ĐỘ CHUYÊN MÔN ──
        col_a, col_b = st.columns([1, 2])

        with col_a:
            df_gt = df[df['gioi_tinh'].isin(["Nam", "Nữ"])]['gioi_tinh'].value_counts().reset_index()
            df_gt.columns = ['Giới tính', 'Số lượng']
            if not df_gt.empty:
                fig_gt = px.pie(df_gt, values='Số lượng', names='Giới tính', hole=0.60,
                                color='Giới tính',
                                color_discrete_map={'Nam': '#1A2E4A', 'Nữ': '#C8102E'},
                                title='<b>Cơ cấu Giới tính</b>')
                fig_gt.update_traces(
                    textposition='outside', textinfo='label+percent+value',
                    textfont_size=13,
                    marker=dict(line=dict(color='#ffffff', width=3)),
                    pull=[0.04, 0.04]
                )
                fig_gt.add_annotation(
                    text=f"<b>{total}</b><br>CB", x=0.5, y=0.5, showarrow=False,
                    font=dict(size=20, color='#1A2E4A', family='Merriweather')
                )
                fig_gt.update_layout(
                    font_family="Source Sans 3",
                    title_font=dict(size=14, color='#1A2E4A'), title_x=0.5,
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(size=12)),
                    margin=dict(t=50, b=30, l=20, r=20), height=320
                )
                st.plotly_chart(fig_gt, use_container_width=True)

        with col_b:
            df_cm = df[df['trinh_do_chuyen_mon'] != 'Chưa xác định']['trinh_do_chuyen_mon'].value_counts().reset_index()
            df_cm.columns = ['Trình độ', 'Số lượng']
            df_cm = df_cm.sort_values('Số lượng', ascending=False)
            if not df_cm.empty:
                n = len(df_cm)
                colors_cm = [f'rgba({int(168 + (232-168)*i/max(n-1,1))},{int(12 + (32-12)*i/max(n-1,1))},{int(35 + (63-35)*i/max(n-1,1))},0.85)' for i in range(n)]
                fig_cm = go.Figure(go.Bar(
                    x=df_cm['Trình độ'], y=df_cm['Số lượng'],
                    marker_color=colors_cm,
                    marker_line=dict(color='#ffffff', width=1.5),
                    text=df_cm['Số lượng'], textposition='outside',
                    textfont=dict(size=14, color='#1A2E4A', family='Merriweather'),
                    hovertemplate='<b>%{x}</b><br>%{y} người<extra></extra>'
                ))
                fig_cm.update_layout(
                    title=dict(text='<b>Trình độ Chuyên môn</b>', x=0.5, font=dict(size=14, color='#1A2E4A')),
                    font_family="Source Sans 3",
                    plot_bgcolor='rgba(248,244,239,0.6)', paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(title=None, tickfont=dict(size=11, color='#3D3D5C'), gridcolor='rgba(0,0,0,0)', linecolor='#D4AF37', linewidth=1.5),
                    yaxis=dict(title='Số người', tickfont=dict(size=11), gridcolor='rgba(212,175,55,0.15)', zeroline=False),
                    margin=dict(t=55, b=20, l=40, r=20), height=320, bargap=0.35
                )
                st.plotly_chart(fig_cm, use_container_width=True)

        # ── HÀNG 3: NGẠCH CÔNG CHỨC + LÝ LUẬN CHÍNH TRỊ ──
        col_c, col_d = st.columns(2)

        with col_c:
            df_ng = df[df['ngach_cong_chuc'] != 'Chưa xác định']['ngach_cong_chuc'].value_counts().reset_index()
            df_ng.columns = ['Ngạch', 'Số lượng']
            df_ng = df_ng.sort_values('Số lượng', ascending=True)
            if not df_ng.empty:
                n2 = len(df_ng)
                colors_ng = [f'rgba({int(10 + (42-10)*i/max(n2-1,1))},{int(22 + (74-22)*i/max(n2-1,1))},{int(40 + (112-40)*i/max(n2-1,1))},0.85)' for i in range(n2)]
                fig_ng = go.Figure(go.Bar(
                    y=df_ng['Ngạch'], x=df_ng['Số lượng'], orientation='h',
                    marker_color=colors_ng,
                    marker_line=dict(color='#D4AF37', width=0.8),
                    text=df_ng['Số lượng'], textposition='outside',
                    textfont=dict(size=13, color='#1A2E4A', family='Merriweather'),
                    hovertemplate='<b>%{y}</b><br>%{x} người<extra></extra>'
                ))
                fig_ng.update_layout(
                    title=dict(text='<b>Ngạch Công chức hiện hưởng</b>', x=0.5, font=dict(size=14, color='#1A2E4A')),
                    font_family="Source Sans 3",
                    plot_bgcolor='rgba(248,244,239,0.6)', paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(title='Số người', tickfont=dict(size=11), gridcolor='rgba(212,175,55,0.15)', zeroline=False),
                    yaxis=dict(title=None, tickfont=dict(size=11, color='#1A2E4A'), gridcolor='rgba(0,0,0,0)', linecolor='#D4AF37', linewidth=1.5, automargin=True),
                    margin=dict(t=55, b=20, l=10, r=50), height=340, bargap=0.3
                )
                st.plotly_chart(fig_ng, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu ngạch công chức.")

        with col_d:
            thu_tu_ll = ["Chưa qua đào tạo", "Sơ cấp", "Trung cấp", "Cao cấp", "Cử nhân"]
            df_ll_raw = df[df['ly_luan_chinh_tri'] != 'Chưa xác định']['ly_luan_chinh_tri'].value_counts().reset_index()
            df_ll_raw.columns = ['Lý luận CT', 'Số lượng']
            df_ll_raw['Lý luận CT'] = pd.Categorical(df_ll_raw['Lý luận CT'], categories=thu_tu_ll, ordered=True)
            df_ll = df_ll_raw.sort_values('Lý luận CT', ascending=True).dropna()
            if not df_ll.empty:
                color_map_ll = {
                    "Chưa qua đào tạo": "rgba(180,180,180,0.7)",
                    "Sơ cấp":           "rgba(212,175,55,0.55)",
                    "Trung cấp":        "rgba(212,175,55,0.72)",
                    "Cao cấp":          "rgba(212,175,55,0.90)",
                    "Cử nhân":          "rgba(184,134,11,0.95)"
                }
                bar_colors_ll = [color_map_ll.get(str(x), "rgba(212,175,55,0.7)") for x in df_ll['Lý luận CT']]
                fig_ll = go.Figure(go.Bar(
                    y=df_ll['Lý luận CT'].astype(str), x=df_ll['Số lượng'], orientation='h',
                    marker_color=bar_colors_ll,
                    marker_line=dict(color='#8B6914', width=0.8),
                    text=df_ll['Số lượng'], textposition='outside',
                    textfont=dict(size=13, color='#1A2E4A', family='Merriweather'),
                    hovertemplate='<b>%{y}</b><br>%{x} người<extra></extra>'
                ))
                fig_ll.update_layout(
                    title=dict(text='<b>Trình độ Lý luận Chính trị</b>', x=0.5, font=dict(size=14, color='#1A2E4A')),
                    font_family="Source Sans 3",
                    plot_bgcolor='rgba(248,244,239,0.6)', paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(title='Số người', tickfont=dict(size=11), gridcolor='rgba(212,175,55,0.15)', zeroline=False),
                    yaxis=dict(title=None, tickfont=dict(size=11, color='#1A2E4A'), gridcolor='rgba(0,0,0,0)', linecolor='#D4AF37', linewidth=1.5),
                    margin=dict(t=55, b=20, l=10, r=50), height=340, bargap=0.3
                )
                st.plotly_chart(fig_ll, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu lý luận chính trị.")

        # ── HÀNG 4: HỌC VỊ + BẢNG TỔNG HỢP ──
        section_title("🎓", "CƠ CẤU HỌC VỊ VÀ BẢNG TỔNG HỢP")
        col_e, col_f = st.columns([1.4, 1])

        with col_e:
            df_hv = df[
                (df['hoc_vi'] != 'Chưa xác định') & (df['hoc_vi'].str.strip() != '') & (df['hoc_vi'] != '—')
            ]['hoc_vi'].value_counts().reset_index()
            df_hv.columns = ['Học vị', 'Số lượng']
            chua_hoc_vi = total - df_hv['Số lượng'].sum()
            if chua_hoc_vi > 0:
                df_hv = pd.concat([df_hv, pd.DataFrame([{'Học vị': 'Đại học / Chưa có học vị', 'Số lượng': chua_hoc_vi}])], ignore_index=True)

            palette_hv = ['#0A1628', '#C8102E', '#D4AF37', '#1A2E4A', '#2A4A70', '#A00C23', '#B8860B', '#6B7280']
            fig_hv = go.Figure(go.Pie(
                labels=df_hv['Học vị'], values=df_hv['Số lượng'], hole=0.55,
                marker=dict(colors=palette_hv[:len(df_hv)], line=dict(color='#ffffff', width=3)),
                textinfo='label+percent', textposition='outside',
                textfont=dict(size=12, color='#1A2E4A'),
                pull=[0.04] * len(df_hv),
                hovertemplate='<b>%{label}</b><br>%{value} người (%{percent})<extra></extra>'
            ))
            fig_hv.add_annotation(
                text="<b>Học vị</b>", x=0.5, y=0.5, showarrow=False,
                font=dict(size=13, color='#1A2E4A', family='Source Sans 3')
            )
            fig_hv.update_layout(
                title=dict(text='<b>Cơ cấu Học vị cán bộ</b>', x=0.5, font=dict(size=14, color='#1A2E4A')),
                font_family="Source Sans 3",
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                showlegend=True,
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02,
                            font=dict(size=11, color='#1A2E4A'),
                            bgcolor='rgba(253,248,240,0.8)', bordercolor='#D4AF37', borderwidth=1),
                margin=dict(t=55, b=20, l=20, r=160), height=360
            )
            st.plotly_chart(fig_hv, use_container_width=True)

        with col_f:
            tyle_dang = round(dang / total * 100) if total else 0
            cao_cap_cn = len(df[df['ly_luan_chinh_tri'].isin(['Cao cấp', 'Cử nhân'])])
            st.markdown(f"""
            <div style="background:#fff;border-radius:12px;padding:22px 24px;
                border-left:5px solid #D4AF37;box-shadow:0 4px 20px rgba(0,0,0,0.08);margin-top:8px;">
                <div style="font-family:'Merriweather',serif;font-size:13px;font-weight:700;
                    color:#0A1628;letter-spacing:1px;text-transform:uppercase;
                    border-bottom:1px dashed rgba(212,175,55,0.4);padding-bottom:10px;margin-bottom:14px;">
                    📋 Bảng Tổng hợp Chỉ tiêu
                </div>
                <table style="width:100%;border-collapse:collapse;font-size:13px;">
                    <tr style="background:rgba(200,16,46,0.05);">
                        <td style="padding:9px 10px;color:#6B7280;font-weight:600;">👥 Tổng biên chế</td>
                        <td style="padding:9px 10px;text-align:right;font-weight:900;color:#C8102E;font-family:'Merriweather',serif;font-size:18px;">{total}</td>
                    </tr>
                    <tr>
                        <td style="padding:9px 10px;color:#6B7280;font-weight:600;">👨 Cán bộ Nam</td>
                        <td style="padding:9px 10px;text-align:right;font-weight:700;color:#1A2E4A;">{nam} &nbsp;<span style="font-size:11px;color:#9CA3AF;">({round(nam/total*100) if total else 0}%)</span></td>
                    </tr>
                    <tr style="background:rgba(212,175,55,0.05);">
                        <td style="padding:9px 10px;color:#6B7280;font-weight:600;">👩 Cán bộ Nữ</td>
                        <td style="padding:9px 10px;text-align:right;font-weight:700;color:#C8102E;">{nu} &nbsp;<span style="font-size:11px;color:#9CA3AF;">({tyle_nu}%)</span></td>
                    </tr>
                    <tr>
                        <td style="padding:9px 10px;color:#6B7280;font-weight:600;">☭ Đảng viên</td>
                        <td style="padding:9px 10px;text-align:right;font-weight:700;color:#1A2E4A;">{dang} &nbsp;<span style="font-size:11px;color:#9CA3AF;">({tyle_dang}%)</span></td>
                    </tr>
                    <tr style="background:rgba(200,16,46,0.05);">
                        <td style="padding:9px 10px;color:#6B7280;font-weight:600;">🎓 Thạc sĩ trở lên</td>
                        <td style="padding:9px 10px;text-align:right;font-weight:700;color:#2E7D32;">{thac_si} &nbsp;<span style="font-size:11px;color:#9CA3AF;">({round(thac_si/total*100) if total else 0}%)</span></td>
                    </tr>
                    <tr style="background:rgba(212,175,55,0.05);">
                        <td style="padding:9px 10px;color:#6B7280;font-weight:600;">🏛️ LLCT Cao cấp / CN</td>
                        <td style="padding:9px 10px;text-align:right;font-weight:700;color:#B8860B;">{cao_cap_cn} người</td>
                    </tr>
                    <tr>
                        <td style="padding:9px 10px;color:#6B7280;font-weight:600;">📅 Cập nhật</td>
                        <td style="padding:9px 10px;text-align:right;font-weight:500;color:#9CA3AF;font-size:11px;">{datetime.now().strftime('%d/%m/%Y %H:%M')}</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

        # ── DANH SÁCH ──
        section_title("📋", "DANH SÁCH CÁN BỘ, CÔNG CHỨC")
        cols_show = ['id','ho_ten','chuc_vu','don_vi','ngay_sinh','gioi_tinh','hoc_vi','trinh_do_chuyen_mon','ly_luan_chinh_tri','ngach_cong_chuc']
        df_show = df[[c for c in cols_show if c in df.columns]].rename(columns={
            'id':'Mã CB','ho_ten':'Họ và tên','chuc_vu':'Chức vụ','don_vi':'Đơn vị',
            'ngay_sinh':'Ngày sinh','gioi_tinh':'Giới tính','hoc_vi':'Học vị',
            'trinh_do_chuyen_mon':'Chuyên môn','ly_luan_chinh_tri':'Lý luận CT','ngach_cong_chuc':'Ngạch CC'
        })
        st.dataframe(df_show, hide_index=True, use_container_width=True)
        csv_data = df_show.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(
            label="📥  XUẤT DANH SÁCH (.CSV)",
            data=csv_data,
            file_name=f"DanhSach_CBCC_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# ==========================================
# MODULE 2: ADMIN DUYỆT TÀI KHOẢN
# ==========================================
elif menu == "🛡️ Admin: Duyệt Tài khoản":
    section_title("🛡️", "QUẢN TRỊ TÀI KHOẢN HỆ THỐNG")
    tk_data = supabase.table("tai_khoan").select("*").execute().data
    if not tk_data:
        st.info("Chưa có tài khoản nào trong hệ thống.")
    else:
        df_tk = pd.DataFrame(tk_data)
        tab_cd, tab_hd = st.tabs(["⏳  Chờ phê duyệt", "✅  Tài khoản hoạt động"])
        with tab_cd:
            df_choduyet = df_tk[df_tk['trang_thai'] == 'Chờ duyệt']
            if df_choduyet.empty:
                st.success("🎉 Không có yêu cầu nào đang chờ phê duyệt.")
            else:
                for idx, row in df_choduyet.iterrows():
                    with st.expander(f"👤  {row['ho_ten']}  ({row['ma_cbcc']})  —  {row['chuc_vu']}"):
                        st.markdown(f"<div style='background:#f8f4ef;border-radius:8px;padding:14px;margin-bottom:12px;'><b>Đơn vị:</b> {row['don_vi']}<br><b>Chức vụ:</b> {row['chuc_vu']}</div>", unsafe_allow_html=True)
                        c_duyet, c_xoa = st.columns(2)
                        if c_duyet.button("✅  PHÊ DUYỆT", key=f"duyet_{row['ma_cbcc']}", use_container_width=True):
                            supabase.table("tai_khoan").update({"trang_thai": "Hoạt động"}).eq("ma_cbcc", row['ma_cbcc']).execute()
                            try:
                                if len(supabase.table("ho_so_cbcc").select("id").eq("id", row['ma_cbcc']).execute().data) == 0:
                                    supabase.table("ho_so_cbcc").insert({"id": row['ma_cbcc'], "ho_ten": row['ho_ten'], "chuc_vu": row['chuc_vu'], "don_vi": row['don_vi'], "quoc_tich": "Việt Nam", "dan_toc": "Kinh"}).execute()
                            except Exception: pass
                            st.success("✅ Đã phê duyệt."); st.rerun()
                        if c_xoa.button("❌  TỪ CHỐI", key=f"xoa_cd_{row['ma_cbcc']}", use_container_width=True):
                            supabase.table("tai_khoan").delete().eq("ma_cbcc", row['ma_cbcc']).execute()
                            st.success("Đã từ chối."); st.rerun()
        with tab_hd:
            df_hd = df_tk[df_tk['trang_thai'] == 'Hoạt động']
            st.dataframe(df_hd[['ma_cbcc','ho_ten','chuc_vu','don_vi','phan_quyen']].rename(columns={'ma_cbcc':'Mã','ho_ten':'Họ tên','chuc_vu':'Chức vụ','don_vi':'Đơn vị','phan_quyen':'Quyền'}), hide_index=True, use_container_width=True)
            st.markdown("---")
            ds_hd = (df_hd['ma_cbcc'] + " — " + df_hd['ho_ten']).tolist()
            c_rs, c_del = st.columns(2)
            with c_rs:
                section_title("🔑", "Tra cứu Mật khẩu")
                rs_ma = st.selectbox("Chọn tài khoản:", ds_hd, key="rs_sel")
                if st.button("👁️  XEM MẬT KHẨU", use_container_width=True):
                    ma_xem = rs_ma.split(" — ")[0]
                    mk_data = supabase.table("tai_khoan").select("mat_khau").eq("ma_cbcc", ma_xem).execute().data
                    if mk_data: st.info(f"🔐 Mật khẩu **{rs_ma.split(' — ')[1]}** ({ma_xem}): `{mk_data[0]['mat_khau']}`")
            with c_del:
                section_title("❌", "Xóa Tài khoản")
                del_ma = st.selectbox("Chọn:", ["— Chọn —"] + ds_hd, key="del_sel")
                if st.button("🗑️  XÁC NHẬN XÓA", use_container_width=True) and del_ma != "— Chọn —":
                    ma_xoa = del_ma.split(" — ")[0]
                    if ma_xoa.upper() == "ADMIN": st.error("⚠️ Không thể xóa Admin gốc!")
                    else:
                        supabase.table("tai_khoan").delete().eq("ma_cbcc", ma_xoa).execute()
                        supabase.table("ho_so_cbcc").delete().eq("id", ma_xoa).execute()
                        st.success(f"✅ Đã xóa {ma_xoa}."); st.rerun()

# ==========================================
# MODULE 3: XEM HỒ SƠ
# ==========================================
elif menu in ["🔍 Tra cứu & Xem Hồ sơ", "🔍 Hồ sơ của tôi"]:
    section_title("🔍", "TRA CỨU & XEM HỒ SƠ CÁN BỘ")
    if df_hoso.empty:
        st.warning("📭 Cơ sở dữ liệu trống.")
    else:
        ma_chon = ""
        if is_admin:
            tu_khoa = st.text_input("🔎  Tìm kiếm theo Tên hoặc Mã CBCC:", placeholder="Nhập từ khóa…")
            if not tu_khoa.strip():
                st.info("👆 Nhập từ khóa để tìm kiếm.")
            else:
                df_kq = df_hoso[df_hoso.apply(lambda r: r.astype(str).str.contains(tu_khoa.strip(), case=False).any(), axis=1)]
                if df_kq.empty:
                    st.warning(f"❌ Không tìm thấy khớp với **'{tu_khoa}'**.")
                else:
                    ds_hien = (df_kq['ho_ten'] + " — " + df_kq['chuc_vu'] + " (" + df_kq['id'] + ")").tolist()
                    chon = st.selectbox("👉 Chọn cán bộ:", ds_hien)
                    if chon: ma_chon = chon.split("(")[-1].replace(")", "").strip()
        else:
            ma_chon = st.session_state["ma_cbcc"]
            if df_hoso[df_hoso['id'] == ma_chon].empty:
                st.warning("❌ Bạn chưa có hồ sơ."); ma_chon = ""

        if ma_chon:
            info = df_hoso[df_hoso['id'] == ma_chon].iloc[0].fillna("—")
            col_btn, col_dl = st.columns([1, 1])
            if col_btn.button("✏️  Chỉnh sửa hồ sơ này", use_container_width=True):
                st.session_state["edit_target_id"] = info['id']
                st.session_state["menu_selection"] = "➕ Admin: Cập nhật Hồ sơ (Tất cả)" if is_admin else "➕ Cập nhật Hồ sơ cá nhân"
                st.rerun()
            df_ct = pd.DataFrame(supabase.table("lich_su_cong_tac").select("tu_ngay,den_ngay,vi_tri,don_vi,quyet_dinh_so").eq("ma_cbcc", ma_chon).order("id").execute().data)
            df_l  = pd.DataFrame(supabase.table("dien_bien_luong").select("ngay_quyet_dinh,bac_luong,he_so,quyet_dinh_so").eq("ma_cbcc", ma_chon).order("id").execute().data)
            df_kt = pd.DataFrame(supabase.table("khen_thuong_ky_luat").select("ngay_quyet_dinh,loai,noi_dung,quyet_dinh_so").eq("ma_cbcc", ma_chon).order("id").execute().data)
            html_data = create_html_export(info, df_ct, df_l, df_kt)
            col_dl.download_button(label="📥  TẢI SƠ YẾU LÝ LỊCH (2C-TW)", data=html_data, file_name=f"SYLL_2C_{info['ho_ten'].replace(' ','_')}.html", mime="text/html", use_container_width=True)

            st.markdown(f"""
            <div class="profile-card">
                <div class="profile-badge">MẪU SƠ YẾU LÝ LỊCH CÁN BỘ 2C-TW</div>
                <div class="profile-name">{info['ho_ten']}</div>
                <div class="profile-title">🏛️ {info.get('chuc_vu','—')} &nbsp;|&nbsp; {info.get('don_vi','—')}</div>
                <hr class="profile-divider">
                <div class="profile-info-grid">
                    <div class="info-item"><span class="lbl">Mã cán bộ</span><span class="val">{info.get('id','—')}</span></div>
                    <div class="info-item"><span class="lbl">Ngày sinh</span><span class="val">{info.get('ngay_sinh','—')}</span></div>
                    <div class="info-item"><span class="lbl">Giới tính</span><span class="val">{info.get('gioi_tinh','—')}</span></div>
                    <div class="info-item"><span class="lbl">Quốc tịch</span><span class="val">{info.get('quoc_tich','Việt Nam')}</span></div>
                    <div class="info-item"><span class="lbl">Dân tộc</span><span class="val">{info.get('dan_toc','—')}</span></div>
                    <div class="info-item"><span class="lbl">Quê quán</span><span class="val">{info.get('que_quan','—')}</span></div>
                    <div class="info-item"><span class="lbl">Khai sinh</span><span class="val">{info.get('noi_khai_sinh','—')}</span></div>
                    <div class="info-item"><span class="lbl">Thường trú</span><span class="val">{info.get('thuong_tru','—')}</span></div>
                    <div class="info-item"><span class="lbl">Nơi ở hiện nay</span><span class="val">{info.get('noi_o_hien_nay','—')}</span></div>
                    <div class="info-item"><span class="lbl">Nghề nghiệp</span><span class="val">{info.get('nghe_nghiep_ht','—')}</span></div>
                    <div class="info-item"><span class="lbl">Chức vụ Đảng</span><span class="val">{info.get('chuc_vu_dang','—')}</span></div>
                    <div class="info-item"><span class="lbl">Ngạch công chức</span><span class="val">{info.get('ngach_cong_chuc','—')}</span></div>
                    <div class="info-item"><span class="lbl">Giáo dục PT</span><span class="val">{info.get('giao_duc_pt','—')}</span></div>
                    <div class="info-item"><span class="lbl">Chuyên môn</span><span class="val">{info.get('trinh_do_chuyen_mon','—')}</span></div>
                    <div class="info-item"><span class="lbl">Học vị</span><span class="val">{info.get('hoc_vi','—')}</span></div>
                    <div class="info-item"><span class="lbl">Lý luận CT</span><span class="val">{info.get('ly_luan_chinh_tri','—')}</span></div>
                    <div class="info-item"><span class="lbl">Ngoại ngữ</span><span class="val">{info.get('ngoai_ngu','—')}</span></div>
                    <div class="info-item"><span class="lbl">Tin học</span><span class="val">{info.get('tin_hoc','—')}</span></div>
                    <div class="info-item" style="grid-column:span 3;"><span class="lbl">Đảng vụ</span><span class="val">Kết nạp: {info.get('ngay_vao_dang','—')} &nbsp;|&nbsp; Chính thức: {info.get('ngay_chinh_thuc','—')}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            section_title("📑", "THÔNG TIN CHI TIẾT")
            t_ct, t_l, t_kt = st.tabs(["🏢  Lịch sử công tác","💰  Diễn biến lương","🏆  Khen thưởng & Kỷ luật"])
            with t_ct:
                if not df_ct.empty: st.dataframe(df_ct.rename(columns={'tu_ngay':'Từ ngày','den_ngay':'Đến ngày','vi_tri':'Vị trí','don_vi':'Đơn vị','quyet_dinh_so':'Quyết định số'}), hide_index=True, use_container_width=True)
                else: st.info("Chưa có dữ liệu.")
            with t_l:
                if not df_l.empty: st.dataframe(df_l.rename(columns={'ngay_quyet_dinh':'Ngày QĐ','bac_luong':'Bậc lương','he_so':'Hệ số','quyet_dinh_so':'Quyết định số'}), hide_index=True, use_container_width=True)
                else: st.info("Chưa có dữ liệu.")
            with t_kt:
                if not df_kt.empty: st.dataframe(df_kt.rename(columns={'ngay_quyet_dinh':'Ngày QĐ','loai':'Loại','noi_dung':'Nội dung','quyet_dinh_so':'Quyết định số'}), hide_index=True, use_container_width=True)
                else: st.info("Chưa có dữ liệu.")

# ==========================================
# MODULE 4: NHẬP LIỆU
# ==========================================
elif menu in ["➕ Cập nhật Hồ sơ cá nhân", "➕ Admin: Cập nhật Hồ sơ (Tất cả)"]:
    section_title("📝", "TRUNG TÂM NHẬP LIỆU HỒ SƠ")

    if is_admin:
        kieu_nhap = st.radio("Chế độ:", ["Chỉnh sửa hồ sơ hiện có", "Thêm cán bộ mới"], horizontal=True)
        if kieu_nhap == "Chỉnh sửa hồ sơ hiện có":
            ds_cbcc = (df_hoso['id'] + " — " + df_hoso['ho_ten']).tolist() if not df_hoso.empty else []
            idx_def = 0
            if st.session_state["edit_target_id"] and ds_cbcc:
                for i, val in enumerate(ds_cbcc):
                    if val.startswith(st.session_state["edit_target_id"]): idx_def = i; break
            chon_cb = st.selectbox("Chọn cán bộ:", ds_cbcc, index=idx_def) if ds_cbcc else ""
            target_id = chon_cb.split(" — ")[0] if chon_cb else ""
        else:
            target_id = st.text_input("Mã CBCC mới:", placeholder="VD: CV999").strip().upper()
    else:
        target_id = st.session_state["ma_cbcc"]
        st.info(f"📋 Đang cập nhật hồ sơ: **{target_id}**")

    ex_data = {}
    if target_id and not df_hoso.empty:
        match = df_hoso[df_hoso['id'] == target_id]
        if not match.empty: ex_data = match.iloc[0].fillna("").to_dict()

    tab_chinh, tab_ct, tab_luong, tab_kt = st.tabs([
        "👤  Hồ sơ chính","🏢  Lịch sử công tác","💰  Diễn biến lương","🏆  Khen thưởng / Kỷ luật"
    ])

    with tab_chinh:
        with st.form("form_ho_so", clear_on_submit=False):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**📋 Thông tin định danh**")
                ho_ten = st.text_input("Họ và tên *", value=ex_data.get("ho_ten",""))
                ngay_sinh = st.text_input("Ngày sinh (DD/MM/YYYY)", value=ex_data.get("ngay_sinh",""))
                gioi_tinh = st.selectbox("Giới tính", DS_GIOI_TINH, index=get_idx(DS_GIOI_TINH, ex_data.get("gioi_tinh","Nam")))
                quoc_tich = st.text_input("Quốc tịch", value=ex_data.get("quoc_tich","Việt Nam"))
                dan_toc = st.text_input("Dân tộc", value=ex_data.get("dan_toc","Kinh"))
            with c2:
                st.markdown("**📍 Địa giới hành chính**")
                que_quan = st.text_input("Quê quán", value=ex_data.get("que_quan",""))
                noi_khai_sinh = st.text_input("Nơi đăng ký khai sinh", value=ex_data.get("noi_khai_sinh",""))
                thuong_tru = st.text_input("Nơi đăng ký thường trú", value=ex_data.get("thuong_tru",""))
                noi_o_hien_nay = st.text_input("Nơi ở hiện nay", value=ex_data.get("noi_o_hien_nay",""))
            with c3:
                st.markdown("**👔 Nghiệp vụ & Đảng vụ**")
                don_vi = st.selectbox("Đơn vị công tác *", DS_DON_VI, index=get_idx(DS_DON_VI, ex_data.get("don_vi","Lãnh đạo Ban")))
                chuc_vu = st.selectbox("Chức vụ chính quyền", DS_CHUC_VU, index=get_idx(DS_CHUC_VU, ex_data.get("chuc_vu","Chuyên viên")))
                chuc_vu_dang = st.text_input("Chức vụ trong Đảng", value=ex_data.get("chuc_vu_dang",""))
                nghe_nghiep_ht = st.text_input("Nghề nghiệp hiện nay", value=ex_data.get("nghe_nghiep_ht",""))
                ngach = st.text_input("Ngạch công chức", value=ex_data.get("ngach_cong_chuc",""))

            st.write("---")
            st.markdown("**🎓 Trình độ học vấn**")
            cx1, cx2, cx3, cx4, cx5 = st.columns(5)
            giao_duc_pt = cx1.text_input("Giáo dục PT", value=ex_data.get("giao_duc_pt",""))
            chuyen_mon = cx2.text_input("Trình độ chuyên môn", value=ex_data.get("trinh_do_chuyen_mon",""))
            hoc_vi = cx3.text_input("Học vị", value=ex_data.get("hoc_vi",""))
            ngoai_ngu = cx4.text_input("Ngoại ngữ", value=ex_data.get("ngoai_ngu",""))
            tin_hoc = cx5.text_input("Tin học", value=ex_data.get("tin_hoc",""))

            st.write("---")
            st.markdown("**☭ Lịch sử Đảng viên**")
            cl1, cl2, cl3 = st.columns(3)
            ly_luan = cl1.selectbox("Lý luận chính trị", DS_LY_LUAN, index=get_idx(DS_LY_LUAN, ex_data.get("ly_luan_chinh_tri","Chưa qua đào tạo")))
            ngay_ket_nap = cl2.text_input("Ngày kết nạp Đảng", value=ex_data.get("ngay_vao_dang",""))
            ngay_chinh_thuc = cl3.text_input("Ngày chính thức", value=ex_data.get("ngay_chinh_thuc",""))

            if st.form_submit_button("💾  LƯU TOÀN BỘ HỒ SƠ CHÍNH", use_container_width=True):
                if not target_id or not ho_ten:
                    st.error("⚠️ Bắt buộc phải có Mã CBCC và Họ tên.")
                else:
                    data = {
                        "id": target_id, "ho_ten": ho_ten.title(), "ngay_sinh": ngay_sinh,
                        "gioi_tinh": gioi_tinh, "quoc_tich": quoc_tich, "dan_toc": dan_toc,
                        "que_quan": que_quan, "noi_khai_sinh": noi_khai_sinh, "thuong_tru": thuong_tru, "noi_o_hien_nay": noi_o_hien_nay,
                        "don_vi": don_vi, "chuc_vu": chuc_vu, "chuc_vu_dang": chuc_vu_dang, "nghe_nghiep_ht": nghe_nghiep_ht, "ngach_cong_chuc": ngach,
                        "giao_duc_pt": giao_duc_pt, "trinh_do_chuyen_mon": chuyen_mon, "hoc_vi": hoc_vi, "ngoai_ngu": ngoai_ngu, "tin_hoc": tin_hoc,
                        "ly_luan_chinh_tri": ly_luan, "ngay_vao_dang": ngay_ket_nap, "ngay_chinh_thuc": ngay_chinh_thuc
                    }
                    supabase.table("ho_so_cbcc").upsert(data).execute()
                    st.session_state["edit_target_id"] = ""
                    st.success("✅ Đã lưu thành công hồ sơ lên CSDL.")
                    st.cache_data.clear()
                    st.rerun()

    def render_sub_tab(table_name, form_key, title_btn, fields_form):
        with st.form(f"form_{form_key}"):
            st.markdown(f"**Thêm mới {title_btn}**")
            vals = {}
            cols_form = st.columns(2)
            for i, (fname, flabel) in enumerate(fields_form):
                with cols_form[i % 2]: vals[fname] = st.text_input(flabel)
            if st.form_submit_button(f"➕  THÊM MỚI {title_btn.upper()}", use_container_width=True):
                supabase.table(table_name).insert({"ma_cbcc": target_id, **vals}).execute()
                st.success("✅ Đã thêm."); st.rerun()

        section_title("🔧", "Chỉnh sửa / Xóa dữ liệu cũ")
        try: df_sub = pd.DataFrame(supabase.table(table_name).select("*").eq("ma_cbcc", target_id).order("id").execute().data)
        except: df_sub = pd.DataFrame()

        if not df_sub.empty:
            edited = st.data_editor(df_sub.drop(columns=['ma_cbcc','created_at'], errors='ignore'), hide_index=True, use_container_width=True, disabled=["id"])
            cs, cd = st.columns([3, 1])
            if cs.button(f"💾  LƯU — {title_btn.upper()}", use_container_width=True, key=f"save_{form_key}"):
                upd = edited.copy(); upd['ma_cbcc'] = target_id
                supabase.table(table_name).upsert(upd.fillna("").to_dict(orient="records")).execute()
                st.success("✅ Đã lưu."); st.rerun()
            del_id = cd.selectbox("ID xóa:", ["—"] + df_sub['id'].astype(str).tolist(), label_visibility="collapsed", key=f"del_sel_{form_key}")
            if cd.button("🗑️  XÓA", key=f"del_btn_{form_key}", use_container_width=True) and del_id != "—":
                supabase.table(table_name).delete().eq("id", del_id).execute(); st.rerun()
        else: st.info("Chưa có dữ liệu.")

    with tab_ct:
        render_sub_tab("lich_su_cong_tac","cong_tac","Lịch sử công tác",[("tu_ngay","Từ ngày"),("den_ngay","Đến ngày"),("vi_tri","Vị trí / Chức danh"),("don_vi","Đơn vị công tác"),("quyet_dinh_so","Quyết định số")])
    with tab_luong:
        render_sub_tab("dien_bien_luong","luong","Diễn biến lương",[("ngay_quyet_dinh","Ngày quyết định"),("bac_luong","Bậc lương"),("he_so","Hệ số"),("quyet_dinh_so","Quyết định số")])

    with tab_kt:
        with st.form("form_kt"):
            st.markdown("**Thêm mới Khen thưởng / Kỷ luật**")
            c1, c2 = st.columns(2)
            ngay_qd = c1.text_input("Ngày quyết định")
            loai = c2.selectbox("Loại", ["Khen thưởng", "Kỷ luật"])
            noi_dung = st.text_area("Nội dung", height=80)
            qd_so = st.text_input("Quyết định số")
            if st.form_submit_button("➕  THÊM MỚI", use_container_width=True):
                supabase.table("khen_thuong_ky_luat").insert({"ma_cbcc": target_id, "ngay_quyet_dinh": ngay_qd, "loai": loai, "noi_dung": noi_dung, "quyet_dinh_so": qd_so}).execute()
                st.success("✅ Đã thêm."); st.rerun()
        section_title("🔧","Chỉnh sửa / Xóa")
        df_kt2 = pd.DataFrame(supabase.table("khen_thuong_ky_luat").select("*").eq("ma_cbcc", target_id).order("id").execute().data)
        if not df_kt2.empty:
            edited_kt = st.data_editor(df_kt2.drop(columns=['ma_cbcc','created_at'], errors='ignore'), hide_index=True, use_container_width=True, disabled=["id"])
            cs3, cd3 = st.columns([3, 1])
            if cs3.button("💾  LƯU KHEN THƯỞNG / KỶ LUẬT", use_container_width=True, key="save_kt"):
                upd = edited_kt.copy(); upd['ma_cbcc'] = target_id
                supabase.table("khen_thuong_ky_luat").upsert(upd.fillna("").to_dict(orient="records")).execute()
                st.success("✅ Đã lưu."); st.rerun()
            del_kt = cd3.selectbox("ID xóa:", ["—"] + df_kt2['id'].astype(str).tolist(), label_visibility="collapsed", key="del_kt")
            if cd3.button("🗑️  XÓA", key="del_btn_kt", use_container_width=True) and del_kt != "—":
                supabase.table("khen_thuong_ky_luat").delete().eq("id", del_kt).execute(); st.rerun()
