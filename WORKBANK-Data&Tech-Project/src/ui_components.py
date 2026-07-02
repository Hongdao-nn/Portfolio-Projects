import streamlit as st
import os

# Visual themes and palettes
THEME_PALETTE = ['#0d5c3a', '#2d845e', '#6bb38a', '#e0a96d', '#f48c06', '#fdba74']

CLUSTER_COLORS = {
    'Vùng an toàn (Safe zone)': '#10b981',           # Emerald Green (Safe)
    'Vùng ổn định (Stable zone)': '#3b82f6',         # Blue (Stable)
    'Vùng tiềm ẩn nguy cơ (At-risk zone)': '#f59e0b', # Amber/Yellow (At-risk)
    'Vùng báo động (Alert zone)': '#ef4444'           # Red (Alert)
}

PERSONA_COLORS = {
    'Chuyên gia tích hợp chiến lược (Strategic power user)': '#0d5c3a',
    'Chuyên gia chuyên môn truyền thống (Traditional domain expert)': '#3a8d67',
    'Nhân sự nhạy bén công nghệ (Adaptive tech adopter)': '#e0a96d',
    'Nhân sự lệ thuộc công nghệ (Replaceable tech dependent)': '#fdba74'
}

PLOTLY_LAYOUT_DEFAULTS = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#334155', family='sans-serif'), 
    xaxis=dict(
        gridcolor='rgba(148,163,184,0.1)',       
        zerolinecolor='rgba(148,163,184,0.2)',   
        showgrid=True
    ),
    yaxis=dict(
        gridcolor='rgba(148,163,184,0.1)', 
        zerolinecolor='rgba(148,163,184,0.2)',
        showgrid=True
    ),
    legend=dict(bgcolor='rgba(0,0,0,0)'),
    margin=dict(l=40, r=40, t=50, b=40)             
)

def load_css(css_path="assets/style.css"):
    """
    Load styling from a CSS stylesheet and inject it into the Streamlit session.
    """
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def apply_chart_style(fig, title_text=None):
    """
    Apply shared Plotly layout presets and set dynamic titles.
    """
    fig.update_layout(**PLOTLY_LAYOUT_DEFAULTS)
    if title_text:
        fig.update_layout(title=dict(text=title_text, font=dict(size=16)))
    return fig

def st_analysis(text):
    """
    Render a standard analysis card block with markdown content.
    """
    st.markdown(
        f"""
        <div style="
            background-color: #0d5c3a; 
            padding: 24px; 
            border-radius: 12px; 
            border-left: 6px solid #fdba74; 
            margin-bottom: 24px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.15);
            color: #f1f5f9;
            font-size: 14.5px;
            line-height: 1.6;
        ">
            <h4 style="color: #fdba74; margin-top: 0; margin-bottom: 12px; font-size: 16px; font-weight: 700; letter-spacing: 0.5px;">Phân tích kết quả</h4>
            
{text}
        </div>
        """,
        unsafe_allow_html=True
    )

def st_header(text):
    """
    Render a standardized section header.
    """
    st.markdown(
        f"<h2 style='color: #1e293b; font-size: 24px; font-weight: 700; margin-top: 30px; margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;'>{text}</h2>",
        unsafe_allow_html=True
    )

def st_subheader(text):
    """
    Render a standardized subsection header.
    """
    st.markdown(
        f"<h3 style='color: #0d5c3a; font-size: 19px; font-weight: 600; margin-top: 25px; margin-bottom: 12px;'>{text}</h3>",
        unsafe_allow_html=True
    )

def st_kpi_card(title, value, color_type):
    """
    Render a standard KPI card with customized green/amber colors.
    """
    border_class = "kpi-card-green" if color_type == "green" else "kpi-card-amber"
    text_color = "#0d5c3a" if color_type == "green" else "#f59e0b"
    st.markdown(
        f"""
        <div class="kpi-card {border_class}">
            <p style='font-size: 14px; color: #64748b; margin-top: 0; margin-bottom: 6px; font-weight: 500;'>{title}</p>
            <h2 style='font-size: 34px; color: {text_color}; margin-top: 0; margin-bottom: 0; font-weight: 700;'>{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
