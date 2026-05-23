# Sửa lại đoạn st.set_page_config và thêm CSS này vào ngay sau đó
st.set_page_config(
    page_title="Hồ sơ CBCC - Ban Tuyên giáo & Dân vận Tuyên Quang",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="auto" # Đổi từ 'expanded' sang 'auto' để Streamlit linh hoạt hơn
)

# THÊM ĐOẠN CSS NÀY VÀO CSS HIỆN TẠI ĐỂ ÉP SIDEBAR HIỂN THỊ NÚT
st.markdown("""
<style>
    /* Ép nút mở rộng sidebar luôn xuất hiện */
    [data-testid="stSidebarCollapse"] {
        visibility: visible !important;
        background: rgba(255,255,255,0.1) !important;
        border-radius: 4px;
    }
    /* Đảm bảo sidebar không bị ẩn mất trên các màn hình hẹp */
    [data-testid="stSidebar"] {
        z-index: 9999 !important;
    }
</style>
""", unsafe_allow_html=True)
