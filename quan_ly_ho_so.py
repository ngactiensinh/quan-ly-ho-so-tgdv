"""
HỆ THỐNG QUẢN LÝ HỒ SƠ CÁN BỘ, CÔNG CHỨC - PHIÊN BẢN V6.3 (MOBILE FIX)
Đã cập nhật: Phục hồi nút mở Sidebar trên giao diện điện thoại di động
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
# 1. CẤU HÌNH TRANG (BẮT BUỘC Ở ĐẦU)
# ==========================================
st.set_page_config(
    page_title="Hồ sơ CBCC - Ban Tuyên giáo & Dân vận Tuyên Quang",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="auto"
)

# Thêm CSS ép sidebar luôn hiển thị nút mở rộng và phục hồi Header trên Mobile
st.markdown("""
<style>
    /* 1. Đưa nút menu về đúng vị trí chuẩn (góc trên bên trái) */
    [data-testid="collapsedControl"] {
        position: fixed !important;
        top: 15px !important;
        left: 15px !important;
        z-index: 999999 !important;
        background-color: #0A1628 !important; /* Navy */
        color: #D4AF37 !important;            /* Gold */
        width: 45px !important;
        height: 45px !important;
        border-radius: 8px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
    }

    /* 2. Làm nút menu nổi bật và dễ bấm */
    [data-testid="collapsedControl"] svg {
        fill: #D4AF37 !important;
        width: 25px !important;
        height: 25px !important;
    }

    /* 3. Đảm bảo sidebar không bị đè bởi bất kỳ thứ gì khác */
    [data-testid="stSidebar"] {
        z-index: 9999999 !important;
    }

    /* 4. Giữ Header sạch sẽ, không bị vướng nút menu */
    .gov-header {
        padding-left: 70px !important; /* Đẩy text sang phải để không chạm nút menu */
        position: relative;
    }

    /* Ẩn bớt các thành phần thừa */
    #MainMenu, footer { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CẤU HÌNH SUPABASE (BẢO MẬT BẰNG SECRETS)
# ==========================================
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("⚠️ Lỗi kết nối cơ sở dữ liệu. Sếp vui lòng kiểm tra lại cấu hình Secrets trên Streamlit nhé!")
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
    else:
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
# 4. CSS PHONG CÁCH CHÍNH TRỊ - ĐỎ & VÀNG
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700;900&family=Source+Sans+3:wght@400;500;600;700&display=swap');

    :root {
        --red-primary: #C8102E; --red-dark: #A00C23; --red-light: #E8203F;
        --gold: #D4AF37; --gold-light: #F0D060; --navy: #0A1628;
        --navy-mid: #1A2E4A; --navy-light: #2A4A70; --cream: #FDF8F0;
        --off-white: #F5F1E8; --text-dark: #1A1A2E; --text-mid: #3D3D5C;
        --text-light: #6B7280; --border: #D4AF3740;
        --shadow-sm: 0 2px 8px rgba(0,0,0,0.08); --shadow-md: 0 4px 20px rgba(0,0,0,0.12); --shadow-lg: 0 8px 40px rgba(0,0,0,0.16);
    }
    html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; color: var(--text-dark); }
    .stApp { background: linear-gradient(160deg, #f8f4ef 0%, #ede8e0 50%, #f5f0e8 100%); }

    /* ---- SIDEBAR ---- */
    [data-testid="stSidebar"] { background: linear-gradient(180deg, var(--navy) 0%, var(--navy-mid) 60%, #0D1E35 100%) !important; border-right: 3px solid var(--gold) !important; }
    [data-testid="stSidebar"] * { color: #e8dfc8 !important; }
    [data-testid="stSidebar"] .stRadio label { color: #c8bfa8 !important; padding: 10px 14px; border-radius: 6px; display: block; transition: all 0.2s; font-weight: 500; font-size: 14px; border-left: 3px solid transparent; }
    [data-testid="stSidebar"] .stRadio label:hover { background: rgba(212,175,55,0.12) !important; border-left-color: var(--gold) !important; color: var(--gold-light) !important; }
    [data-testid="stSidebar"] [aria-checked="true"] + label, [data-testid="stSidebar"] .stRadio [data-checked="true"] label { background: rgba(200,16,46,0.25) !important; border-left-color: var(--red-primary) !important; color: #fff !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(212,175,55,0.25) !important; }

    /* ---- HEADER ---- */
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

    /* ---- DATA TABLE OVERRIDE ---- */
    [data-testid="stDataFrame"] thead th { background-color: var(--navy) !important; color: #fff !important; font-weight: 700 !important; font-size: 13px !important; letter-spacing: 0.5px !important; }
    [data-testid="stDataFrame"] tbody tr:hover { background: rgba(200,16,46,0.04) !important; }

    /* ---- FORMS ---- */
    div[data-testid="stForm"] { background: #fff; border: 1px solid rgba(212,175,55,0.25); border-top: 3px solid var(--gold); border-radius: 10px; padding: 24px !important; box-shadow: var(--shadow-sm); }
    .stTextInput input, .stSelectbox select, .stTextArea textarea { border: 1.5px solid #e0d8cc !important; border-radius: 6px !important; background: var(--cream) !important; font-family: 'Source Sans 3', sans-serif !important; transition: border-color 0.2s !important; }
    .stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus { border-color: var(--red-primary) !important; box-shadow: 0 0 0 3px rgba(200,16,46,0.08) !important; }

    /* ---- BUTTONS ---- */
    div[data-testid="stButton"] > button, div[data-testid="stFormSubmitButton"] > button, div[data-testid="stDownloadButton"] > button { background: linear-gradient(135deg, var(--red-primary), var(--red-dark)) !important; color: #fff !important; border: none !important; font-family: 'Source Sans 3', sans-serif !important; font-weight: 700 !important; font-size: 13px !important; letter-spacing: 0.8px !important; text-transform: uppercase !important; padding: 10px 20px !important; border-radius: 6px !important; box-shadow: 0 3px 12px rgba(200,16,46,0.3) !important; transition: all 0.25s ease !important; }
    div[data-testid="stButton"] > button:hover, div[data-testid="stFormSubmitButton"] > button:hover, div[data-testid="stDownloadButton"] > button:hover { background: linear-gradient(135deg, var(--red-light), var(--red-primary)) !important; box-shadow: 0 5px 18px rgba(200,16,46,0.4) !important; transform: translateY(-1px) !important; }

    /* ---- TABS ---- */
    .stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 2px solid rgba(200,16,46,0.15) !important; gap: 4px !important; }
    .stTabs [data-baseweb="tab"] { font-family: 'Source Sans 3', sans-serif !important; font-weight: 600 !important; font-size: 13px !important; color: var(--text-mid) !important; padding: 10px 18px !important; border-radius: 6px 6px 0 0 !important; border: none !important; background: transparent !important; transition: all 0.2s !important; }
    .stTabs [aria-selected="true"] { color: var(--red-primary) !important; background: rgba(200,16,46,0.06) !important; border-bottom: 3px solid var(--red-primary) !important; }

    /* ---- EXPANDER ---- */
    [data-testid="stExpander"] summary { font-weight: 600 !important; color: var(--navy-mid) !important; background: var(--off-white) !important; border-left: 4px solid var(--gold) !important; border-radius: 6px !important; padding: 12px 16px !important; }
    
    /* ---- ĐÃ FIX LỖI ẨN HEADER TRÊN ĐIỆN THOẠI ---- */
    #MainMenu, footer { visibility: hidden !important; }
    header { background-color: transparent !important; }
    .block-container { padding-top: 24px !important; padding-bottom: 40px !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 5. SESSION STATE
# ==========================================
defaults = {"logged_in": False, "ma_cbcc": "", "ho_ten": "", "role": "User", "edit_target_id": "", "menu_selection": ""}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==========================================
# 6. MÀN HÌNH ĐĂNG NHẬP
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown(f"""
    <div style="max-width:900px; margin: 0 auto 32px auto;">
        <div style="background: linear-gradient(135deg, var(--navy, #0A1628) 0%, #1A2E4A 50%, #C8102E 100%);
            padding: 28px 36px; border-radius: 14px; display:flex; align-items:center;
            gap: 24px; box-shadow: 0 8px 40px rgba(0,0,0,0.18); border-bottom: 4px solid #D4AF37;
            position:relative; overflow:hidden;">
            <div style="position:absolute;top:0;left:0;right:0;bottom:0;
                background: repeating-linear-gradient(45deg,transparent,transparent 40px,
                rgba(212,175,55,0.03) 40px,rgba(212,175,55,0.03) 41px);"></div>
            <div style="position:relative;">{get_logo_html("90px")}</div>
            <div style="width:3px;height:70px;background:linear-gradient(180deg,#F0D060,#D4AF37,transparent);border-radius:2px;flex-shrink:0;position:relative;"></div>
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
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
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
                                    st.error("❌ Sai mật khẩu. Liên hệ Quản trị viên nếu quên mật khẩu.")
                            else:
                                st.error("❌ Không tìm thấy Mã CBCC này trong hệ thống.")
                        except Exception as e:
                            st.error(f"Lỗi kết nối máy chủ: {e}")

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
                                st.error("⚠️ Mã CBCC này đã được đăng ký trong hệ thống.")
                            else:
                                supabase.table("tai_khoan").insert({
                                    "ma_cbcc": reg_ma, "mat_khau": reg_pass,
                                    "ho_ten": reg_name.title(), "chuc_vu": reg_cv, "don_vi": reg_dv
                                }).execute()
                                st.success("✅ Đã gửi yêu cầu. Vui lòng chờ Quản trị viên phê duyệt.")
                        except Exception as e:
                            st.error(f"Lỗi: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# 7. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown(f"<div style='text-align:center;padding:20px 0 16px;'>{get_logo_html('90px')}</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="user-chip">
        <div class="name">👤 {st.session_state['ho_ten']}</div>
        <div><span class="role-badge">{'QUẢN TRỊ VIÊN' if st.session_state['role']=='Admin' else 'CÁN BỘ'}</span></div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪  Đăng xuất", use_container_width=True):
        for key in list(defaults.keys()):
            st.session_state[key] = defaults[key]
        st.rerun()

    st.markdown("---")
    st.markdown("<div style='font-size:10px;color:rgba(212,175,55,0.5);letter-spacing:1.5px;text-transform:uppercase;padding: 0 4px;margin-bottom:8px;'>Chức năng</div>", unsafe_allow_html=True)

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
        <span style='font-size:10px;opacity:0.6;'>© Hệ thống quản lý CBCC</span>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 8. HEADER CHÍNH
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
# 9. HÀM TIỆN ÍCH XỬ LÝ DỮ LIỆU
# ==========================================
@st.cache_data(ttl=5)
def load_profiles():
    try: return pd.DataFrame(supabase.table("ho_so_cbcc").select("*").execute().data)
    except Exception: return pd.DataFrame()

df_hoso = load_profiles()

def get_idx(lst, val):
    try: return lst.index(val)
    except Exception: return 0

def section_title(icon, text):
    st.markdown(f'<div class="section-title">{icon} {text}</div>', unsafe_allow_html=True)

def create_html_export(info, df_ct, df_l, df_kt, df_gd):
    def tbl(df, rename_map):
        if df.empty: return "<tr><td colspan='10' style='text-align:center;color:#888;padding:16px;'>Chưa có dữ liệu.</td></tr>"
        df2 = df.rename(columns=rename_map).drop(columns=['id', 'ma_cbcc'], errors='ignore')
        rows = ""
        for _, row in df2.iterrows():
            rows += "<tr>" + "".join(f"<td>{v}</td>" for v in row) + "</tr>"
        header = "<tr>" + "".join(f"<th>{c}</th>" for c in df2.columns) + "</tr>"
        return header + rows

    ct_rows = tbl(df_ct, {'tu_ngay':'Từ ngày','den_ngay':'Đến ngày','vi_tri':'Vị trí','don_vi':'Đơn vị','quyet_dinh_so':'Quyết định số'})
    l_rows = tbl(df_l, {'ngay_quyet_dinh':'Ngày QĐ','bac_luong':'Bậc lương','he_so':'Hệ số','quyet_dinh_so':'Quyết định số'})
    kt_rows = tbl(df_kt, {'ngay_quyet_dinh':'Ngày QĐ','loai':'Loại','noi_dung':'Nội dung','quyet_dinh_so':'Quyết định số'})

    gd_html = ""
    if not df_gd.empty:
        df_gd2 = df_gd.drop(columns=['id','ma_cbcc','created_at','thong_tin_khac'], errors='ignore')
        df_gd2 = df_gd2.rename(columns={'loai_quan_he':'Phân loại','quan_he':'Quan hệ','ho_ten':'Họ tên','nam_sinh':'Năm sinh','que_quan_gd':'Quê quán','nghe_nghiep_gd':'Nghề nghiệp','noi_o_gd':'Nơi ở'})
        for _, row in df_gd2.iterrows():
            gd_html += "<tr>" + "".join(f"<td>{v}</td>" for v in row) + "</tr>"
        header_gd = "<tr>" + "".join(f"<th>{c}</th>" for c in df_gd2.columns) + "</tr>"
        gd_html = header_gd + gd_html
    else:
        gd_html = "<tr><td colspan='7' style='text-align:center;color:#888;padding:16px;'>Chưa có dữ liệu.</td></tr>"

    html = f"""<!DOCTYPE html>
<html lang="vi"><head><meta charset="utf-8">
<title>Sơ yếu lý lịch — {info['ho_ten']}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Source+Sans+3:wght@400;600&display=swap');
  body {{ font-family: 'Source Sans 3', 'Times New Roman', serif; line-height: 1.7; padding: 48px 56px; max-width: 860px; margin: auto; color: #1a1a2e; font-size: 14px; }}
  .header {{ text-align: center; border-bottom: 3px double #C8102E; padding-bottom: 16px; margin-bottom: 25px; }}
  .header h1 {{ font-family: 'Merriweather', serif; font-size: 20px; text-transform: uppercase; letter-spacing: 2px; color: #0A1628; margin-bottom: 4px; }}
  .header .org {{ color: #C8102E; font-size: 13px; font-weight: 600; }}
  .info-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
  .info-table td {{ border: none; padding: 6px 10px; border-bottom: 1px dotted #ddd; width: 50%; }}
  h3 {{ font-family: 'Merriweather', serif; color: #0A1628; background: linear-gradient(90deg, #f5e8e8, #fff); padding: 6px 12px; border-left: 5px solid #C8102E; margin: 24px 0 12px; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; }}
  table.data-table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
  table.data-table th {{ background: #0A1628; color: #fff; padding: 8px 10px; text-align: left; }}
  table.data-table td {{ padding: 7px 10px; border-bottom: 1px solid #e8e0d4; vertical-align: top; }}
  table.data-table tr:nth-child(even) td {{ background: #fdf8f0; }}
  .footer {{ margin-top: 40px; text-align: right; font-size: 12px; color: #888; border-top: 1px solid #ddd; padding-top: 12px; }}
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
  <tr><td colspan="2"><strong>Ngày vào Đảng:</strong> Kết nạp: {info.get('ngay_vao_dang','—')} &nbsp;|&nbsp; Chính thức: {info.get('ngay_chinh_thuc','—')}</td></tr>
</table>
<h3>II. Lịch sử công tác</h3>
<table class="data-table">{ct_rows}</table>
<h3>III. Diễn biến lương</h3>
<table class="data-table">{l_rows}</table>
<h3>IV. Khen thưởng & kỷ luật</h3>
<table class="data-table">{kt_rows}</table>
<h3>V. Quan hệ gia đình</h3>
<table class="data-table">{gd_html}</table>
<div class="footer">Tài liệu này được xuất tự động từ Hệ thống Quản lý Hồ sơ CBCC — Ban Tuyên giáo và Dân vận Tỉnh ủy Tuyên Quang</div>
</body></html>"""
    return html.encode('utf-8')

# ==========================================
# MODULE 1: DASHBOARD
# ==========================================
if menu == "📊 Dashboard":
    section_title("📊", "THỐNG KÊ NHÂN SỰ TỔNG QUAN")

    if df_hoso.empty:
        st.info("Chưa có dữ liệu để thống kê.")
    else:
        df = df_hoso.fillna("Chưa xác định").copy()
        total = len(df)
        nam = len(df[df["gioi_tinh"] == "Nam"])
        nu = len(df[df["gioi_tinh"] == "Nữ"])
        thac_si = len(df[df["trinh_do_chuyen_mon"].str.contains("Thạc|Tiến", case=False, na=False)])

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
                <div class="m-sub">{round(nu/total*100) if total else 0}% tổng số</div>
            </div>
            <div class="metric-card green">
                <div class="m-label">🎓 Thạc sĩ trở lên</div>
                <div class="m-value">{thac_si}</div>
                <div class="m-sub">{round(thac_si/total*100) if total else 0}% tổng số</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            df_gt = df['gioi_tinh'].value_counts().reset_index()
            df_gt.columns = ['Giới tính', 'Số lượng']
            fig_gt = px.pie(df_gt, values='Số lượng', names='Giới tính', hole=0.55,
                            title='<b>Cơ cấu Giới tính</b>',
                            color='Giới tính', color_discrete_map={'Nam': '#0A1628', 'Nữ': '#C8102E'})
            fig_gt.update_traces(textposition='outside', textinfo='percent+label', marker=dict(line=dict(color='#fff', width=3)))
            fig_gt.update_layout(font_family="Source Sans 3", title_font_size=15, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_gt, use_container_width=True)

            # Cải tiến biểu đồ ngạch công chức
        df_ng = df['ngach_cong_chuc'].value_counts().reset_index()
        df_ng.columns = ['Ngạch', 'Số lượng']
        
        # Chuyển sang bar chart ngang (h) và tăng kích thước figure
        fig_ng = px.bar(
            df_ng, 
            y='Ngạch', 
            x='Số lượng', 
            title='<b>Ngạch Công chức hiện hưởng</b>', 
            orientation='h',  # Cột ngang
            color_discrete_sequence=['#1A2E4A'], 
            text_auto=True
        )
        
        # Căn chỉnh để tên ngạch không bị cắt
        fig_ng.update_layout(
            font_family="Source Sans 3", 
            title_font_size=15, 
            plot_bgcolor='rgba(248,244,239,0.5)', 
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis={'categoryorder': 'total ascending'}, # Xếp từ ít đến nhiều
            margin=dict(l=150, r=20, t=50, b=20) # Thêm lề trái để tên ngạch dài không bị mất
        )
        st.plotly_chart(fig_ng, use_container_width=True)

        with col2:
            df_ll = df['ly_luan_chinh_tri'].value_counts().reset_index()
            df_ll.columns = ['Lý luận CT', 'Số lượng']
            fig_ll = px.bar(df_ll, x='Lý luận CT', y='Số lượng', title='<b>Trình độ Lý luận Chính trị</b>', color_discrete_sequence=['#C8102E'], text_auto=True)
            fig_ll.update_layout(font_family="Source Sans 3", title_font_size=15, plot_bgcolor='rgba(248,244,239,0.5)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_ll, use_container_width=True)

            df_cm = df['trinh_do_chuyen_mon'].value_counts().reset_index()
            df_cm.columns = ['Trình độ', 'Số lượng']
            fig_cm = px.bar(df_cm, y='Trình độ', x='Số lượng', orientation='h', title='<b>Trình độ Chuyên môn</b>', color_discrete_sequence=['#D4AF37'], text_auto=True)
            fig_cm.update_layout(font_family="Source Sans 3", title_font_size=15, yaxis={'categoryorder': 'total ascending'}, plot_bgcolor='rgba(248,244,239,0.5)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_cm, use_container_width=True)

        section_title("📋", "DANH SÁCH CÁN BỘ, CÔNG CHỨC")
        cols_show = ['id', 'ho_ten', 'chuc_vu', 'don_vi', 'ngay_sinh', 'gioi_tinh', 'trinh_do_chuyen_mon', 'ly_luan_chinh_tri']
        df_show = df[[c for c in cols_show if c in df.columns]].rename(columns={
            'id': 'Mã', 'ho_ten': 'Họ và tên', 'chuc_vu': 'Chức vụ', 'don_vi': 'Đơn vị',
            'ngay_sinh': 'Ngày sinh', 'gioi_tinh': 'Giới tính', 'trinh_do_chuyen_mon': 'Chuyên môn', 'ly_luan_chinh_tri': 'Lý luận CT'
        })
        st.dataframe(df_show, hide_index=True, use_container_width=True)

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
                        st.markdown(f"""
                        <div style='background:#f8f4ef;border-radius:8px;padding:14px;margin-bottom:12px;'>
                            <b>Đơn vị:</b> {row['don_vi']}<br>
                            <b>Chức vụ:</b> {row['chuc_vu']}
                        </div>
                        """, unsafe_allow_html=True)
                        c_duyet, c_xoa = st.columns(2)
                        if c_duyet.button("✅  PHÊ DUYỆT TÀI KHOẢN", key=f"duyet_{row['ma_cbcc']}", use_container_width=True):
                            supabase.table("tai_khoan").update({"trang_thai": "Hoạt động"}).eq("ma_cbcc", row['ma_cbcc']).execute()
                            
                            try:
                                hoso_exist = supabase.table("ho_so_cbcc").select("id").eq("id", row['ma_cbcc']).execute().data
                                if len(hoso_exist) == 0:
                                    supabase.table("ho_so_cbcc").insert({
                                        "id": row['ma_cbcc'], "ho_ten": row['ho_ten'],
                                        "chuc_vu": row['chuc_vu'], "don_vi": row['don_vi'],
                                        "quoc_tich": "Việt Nam", "dan_toc": "Kinh"
                                    }).execute()
                            except Exception:
                                pass
                                
                            st.success("✅ Đã phê duyệt tài khoản và khởi tạo hồ sơ gốc.")
                            st.rerun()
                        if c_xoa.button("❌  TỪ CHỐI & XÓA", key=f"xoa_cd_{row['ma_cbcc']}", use_container_width=True):
                            supabase.table("tai_khoan").delete().eq("ma_cbcc", row['ma_cbcc']).execute()
                            st.success("Đã từ chối và xóa yêu cầu.")
                            st.rerun()

        with tab_hd:
            df_hd = df_tk[df_tk['trang_thai'] == 'Hoạt động']
            cols_show = ['ma_cbcc', 'ho_ten', 'chuc_vu', 'don_vi', 'phan_quyen']
            rename_map = {'ma_cbcc': 'Mã', 'ho_ten': 'Họ tên', 'chuc_vu': 'Chức vụ', 'don_vi': 'Đơn vị', 'phan_quyen': 'Quyền'}
            st.dataframe(df_hd[[c for c in cols_show if c in df_hd.columns]].rename(columns=rename_map), hide_index=True, use_container_width=True)

            st.markdown("---")
            ds_hd = (df_hd['ma_cbcc'] + " — " + df_hd['ho_ten']).tolist()
            c_rs, c_del = st.columns(2)
            with c_rs:
                section_title("🔑", "Tra cứu Mật khẩu")
                rs_ma = st.selectbox("Chọn tài khoản:", ds_hd, key="rs_sel")
                if st.button("👁️  XEM MẬT KHẨU", use_container_width=True):
                    ma_xem = rs_ma.split(" — ")[0]
                    ten_xem = rs_ma.split(" — ")[1]
                    mk_data = supabase.table("tai_khoan").select("mat_khau").eq("ma_cbcc", ma_xem).execute().data
                    if mk_data:
                        st.info(f"🔐 Mật khẩu của **{ten_xem}** ({ma_xem}): `{mk_data[0]['mat_khau']}`")
                    else:
                        st.error("Không tìm thấy dữ liệu.")
            with c_del:
                section_title("❌", "Xóa Tài khoản")
                del_ma = st.selectbox("Chọn tài khoản cần xóa:", ["— Chọn tài khoản —"] + ds_hd, key="del_sel")
                if st.button("🗑️  XÁC NHẬN XÓA VĨNH VIỄN", use_container_width=True):
                    if del_ma != "— Chọn tài khoản —":
                        ma_xoa = del_ma.split(" — ")[0]
                        if ma_xoa.upper() == "ADMIN":
                            st.error("⚠️ Không thể xóa tài khoản Admin gốc!")
                        else:
                            supabase.table("tai_khoan").delete().eq("ma_cbcc", ma_xoa).execute()
                            supabase.table("ho_so_cbcc").delete().eq("id", ma_xoa).execute()
                            st.success(f"✅ Đã xóa hoàn toàn tài khoản và hồ sơ {ma_xoa}.")
                            st.rerun()

# ==========================================
# MODULE 3: XEM HỒ SƠ
# ==========================================
elif menu in ["🔍 Tra cứu & Xem Hồ sơ", "🔍 Hồ sơ của tôi"]:
    section_title("🔍", "TRA CỨU & XEM HỒ SƠ CÁN BỘ")

    if df_hoso.empty:
        st.warning("📭 Cơ sở dữ liệu hồ sơ đang trống. Vui lòng thêm hồ sơ cán bộ trước.")
    else:
        ma_chon = ""
        if is_admin:
            tu_khoa = st.text_input("🔎  Tìm kiếm theo Tên hoặc Mã CBCC:", placeholder="Nhập từ khóa và ấn Enter…")
            if not tu_khoa.strip():
                st.info("👆 Nhập tên hoặc mã cán bộ vào ô tìm kiếm để bắt đầu.")
            else:
                df_kq = df_hoso[df_hoso.apply(lambda r: r.astype(str).str.contains(tu_khoa.strip(), case=False).any(), axis=1)]
                if df_kq.empty:
                    st.warning(f"❌ Không tìm thấy cán bộ nào khớp với từ khóa **'{tu_khoa}'**.")
                else:
                    ds_hien = (df_kq['ho_ten'] + " — " + df_kq['chuc_vu'] + " (" + df_kq['id'] + ")").tolist()
                    chon = st.selectbox("👉 Chọn cán bộ để xem chi tiết:", ds_hien)
                    if chon:
                        ma_chon = chon.split("(")[-1].replace(")", "").strip()
        else:
            ma_chon = st.session_state["ma_cbcc"]
            if df_hoso[df_hoso['id'] == ma_chon].empty:
                st.warning("❌ Bạn chưa có hồ sơ. Vui lòng chuyển sang mục **Cập nhật Hồ sơ** để tạo.")
                ma_chon = ""

        if ma_chon:
            info = df_hoso[df_hoso['id'] == ma_chon].iloc[0].fillna("—")

            col_btn, col_dl = st.columns([1, 1])
            if col_btn.button("✏️  Chỉnh sửa hồ sơ này", use_container_width=True):
                st.session_state["edit_target_id"] = info['id']
                st.session_state["menu_selection"] = "➕ Admin: Cập nhật Hồ sơ (Tất cả)" if is_admin else "➕ Cập nhật Hồ sơ cá nhân"
                st.rerun()

            df_ct = pd.DataFrame(supabase.table("lich_su_cong_tac").select("tu_ngay, den_ngay, vi_tri, don_vi, quyet_dinh_so").eq("ma_cbcc", ma_chon).order("id").execute().data)
            df_l = pd.DataFrame(supabase.table("dien_bien_luong").select("ngay_quyet_dinh, bac_luong, he_so, quyet_dinh_so").eq("ma_cbcc", ma_chon).order("id").execute().data)
            df_kt = pd.DataFrame(supabase.table("khen_thuong_ky_luat").select("ngay_quyet_dinh, loai, noi_dung, quyet_dinh_so").eq("ma_cbcc", ma_chon).order("id").execute().data)
            try: df_gd = pd.DataFrame(supabase.table("quan_he_gia_dinh").select("*").eq("ma_cbcc", ma_chon).order("loai_quan_he").execute().data)
            except Exception: df_gd = pd.DataFrame()

            html_data = create_html_export(info, df_ct, df_l, df_kt, df_gd)
            col_dl.download_button(
                label="📥  TẢI SƠ YẾU LÝ LỊCH (BẢN IN CHUẨN 2C-TW)",
                data=html_data,
                file_name=f"SYLL_2C_{info['ho_ten'].replace(' ', '_')}.html",
                mime="text/html",
                use_container_width=True
            )

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
                    <div class="info-item"><span class="lbl">Đăng ký khai sinh</span><span class="val">{info.get('noi_khai_sinh','—')}</span></div>
                    <div class="info-item"><span class="lbl">Đăng ký thường trú</span><span class="val">{info.get('thuong_tru','—')}</span></div>
                    <div class="info-item"><span class="lbl">Nơi ở hiện nay</span><span class="val">{info.get('noi_o_hien_nay','—')}</span></div>
                    <div class="info-item"><span class="lbl">Nghề nghiệp hiện nay</span><span class="val">{info.get('nghe_nghiep_ht','—')}</span></div>
                    <div class="info-item"><span class="lbl">Chức vụ trong Đảng</span><span class="val">{info.get('chuc_vu_dang','—')}</span></div>
                    <div class="info-item"><span class="lbl">Ngạch công chức</span><span class="val">{info.get('ngach_cong_chuc','—')}</span></div>
                    <div class="info-item"><span class="lbl">Giáo dục phổ thông</span><span class="val">{info.get('giao_duc_pt','—')}</span></div>
                    <div class="info-item"><span class="lbl">Trình độ chuyên môn</span><span class="val">{info.get('trinh_do_chuyen_mon','—')}</span></div>
                    <div class="info-item"><span class="lbl">Học vị cao nhất</span><span class="val">{info.get('hoc_vi','—')}</span></div>
                    <div class="info-item"><span class="lbl">Lý luận chính trị</span><span class="val">{info.get('ly_luan_chinh_tri','—')}</span></div>
                    <div class="info-item"><span class="lbl">Trình độ Ngoại ngữ</span><span class="val">{info.get('ngoai_ngu','—')}</span></div>
                    <div class="info-item"><span class="lbl">Trình độ Tin học</span><span class="val">{info.get('tin_hoc','—')}</span></div>
                    <div class="info-item" style="grid-column: span 3;"><span class="lbl">Thông tin Đảng vụ</span><span class="val">Ngày kết nạp: {info.get('ngay_vao_dang','—')} &nbsp;|&nbsp; Ngày chính thức: {info.get('ngay_chinh_thuc','—')}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            section_title("📑", "THÔNG TIN CHI TIẾT")
            t_ct, t_l, t_kt, t_gd = st.tabs(["🏢  Lịch sử công tác", "💰  Diễn biến lương", "🏆  Khen thưởng & Kỷ luật", "👨‍👩‍👧‍👦  Quan hệ gia đình"])

            with t_ct:
                if not df_ct.empty: st.dataframe(df_ct.rename(columns={'tu_ngay': 'Từ ngày', 'den_ngay': 'Đến ngày', 'vi_tri': 'Vị trí', 'don_vi': 'Đơn vị', 'quyet_dinh_so': 'Quyết định số'}), hide_index=True, use_container_width=True)
                else: st.info("Chưa có dữ liệu lịch sử công tác.")
            with t_l:
                if not df_l.empty: st.dataframe(df_l.rename(columns={'ngay_quyet_dinh': 'Ngày QĐ', 'bac_luong': 'Bậc lương', 'he_so': 'Hệ số', 'quyet_dinh_so': 'Quyết định số'}), hide_index=True, use_container_width=True)
                else: st.info("Chưa có dữ liệu diễn biến lương.")
            with t_kt:
                if not df_kt.empty: st.dataframe(df_kt.rename(columns={'ngay_quyet_dinh': 'Ngày QĐ', 'loai': 'Loại', 'noi_dung': 'Nội dung', 'quyet_dinh_so': 'Quyết định số'}), hide_index=True, use_container_width=True)
                else: st.info("Chưa có dữ liệu khen thưởng / kỷ luật.")
            with t_gd:
                if not df_gd.empty:
                    df_gd_show = df_gd.drop(columns=['id', 'ma_cbcc', 'created_at', 'thong_tin_khac'], errors='ignore').rename(columns={
                        'loai_quan_he': 'Phân loại', 'quan_he': 'Quan hệ', 'ho_ten': 'Họ tên', 'nam_sinh': 'Năm sinh', 'que_quan_gd': 'Quê quán', 'nghe_nghiep_gd': 'Nghề nghiệp / Công tác', 'noi_o_gd': 'Nơi ở hiện nay'
                    })
                    st.dataframe(df_gd_show, hide_index=True, use_container_width=True)
                else: st.info("Chưa có dữ liệu quan hệ gia đình.")

# ==========================================
# MODULE 4: NHẬP LIỆU & CHỈNH SỬA
# ==========================================
elif menu in ["➕ Cập nhật Hồ sơ cá nhân", "➕ Admin: Cập nhật Hồ sơ (Tất cả)"]:
    section_title("📝", "TRUNG TÂM NHẬP LIỆU HỒ SƠ HỆ THỐNG")

    if is_admin:
        kieu_nhap = st.radio("Chế độ nhập liệu:", ["Chỉnh sửa hồ sơ hiện có", "Thêm cán bộ mới"], horizontal=True)
        if kieu_nhap == "Chỉnh sửa hồ sơ hiện có":
            ds_cbcc = (df_hoso['id'] + " — " + df_hoso['ho_ten']).tolist() if not df_hoso.empty else []
            idx_def = 0
            if st.session_state["edit_target_id"] and ds_cbcc:
                for i, val in enumerate(ds_cbcc):
                    if val.startswith(st.session_state["edit_target_id"]):
                        idx_def = i; break
            chon_cb = st.selectbox("Chọn cán bộ cần chỉnh sửa:", ds_cbcc, index=idx_def) if ds_cbcc else ""
            target_id = chon_cb.split(" — ")[0] if chon_cb else ""
        else:
            target_id = st.text_input("Mã CBCC mới:", placeholder="VD: CV999").strip().upper()
    else:
        target_id = st.session_state["ma_cbcc"]
        st.info(f"📋 Đang cập nhật hồ sơ cá nhân — Mã: **{target_id}**")

    ex_data = {}
    if target_id and not df_hoso.empty:
        match = df_hoso[df_hoso['id'] == target_id]
        if not match.empty:
            ex_data = match.iloc[0].fillna("").to_dict()

    tab_chinh, tab_ct, tab_luong, tab_kt, tab_gd = st.tabs([
        "👤  Hồ sơ chính", "🏢  Lịch sử công tác", "💰  Diễn biến lương", "🏆  Khen thưởng / Kỷ luật", "👨‍👩‍👧‍👦  Quan hệ gia đình"
    ])

    with tab_chinh:
        with st.form("form_ho_so", clear_on_submit=False):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**📋 Thông tin định danh**")
                ho_ten = st.text_input("Họ và tên *", value=ex_data.get("ho_ten", ""))
                ngay_sinh = st.text_input("Ngày sinh (DD/MM/YYYY)", value=ex_data.get("ngay_sinh", ""))
                gioi_tinh = st.selectbox("Giới tính", DS_GIOI_TINH, index=get_idx(DS_GIOI_TINH, ex_data.get("gioi_tinh", "Nam")))
                quoc_tich = st.text_input("Quốc tịch", value=ex_data.get("quoc_tich", "Việt Nam"))
                dan_toc = st.text_input("Dân tộc", value=ex_data.get("dan_toc", "Kinh"))
                
            with c2:
                st.markdown("**📍 Địa giới hành chính**")
                que_quan = st.text_input("Quê quán", value=ex_data.get("que_quan", ""))
                noi_khai_sinh = st.text_input("Nơi đăng ký khai sinh", value=ex_data.get("noi_khai_sinh", ""))
                thuong_tru = st.text_input("Nơi đăng ký thường trú", value=ex_data.get("thuong_tru", ""))
                noi_o_hien_nay = st.text_input("Nơi ở hiện nay", value=ex_data.get("noi_o_hien_nay", ""))
                
            with c3:
                st.markdown("**👔 Nghiệp vụ & Đảng vụ**")
                don_vi = st.selectbox("Đơn vị công tác *", DS_DON_VI, index=get_idx(DS_DON_VI, ex_data.get("don_vi", "Lãnh đạo Ban")))
                chuc_vu = st.selectbox("Chức vụ chính quyền", DS_CHUC_VU, index=get_idx(DS_CHUC_VU, ex_data.get("chuc_vu", "Chuyên viên")))
                chuc_vu_dang = st.text_input("Chức vụ trong Đảng", value=ex_data.get("chuc_vu_dang", ""))
                nghe_nghiep_ht = st.text_input("Nghề nghiệp hiện nay", value=ex_data.get("nghe_nghiep_ht", ""))
                ngach = st.text_input("Ngạch công chức", value=ex_data.get("ngach_cong_chuc", ""))

            st.write("---")
            st.markdown("**🎓 Trình độ học vấn & Chuyên môn nâng cao**")
            cx1, cx2, cx3, cx4, cx5 = st.columns(5)
            giao_duc_pt = cx1.text_input("Giáo dục phổ thông (VD: 12/12)", value=ex_data.get("giao_duc_pt", ""))
            chuyen_mon = cx2.text_input("Trình độ chuyên môn", value=ex_data.get("trinh_do_chuyen_mon", ""))
            hoc_vi = cx3.text_input("Học vị (VD: Thạc sĩ, Tiến sĩ)", value=ex_data.get("hoc_vi", ""))
            ngoai_ngu = cx4.text_input("Ngoại ngữ (VD: Anh B1, Trung Khá)", value=ex_data.get("ngoai_ngu", ""))
            tin_hoc = cx5.text_input("Tin học (VD: Cơ bản, B)", value=ex_data.get("tin_hoc", ""))

            st.write("---")
            st.markdown("**☭ Lịch sử Đảng viên**")
            cl1, cl2, cl3 = st.columns(3)
            ly_luan = cl1.selectbox("Lý luận chính trị", DS_LY_LUAN, index=get_idx(DS_LY_LUAN, ex_data.get("ly_luan_chinh_tri", "Chưa qua đào tạo")))
            ngay_ket_nap = cl2.text_input("Ngày kết nạp Đảng", value=ex_data.get("ngay_vao_dang", ""))
            ngay_chinh_thuc = cl3.text_input("Ngày chính thức", value=ex_data.get("ngay_chinh_thuc", ""))

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
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
                    st.success("✅ Tuyệt vời! Hệ thống đã lưu toàn bộ thông tin Sơ yếu lý lịch chuẩn 2C-TW lên CSDL.")
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
                row = {"ma_cbcc": target_id, **vals}
                supabase.table(table_name).insert(row).execute()
                st.success("✅ Đã thêm mới.")
                st.rerun()

        section_title("🔧", "Chỉnh sửa / Xóa dữ liệu cũ")
        try: df_sub = pd.DataFrame(supabase.table(table_name).select("*").eq("ma_cbcc", target_id).order("id").execute().data)
        except Exception: df_sub = pd.DataFrame()

        if not df_sub.empty:
            edited = st.data_editor(df_sub.drop(columns=['ma_cbcc', 'created_at'], errors='ignore'), hide_index=True, use_container_width=True, disabled=["id"])
            cs, cd = st.columns([3, 1])
            if cs.button(f"💾  LƯU THAY ĐỔI — {title_btn.upper()}", use_container_width=True, key=f"save_{form_key}"):
                upd = edited.copy(); upd['ma_cbcc'] = target_id
                supabase.table(table_name).upsert(upd.fillna("").to_dict(orient="records")).execute()
                st.success("✅ Đã lưu."); st.rerun()
            del_id = cd.selectbox("ID cần xóa:", ["—"] + df_sub['id'].astype(str).tolist(), label_visibility="collapsed", key=f"del_sel_{form_key}")
            if cd.button("🗑️  XÓA", key=f"del_btn_{form_key}", use_container_width=True) and del_id != "—":
                supabase.table(table_name).delete().eq("id", del_id).execute(); st.rerun()
        else: st.info("Chưa có dữ liệu. Hãy thêm mới ở phía trên.")

    with tab_ct:
        render_sub_tab("lich_su_cong_tac", "cong_tac", "Lịch sử công tác", [("tu_ngay","Từ ngày"), ("den_ngay","Đến ngày"), ("vi_tri","Vị trí / Chức danh"), ("don_vi","Đơn vị công tác"), ("quyet_dinh_so","Quyết định số")])
    with tab_luong:
        render_sub_tab("dien_bien_luong", "luong", "Diễn biến lương", [("ngay_quyet_dinh","Ngày quyết định"), ("bac_luong","Bậc lương"), ("he_so","Hệ số"), ("quyet_dinh_so","Quyết định số")])

    with tab_kt:
        with st.form("form_kt"):
            st.markdown("**Thêm mới Khen thưởng / Kỷ luật**")
            c1, c2 = st.columns(2)
            ngay_qd = c1.text_input("Ngày quyết định")
            loai = c2.selectbox("Loại", ["Khen thưởng", "Kỷ luật"])
            noi_dung = st.text_area("Nội dung hình thức", height=80)
            qd_so = st.text_input("Quyết định số")
            if st.form_submit_button("➕  THÊM MỚI KHEN THƯỞNG / KỶ LUẬT", use_container_width=True):
                supabase.table("khen_thuong_ky_luat").insert({"ma_cbcc": target_id, "ngay_quyet_dinh": ngay_qd, "loai": loai, "noi_dung": noi_dung, "quyet_dinh_so": qd_so}).execute()
                st.success("✅ Đã thêm."); st.rerun()

        section_title("🔧", "Chỉnh sửa / Xóa dữ liệu cũ")
        df_kt2 = pd.DataFrame(supabase.table("khen_thuong_ky_luat").select("*").eq("ma_cbcc", target_id).order("id").execute().data)
        if not df_kt2.empty:
            edited_kt = st.data_editor(df_kt2.drop(columns=['ma_cbcc', 'created_at'], errors='ignore'), hide_index=True, use_container_width=True, disabled=["id"])
            cs3, cd3 = st.columns([3, 1])
            if cs3.button("💾  LƯU THAY ĐỔI — KHEN THƯỞNG / KỶ LUẬT", use_container_width=True, key="save_kt"):
                upd = edited_kt.copy(); upd['ma_cbcc'] = target_id
                supabase.table("khen_thuong_ky_luat").upsert(upd.fillna("").to_dict(orient="records")).execute()
                st.success("✅ Đã lưu."); st.rerun()
            del_kt = cd3.selectbox("ID cần xóa:", ["—"] + df_kt2['id'].astype(str).tolist(), label_visibility="collapsed", key="del_kt")
            if cd3.button("🗑️  XÓA", key="del_btn_kt", use_container_width=True) and del_kt != "—":
                supabase.table("khen_thuong_ky_luat").delete().eq("id", del_kt).execute(); st.rerun()

    with tab_gd:
        st.info("📌 Kê khai quan hệ gia đình: bao gồm bản thân (bố, mẹ, vợ/chồng, con, anh chị em ruột) và bên vợ/chồng.")
        st.info("📌 Lưu ý: Nếu người thân đã mất, ghi 'Đã chết (năm...)' vào mục Nghề nghiệp, chức vụ, đơn vị.")
        with st.form("form_giadinh"):
            c1, c2, c3 = st.columns([1, 1, 2])
            loai_qh = c1.selectbox("Phân loại", ["Bản thân", "Bên vợ/chồng"])
            quan_he = c2.selectbox("Quan hệ", ["Bố đẻ", "Mẹ đẻ", "Bố vợ", "Mẹ vợ", "Bố chồng", "Mẹ chồng", "Vợ", "Chồng", "Con đẻ", "Anh ruột", "Chị ruột", "Em ruột"])
            ho_ten_gd = c3.text_input("Họ và tên")
            c4, c5 = st.columns([1, 3])
            nam_sinh_gd = c4.text_input("Năm sinh")
            que_quan_gd = c5.text_input("Quê quán")
            c6, c7 = st.columns(2)
            nghe_nghiep_gd = c6.text_input("Nghề nghiệp, chức vụ, đơn vị")
            noi_o_gd = c7.text_input("Nơi ở hiện nay")
            if st.form_submit_button("➕  THÊM NGƯỜI THÂN", use_container_width=True):
                try:
                    supabase.table("quan_he_gia_dinh").insert({"ma_cbcc": target_id, "loai_quan_he": loai_qh, "quan_he": quan_he, "ho_ten": ho_ten_gd, "nam_sinh": nam_sinh_gd, "que_quan_gd": que_quan_gd, "nghe_nghiep_gd": nghe_nghiep_gd, "noi_o_gd": noi_o_gd}).execute()
                    st.success("✅ Đã thêm người thân."); st.rerun()
                except Exception as e: st.error(f"Lỗi: {e}")

        section_title("🔧", "Chỉnh sửa / Xóa dữ liệu cũ")
        try:
            df_gd2 = pd.DataFrame(supabase.table("quan_he_gia_dinh").select("*").eq("ma_cbcc", target_id).order("loai_quan_he").execute().data)
            if not df_gd2.empty:
                edited_gd = st.data_editor(df_gd2.drop(columns=['ma_cbcc', 'created_at', 'thong_tin_khac'], errors='ignore'), hide_index=True, use_container_width=True, disabled=["id"])
                cs4, cd4 = st.columns([3, 1])
                if cs4.button("💾  LƯU THAY ĐỔI — QUAN HỆ GIA ĐÌNH", use_container_width=True, key="save_gd"):
                    upd = edited_gd.copy(); upd['ma_cbcc'] = target_id
                    supabase.table("quan_he_gia_dinh").upsert(upd.fillna("").to_dict(orient="records")).execute()
                    st.success("✅ Đã lưu."); st.rerun()
                del_gd = cd4.selectbox("ID cần xóa:", ["—"] + df_gd2['id'].astype(str).tolist(), label_visibility="collapsed", key="del_gd")
                if cd4.button("🗑️  XÓA", key="del_btn_gd", use_container_width=True) and del_gd != "—":
                    supabase.table("quan_he_gia_dinh").delete().eq("id", del_gd).execute(); st.rerun()
            else: st.info("Chưa có dữ liệu. Thêm người thân ở phía trên.")
        except Exception as e: st.warning(f"⚠️ Không tải được dữ liệu gia đình. Lỗi: {e}")
