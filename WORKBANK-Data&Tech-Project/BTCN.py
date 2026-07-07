import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
st.set_page_config(
    page_title="PHÂN TÍCH TÁC ĐỘNG CỦA AI ĐỐI VỚI NGÀNH CÔNG NGHỆ VÀ DỮ LIỆU",
    layout="wide"
)
st.markdown("<h1 style='text-align: center; color: #0d5c3a; font-size: 38px; font-weight: 800; margin-top: 10px; margin-bottom: 25px; text-transform: uppercase;'>PHÂN TÍCH TÁC ĐỘNG CỦA AI ĐỐI VỚI NGÀNH CÔNG NGHỆ VÀ DỮ LIỆU</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
        /* Active and hover tab borders */
        button[data-baseweb="tab"] {
            font-weight: 500 !important;
            color: #64748b !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #0d5c3a !important;
            font-weight: 700 !important;
        }
        button[data-baseweb="tab"]:hover {
            color: #0d5c3a !important;
        }
        /* Tab highlight border line */
        div[data-baseweb="tab-highlight"] {
            background-color: #0d5c3a !important;
        }

        /* Custom KPI Card Styling with Hover Effects */
        .kpi-card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            margin-bottom: 16px;
        }
        .kpi-card-green {
            border: 2px solid #0d5c3a;
        }
        .kpi-card-green:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(13, 92, 58, 0.15), 0 4px 6px -4px rgba(13, 92, 58, 0.15);
            border-color: #2d845e;
        }
        .kpi-card-amber {
            border: 2px solid #f59e0b;
        }
        .kpi-card-amber:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(245, 158, 11, 0.15), 0 4px 6px -4px rgba(245, 158, 11, 0.15);
            border-color: #f97316;
        }

        /* Streamlit Slider custom colors (deep green) */
        .stSlider [data-baseweb="slider"] > div {
            background: #e2e8f0 !important;
        }
        .stSlider [data-baseweb="slider"] > div > div > div {
            background-color: #0d5c3a !important;
        }
        .stSlider [role="slider"] {
            background-color: #0d5c3a !important;
            border-color: #0d5c3a !important;
            box-shadow: 0 0 0 4px rgba(13, 92, 58, 0.15) !important;
        }
        .stSlider [role="slider"]:hover {
            box-shadow: 0 0 0 6px rgba(13, 92, 58, 0.25) !important;
        }
        .stSlider [role="slider"]:focus {
            box-shadow: 0 0 0 6px rgba(13, 92, 58, 0.25) !important;
        }
        .stSlider [data-testid="stThumbValue"] {
            color: #0d5c3a !important;
            font-weight: bold !important;
        }
        .stSlider [data-baseweb="slider"] div {
            color: #0d5c3a !important;
        }
        .stSlider [data-testid="stThumbValue"] {
            color: #0d5c3a !important;
            font-weight: bold !important;
        }
        .stSlider [data-baseweb="slider"] div {
            color: #0d5c3a !important;
        }

        /* Custom Recommendation Card Styling */
        .rec-card {
            background-color: #ffffff;
            border-radius: 16px;
            padding: 24px;
            border: 2px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 20px;
        }
        .rec-card:hover {
            transform: translateY(-6px);
            border-color: #0d5c3a;
            box-shadow: 0 20px 25px -5px rgba(13, 92, 58, 0.15), 0 10px 10px -5px rgba(13, 92, 58, 0.05);
        }
        .rec-tag {
            display: inline-block;
            background: linear-gradient(135deg, #0d5c3a 0%, #2d845e 100%);
            color: #ffffff;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
        }
        .rec-title {
            font-size: 16px;
            font-weight: 700;
            color: #1e293b;
            margin-top: 0;
            margin-bottom: 14px;
            line-height: 1.4;
            min-height: 48px;
        }
        .rec-metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #f1f5f9;
            padding: 8px 0;
            font-size: 13.5px;
        }
        .rec-metric-label {
            color: #64748b;
            font-weight: 500;
        }
        .rec-metric-val {
            color: #1e293b;
            font-weight: 700;
        }
    </style>
    """,
    unsafe_allow_html=True
)

THEME_PALETTE = ['#0d5c3a', '#2d845e', '#6bb38a', '#e0a96d', '#f48c06', '#fdba74']

CLUSTER_COLORS = {
    'Vùng an toàn (Safe zone)': '#10b981',           # Emerald Green (Safe)
    'Vùng ổn định (Stable zone)': '#3b82f6',         # Blue (Stable)
    'Vùng tiềm ẩn nguy cơ (At-risk zone)': '#f59e0b', # Amber/Yellow (At-risk)
    'Vùng báo động (Alert zone)': '#ef4444'           # Red (Alert)
}

CLUSTER_MULTIPLIERS = {
    'Vùng an toàn (Safe zone)': 0.5,        # AI tự động hóa chậm hơn đối với tác vụ an toàn
    'Vùng ổn định (Stable zone)': 0.8,
    'Vùng tiềm ẩn nguy cơ (At-risk zone)': 1.1,
    'Vùng báo động (Alert zone)': 1.3       # AI tự động hóa nhanh hơn đối với tác vụ lặp lại/thủ công
}

EXCHANGE_RATE_USD_VND = 25400
VN_WAGE_ADJUSTMENT_FACTOR = 0.22  # Hệ số hiệu chỉnh lương IT Việt Nam so với Mỹ do sự chênh lệch mức sống và sức mua (22%)

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

def apply_chart_style(fig, title_text=None):
    fig.update_layout(**PLOTLY_LAYOUT_DEFAULTS)
    # Đồng bộ quy cách chỉ viết hoa chữ cái đầu tiên của tiêu đề biểu đồ
    if title_text:
        fig.update_layout(title=dict(text=title_text, font=dict(size=16)))
    return fig

def st_analysis(text):
    # Chỉ cần một khối st.markdown duy nhất để dựng khung và render văn bản
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
        """,
        unsafe_allow_html=True
    )

def st_header(text):
    st.markdown(
        f"<h2 style='color: #1e293b; font-size: 24px; font-weight: 700; margin-top: 30px; margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;'>{text}</h2>",
        unsafe_allow_html=True
    )

def st_subheader(text):
    st.markdown(
        f"<h3 style='color: #0d5c3a; font-size: 19px; font-weight: 600; margin-top: 25px; margin-bottom: 12px;'>{text}</h3>",
        unsafe_allow_html=True
    )

def st_kpi_card(title, value, color_type):
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



def classify_worker_persona(row):
    income = str(row['Income']).strip()
    experience = str(row['Experience']).strip()
    coding = str(row['LLM Usage by Type - Coding']).strip()
    sysdesign = str(row['LLM Usage by Type - System Design']).strip()
    analysis = str(row['LLM Usage by Type - Analysis']).strip()
    dataproc = str(row['LLM Usage by Type - Data Processing']).strip()
    ideagen = str(row['LLM Usage by Type - Idea Generation']).strip()

    is_high_income = income in ['86K-165K', '165K-209K', '209K-529K', '529K+']
    is_high_exp = experience in ['3-5 years', '6-10 years', 'More than 10 years']
    is_low_exp = experience in ['Less than 1 year', '1-2 year']
    is_low_income = income in ['0-30K', '30-60K', 'Prefer not to say']

    use_coding = coding in ['Daily', 'Weekly']
    use_sysdesign = sysdesign in ['Daily', 'Weekly']
    use_analysis = analysis in ['Daily', 'Weekly']
    use_dataproc = dataproc in ['Daily', 'Weekly']
    use_ideagen = ideagen in ['Daily', 'Weekly']
    has_any_usage = any([use_coding, use_sysdesign, use_analysis, use_dataproc, use_ideagen])

    if is_high_income and is_high_exp and use_analysis and use_sysdesign:
        return 'Chuyên gia tích hợp chiến lược (Strategic power user)'
    if is_low_exp and use_coding and use_sysdesign:
        return 'Nhân sự nhạy bén công nghệ (Adaptive tech adopter)'
    if is_high_exp and not has_any_usage:
        return 'Chuyên gia chuyên môn truyền thống (Traditional domain expert)'
    if is_low_income and use_coding and not use_sysdesign:
        return 'Nhân sự lệ thuộc công nghệ (Replaceable tech dependent)'
    
    if is_low_exp:
        return 'Nhân sự nhạy bén công nghệ (Adaptive tech adopter)' if has_any_usage else 'Nhân sự lệ thuộc công nghệ (Replaceable tech dependent)'
    return 'Chuyên gia tích hợp chiến lược (Strategic power user)' if has_any_usage else 'Chuyên gia chuyên môn truyền thống (Traditional domain expert)'

df_worker = pd.read_csv("data/domain_worker_desires.csv")
df_worker_meta = pd.read_csv("data/domain_worker_metadata.csv")
df_expert = pd.read_csv("data/expert_rated_technological_capability.csv")
df_task = pd.read_csv("data/task_statement_with_metadata.csv")

# Bản dịch và lọc các ngành nghề phù hợp với thị trường Việt Nam
VIETNAMESE_JOB_MAP = {
    'Computer Programmers': 'Lập trình viên (Computer Programmer)',
    'Web Developers': 'Lập trình viên Web (Web Developer)',
    'Software Quality Assurance Analysts and Testers': 'Kỹ sư kiểm thử phần mềm (QA/Tester)',
    'Database Administrators': 'Quản trị viên cơ sở dữ liệu (Database Administrator)',
    'Information Technology Project Managers': 'Quản lý dự án CNTT (IT Project Manager)',
    'Computer Network Support Specialists': 'Chuyên viên hỗ trợ mạng (Network Support)',
    'Computer Systems Engineers/Architects': 'Kỹ sư/Kiến trúc sư hệ thống (Systems Engineer/Architect)',
    'Computer and Information Systems Managers': 'Quản lý hệ thống thông tin (IT Manager)',
    'Computer User Support Specialists': 'Chuyên viên hỗ trợ kỹ thuật (IT Support)',
    'Information Security Analysts': 'Chuyên viên an ninh thông tin (Security Analyst)',
    'Computer Systems Analysts': 'Chuyên viên phân tích hệ thống (Systems Analyst)',
    'Business Intelligence Analysts': 'Chuyên viên phân tích dữ liệu kinh doanh (BI Analyst)',
    'Data Entry Keyers': 'Nhân viên nhập liệu (Data Entry Keyer)',
    'Network and Computer Systems Administrators': 'Quản trị viên hệ thống mạng (Network Administrator)',
    'Clinical Data Managers': 'Quản lý dữ liệu lâm sàng (Clinical Data Manager)',
    'Computer and Information Research Scientists': 'Nhà nghiên cứu khoa học máy tính (Research Scientist)',
    'Web Administrators': 'Quản trị viên Web (Web Administrator)'
}

all_jobs = df_worker_meta['Occupation (O*NET-SOC Title)'].dropna().unique()
tech_jobs = [job for job in all_jobs if job in VIETNAMESE_JOB_MAP]

df_meta_it = df_worker_meta[df_worker_meta['Occupation (O*NET-SOC Title)'].isin(tech_jobs)].copy()
df_meta_it['Occupation (O*NET-SOC Title)'] = df_meta_it['Occupation (O*NET-SOC Title)'].map(VIETNAMESE_JOB_MAP)

df_tasks_it = df_task[df_task['Occupation (O*NET-SOC Title)'].isin(tech_jobs)].copy()
df_tasks_it['Occupation (O*NET-SOC Title)'] = df_tasks_it['Occupation (O*NET-SOC Title)'].map(VIETNAMESE_JOB_MAP)

df_worker_it = df_worker[df_worker['Occupation (O*NET-SOC Title)'].isin(tech_jobs)].copy()
df_worker_it['Occupation (O*NET-SOC Title)'] = df_worker_it['Occupation (O*NET-SOC Title)'].map(VIETNAMESE_JOB_MAP)

df_expert_it = df_expert[df_expert['Occupation (O*NET-SOC Title)'].isin(tech_jobs)].copy()
df_expert_it['Occupation (O*NET-SOC Title)'] = df_expert_it['Occupation (O*NET-SOC Title)'].map(VIETNAMESE_JOB_MAP)

# Xây dựng bảng dữ liệu tác vụ chính (df_model)
df_model = pd.merge(
    df_worker_it.groupby(['Task ID', 'Task', 'Occupation (O*NET-SOC Title)'])['Automation Desire Rating'].mean().reset_index(),
    df_expert_it.groupby('Task ID')[['Automation Capacity Rating', 'Involved Uncertainty',
                                      'Interpersonal Communication Requirement', 'Domain Expertise Requirement',
                                      'Human Agency Scale Rating']].mean().reset_index(),
    on='Task ID', how='inner'
).rename(columns={
    'Automation Capacity Rating': 'Khả năng tự động hóa (chuyên gia)',
    'Automation Desire Rating': 'Mong muốn tự động hóa (người lao động)',
    'Task': 'Tác vụ',
    'Occupation (O*NET-SOC Title)': 'Ngành nghề'
})

df_model = pd.merge(
    df_model,
    df_tasks_it.groupby('Task ID').agg({
        'Skill (O*NET Work Activity)': 'first',
        'Occupation Mean Annual Wage': 'first',
        'Importance': 'mean'
    }).reset_index(),
    on='Task ID', how='left'
)

df_model['Importance'] = df_model['Importance'].fillna(3.0)
df_model['Occupation Mean Annual Wage'] = df_model['Occupation Mean Annual Wage'].fillna(df_model['Occupation Mean Annual Wage'].median())
df_model['Skill (O*NET Work Activity)'] = df_model['Skill (O*NET Work Activity)'].astype(str).str.replace(r"[\[\]\']", "", regex=True)

df_model['Gap_Rating'] = df_model['Mong muốn tự động hóa (người lao động)'] - df_model['Khả năng tự động hóa (chuyên gia)']
df_model['Tác vụ rút gọn'] = df_model['Tác vụ'].apply(lambda x: str(x)[:40] + '...' if len(str(x)) > 40 else str(x))

df_model['Risk_Score'] = (
    df_model['Khả năng tự động hóa (chuyên gia)'] * (6 - df_model['Involved Uncertainty']) *
    (6 - df_model['Interpersonal Communication Requirement']) / 25
)

features_cluster = ['Khả năng tự động hóa (chuyên gia)', 'Mong muốn tự động hóa (người lao động)',
                     'Domain Expertise Requirement', 'Involved Uncertainty',
                     'Interpersonal Communication Requirement', 'Occupation Mean Annual Wage']
X = df_model[features_cluster].fillna(df_model[features_cluster].median())
X_scaled = StandardScaler().fit_transform(X)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_model['Cluster'] = kmeans.fit_predict(X_scaled)

# Sắp xếp nhãn cụm theo thứ tự điểm rủi ro tăng dần
cluster_risk_rank = df_model.groupby('Cluster')['Risk_Score'].mean().sort_values().index.tolist()
ordered_persona_names = [
    "Vùng an toàn (Safe zone)",
    "Vùng ổn định (Stable zone)",
    "Vùng tiềm ẩn nguy cơ (At-risk zone)",
    "Vùng báo động (Alert zone)"
]
persona_labels = {cluster_id: ordered_persona_names[rank] for rank, cluster_id in enumerate(cluster_risk_rank)}
df_model['Vùng rủi ro'] = df_model['Cluster'].map(persona_labels)

df_worker_agg = df_worker_it.groupby('User ID').agg({
    'Reasons for Automation Desire - Free Time': 'mean',
    'Reasons for Automation Desire - Repetitive': 'mean',
    'Reasons for Automation Desire - Human Error': 'mean',
    'Reasons for Automation Desire - Stress': 'mean',
    'Reasons for Automation Desire - Difficulty': 'mean',
    'Reasons for Automation Desire - Scale': 'mean'
}).reset_index()

df_user = pd.merge(df_worker_meta, df_worker_agg, on='User ID', how='inner')
df_user_it = df_user[df_user['Occupation (O*NET-SOC Title)'].isin(tech_jobs)].copy()

llm_cols = [
    'LLM Usage by Type - Coding', 
    'LLM Usage by Type - System Design', 
    'LLM Usage by Type - Data Processing', 
    'LLM Usage by Type - Analysis', 
    'LLM Usage by Type - Idea Generation'
]
for col in llm_cols:
    df_user_it[col] = df_user_it[col].fillna('Never')

df_user_it['Chân dung nhân sự'] = df_user_it.apply(classify_worker_persona, axis=1)

# Thiết lập bộ điều khiển toàn cầu tại Sidebar
st.sidebar.markdown("<h2 style='color: #0d5c3a; font-size: 20px; font-weight: 700; margin-top: 15px; margin-bottom: 5px;'>Bộ điều khiển toàn cầu</h2>", unsafe_allow_html=True)
st.sidebar.write("Các tùy chọn dưới đây sẽ lọc dữ liệu và cập nhật phân tích trên toàn bộ các trang của ứng dụng.")

occ_options = ["Tất cả các ngành"] + sorted(df_model['Ngành nghề'].unique().tolist())
selected_occ = st.sidebar.selectbox("Chọn ngành nghề phân tích:", occ_options, index=0, key="global_job_dropdown")
selected_year = st.sidebar.slider(
    "Chọn năm mô phỏng dự báo:",
    min_value=2025,
    max_value=2030,
    value=2025,
    step=1,
    key="global_year_slider"
)

st.sidebar.markdown("---")
st.sidebar.write("Tải bản báo cáo nghiên cứu đầy đủ dạng PDF:")
with open("Báo cáo phân tích tác động của trí tuệ nhân tạo đối với lực lượng lao động công nghệ và dữ liệu.pdf", "rb") as f:
    pdf_bytes = f.read()
st.sidebar.download_button(
    label="Tải báo cáo phân tích PDF",
    data=pdf_bytes,
    file_name="Báo cáo phân tích tác động của trí tuệ nhân tạo đối với lực lượng lao động công nghệ và dữ liệu.pdf",
    mime="application/pdf"
)

tab1, tab2, tab3, tab4 = st.tabs([
    "Hiện trạng nhân sự và bản đồ rủi ro công nghiệp",
    "Động lực chuyển giao và tấm khiên phòng ngự con người",
    "Mô phỏng đà phát triển AI và dự báo rủi ro tác vụ",
    "Hệ thống khuyến nghị dịch chuyển nghề nghiệp và nâng cao kỹ năng"
])

# =========================================================================
# TAB 1: Hiện trạng nhân sự và bản đồ rủi ro công nghiệp
# =========================================================================
with tab1:
    st_header("Hiện trạng nhân sự và bản đồ rủi ro công nghiệp")
    st.write(
        "Nhồm phân tích ảnh hướng của trí tuệ nhân tạo đối với thị trường lao động, báo cáo khảo sát lực lượng lao động công nghệ "
        "và ánh xạ các tác vụ công việc vào các phân vùng rủi ro khác nhau. Bộ dữ liệu tập trung vào các nhóm nghề nghiệp liên quan đỿn "
        "phát triển phần mềm, phân tích hệ thống, xử lý dữ liệu và an ninh mạng, được trích xuất từ dữ liệu khảo sạt gốc bằng bộ lọc "
        "tên ngành nghề chứa các từ khóa trọng tâm: **computer, software, data, information, network, web, programmer, developer, "
        "analyst, systems, ai, artificial intelligence, machine learning, algorithm**."
    )
    if selected_occ == "Tất cả các ngành":
        df_meta_occ = df_meta_it.copy()
        df_occ_tasks = df_model.copy()
    else:
        df_meta_occ = df_meta_it[df_meta_it['Occupation (O*NET-SOC Title)'] == selected_occ]
        df_occ_tasks = df_model[df_model['Ngành nghề'] == selected_occ]
        
    total_workers_occ = len(df_meta_occ)
    ai_usage_pct_occ = (df_meta_occ[llm_cols].apply(lambda r: any(r != 'Never'), axis=1).mean() * 100) if total_workers_occ > 0 else 0.0
    total_occ_tasks = len(df_occ_tasks)
    
    # Tính tỷ lệ thâm niên của ngành được chọn
    if total_workers_occ > 0:
        senior_count = len(df_meta_occ[df_meta_occ['Experience'].isin(['3-5 years', '6-10 years', 'More than 10 years'])])
        senior_pct = (senior_count / total_workers_occ) * 100
    else:
        senior_pct = 0.0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st_kpi_card("Nhân sự khảo sát (ngành)", f"{total_workers_occ}", "green")
    with col2:
        st_kpi_card("Tác vụ phân tích (ngành)", f"{total_occ_tasks}", "amber")
    with col3:
        st_kpi_card("Tỷ lệ nhân sự dùng AI", f"{ai_usage_pct_occ:.1f}%", "green")
    with col4:
        # Tỷ lệ tác vụ Safe/Stable zone của ngành
        safe_stable_tasks = df_occ_tasks[df_occ_tasks['Vùng rủi ro'].isin(['Vùng an toàn (Safe zone)', 'Vùng ổn định (Stable zone)'])]
        safe_ratio = len(safe_stable_tasks) / total_occ_tasks * 100 if total_occ_tasks > 0 else 0.0
        st_kpi_card("Tỷ lệ tác vụ An toàn/Ổn định", f"{safe_ratio:.1f}%", "amber")
        
    st.write("")
    
    st_subheader(f"Phân bố thâm niên lực lượng lao động: {selected_occ}")
    col_donut_text, col_donut_chart = st.columns([1, 1.2])
    with col_donut_text:
        st_analysis(
            f"*Đối với riêng ngành **{selected_occ}**, biểu đồ thâm niên chỉ ra rằng lực lượng lao động được dẫn dắt bởi "
            f"nhóm giàu kinh nghiệm, với **{senior_pct:.1f}%** nhân sự có thâm niên từ **3 năm trở lên** (trong đó nhóm từ **3–5 năm** và **trên 10 năm** chiếm tỷ lệ cao). "
            f"Sự áp đảo của nhóm Senior khẳng định rằng bất kỳ sự thay đổi công nghệ nào ở đây cũng sẽ tác động trực tiếp đến những cột trụ cốt lõi của ngành này. "
            f"Tuy nhiên, liệu nhóm giàu kinh nghiệm này có thực sự an toàn trước làn sóng tự động hóa? Hãy cùng đối chiếu cơ cấu thâm niên này với bản đồ phân cụm rủi ro tác vụ bên dưới.*"
        )
    with col_donut_chart:
        EXP_ORDER = ['Less than 1 year', '1-2 year', '3-5 years', '6-10 years', 'More than 10 years']
        EXP_MAP_VN = {
            'Less than 1 year': 'Dưới 1 năm',
            '1-2 year': 'Từ 1–2 năm',
            '3-5 years': 'Từ 3–5 năm',
            '6-10 years': 'Từ 6–10 năm',
            'More than 10 years': 'Trên 10 năm'
        }
        
        if total_workers_occ > 0:
            df_donut = df_meta_occ['Experience'].value_counts().reset_index()
            df_donut.columns = ['Experience', 'Count']
            df_donut['Thâm niên'] = df_donut['Experience'].map(EXP_MAP_VN)
            
            fig_donut = px.pie(
                df_donut, 
                values='Count', 
                names='Thâm niên', 
                hole=0.4,
                category_orders={'Thâm niên': [EXP_MAP_VN[x] for x in EXP_ORDER]},
                color_discrete_sequence=THEME_PALETTE
            )
            apply_chart_style(fig_donut, f"Phân bổ thâm niên kinh nghiệm: {selected_occ}")
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.write("Không có dữ liệu thâm niên khảo sát cho ngành này.")
    
        
    st_subheader("Ma trận định vị chiến lược tác vụ")
    st.write(
        "Thuật toán phân cụm **K-Means** phân nhóm các tác vụ vào 4 vùng rủi ro khác nhau "
        "dựa trên sự kết hợp đa chiều của 6 yếu tố cốt lõi: "
        "(1) **Khả năng tự động hóa** (đánh giá từ chuyên gia), "
        "(2) **Mong muốn tự động hóa** (khảo sát từ người lao động), "
        "(3) **Yêu cầu chuyên môn nghiệp vụ** (*Domain Expertise Requirement*), "
        "(4) **Mức độ bất định của tác vụ** (*Involved Uncertainty*), "
        "(5) **Yêu cầu giao tiếp tương tác con người** (*Interpersonal Communication Requirement*), và "
        "(6) **Mức lương trung bình năm của ngành nghề** (*Occupation Mean Annual Wage*)."
    )
    col_scatter_text, col_scatter_chart = st.columns([1, 1.2])
    with col_scatter_text:
        # Số tác vụ trong Vùng báo động + Tiềm ẩn nguy cơ
        risk_tasks = df_occ_tasks[df_occ_tasks['Vùng rủi ro'].isin(['Vùng báo động (Alert zone)', 'Vùng tiềm ẩn nguy cơ (At-risk zone)'])]
        risk_pct = (len(risk_tasks) / total_occ_tasks) * 100 if total_occ_tasks > 0 else 0.0
        
        # Số tác vụ trong Vùng an toàn + Ổn định
        safe_tasks = df_occ_tasks[df_occ_tasks['Vùng rủi ro'].isin(['Vùng an toàn (Safe zone)', 'Vùng ổn định (Stable zone)'])]
        safe_pct = (len(safe_tasks) / total_occ_tasks) * 100 if total_occ_tasks > 0 else 0.0

        st_analysis(
            f"*Khi đi sâu vào ngành **{selected_occ}**, ma trận phân cụm chỉ ra một kết nối quan trọng: "
            f"Có đến **{risk_pct:.1f}%** số tác vụ của ngành này tập trung ở **Vùng báo động** và **Vùng tiềm ẩn nguy cơ** (phía bên phải ma trận), "
            f"trong khi chỉ có **{safe_pct:.1f}%** tác vụ nằm ở **Vùng an toàn** và **Vùng ổn định** (phía bên trái ma trận). <br><br>"
            f"Kết hợp với cơ cấu thâm niên ở trên: mặc dù ngành này có **{senior_pct:.1f}%** nhân sự giàu kinh nghiệm (Senior), "
            f"nhưng nếu phần lớn tác vụ họ làm hằng ngày nằm ở Vùng rủi ro, họ vẫn đối mặt với nguy cơ bị thay thế cao. "
            f"Đặc biệt đối với các Junior, do chủ yếu làm các tác vụ cơ bản thuộc Vùng báo động, họ là những người dễ bị tổn thương nhất.*"
        )
    with col_scatter_chart:
        fig_scatter = px.scatter(
            df_occ_tasks,
            x='Khả năng tự động hóa (chuyên gia)',
            y='Mong muốn tự động hóa (người lao động)',
            size='Importance',
            color='Vùng rủi ro',
            color_discrete_map=CLUSTER_COLORS,
            hover_data=['Tác vụ', 'Task ID']
        )
        apply_chart_style(fig_scatter, f"Phân nhóm rủi ro các tác vụ: {selected_occ}")
        st.plotly_chart(fig_scatter, use_container_width=True)

# =========================================================================
# TAB 2: Động lực chuyển giao và tấm khiên phòng ngự con người
# =========================================================================
with tab2:
    st_header("Động lực chuyển giao và tấm khiên phòng ngự con người")
    st.write(
        "Để bảo vệ mình trước làn sóng tự động hóa, người lao động cần hiểu rõ động cơ tâm lý thúc đẩy "
        "hành vi chuyển giao tác vụ cho AI, cũng như định hình các rào cản phi kỹ thuật giúp bảo vệ năng lực cốt lõi."
    )
    
    st_subheader("Cường độ động lực thúc đẩy tự động hóa")
    col_rose_text, col_rose_chart = st.columns([1, 1.2])
    with col_rose_text:
        st_analysis(
            "*Chương này giải mã động cơ thực tế của con người: tại sao chúng ta lại muốn tự động hóa? "
            "Biểu đồ hoa hồng chỉ ra rằng động lực mạnh mẽ nhất không phải là để giải quyết các tác vụ có độ khó cao, mà là để "
            "giải phóng bản thân khỏi công việc lặp đi lặp lại và giành lại thời gian rảnh (lần lượt chiếm các thang điểm cao nhất). "
            "Con người muốn chuyển giao phần cơ bắp thủ công cho máy tính để dành năng lượng cho những việc đòi hỏi tư duy chiến lược.*"
        )
    with col_rose_chart:
        reasons_cols = [
            'Reasons for Automation Desire - Free Time',
            'Reasons for Automation Desire - Repetitive',
            'Reasons for Automation Desire - Human Error',
            'Reasons for Automation Desire - Stress',
            'Reasons for Automation Desire - Difficulty',
            'Reasons for Automation Desire - Scale'
        ]
        reasons_labels = [
            'Tăng thời gian rảnh',
            'Tránh việc lặp lại',
            'Giảm thiểu sai sót',
            'Giảm bớt áp lực',
            'Giải quyết độ khó',
            'Mở rộng quy mô'
        ]
        reasons_mean = df_worker_it[reasons_cols].mean().values
        
        fig_rose = go.Figure(go.Barpolar(
            r=reasons_mean,
            theta=reasons_labels,
            marker_color=THEME_PALETTE
        ))
        apply_chart_style(fig_rose, "Đánh giá cường độ động lực tự động hóa theo thang đo trung bình")
        st.plotly_chart(fig_rose, use_container_width=True)
        
    st_subheader("Mật độ phân bổ rào cản phòng thủ phi kỹ thuật")
    col_heat_text, col_heat_chart = st.columns([1, 1.2])
    with col_heat_text:
        st_analysis(
            "*Tấm khiên phòng ngự tự nhiên của con người được định hình rõ nét qua bản đồ mật độ nhiệt. "
            "Trong khi hầu hết các tác vụ kỹ thuật tập trung ở vùng có độ bất định và giao tiếp thấp (dễ bị thay thế), "
            "thì những tác vụ nằm ở góc trên bên phải — đòi hỏi tương tác con người trực tiếp và khả năng ứng biến linh hoạt "
            "trước sự bất định — lại cực kỳ thưa thớt và an toàn. Đây chính là các rào cản phi kỹ thuật giúp con người giữ vững vị thế.*"
        )
    with col_heat_chart:
        fig_density = px.density_heatmap(
            df_model,
            x='Involved Uncertainty',
            y='Interpersonal Communication Requirement',
            labels={
                'Involved Uncertainty': 'Mức độ bất định',
                'Interpersonal Communication Requirement': 'Yêu cầu giao tiếp'
            },
            color_continuous_scale=[[0, '#0d5c3a'], [1, '#fdba74']]
        )
        apply_chart_style(fig_density, "Phân bố mật độ tác vụ trên hai chiều rào cản phi kỹ thuật")
        st.plotly_chart(fig_density, use_container_width=True)
        
    st_subheader("Bẫy năng lực từ AI Agent: mối đe dọa đến tấm khiên chuyên môn")
    
    # Lọc dữ liệu radar theo ngành được chọn, có fallback
    junior_meta = df_meta_it[(df_meta_it['Occupation (O*NET-SOC Title)'] == selected_occ) & (df_meta_it['Experience'].isin(['Less than 1 year', '1-2 year']))]
    senior_meta = df_meta_it[(df_meta_it['Occupation (O*NET-SOC Title)'] == selected_occ) & (df_meta_it['Experience'].isin(['6-10 years', 'More than 10 years']))]
    is_radar_fallback = False
    if len(junior_meta) < 5 or len(senior_meta) < 5:
        junior_meta = df_meta_it[df_meta_it['Experience'].isin(['Less than 1 year', '1-2 year'])]
        senior_meta = df_meta_it[df_meta_it['Experience'].isin(['6-10 years', 'More than 10 years'])]
        is_radar_fallback = True
        


    col_radar_text, col_radar_chart = st.columns([1, 1.2])
    with col_radar_text:
        st_analysis(
            f"*Biểu đồ mạng nhện chỉ ra thực tế đối với ngành **{selected_occ if not is_radar_fallback else 'Công nghệ thông tin'}**: "
            f"Nhóm Senior (>= 6 năm kinh nghiệm) có tỷ lệ sử dụng LLM thường xuyên vượt trội hơn nhóm Junior ở hầu hạft các tác vụ phức tạp như Phân tích (59.9%), Tạo ý tưởng (57.8%) và Thiết kế hệ thống (33.3%). Trong khi đó, Junior chỉ nhỉnh hơn ở tác vụ Viết mã cơ bản. <br><br>"
            f"**Bấy năng lực và Độ lệch kiểm duyệt (Verification Deficit):** Khi Junior lạm dụng AI để viết code nhanh nhưng thiếu tư duy thiết kế hệ thống và khả năng kiểm duyệt của Senior, họ sẽ dễ rơi vào bấy ảo tưởng năng lực. Họ tạo ra hàng ngàn dòng code mà không hiểu rõ cấu trúc hệ thống, dẫn đến việc tích lũy kinh nghiệm thực tế bằng không, khiến họ bị mắc kẹt mãi ở trình độ Junior và dễ bị đào thải nhất khi AI tự động hóa hoàn toàn vùng viết code cơ bản.*"
        )
    with col_radar_chart:
        abilities = ['Viết mã', 'Thiết kế hệ thống', 'Xử lý dữ liệu', 'Phân tích', 'Tạo ý tưởng']
        meta_cols = [
            'LLM Usage by Type - Coding', 
            'LLM Usage by Type - System Design',
            'LLM Usage by Type - Data Processing', 
            'LLM Usage by Type - Analysis',
            'LLM Usage by Type - Idea Generation'
        ]
        
        junior_rates = [junior_meta[c].isin(['Daily', 'Weekly']).mean() * 100 if len(junior_meta) > 0 else 0 for c in meta_cols]
        senior_rates = [senior_meta[c].isin(['Daily', 'Weekly']).mean() * 100 if len(senior_meta) > 0 else 0 for c in meta_cols]
        
        abilities_closed = abilities + [abilities[0]]
        junior_closed = junior_rates + [junior_rates[0]]
        senior_closed = senior_rates + [senior_rates[0]]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=junior_closed,
            theta=abilities_closed,
            fill='toself',
            name='Junior (< 3 năm thâm niên)',
            line=dict(color=THEME_PALETTE[5])
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=senior_closed,
            theta=abilities_closed,
            fill='toself',
            name='Senior (>= 6 năm thâm niên)',
            line=dict(color=THEME_PALETTE[0])
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            )
        )
        apply_chart_style(fig_radar, "Đánh giá tỷ lệ sử dụng LLM thường xuyên theo kinh nghiệm làm việc")
        st.plotly_chart(fig_radar, use_container_width=True)

    # Thêm tiểu mục "Tấm khiên thích ứng" từ dữ liệu thực tế
    st_subheader("Tấm khiên thích ứng: Đào tạo & Năng lực học hỏi liên tục")
    st.write(
        "Bên cạnh các rào cản về giao tiếp và sự bất định, bộ dữ liệu khảo sát và đánh giá của chuyên gia còn chứng minh "
        "rằng **khả năng tự đào tạo và học hỏi liên tục (Adaptability & Learning)** chính là vũ khí tối tân nhất của con người chống lại AI."
    )
    col_shield_text, col_shield_chart = st.columns([1.2, 1])
    with col_shield_text:
        st_analysis(
            "1. **Tác vụ đào tạo/hướng dẫn người khác (Training & Teaching Others):** Cã điểm khả năng tự động hóa bởi AI trung bình cực thấp, chính là **2.5/5.0** (trong khi các tác vụ thường là **3.4/5.0**). Tác vụ này đòi hỏi sự thấm cả, khả năng truyền đạt phi ngôn ngữ và hiểu biết tâm lý con người.\n\n"
            "2. **Tác vụ tự cập nhật kiến thức (Updating & Using Relevant Knowledge):** Cã điểm khả năng tự động hóa bởi AI trung bình chính là **3.1/5.0** (vẫn thấp hơn nhiều so với trung bình). Khả năng thích ứng với công nghệ mới là kỹ năng cực kỳ khó để AI mô phỏng một cách chủ động.\n\n"
            "3. **Học vấn tỷ lệ thuận với khả năng làm chủ AI:** Phân tích dữ liệu khảo sát người lao động cho thấy tỷ lệ sử dụng LLM hàng ngày để nâng cao hiệu suất tăng vọt theo trình độ học vấn: **Doctorate (Tiến sĩ) đạt 61.1%**, **Master's (Thạc sĩ) đạt 44.7%**, trong khi nhóm còn lại chỉ dao động từ **16% - 32%**.\n\n"
            "**Kết luận then chốt:** AI phát triển nhanh chỉ thực sự nguy hiểm khi tốc độ đào tạo lại (Reskilling) và năng lực thích ứng của nhân sự bị tụt hạu. Học vấn cao và tư duy thích nghì là tấm khiên giúp lao động chủ động biến AI thành trợ thủ đắc lực (Strategic power user), thay vì bị động chịu rủi ro thay thế."
        )
    with col_shield_chart:
        # Vẽ một biểu đồ so sánh nhỏ
        df_shield_compare = pd.DataFrame({
            'Loại tác vụ': ['Đào tạo người khác', 'Tự cập nhật kiến thức', 'Các tác vụ khác'],
            'Khả năng tự động hóa bởi AI': [2.5, 3.1, 3.4]
        })
        fig_shield = px.bar(
            df_shield_compare,
            y='Loại tác vụ',
            x='Khả năng tự động hóa bởi AI',
            orientation='h',
            color='Loại tác vụ',
            color_discrete_sequence=['#0d5c3a', '#2d6a4f', '#74c69d'],
            range_x=[0, 5.0]
        )
        apply_chart_style(fig_shield, "Khả năng tự động hóa của các nhóm tác vụ kỹ năng cốt lõi (Thang điểm 5.0)")
        fig_shield.update_layout(showlegend=False)
        st.plotly_chart(fig_shield, use_container_width=True)

# =========================================================================
# TAB 3: Trục thời gian và dự báo (Temporal & forecasting)
# =========================================================================
with tab3:
    st_header("Mô phỏng đà phát triển AI và dự báo rủi ro tác vụ")
    st.write(
        "Năng lực tự động hóa của công nghệ không đứng yên mà phát triển theo thời gian. Ở phần này, chúng ta mô phỏng "
        "đà phát triển của AI tại Mỹ và Việt Nam từ năm 2025 đến 2030, từ đó dự báo cấu trúc rủi ro của từng ngành nghề."
    )
    
    st.markdown(
        r"""
        ### 1. Chỉ số sẵn sàng AI và đà tăng trưởng công nghệ
        Mô hình mô phỏng này tích hợp chỉ số **Government AI Readiness Index (2025)** công bố bởi Oxford Insights để định hình điểm xuất phát của Việt Nam so với Mỹ:
        *   **Chỉ số sẵn sàng của Mỹ (US):** **88.36/100** (hạng 1 thế giới).
        *   **Chỉ số sẵn sàng của Việt Nam (VN):** **59.98/100** (hạng 45 thế giới).
        *   **Tỷ lệ sẵn sàng tương đối ($K_{readiness}$):**
        """
    )
    st.latex(r"K_{readiness} = \frac{59.98}{88.36} \approx 67.9\%")
    st.markdown(
        r"""
        ### 2. Mô hình dự báo quỹ đạo phát triển AI tích hợp Phân cụm K-Means
        Năng lực tự động hóa tích lũy của AI đối với từng tác vụ tại năm $t$ ($t \in [2025, 2030]$) không tăng trưởng cào bằng mà phụ thuộc vào bản chất của tác vụ (được định hình từ phân cụm K-Means ở Trang 1).
        Hệ số điều chỉnh tốc độ tăng trưởng ($M_{cluster}$) được quy định như sau:
        *   **Vùng báo động (Alert zone):** $M_{cluster} = 1.3$ (Tác vụ lặp đi lặp lại, dễ số hóa nên tốc độ tự động hóa cực nhanh).
        *   **Vùng tiềm ẩn nguy cơ (At-risk zone):** $M_{cluster} = 1.1$.
        *   **Vùng ổn định (Stable zone):** $M_{cluster} = 0.8$.
        *   **Vùng an toàn (Safe zone):** $M_{cluster} = 0.5$ (Tác vụ đòi hỏi giao tiếp con người và xử lý sự bất định cao nên tốc độ tự động hóa rất chậm).
        
        Mô hình dự báo tích hợp hệ số điều chỉnh:
        *   **Quỹ đạo AI tại Mỹ (CAGR danh nghĩa g_US = 24.1%):**
        """
    )
    st.latex(r"AI_{US}(t) = \min\left(AI_{base} \times (1 + g_{US} \times M_{cluster})^{t - 2025},\ 5.0\right)")
    st.markdown(
        r"""
        *   **Quỹ đạo AI tại Việt Nam (Việt Nam có độ trễ và CAGR danh nghĩa g_VN = 20.0%):**
        """
    )
    st.latex(r"AI_{VN}(t) = \min\left(AI_{base} \times K_{readiness} \times (1 + g_{VN} \times M_{cluster})^{t - 2025},\ 5.0\right)")
    st.markdown(
        r"""
        *Trong đó:*
        *   $AI_{base}$: Điểm năng lực tự động hóa ban đầu do chuyên gia đánh giá (thang điểm 5.0).
        *   $g_{US} = 24.1\%$: Tốc độ tăng trưởng kép hàng năm của thị trường AI tại Mỹ.
        *   $g_{VN} = 20.0\%$: Tốc độ tăng trưởng kép hàng năm của thị trường AI tại Việt Nam.
        *   $M_{cluster}$: Hệ số nhân điều chỉnh theo cụm rủi ro K-Means của tác vụ.
        
        ### 3. Tại sao tốc độ phát triển AI nhanh ở Mỹ lại là mối nguy hiểm vĩ mô trực diện đối với Việt Nam?
        Nhiều lập luận cho rằng Mỹ phát triển AI nhanh hơn thì chỉ người lao động Mỹ chịu ảnh hưởng trước. Tuy nhiên, dưới góc độ kinh tế vĩ mô và chuỗi giá trị toàn cầu, điều này mang lại 3 nguy cơ đe dọa trực tiếp nền kinh tế số Việt Nam:
        1.  **Hiệu ứng Dịch chuyển ngược kỹ thuật số (Digital Reshoring Effect):** Ngành công nghiệp phần mềm Việt Nam sống dựa vào gia công (IT Outsourcing) cho các doanh nghiệp Mỹ nhờ lợi thế nhân công giá rẻ. Khi AI ở Mỹ phát triển nhanh, chi phí biên để AI thực hiện các tác vụ viết code cơ bản, kiểm thử (thuộc *Vùng báo động*) giảm xuống gần như bằng 0 (chỉ vài cent cho 1 triệu token). Khi chi phí tự động hóa tại nước sở tại rẻ hơn chi phí thuê lao động giá rẻ ở nước ngoài, các công ty Mỹ sẽ rút việc về nước để AI xử lý tự động thay vì thuê offshore. Lợi thế chi phí nhân công rẻ của Việt Nam bị xóa sổ hoàn toàn.
        2.  **Sự chênh lệch về Tấm khiên thích ứng (Readiness & Safety Net Gap):** Mỹ có Chỉ số sẵn sàng AI đứng số 1 thế giới (88.36), họ sở hữu hạ tầng điện toán đám mây khổng lồ, nguồn vốn dồi dào và mạng lưới an sinh xã hội để hỗ trợ chuyển dịch lao động dôi dư. Trong khi đó, Việt Nam có chỉ số sẵn sàng thấp (59.98). Khi làn sóng tự động hóa tràn tới qua các công cụ toàn cầu như GitHub Copilot hay Devin, Việt Nam sẽ đối mặt với cú sốc thất nghiệp cơ cấu ở quy mô rộng mà không có đủ hạ tầng chính sách để bảo vệ và tái đào tạo người lao động kịp thời.
        3.  **Bất đối xứng năng lượng số và Lệ thuộc công nghệ lõi:** Việt Nam không làm chủ các mô hình AI lớn (LLM foundation models) mà chỉ đóng vai trò ứng dụng API từ các tập đoàn công nghệ lớn của Mỹ. Tốc độ AI Mỹ tăng mạnh làm gia tăng khoảng cách công nghệ, khiến Việt Nam hoàn toàn lệ thuộc vào chính sách phân phối dữ liệu, chi phí vận hành và tính bảo mật của các hệ thống nước ngoài, làm xói mòn chủ quyền công nghệ quốc gia.
        
        ### 4. Ngưỡng phân loại rủi ro tác vụ tại Việt Nam
        Tại năm được chọn, các tác vụ trong ngành nghề sẽ được gán vào 3 nhóm rủi ro dựa trên điểm năng lực mô phỏng thực tế $AI_{VN}(t)$:
        *   **Lệ thuộc AI (AI-Automated):** $AI_{VN}(t) \ge 4.0$ (AI có khả năng tự động hóa và thay thế cao).
        *   **Cộng tác AI (AI-Collaborative):** $2.5 \le AI_{VN}(t) < 4.0$ (AI đóng vai trò đồng hành, hỗ trợ con người thực thi).
        *   **Lõi con người (Human Core):** $AI_{VN}(t) < 2.5$ (Tác vụ đòi hỏi năng lực chuyên môn và quyền tự quyết cao của con người).
        """
    )
    st.markdown("---")
    
    st_subheader("Phòng thí nghiệm giả lập và phân tích lộ trình")
    
    # Widget điều khiển (đã đồng bộ từ Sidebar toàn cầu)
    st.info(f"Đang phân tích ngành nghề: **{selected_occ}** | Năm mô phỏng dự báo: **{selected_year}** (Điều chỉnh tại Sidebar thanh bên)")
        
    # Lọc dữ liệu
    if selected_occ == "Tất cả các ngành":
        df_filtered = df_model.copy()
    else:
        df_filtered = df_model[df_model['Ngành nghề'] == selected_occ].copy()
        
    # Tính toán lộ trình
    g_us = 0.241
    g_vn = 0.20
    K_READINESS = 59.98 / 88.36
    
    # Áp dụng hệ số điều chỉnh tốc độ từ K-Means
    multipliers = df_filtered['Vùng rủi ro'].map(CLUSTER_MULTIPLIERS).fillna(1.0)
    
    years_range = list(range(2025, 2031))
    us_trend = []
    vn_trend = []
    for yr in years_range:
        n = yr - 2025
        us_cap_yr = (df_filtered['Khả năng tự động hóa (chuyên gia)'] * ((1 + g_us * multipliers) ** n)).clip(upper=5.0)
        us_trend.append(us_cap_yr.mean())
        
        vn_cap_yr = (df_filtered['Khả năng tự động hóa (chuyên gia)'] * K_READINESS * ((1 + g_vn * multipliers) ** n)).clip(upper=5.0)
        vn_trend.append(vn_cap_yr.mean())
        
    df_chart_data = pd.DataFrame({
        'Năm': years_range,
        'Mỹ': us_trend,
        'Việt Nam': vn_trend
    })
    
    # Vẽ biểu đồ đường
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=df_chart_data['Năm'],
        y=df_chart_data['Mỹ'],
        name='AI tại Mỹ (CAGR K-Means)',
        line=dict(color=THEME_PALETTE[5], width=3, shape='spline')
    ))
    fig_trend.add_trace(go.Scatter(
        x=df_chart_data['Năm'],
        y=df_chart_data['Việt Nam'],
        name='AI tại Việt Nam (CAGR K-Means)',
        line=dict(color=THEME_PALETTE[0], width=3, shape='spline')
    ))
    # Đường ngưỡng rủi ro cao Y=4.0
    fig_trend.add_hline(
        y=4.0,
        line_dash="dash",
        line_color="#ef4444",
        annotation_text="Ngưỡng rủi ro cao (4.0)",
        annotation_position="bottom right"
    )
    # Đường thẳng đứng tại năm được chọn
    fig_trend.add_vline(x=selected_year, line_dash="dot", line_color="#64748b")
    
    apply_chart_style(fig_trend, f"So sánh lộ trình năng lực AI: Mỹ vs Việt Nam ({selected_occ})")
    fig_trend.update_yaxes(range=[1.0, 5.2], title="Điểm năng lực tự động hóa trung bình")
    fig_trend.update_xaxes(tickmode='linear', tick0=2025, dtick=1, title="Năm")
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Tính toán rủi ro tác vụ cho VN tại năm được chọn
    n_sel = selected_year - 2025
    df_sim = df_filtered.copy()
    sim_multipliers = df_sim['Vùng rủi ro'].map(CLUSTER_MULTIPLIERS).fillna(1.0)
    df_sim['AI_VN_sim'] = (df_sim['Khả năng tự động hóa (chuyên gia)'] * K_READINESS * ((1 + g_vn * sim_multipliers) ** n_sel)).clip(upper=5.0)
    
    automated_tasks = df_sim[df_sim['AI_VN_sim'] >= 4.0]
    collaborative_tasks = df_sim[(df_sim['AI_VN_sim'] >= 2.5) & (df_sim['AI_VN_sim'] < 4.0)]
    human_core_tasks = df_sim[df_sim['AI_VN_sim'] < 2.5]
    
    total_tasks = len(df_sim)
    pct_auto = (len(automated_tasks) / total_tasks) * 100 if total_tasks > 0 else 0
    pct_collab = (len(collaborative_tasks) / total_tasks) * 100 if total_tasks > 0 else 0
    pct_human = (len(human_core_tasks) / total_tasks) * 100 if total_tasks > 0 else 0
    
    st_subheader(f"Phân tích cấu trúc rủi ro tác vụ năm {selected_year} (Việt Nam)")
    st.write(
        f"Tại năm dự báo {selected_year}, trong ngành **{selected_occ}**, tổng số {total_tasks} tác vụ được mô phỏng "
        f"và phân loại thành 3 nhóm rủi ro tương ứng:"
    )
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.markdown(
            f"""
            <div style='background-color: #fef2f2; border: 1px solid #fee2e2; border-left: 4px solid #ef4444; padding: 15px; border-radius: 8px;'>
                <p style='margin: 0; font-size: 13px; color: #991b1b; font-weight: bold;'>LỆ THUỘC AI (AI-Automated)</p>
                <h3 style='margin: 4px 0 0 0; color: #ef4444; font-size: 20px; font-weight: 800;'>{len(automated_tasks)} tác vụ ({pct_auto:.1f}%)</h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
    with col_stat2:
        st.markdown(
            f"""
            <div style='background-color: #fffbeb; border: 1px solid #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; border-radius: 8px;'>
                <p style='margin: 0; font-size: 13px; color: #92400e; font-weight: bold;'>CỘNG TÁC AI (AI-Collaborative)</p>
                <h3 style='margin: 4px 0 0 0; color: #d97706; font-size: 20px; font-weight: 800;'>{len(collaborative_tasks)} tác vụ ({pct_collab:.1f}%)</h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
    with col_stat3:
        st.markdown(
            f"""
            <div style='background-color: #f0fdf4; border: 1px solid #dcfce7; border-left: 4px solid #10b981; padding: 15px; border-radius: 8px;'>
                <p style='margin: 0; font-size: 13px; color: #166534; font-weight: bold;'>LÕI CON NGƯỜI (Human Core)</p>
                <h3 style='margin: 4px 0 0 0; color: #10b981; font-size: 20px; font-weight: 800;'>{len(human_core_tasks)} tác vụ ({pct_human:.1f}%)</h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    st.write("")
    
    with st.expander(f"Danh sách tác vụ Lệ thuộc AI ({len(automated_tasks)})", expanded=False):
        if len(automated_tasks) > 0:
            for idx, row in automated_tasks.sort_values(by='AI_VN_sim', ascending=False).reset_index().iterrows():
                st.markdown(f"**{idx+1}. {row['Tác vụ']}**")
                st.caption(f"Yêu cầu kỹ năng: {row['Skill (O*NET Work Activity)']} | Điểm mô phỏng VN: {row['AI_VN_sim']:.2f}/5.0 (Chuyên gia gốc: {row['Khả năng tự động hóa (chuyên gia)']:.2f})")
        else:
            st.write("Không có tác vụ nào thuộc nhóm này.")
            
    with st.expander(f"Danh sách tác vụ Cộng tác AI ({len(collaborative_tasks)})", expanded=False):
        if len(collaborative_tasks) > 0:
            for idx, row in collaborative_tasks.sort_values(by='AI_VN_sim', ascending=False).reset_index().iterrows():
                st.markdown(f"**{idx+1}. {row['Tác vụ']}**")
                st.caption(f"Yêu cầu kỹ năng: {row['Skill (O*NET Work Activity)']} | Điểm mô phỏng VN: {row['AI_VN_sim']:.2f}/5.0 (Chuyên gia gốc: {row['Khả năng tự động hóa (chuyên gia)']:.2f})")
        else:
            st.write("Không có tác vụ nào thuộc nhóm này.")
            
    with st.expander(f"Danh sách tác vụ Lõi con người ({len(human_core_tasks)})", expanded=False):
        if len(human_core_tasks) > 0:
            for idx, row in human_core_tasks.sort_values(by='AI_VN_sim', ascending=True).reset_index().iterrows():
                st.markdown(f"**{idx+1}. {row['Tác vụ']}**")
                st.caption(f"Yêu cầu kỹ năng: {row['Skill (O*NET Work Activity)']} | Điểm mô phỏng VN: {row['AI_VN_sim']:.2f}/5.0 (Chuyên gia gốc: {row['Khả năng tự động hóa (chuyên gia)']:.2f})")
        else:
            st.write("Không có tác vụ nào thuộc nhóm này.")
            
    st_analysis(
        f"*Biểu đồ lộ trình và phân tích cấu trúc rủi ro của ngành **{selected_occ}** chỉ ra khoảng cách vật lý rõ rệt "
        f"giữa tốc độ phát triển AI tại Mỹ và Việt Nam. Điểm xuất phát của Việt Nam thấp hơn đáng kể ($K_{{readiness}} \\approx 67.9\\%$) "
        f"và tốc độ phát triển chậm hơn ($20.0\\%$) tạo ra một khoảng trễ thời gian từ 1 đến 2 năm. Tuy nhiên, mô hình dự báo đã tích hợp "
        f"**hệ số nhân tốc độ từ K-Means (Trang 1)**: các tác vụ thuộc Vùng báo động (như Routine Coding) sẽ bị tự động hóa nhanh hơn 1.3 lần, "
        f"trong khi các tác vụ thuộc Vùng an toàn sẽ được trì hoãn chậm hơn 0.5 lần. <br><br>"
        f"**Rủi ro vĩ mô đối với Việt Nam:** Do cơ cấu ngành IT Việt Nam tập trung cao vào **Gia công phần mềm (Outsourcing)** (vốn là những tác vụ "
        f"thuộc Vùng báo động), việc Mỹ phát triển AI nhanh hơn thực chất sẽ đẩy nhanh tốc độ tự động hóa các dịch vụ này tại nước họ, dẫn đến nguy cơ "
        f"giảm mạnh nhu cầu thuê ngoài (offshoring) đối với nhân lực Việt Nam. Tính đến năm {selected_year}, mô phỏng ghi nhận "
        f"**{pct_auto:.1f}%** số tác vụ của ngành này tại Việt Nam đã rơi vào trạng thái lệ thuộc công nghệ cao (AI-Automated) "
        f"và **{pct_collab:.1f}%** ở trạng thái cộng tác (AI-Collaborative). Người lao động chỉ còn **{pct_human:.1f}%** các tác vụ lõi để phòng ngự.*"
    )

# =========================================================================
# TAB 4: Hệ thống khuyến nghị dịch chuyển nghề nghiệp
# =========================================================================
with tab4:
    st_header("Hệ thống khuyến nghị dịch chuyển nghề nghiệp và nâng cao kỹ năng")
    st.write(
        "Dấu chân phát triển AI tại Việt Nam đặt ra thách thức lớn đối với thị trường lao động. Để giúp người lao động chủ động ứng phó, "
        "hệ thống đề xuất 3 ngành nghề phù hợp nhất dựa trên mức độ tương thích kỹ năng và điều kiện rủi ro tự động hóa tại năm được chọn."
    )
    
    st.markdown(
        r"""
        ### 1. Chỉ số tương đồng kỹ năng Jaccard (Jaccard Similarity Index)
        Chỉ số Jaccard đo lường mức độ chồng chéo giữa tập hợp kỹ năng yêu cầu của ngành nghề nguồn ($S_{source}$) và ngành nghề mục tiêu ($S_{target}$):
        """
    )
    st.latex(r"J(S_{source}, S_{target}) = \frac{|S_{source} \cap S_{target}|}{|S_{source} \cup S_{target}|} \times 100\%")
    st.markdown(
        r"""
        ### 2. Các điều kiện lọc ràng buộc tối ưu hóa dịch chuyển
        Để đảm bảo tính thực tiễn và an toàn, các ngành nghề được đề xuất phải thỏa mãn đồng thời ba bộ lọc:
        *   **Bộ lọc An toàn công nghệ (Rủi ro thấp hơn):** Mức độ rủi ro trung bình của ngành nghề mục tiêu phải thấp hơn ngành gốc tại năm mô phỏng được chọn:
        """
    )
    st.latex(r"AI_{target}(t) < AI_{source}(t)")
    st.markdown(
        r"""
        *   **Bộ lọc Bảo vệ thu nhập (Lương tối thiểu 85%):** Mức lương trung bình năm của ngành mục tiêu không thấp hơn 85% mức lương của ngành nguồn:
        """
    )
    st.latex(r"Wage_{target} \ge 85\% \times Wage_{source}")
    st.markdown(
        r"""
        *   **Bộ lọc Tương đồng kỹ năng (Tương đồng cao):** Chỉ chọn các ngành nghề có độ tương đồng kỹ năng Jaccard so với ngành gốc từ 20% trở lên:
        """
    )
    st.latex(r"J(S_{source}, S_{target}) \ge 20\%")
    st.markdown(
        r"""
        ### 3. Nguyên lý phân loại tác vụ dịch chuyển
        Các tác vụ của ngành đề xuất được đối chiếu với kỹ năng của ngành gốc để hỗ trợ định hướng đào tạo:
        *   **Tác vụ tương đồng (Kỹ năng sẵn có):** Yêu cầu kỹ năng đã được tích lũy trong ngành nguồn:
        """
    )
    st.latex(r"S(Task) \in S_{source}")
    st.markdown(
        r"""
        *   **Tác vụ mới cần học (Kỹ năng bổ sung):** Yêu cầu kỹ năng mới, đòi hỏi người lao động phải học tập bồi dưỡng thêm:
        """
    )
    st.latex(r"S(Task) \notin S_{source}")
    st.markdown("---")
    
    # Sử dụng trực tiếp selected_occ và selected_year từ Sidebar toàn cầu
    if selected_occ == "Tất cả các ngành":
        st.warning("Vui lòng chọn một ngành nghề cụ thể ở thanh bên (Sidebar) để nhận gợi ý dịch chuyển sự nghiệp phù hợp.")
        st.stop()
        
    st.success(f"Ngành nghề đang phân tích: **{selected_occ}** (Năm mô phỏng dự báo: **{selected_year}**)")

    # Helper to calculate simulated risk with K-Means multipliers
    K_READINESS = 59.98 / 88.36
    g_vn = 0.20
    
    def calculate_occ_risk(df_tasks, year):
        n = year - 2025
        mults = df_tasks['Vùng rủi ro'].map(CLUSTER_MULTIPLIERS).fillna(1.0)
        caps = (df_tasks['Khả năng tự động hóa (chuyên gia)'] * K_READINESS * ((1 + g_vn * mults) ** n)).clip(upper=5.0)
        return caps.mean()
        
    def calculate_safe_ratio(df_tasks):
        safe_stable = df_tasks[df_tasks['Vùng rủi ro'].isin(['Vùng an toàn (Safe zone)', 'Vùng ổn định (Stable zone)'])]
        return len(safe_stable) / len(df_tasks) if len(df_tasks) > 0 else 0.0

    # Tính toán các thông số của ngành nguồn
    df_src_tasks = df_model[df_model['Ngành nghề'] == selected_occ]
    skills_src = set(df_src_tasks['Skill (O*NET Work Activity)'].dropna().unique())
    src_wage = df_src_tasks['Occupation Mean Annual Wage'].mean()
    src_avg_risk = calculate_occ_risk(df_src_tasks, selected_year)
    
    # Tìm kiếm các ứng viên dịch chuyển phù hợp
    candidates = []
    for occ in sorted(df_model['Ngành nghề'].unique()):
        if occ == selected_occ:
            continue
            
        df_occ_tasks = df_model[df_model['Ngành nghề'] == occ]
        occ_wage = df_occ_tasks['Occupation Mean Annual Wage'].mean()
        occ_avg_risk = calculate_occ_risk(df_occ_tasks, selected_year)
        safe_ratio = calculate_safe_ratio(df_occ_tasks)
        
        # Tính tương đồng Jaccard
        skills_tgt = set(df_occ_tasks['Skill (O*NET Work Activity)'].dropna().unique())
        union_skills = skills_src.union(skills_tgt)
        jaccard = len(skills_src.intersection(skills_tgt)) / len(union_skills) if len(union_skills) > 0 else 0
        
        # Thỏa mãn đồng thời ba bộ lọc (Rủi ro thấp hơn, Lương >= 85%, Tương đồng Jaccard >= 20%)
        if occ_avg_risk < src_avg_risk and occ_wage >= 0.85 * src_wage and jaccard >= 0.20:
            candidates.append({
                'Ngành nghề': occ,
                'Rủi ro': occ_avg_risk,
                'Lương': occ_wage,
                'Jaccard': jaccard,
                'Kỹ năng': skills_tgt,
                'SafeRatio': safe_ratio
            })
            
    is_relaxed = False
    
    # Bước 1: Nới lỏng Jaccard tương đồng xuống 10% nhưng giữ nguyên rủi ro và lương >= 85%
    if len(candidates) < 3:
        candidates = []
        for occ in sorted(df_model['Ngành nghề'].unique()):
            if occ == selected_occ:
                continue
            df_occ_tasks = df_model[df_model['Ngành nghề'] == occ]
            occ_wage = df_occ_tasks['Occupation Mean Annual Wage'].mean()
            occ_avg_risk = calculate_occ_risk(df_occ_tasks, selected_year)
            safe_ratio = calculate_safe_ratio(df_occ_tasks)
            skills_tgt = set(df_occ_tasks['Skill (O*NET Work Activity)'].dropna().unique())
            union_skills = skills_src.union(skills_tgt)
            jaccard = len(skills_src.intersection(skills_tgt)) / len(union_skills) if len(union_skills) > 0 else 0
            
            if occ_avg_risk < src_avg_risk and occ_wage >= 0.85 * src_wage and jaccard >= 0.10:
                candidates.append({
                    'Ngành nghề': occ,
                    'Rủi ro': occ_avg_risk,
                    'Lương': occ_wage,
                    'Jaccard': jaccard,
                    'Kỹ năng': skills_tgt,
                    'SafeRatio': safe_ratio
                })
        is_relaxed = True
        
    # Bước 2: Nới lỏng thêm lương >= 70% và tương đồng 10%
    if len(candidates) < 3:
        candidates = []
        for occ in sorted(df_model['Ngành nghề'].unique()):
            if occ == selected_occ:
                continue
            df_occ_tasks = df_model[df_model['Ngành nghề'] == occ]
            occ_wage = df_occ_tasks['Occupation Mean Annual Wage'].mean()
            occ_avg_risk = calculate_occ_risk(df_occ_tasks, selected_year)
            safe_ratio = calculate_safe_ratio(df_occ_tasks)
            skills_tgt = set(df_occ_tasks['Skill (O*NET Work Activity)'].dropna().unique())
            union_skills = skills_src.union(skills_tgt)
            jaccard = len(skills_src.intersection(skills_tgt)) / len(union_skills) if len(union_skills) > 0 else 0
            
            if occ_avg_risk < src_avg_risk and occ_wage >= 0.70 * src_wage and jaccard >= 0.10:
                candidates.append({
                    'Ngành nghề': occ,
                    'Rủi ro': occ_avg_risk,
                    'Lương': occ_wage,
                    'Jaccard': jaccard,
                    'Kỹ năng': skills_tgt,
                    'SafeRatio': safe_ratio
                })
        is_relaxed = True
        
    # Bước 3: Nới lỏng hoàn toàn lương (chỉ lọc rủi ro thấp hơn và tương đồng >= 10%)
    if len(candidates) < 3:
        candidates = []
        for occ in sorted(df_model['Ngành nghề'].unique()):
            if occ == selected_occ:
                continue
            df_occ_tasks = df_model[df_model['Ngành nghề'] == occ]
            occ_wage = df_occ_tasks['Occupation Mean Annual Wage'].mean()
            occ_avg_risk = calculate_occ_risk(df_occ_tasks, selected_year)
            safe_ratio = calculate_safe_ratio(df_occ_tasks)
            skills_tgt = set(df_occ_tasks['Skill (O*NET Work Activity)'].dropna().unique())
            union_skills = skills_src.union(skills_tgt)
            jaccard = len(skills_src.intersection(skills_tgt)) / len(union_skills) if len(union_skills) > 0 else 0
            
            if occ_avg_risk < src_avg_risk and jaccard >= 0.10:
                candidates.append({
                    'Ngành nghề': occ,
                    'Rủi ro': occ_avg_risk,
                    'Lương': occ_wage,
                    'Jaccard': jaccard,
                    'Kỹ năng': skills_tgt,
                    'SafeRatio': safe_ratio
                })
        is_relaxed = True
 
    # Bước 4: Lọc chỉ theo rủi ro thấp hơn
    if len(candidates) < 3:
        candidates = []
        for occ in sorted(df_model['Ngành nghề'].unique()):
            if occ == selected_occ:
                continue
            df_occ_tasks = df_model[df_model['Ngành nghề'] == occ]
            occ_wage = df_occ_tasks['Occupation Mean Annual Wage'].mean()
            occ_avg_risk = calculate_occ_risk(df_occ_tasks, selected_year)
            safe_ratio = calculate_safe_ratio(df_occ_tasks)
            skills_tgt = set(df_occ_tasks['Skill (O*NET Work Activity)'].dropna().unique())
            union_skills = skills_src.union(skills_tgt)
            jaccard = len(skills_src.intersection(skills_tgt)) / len(union_skills) if len(union_skills) > 0 else 0
            
            if occ_avg_risk < src_avg_risk:
                candidates.append({
                    'Ngành nghề': occ,
                    'Rủi ro': occ_avg_risk,
                    'Lương': occ_wage,
                    'Jaccard': jaccard,
                    'Kỹ năng': skills_tgt,
                    'SafeRatio': safe_ratio
                })
        is_relaxed = True
        
    # Bước 5: Lấy tất cả các ngành tương đồng cao nhất
    if len(candidates) < 3:
        candidates = []
        for occ in sorted(df_model['Ngành nghề'].unique()):
            if occ == selected_occ:
                continue
            df_occ_tasks = df_model[df_model['Ngành nghề'] == occ]
            occ_wage = df_occ_tasks['Occupation Mean Annual Wage'].mean()
            occ_avg_risk = calculate_occ_risk(df_occ_tasks, selected_year)
            safe_ratio = calculate_safe_ratio(df_occ_tasks)
            skills_tgt = set(df_occ_tasks['Skill (O*NET Work Activity)'].dropna().unique())
            union_skills = skills_src.union(skills_tgt)
            jaccard = len(skills_src.intersection(skills_tgt)) / len(union_skills) if len(union_skills) > 0 else 0
            
            candidates.append({
                'Ngành nghề': occ,
                'Rủi ro': occ_avg_risk,
                'Lương': occ_wage,
                'Jaccard': jaccard,
                'Kỹ năng': skills_tgt,
                'SafeRatio': safe_ratio
            })
        is_relaxed = True
        
    # Sắp xếp và lấy top 3
    candidates = sorted(candidates, key=lambda x: x['Jaccard'], reverse=True)
    top_3 = candidates[:3]
    
    st_subheader("La bàn dịch chuyển sự nghiệp")
    
    if is_relaxed:
        st.warning("Không tìm thấy đủ 3 ngành nghề thỏa mãn đồng thời bộ lọc an toàn công nghệ, tương đồng kỹ năng và bảo vệ thu nhập tối thiểu 85%. Hệ thống đã tự động nới lỏng các điều kiện để tối ưu hóa gợi ý.")
        
    if len(top_3) > 0:
        col_rec1, col_rec2, col_rec3 = st.columns(3)
        cols = [col_rec1, col_rec2, col_rec3]
        
        for idx, cand in enumerate(top_3):
            with cols[idx]:
                # Quy đổi lương sang VND thực tế tại Việt Nam
                wage_vnd_year = cand['Lương'] * EXCHANGE_RATE_USD_VND * VN_WAGE_ADJUSTMENT_FACTOR
                wage_vnd_month = wage_vnd_year / 12

                # 1. Phân loại tác vụ trước để tính toán Độ sẵn sàng chuyển đổi (Transition Readiness)
                df_tgt_tasks = df_model[df_model['Ngành nghề'] == cand['Ngành nghề']].copy()
                df_similar = df_tgt_tasks[df_tgt_tasks['Skill (O*NET Work Activity)'].isin(skills_src)]
                df_new = df_tgt_tasks[~df_tgt_tasks['Skill (O*NET Work Activity)'].isin(skills_src)]
                
                total_tgt_tasks = len(df_tgt_tasks)
                retraining_load = (len(df_new) / total_tgt_tasks * 100) if total_tgt_tasks > 0 else 0.0
                readiness_score = 100.0 - retraining_load
                
                # Phân loại tác vụ mới thành dễ và khó dựa trên yêu cầu chuyên môn
                df_new_easy = df_new[df_new['Domain Expertise Requirement'] < 3.0]
                df_new_hard = df_new[df_new['Domain Expertise Requirement'] >= 3.0]
                
                # Xác định màu sắc chỉ báo mức độ sẵn sàng chuyển đổi
                readiness_color = "#10b981" if readiness_score >= 70 else "#f59e0b" if readiness_score >= 40 else "#ef4444"
                readiness_level = "Cao (Dễ chuyển đổi)" if readiness_score >= 70 else "Trung bình" if readiness_score >= 40 else "Thấp (Cần đào tạo nhiều)"

                # 2. Vẽ card thông tin đẹp mắt sử dụng custom CSS class rec-card
                st.markdown(
                    f"""
                    <div class="rec-card">
                        <span class="rec-tag">Đề xuất {idx+1}</span>
                        <div class="rec-title"><b>{cand['Ngành nghề']}</b></div>
                        <div class="rec-metric">
                            <span class="rec-metric-label">Tương thích Jaccard:</span>
                            <span class="rec-metric-val" style="color: #0d5c3a; font-size: 15px;">{cand['Jaccard']*100:.1f}%</span>
                        </div>
                        <div class="rec-metric">
                            <span class="rec-metric-label">Tỷ lệ tác vụ An toàn/Ổn định:</span>
                            <span class="rec-metric-val" style="color: #10b981; font-weight: 700;">{cand['SafeRatio']*100:.1f}%</span>
                        </div>
                        <div class="rec-metric">
                            <span class="rec-metric-label">Độ sẵn sàng Chuyển đổi:</span>
                            <span class="rec-metric-val" style="color: {readiness_color}; font-weight: 700;">
                                {readiness_score:.1f}%<br>
                                <span style="font-size: 10px; font-weight: 500; color: #64748b;">({readiness_level})</span>
                            </span>
                        </div>
                        <div class="rec-metric">
                            <span class="rec-metric-label">Rủi ro AI (VN - {selected_year}):</span>
                            <span class="rec-metric-val" style="color: {'#ef4444' if cand['Rủi ro'] >= 4.0 else '#f59e0b' if cand['Rủi ro'] >= 2.5 else '#10b981'};">{cand['Rủi ro']:.2f}/5.0</span>
                        </div>
                        <div class="rec-metric" style="border-bottom: none; margin-bottom: 0;">
                            <span class="rec-metric-label">Mức lương trung bình:</span>
                            <span class="rec-metric-val" style="color: #0d5c3a; text-align: right; line-height: 1.2;">
                                <b>{wage_vnd_year/1e6:.1f} tr VND/năm</b><br>
                                <span style="color: #64748b; font-weight: 500; font-size: 11px;">(~{wage_vnd_month/1e6:.1f} tr/tháng)</span>
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # 3. Lời khuyên thích ứng nhanh
                if readiness_score >= 70:
                    st.caption(" **Lộ trình:** Rất tiềm năng! Các kỹ năng của bạn tương thích rất tốt, chỉ cần tự học một vài mảnh ghép nhỏ.")
                elif readiness_score >= 40:
                    st.caption(" **Lộ trình:** Cân bằng. Vừa làm vừa tích lũy thêm các kỹ năng mới trong vòng 3-6 tháng.")
                else:
                    st.caption(" **Lộ trình:** Thử thách nhưng xứng đáng! Cần chuẩn bị học tập nghiêm túc để tạo lợi thế bền vững.")

                # 4. Hiển thị chi tiết tác vụ (nằm dưới card)
                with st.expander(f"Tác vụ tương đồng (Kỹ năng sẵn có) - {len(df_similar)}", expanded=False):
                    if len(df_similar) > 0:
                        for t_idx, t_row in df_similar.reset_index().iterrows():
                            st.markdown(f"- **{t_row['Tác vụ']}**")
                            st.caption(f"Kỹ năng sở hữu: {t_row['Skill (O*NET Work Activity)']}")
                    else:
                        st.write("Không có tác vụ tương đồng.")
                        
                with st.expander(f"Tác vụ bổ trợ dễ học (Kỹ năng bổ sung nhanh) - {len(df_new_easy)}", expanded=False):
                    if len(df_new_easy) > 0:
                        for t_idx, t_row in df_new_easy.reset_index().iterrows():
                            st.markdown(f"- **{t_row['Tác vụ']}**")
                            st.caption(f"Kỹ năng cần bổ sung nhanh: {t_row['Skill (O*NET Work Activity)']}")
                    else:
                        st.write("Không có tác vụ bổ trợ dễ học.")

                with st.expander(f"Tác vụ chuyên sâu cần học (Kỹ năng cốt lõi) - {len(df_new_hard)}", expanded=False):
                    if len(df_new_hard) > 0:
                        for t_idx, t_row in df_new_hard.reset_index().iterrows():
                            st.markdown(f"- **{t_row['Tác vụ']}**")
                            st.caption(f"Kỹ năng chuyên sâu: {t_row['Skill (O*NET Work Activity)']}")
                    else:
                        st.write("Không có tác vụ chuyên sâu.")
    else:
        st.write("Không tìm thấy đề xuất dịch chuyển phù hợp.")
        
    # Phân tích kết quả
    recs_names = [c['Ngành nghề'] for c in top_3]
    recs_str = ", ".join([f"**{r}**" for r in recs_names])
    analysis_text = f"""
*   **Chiến lược dịch chuyển chủ động:** Đối với ngành nghề nguồn là **{selected_occ}**, việc dịch chuyển sang các vị trí như {recs_str} sẽ giúp giảm thiểu đáng kể mức độ rủi ro bị thay thế bởi AI tại Việt Nam vào năm {selected_year}, đồng thời vẫn đảm bảo bảo vệ tối ưu mức thu nhập của bạn (không thấp hơn 85% lương gốc). Đặc biệt, tỷ lệ tác vụ an toàn/ổn định cao trong cụm K-Means cho thấy tính bền vững dài hạn của các đề xuất chuyển đổi này trước làn sóng tự động hóa.
*   **Chỉ số Độ sẵn sàng Chuyển đổi (Transition Readiness Index):** Chỉ số này phản ánh phần trăm số lượng kỹ năng của ngành mục tiêu mà bạn **đã sở hữu sẵn** từ công việc hiện tại. Số điểm này càng cao, quá trình chuyển đổi nghề nghiệp của bạn càng diễn ra thuận lợi và nhanh chóng.
*   **Phân rã Kỹ năng thông minh:** Bằng cách chia tách các tác vụ mới thành nhóm **"Dễ học tự tích lũy"** và **"Chuyên sâu cần đào tạo"**, người lao động sẽ không bị ngợp và có thể xây dựng lộ trình học tập cuốn chiếu, tối ưu hóa thời gian thích nghi công nghệ mới.
"""
    st_analysis(analysis_text)

    # Chốt hạ đề tài - Khuyến nghị chính sách vĩ mô và chiến lược thích ứng
    st_subheader("Khuyến nghị chính sách vĩ mô và chiến lược lao động quốc gia")
    st.markdown(
        """<div style="background-color: #f8fafc; padding: 24px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 24px; color: #334155; font-size: 14px; line-height: 1.6;">
<h4 style="color: #0d5c3a; margin-top: 0; margin-bottom: 16px; font-size: 16px; font-weight: 700; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">Định hướng chiến lược khi chốt hạ đề tài</h4>
<p>Để bảo vệ nền kinh tế số và lực lượng lao động công nghệ trước làn sóng tự động hóa, Việt Nam cần thực thi đồng bộ ba chiến lược:</p>
<div style="margin-bottom: 16px; border-left: 4px solid #0d5c3a; padding-left: 12px;">
<strong style="color: #0d5c3a; font-size: 14.5px;">1. Dịch chuyển Chuỗi giá trị IT (Value Chain Upgrading)</strong><br>
Các doanh nghiệp Việt Nam không thể tiếp tục cạnh tranh bằng mô hình gia công phần mềm cơ bản (IT Outsourcing viết mã cơ bắp). Cần tái định vị nhân sự lên các tác vụ thuộc <strong>Vùng an toàn (Safe zone)</strong> như thiết kế hệ thống, kiến trúc giải pháp và kỹ năng giao tiếp khách hàng liên nhân sự.
</div>
<div style="margin-bottom: 16px; border-left: 4px solid #f59e0b; padding-left: 12px;">
<strong style="color: #d97706; font-size: 14.5px;">2. Tối ưu hóa Lộ trình thích ứng & Giảm độ trễ Đào tạo lại (Adaptation Path Optimization)</strong><br>
Thay vì đặt ra những rào cản đào tạo lại gây nản lòng cho người lao động, các cơ sở đào tạo cần sử dụng <strong>Chỉ số Độ sẵn sàng Chuyển đổi (Transition Readiness Index)</strong> để thiết kế các lộ trình thích ứng theo từng giai đoạn. Phân tách rõ các kỹ năng bổ sung nhanh (tự học qua các khóa học ngắn hạn) và các kỹ năng chuyên sâu (đào tạo chính quy dài hạn) để rút ngắn độ trễ thích nghi công nghệ của lực lượng lao động IT.
</div>
<div style="border-left: 4px solid #ef4444; padding-left: 12px;">
<strong style="color: #ef4444; font-size: 14.5px;">3. Tăng cường "Tấm khiên thích ứng" quốc gia</strong><br>
Chính phủ cần đẩy mạnh các chính sách nâng cao Chỉ số sẵn sàng AI (Government AI Readiness Index). Cụ thể là xây dựng hạ tầng điện toán đám mây dùng chung, kiến tạo sandbox pháp lý an toàn và ban hành các quỹ hỗ trợ an sinh xã hội dành riêng cho việc chuyển đổi số và tái đào tạo nghề nghiệp cho lao động dôi dư.
</div>
</div>""",
        unsafe_allow_html=True
    )
