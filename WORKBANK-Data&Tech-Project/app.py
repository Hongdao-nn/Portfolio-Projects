import streamlit as st
from src.ui_components import load_css
from src.data_loader import load_and_preprocess_data

# Import tab renderers
from src.tabs.tab_general import render_tab_general
from src.tabs.tab_demand import render_tab_demand
from src.tabs.tab_risk import render_tab_risk
from src.tabs.tab_vulnerability import render_tab_vulnerability
from src.tabs.tab_sandbox import render_tab_sandbox

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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Bức tranh toàn cảnh (Industry overview)",
    "Kỳ vọng và thực tế (Expectation vs. reality)",
    "Động lực và rào cản (Drivers & barriers)",
    "Trục thời gian và dự báo (Temporal & forecasting)",
    "Phân khúc và định hình chân dung (Human segmentation)"
])

# 6. Render Tab Content
with tab1:
    render_tab_general(data)

with tab2:
    render_tab_demand(data)

with tab3:
    render_tab_risk(data)

with tab4:
    render_tab_vulnerability(data)

with tab5:
    render_tab_sandbox(data)