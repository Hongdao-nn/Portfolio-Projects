import streamlit as st
from src.ui_components import load_css
from src.data_loader import load_and_preprocess_data

# Import tab renderers
from src.tabs.tab_general import render_tab_general
from src.tabs.tab_risk import render_tab_risk
from src.tabs.tab_vulnerability import render_tab_vulnerability
from src.tabs.tab_recommendation import render_tab_recommendation

# 1. Page Config (Must be the very first Streamlit command)
st.set_page_config(
    page_title="PHÂN TÍCH TÁC ĐỘNG CỦA AI ĐỐI VỚI NGÀNH CÔNG NGHỆ VÀ DỮ LIỆU",
    layout="wide"
)

# 2. Main Title
st.markdown(
    "<h1 style='text-align: center; color: #0d5c3a; font-size: 38px; font-weight: 800; "
    "margin-top: 10px; margin-bottom: 25px; text-transform: uppercase;'>"
    "PHÂN TÍCH TÁC ĐỘNG CỦA AI ĐỐI VỚI NGÀNH CÔNG NGHỆ VÀ DỮ LIỆU</h1>", 
    unsafe_allow_html=True
)

# 3. Load Custom Stylesheet
load_css("assets/style.css")

# 4. Load and Preprocess Datasets
data = load_and_preprocess_data(data_dir="data")

# 5. Define Tab Layout
tab1, tab2, tab3, tab4 = st.tabs([
    "Hiện trạng nhân sự và Bản đồ rủi ro công nghiệp",
    "Động lực chuyển giao và Tấm khiên phòng ngự con người",
    "Mô phỏng đà phát triển AI và dự báo rủi ro tác vụ",
    "Hệ thống khuyến nghị dịch chuyển nghề nghiệp"
])

# 6. Render Tab Content
with tab1:
    render_tab_general(data)

with tab2:
    render_tab_risk(data)

with tab3:
    render_tab_vulnerability(data)

with tab4:
    render_tab_recommendation(data)