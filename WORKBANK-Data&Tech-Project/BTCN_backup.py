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
    </style>
    """,
    unsafe_allow_html=True
)

THEME_PALETTE = ['#0d5c3a', '#2d845e', '#6bb38a', '#e0a96d', '#f48c06', '#fdba74']

CLUSTER_COLORS = {
    'Vùng an toàn (Safe zone)': '#0d5c3a',           
    'Vùng ổn định (Stable zone)': '#3a8d67',         
    'Vùng tiềm ẩn nguy cơ (At-risk zone)': '#e0a96d', 
    'Vùng báo động (Alert zone)': '#fdba74'           
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

TECH_KEYWORDS = ['computer','software','data','information','network','web','programmer',
                 'developer','analyst','systems','ai','artificial intelligence',
                 'machine learning','algorithm']

all_jobs = df_worker_meta['Occupation (O*NET-SOC Title)'].dropna().unique()
tech_jobs = [job for job in all_jobs if any(kw in str(job).lower() for kw in TECH_KEYWORDS)]

df_meta_it = df_worker_meta[df_worker_meta['Occupation (O*NET-SOC Title)'].isin(tech_jobs)].copy()
df_tasks_it = df_task[df_task['Occupation (O*NET-SOC Title)'].isin(tech_jobs)].copy()
df_worker_it = df_worker[df_worker['Occupation (O*NET-SOC Title)'].isin(tech_jobs)].copy()
df_expert_it = df_expert[df_expert['Occupation (O*NET-SOC Title)'].isin(tech_jobs)].copy()

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

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Bức tranh toàn cảnh (Industry overview)",
    "Kỳ vọng và thực tế (Expectation vs. reality)",
    "Động lực và rào cản (Drivers & barriers)",
    "Trục thời gian và dự báo (Temporal & forecasting)",
    "Phân khúc và định hình chân dung (Human segmentation)"
])

# =========================================================================
# TAB 1: Bức tranh toàn cảnh (Industry overview)
# =========================================================================
with tab1:
    st_header("Bức tranh toàn cảnh về bộ dữ liệu và thực trạng công nghiệp")
    st.write(
        "Nhằm đảm bảo tính đại diện và khách quan khi định hình chân dung phân khúc dữ liệu và công nghệ, "
        "phần trình bày đã áp dụng kỹ thuật lọc dữ liệu dựa trên văn bản từ tổng thể dữ liệu Work Bank. "
        "Quy trình trích xuất mẫu sử dụng bộ lọc danh mục nghề nghiệp chứa các từ khóa trọng tâm: "
        "**computer, software, data, information, network, web, programmer, developer, analyst, systems, ai,"
        "artificial intelligence, machine learning và algorithm**."
    )
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st_kpi_card("Tổng số nhân sự khảo sát", "505", "green")
    with col2:
        st_kpi_card("Số ngành khảo sát", f"{df_model['Ngành nghề'].nunique()}", "amber")
    with col3:
        st_kpi_card("Số lượng tác vụ phân tích", "288", "green")
    with col4:
        st_kpi_card("Mức lương trung bình năm", f"${df_model['Occupation Mean Annual Wage'].mean():,.0f}", "amber")
    
    st_subheader("Phân bố thâm niên lực lượng lao động")
    col_donut_text, col_donut_chart = st.columns([1, 1.2])
    with col_donut_text:
        st_analysis(
    "*Biểu đồ tròn thể hiện cơ cấu phân bổ thâm niên kinh nghiệm làm việc của lực lượng lao động tham gia khảo sát với sự áp đảo hoàn toàn từ nhóm nhân sự dày dặn kinh nghiệm. Cụ thể, nhóm chuyên gia có thâm niên **trên 10 năm** chiếm tỷ lệ cao nhất với **27.7%**, bám sát ngay sau đó là nhóm **từ 3–5 năm** với **27.1%**, và nhóm **từ 6–10 năm** giữ tỷ lệ **23.6%**. Trong khi đó, các nhóm nhân sự trẻ hơn chiếm tỷ trọng khiêm tốn hơn nhiều, với nhóm **1–2 năm** đạt **16.8%** và nhóm **dưới 1 năm** chỉ chiếm vỏn vẹn **4.75%**. Việc tổng nhóm lao động có từ **3 năm kinh nghiệm trở lên** chiếm tới **78.4%** cho thấy tập dữ liệu mang tính đại diện rất cao cho những nhân sự có trải nghiệm thực tế sâu sắc trong các ngành liên quan đến công nghệ và dữ liệu.*"
)
    with col_donut_chart:
        EXP_ORDER = ['Less than 1 year', '1-2 year', '3-5 years', '6-10 years', 'More than 10 years']
        EXP_MAP_VN = {
            'Less than 1 year': 'Dưới 1 năm',
            '1-2 year': '1-2 năm',
            '3-5 years': '3-5 năm',
            '6-10 years': '6-10 năm',
            'More than 10 years': 'Trên 10 năm'
        }
        
        exp_counts = df_meta_it['Experience'].value_counts().reindex(EXP_ORDER).dropna().reset_index()
        exp_counts.columns = ['Kinh nghiệm', 'Số lượng']
        exp_counts['Kinh nghiệm'] = exp_counts['Kinh nghiệm'].map(EXP_MAP_VN)
        
        fig_donut = px.pie(
            exp_counts, 
            values='Số lượng', 
            names='Kinh nghiệm', 
            hole=0.6,
            color_discrete_sequence=THEME_PALETTE
        )
        apply_chart_style(fig_donut, "Tỷ lệ phân bổ thâm niên kinh nghiệm làm việc")
        st.plotly_chart(fig_donut, use_container_width=True)
    
    st_subheader("Tần suất sử dụng LLM theo giới tính")
    col_gender_text, col_gender_chart = st.columns([1, 1.2])
    
    usage_rank = {'Never': 0, 'Occasionally': 1, 'Weekly': 2, 'Daily': 3}
    inv_usage_rank = {0: 'Never', 1: 'Occasionally', 2: 'Weekly', 3: 'Daily'}
    
    df_meta_it_temp = df_meta_it.copy()
    for col in llm_cols:
        df_meta_it_temp[col] = df_meta_it_temp[col].fillna('Never').astype(str).str.strip()
        
    df_meta_it_temp['LLM Usage Overall'] = df_meta_it_temp[llm_cols].apply(
        lambda r: inv_usage_rank[max([usage_rank.get(val, 0) for val in r])],
        axis=1
    )
    
    FREQ_MAP_VN = {
        'Daily': 'Hàng ngày',
        'Weekly': 'Hàng tuần',
        'Occasionally': 'Thỉnh thoảng',
        'Never': 'Chưa từng dùng'
    }
    
    gender_llm = df_meta_it_temp.groupby(['Gender', 'LLM Usage Overall']).size().reset_index(name='Số lượng')
    gender_llm = gender_llm[gender_llm['LLM Usage Overall'] != 'Occasionally'].copy()
    gender_totals = gender_llm.groupby('Gender')['Số lượng'].sum().reset_index(name='Tổng số')
    gender_llm = pd.merge(gender_llm, gender_totals, on='Gender')
    gender_llm['Tỷ lệ phần trăm'] = (gender_llm['Số lượng'] / gender_llm['Tổng số']) * 100
    gender_llm['Giới tính'] = gender_llm['Gender'].map({'Male': 'Nam', 'Female': 'Nữ'})
    gender_llm['Tần suất sử dụng'] = gender_llm['LLM Usage Overall'].map(FREQ_MAP_VN)
    gender_llm = gender_llm.dropna()
    
    def get_pct(gender, freq):
        try:
            val = gender_llm[(gender_llm['Gender'] == gender) & (gender_llm['LLM Usage Overall'] == freq)]['Tỷ lệ phần trăm'].values[0]
            return f"{val:.1f}%"
        except:
            return "0.0%"
            
    pct_female_weekly = get_pct('Female', 'Weekly')
    pct_male_weekly = get_pct('Male', 'Weekly')
    pct_female_daily = get_pct('Female', 'Daily')
    pct_male_daily = get_pct('Male', 'Daily')
    pct_female_never = get_pct('Female', 'Never')
    pct_male_never = get_pct('Male', 'Never')
    
    with col_gender_text:
        pct_female_num = float(pct_female_weekly.replace('%','')) + float(pct_female_daily.replace('%',''))
        pct_male_num = float(pct_male_weekly.replace('%','')) + float(pct_male_daily.replace('%',''))
        st_analysis(
            f"*Biểu đồ cột thể hiện cơ cấu so sánh tỷ lệ tần suất sử dụng LLM tổng thể cho các tác vụ công việc giữa hai nhóm giới tính Nam và Nữ sau khi chuẩn hóa. "
            f"Kết quả cho thấy một **xu thế bình đẳng hóa trong việc làm chủ công nghệ** khi cả hai giới đều có tỷ lệ tương đồng cao ở các nhóm sử dụng thường xuyên. "
            f"Cụ thể, ở mức độ **'Hàng tuần'**, tỷ lệ đạt **{pct_female_weekly} ở Nữ** và **{pct_male_weekly} ở Nam**; "
            f"ở mức độ **'Hàng ngày'**, tỷ lệ lần lượt là **{pct_female_daily} ở Nữ** và **{pct_male_daily} ở Nam**. "
            f"Mặc dù tỷ lệ nhóm **'Chưa từng dùng'** ở Nữ giới vẫn còn cao hơn Nam giới (**{pct_female_never}** so với **{pct_male_never}**), "
            f"việc tổng tỷ lệ nhân sự có thói quen ứng dụng công cụ hàng tuần hoặc hàng ngày đạt tới **{pct_female_num:.1f}% ở Nữ** "
            f"và **{pct_male_num:.1f}% ở Nam** cho thấy AI đã thực sự "
            f"trở thành một trợ thủ đắc lực không thể thiếu trong công việc thường nhật của cả hai giới mà không chịu rào cản lớn nào.*"
        )
    with col_gender_chart:
        fig_gender = px.bar(
            gender_llm,
            x='Tần suất sử dụng',
            y='Tỷ lệ phần trăm',
            color='Giới tính',
            barmode='group',
            category_orders={'Tần suất sử dụng': ['Chưa từng dùng', 'Hàng tuần', 'Hàng ngày']},
            color_discrete_sequence=[THEME_PALETTE[0], THEME_PALETTE[5]]
        )
        fig_gender.update_yaxes(title="Tỷ lệ phần trăm trong nhóm giới tính")
        apply_chart_style(fig_gender, "So sánh tỷ lệ tần suất sử dụng LLM tổng thể giữa nam và nữ")
        st.plotly_chart(fig_gender, use_container_width=True)
    
    st_subheader("Bẫy năng lực từ AI Agent: Khi công nghệ đi trước kinh nghiệm")
    col_radar_text, col_radar_chart = st.columns([1, 1.2])
    with col_radar_text:
        st_analysis(
            "*Biểu đồ mạng nhện chỉ ra hiện tượng <strong>ảo tưởng năng lực do phụ thuộc vào AI Agent</strong>: Nhóm nhân sự trẻ (<strong>Junior dưới 3 năm</strong>) có tỷ lệ sử dụng "
            "công nghệ tự động hóa cho các công việc vĩ mô như <strong>thiết kế hệ thống và tạo ý tưởng cao hơn hẳn</strong> so với "
            "đội ngũ <strong>Senior (trên 6 năm)</strong>. Sự phụ thuộc sớm vào công cụ khi chưa tích lũy đủ kinh nghiệm thực tế có thể dẫn đến "
            "<strong>tạo ra lỗ hổng lớn về mặt kỹ thuật</strong> và làm suy yếu khả năng tự kiểm định hệ thống của nhóm nhân sự lệ thuộc vào công nghệ.*"
        )
    with col_radar_chart:
        junior_meta = df_meta_it[df_meta_it['Experience'].isin(['Less than 1 year', '1-2 year'])]
        senior_meta = df_meta_it[df_meta_it['Experience'].isin(['6-10 years', 'More than 10 years'])]
        
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
            name="Nhân sự junior (dưới 3 năm)",
            line=dict(color=THEME_PALETTE[5], width=2)
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=senior_closed, 
            theta=abilities_closed, 
            fill='toself', 
            name="Nhân sự senior (trên 6 năm)",
            line=dict(color=THEME_PALETTE[0], width=2)
        ))
        apply_chart_style(fig_radar, "Mức độ sử dụng công nghệ thường xuyên theo thâm niên chuyên môn")
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], ticksuffix='%')
            ),
            margin=dict(t=120, b=40, l=40, r=40)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# =========================================================================
# TAB 2: Kỳ vọng và thực tế (Expectation vs. reality)
# =========================================================================
with tab2:
    st_header("Đối chiếu khoảng cách kỳ vọng của con người và năng lực thực tế của AI Agent")
    st.write(
        "Phân tích khoảng cách giữa nhu cầu chủ quan của lập trình viên (mong muốn tự động hóa tác vụ) "
        "và năng lực khách quan của hệ thống công nghệ (được đánh giá bởi chuyên gia) chỉ ra độ lệch pha lớn. "
        "Điều này giúp định vị các nhóm công việc vào các phân vùng rủi ro khác nhau để doanh nghiệp kịp thời ứng phó."
    )
    
    st_subheader("Ma trận định vị chiến lược tác vụ")
    st.write(
        "Thuật toán phân cụm chia các tác vụ thành bốn vùng rủi ro đặc trưng. Trục hoành biểu thị năng lực của AI Agent, "
        "trục tung biểu thị mức độ mong muốn chuyển giao công việc của lập trình viên. Những tác vụ có kích thước bóng "
        "càng lớn thể hiện mức độ quan trọng càng cao đối với hiệu suất làm việc."
    )
    
    fig_scatter = px.scatter(
        df_model,
        x='Khả năng tự động hóa (chuyên gia)',
        y='Mong muốn tự động hóa (người lao động)',
        size='Importance',
        color='Vùng rủi ro',
        color_discrete_map=CLUSTER_COLORS,
        hover_data=['Tác vụ', 'Task ID']
    )
    apply_chart_style(fig_scatter, "Phân nhóm rủi ro các tác vụ công việc bằng thuật toán phân cụm")
    st.plotly_chart(fig_scatter, use_container_width=True)
    st_analysis(
        "*Ma trận định vị cho thấy một sự dịch chuyển rõ rệt khi các tác vụ khảo sát tập trung phần lớn về phía bên phải sơ đồ, thuộc **vùng báo động (Alert zone)** và **vùng tiềm ẩn nguy cơ (At-risk zone)**. Tại đây, mật độ các điểm dữ liệu xuất hiện **dày đặc nhất** ở nhóm có khả năng tự động hóa cao (**từ mức 3.0 đến 5.0**), chứng tỏ phần lớn các tác vụ trong ngành đều đã đủ điều kiện công nghệ để AI can thiệp sâu. Ngược lại, số lượng tác vụ nằm ở **vùng an toàn (Safe zone)** và **vùng ổn định (Stable zone)** phía bên trái lại **thưa thớt hơn hẳn**, chỉ giới hạn chủ yếu ở nhóm có khả năng tự động hóa thấp (**từ mức 1.5 đến 2.5**). Sự chênh lệch lớn này khẳng định rằng số lượng công việc có nguy cơ bị thay thế hoặc chuyển giao cho AI đang chiếm tỷ trọng áp đảo, trong khi những tác vụ mà con người giữ quyền tự quyết hoàn toàn đang ngày càng thu hẹp và ít đi.*"
)
    
    st_subheader("Bảy tác vụ có khoảng cách kỳ vọng và thực tế lớn nhất")
    st.write(
        "Biểu đồ thể hiện các tác vụ có sự chênh lệch tuyệt đối cao nhất giữa kỳ vọng con người và năng lực công cụ. "
        "Đây chính là những điểm nhạy cảm rủi ro nhất của doanh nghiệp do ảo tưởng công nghệ hoặc do áp lực công việc quá tải "
        "nhưng công nghệ chưa thể gánh vác."
    )
    
    df_model['Khoảng cách tuyệt đối'] = (df_model['Mong muốn tự động hóa (người lao động)'] - df_model['Khả năng tự động hóa (chuyên gia)']).abs()
    top_gaps = df_model.sort_values(by='Khoảng cách tuyệt đối', ascending=False).head(7).copy()
    top_gaps = top_gaps.sort_values(by='Khoảng cách tuyệt đối', ascending=True).reset_index(drop=True)
    top_gaps['Mã tác vụ'] = [f"Tác vụ {7 - i}" for i in range(len(top_gaps))]
    
    fig_gap = px.bar(
        top_gaps,
        x='Khoảng cách tuyệt đối',
        y='Mã tác vụ',
        orientation='h',
        color='Khoảng cách tuyệt đối',
        color_continuous_scale=[[0, '#0d5c3a'], [1, '#fdba74']],
        custom_data=['Tác vụ']
    )
    fig_gap.update_traces(
        hovertemplate="<b>%{y}</b><br>Khoảng cách: %{x:.2f}<br>Tác vụ: %{customdata[0]}<extra></extra>"
    )
    fig_gap.update_layout(coloraxis_showscale=False)
    apply_chart_style(fig_gap, "Khoảng cách chênh lệch tuyệt đối giữa mong muốn và năng lực tự động hóa")
    st.plotly_chart(fig_gap, use_container_width=True)
    st_analysis(
        "*Bảy tác vụ có khoảng cách tuyệt đối lớn nhất là những điểm nóng cần được doanh nghiệp quan tâm. Chúng đại diện cho những công việc mà lập trình viên mong muốn được tự động hóa nhưng hiện tại AI Agent chưa đủ năng lực để thực hiện. Việc nhận diện sớm các tác vụ này giúp doanh nghiệp **tối ưu hóa nguồn lực**, **đào tạo nhân sự** và **đầu tư công nghệ** một cách hiệu quả hơn. Tác vụ có độ chênh lệch cao nhất là **'Write and code logical and physical database descriptions and specify identifiers of database to management system, or direct others in coding descriptions'** với độ chênh lệch là **2.83*** "
    )
    
    st_subheader("Ranh giới phân cực năng lực tự động hóa của các tác vụ cực đoan")
    st.write(
        "Đối chiếu năm tác vụ mà công cụ tự động hóa thực hiện tốt nhất so với năm tác vụ thực hiện kém nhất. "
        "Giá trị trên biểu đồ thể hiện độ lệch so với mức năng lực trung bình (trung điểm 3.0), làm nổi bật "
        "sự phân cực rõ rệt của khả năng kỹ thuật hiện tại."
    )
    
    top_5 = df_model.nlargest(5, 'Khả năng tự động hóa (chuyên gia)').copy()
    worst_5 = df_model.nsmallest(5, 'Khả năng tự động hóa (chuyên gia)').copy()
    df_extreme = pd.concat([top_5, worst_5])
    df_extreme['Độ lệch tự động hóa'] = df_extreme['Khả năng tự động hóa (chuyên gia)'] - 3.0
    df_extreme['Phân loại tác vụ'] = df_extreme['Độ lệch tự động hóa'].apply(lambda x: 'Khả năng cao' if x >= 0 else 'Khả năng thấp')
    
    fig_diverge = px.bar(
        df_extreme,
        x='Độ lệch tự động hóa',
        y='Tác vụ rút gọn',
        orientation='h',
        color='Phân loại tác vụ',
        color_discrete_map={'Khả năng cao': THEME_PALETTE[5], 'Khả năng thấp': THEME_PALETTE[0]}
    )
    apply_chart_style(fig_diverge, "Mức độ lệch so với trung điểm của mười tác vụ phân cực")
    st.plotly_chart(fig_diverge, use_container_width=True)
    st_analysis(
        "*Biểu đồ ranh giới phân cực thể hiện sự đối chiếu mười tác vụ cực đoan dựa trên mức độ lệch so với trung điểm năng lực tự động hóa (mức 3.0). Kết quả phân tích cho thấy một sự phân cực rõ rệt và không đối xứng về mặt kỹ thuật hiện tại. Ở nhóm **khả năng cao (màu cam)**, cả năm tác vụ mà công cụ tự động hóa thực hiện **tốt nhất** bao gồm các công việc **mang tính quy trình** như **ghi chép thủ tục kiểm thử, duy trì cơ sở dữ liệu, giám sát hiệu suất máy tính, lập biểu đồ quy trình và điều tra mạng** đều đạt mức lệch dương tuyệt đối là **+2.0**, chạm trần năng lực tự động hóa tối đa. Ngược lại, ở nhóm **khả năng thấp (màu xanh lá)**, mức độ lệch âm của các tác vụ mà AI thực hiện **kém nhất** lại có sự phân hóa và biên độ hẹp hơn, dao động từ **-1.0 đến -1.5** (như **thiết kế chương trình phát triển, ứng dụng chuyên môn lý thuyết, hay sao lưu phục hồi dữ liệu**). Sự chênh lệch này khẳng định rằng các tác vụ phù hợp cho tự động hóa đã đạt đến độ chín muồi tối đa về mặt công nghệ, trong khi những tác vụ đòi hỏi tư duy chiến lược nâng cao của con người vẫn tạo ra một vùng đệm an toàn mà AI chưa thể hoàn toàn san lấp.*"
    )

# =========================================================================
# TAB 3: Động lực và rào cản (Drivers & barriers)
# =========================================================================
with tab3:
    st_header("Động lực thúc đẩy và rào cản phòng thủ tự nhiên của con người")
    st.write(
        "Để giải thích bản chất đằng sau việc phân cụm tác vụ, chúng ta cần tìm hiểu động cơ tâm lý thúc đẩy "
        "lập trình viên chuyển giao công việc, cũng như các rào cản tự nhiên được định nghĩa bởi các thuộc tính "
        "kỹ năng nghề nghiệp bảo vệ năng lực lõi của con người trước sự can thiệp của thuật toán."
    )
    
    st_subheader("Cường độ động lực thúc đẩy tự động hóa")
    st.write(
        "Trực quan hóa mức độ đồng thuận của đội ngũ nhân sự đối với các động lực tâm lý. Mong muốn "
        "giải phóng bản thân khỏi các tác vụ lặp đi lặp lại và giảm tải áp lực thời gian đóng vai trò chi phối."
    )
    
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
    st_analysis(
        "*Biểu đồ mạng cực hoa hồng thể hiện đánh giá cường độ đồng thuận của sáu lý do muốn tự động hóa theo thang đo trung bình, mang lại cái nhìn rõ nét về sự chênh lệch mức độ ưu tiên của người lao động. Kết quả phân tích cho thấy các lý do liên quan đến tối ưu hóa thời gian và công việc có sự áp đảo vượt trội so với các yếu tố còn lại. Cụ thể, động lực **mạnh mẽ nhất** xuất phát từ nhu cầu **'Tăng thời gian rảnh'**, khoảng **0.45** và **'Tránh việc lặp lại'** các công việc nhàm chán. Theo sau đó là nhóm động lực về chất lượng vận hành bao gồm **'Giảm thiểu sai sót'** và **'Mở rộng quy mô'**. Ngược lại, hai khía cạnh là **'Giảm bớt áp lực'** và **'Giải quyết độ khó'** lại chiếm tỷ trọng thấp và thưa thớt hơn hẳn khi nằm sát vùng trung tâm. Sự chênh lệch nhiều - ít này khẳng định việc giảm tải gánh nặng thực thi thủ công và giải phóng thời gian chính là mục tiêu hàng đầu của nhân sự khi tiếp cận công nghệ tự động hóa, vượt trội hơn hẳn so với kỳ vọng giải quyết các áp lực hay công việc có độ khó cao.*"
    )
    
    col_t3_left, col_t3_right = st.columns(2)
    
    with col_t3_left:
        st_subheader("Mật độ phân bổ rào cản phòng thủ")
        st.write(
            "Đối chiếu mức độ bất định của công việc và yêu cầu giao tiếp xã hội. Khu vực mật độ cao "
            "ở góc trên bên phải đại diện cho các tác vụ đòi hỏi sự thích ứng liên tục và tương tác trực tiếp "
            "giữa con người, tạo nên tấm khiên phòng thủ tự nhiên chống lại sự thay thế từ công nghệ."
        )
        
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
        st_analysis(
            "*Bản đồ nhiệt làm nổi bật sự chênh lệch mật độ tác vụ rõ rệt giữa hai chiều rào cản phi kỹ thuật. Số lượng tác vụ tập trung phần lớn (**đạt đỉnh từ 15 đến hơn 20**) ở khu vực có **mức độ bất định thấp đến trung bình** và **yêu cầu giao tiếp thấp (mức 1.5 - 2.5)**, cho thấy các công việc mang tính quy trình, ít biến động vẫn chiếm tỷ trọng áp đảo. Ngược lại, các tác vụ ở góc trên bên phải lại ít hơn hẳn, chứng minh rằng những công việc có **độ bất định cao** và **yêu cầu giao tiếp lớn** tuy xuất hiện thưa thớt nhưng lại chính là **rào cản phòng thủ vững chắc** giúp con người không bị máy tính thay thế.*"
        )
        
    with col_t3_right:
        st_subheader("Tọa độ đa biến của các tác vụ cực đoan")
        st.write(
            "Sợi chỉ liên kết cấu trúc thuộc tính của mười tác vụ phân cực. Kết quả chỉ ra các công việc có "
            "yêu cầu chuyên môn sâu kết hợp quyền tự quyết của con người ở mức cao luôn duy trì năng lực tự động hóa ở mức thấp nhất."
        )
        
        fig_parallel = go.Figure(data=go.Parcoords(
            line=dict(color=df_extreme['Khả năng tự động hóa (chuyên gia)'], colorscale=[[0, '#0d5c3a'], [1, '#fdba74']]),
            dimensions=[
                dict(range=[1, 5], label='Yêu cầu chuyên môn', values=df_extreme['Domain Expertise Requirement']),
                dict(range=[1, 5], label='Quyền tự quyết con người', values=df_extreme['Human Agency Scale Rating']),
                dict(range=[1, 5], label='Năng lực tự động hóa', values=df_extreme['Khả năng tự động hóa (chuyên gia)'])
            ]
        ))
        apply_chart_style(fig_parallel, "Đường biểu diễn thuộc tính của nhóm tác vụ phân cực")
        fig_parallel.update_layout(margin=dict(t=120, b=40, l=60, r=60))
        st.plotly_chart(fig_parallel, use_container_width=True)
        st_analysis(
            "*Biểu đồ tọa độ đa biến vạch rõ sự tương phản tuyệt đối trong cấu trúc thuộc tính giữa hai nhóm tác vụ phân cực thông qua hệ thống các sợi chỉ liên kết. Đối với nhóm **5 đường màu xanh lá**, dữ liệu tập trung áp đảo ở mức cao tại hai cột thuộc tính đầu tiên khi **yêu cầu chuyên môn cao** kết hợp với **quyền tự quyết của con người** ở mức cao. Sự cộng hưởng này đã kéo ghì năng lực tự động hóa của máy tính xuống mức thấp nhất. Ngược lại, nhóm **5 đường màu vàng cam** thể hiện xu hướng ngược lại hoàn toàn khi chạm đáy ở hai thuộc tính đầu với **yêu cầu chuyên môn thấp** và **quyền tự quyết gần như bằng không**, khiến các đường biểu diễn bật vọt thẳng lên mức đỉnh tuyệt đối là **5.0** ở cột năng lực tự động hóa. Sự đối lập giữa các đường đi ngang ổn định của nhóm xanh và các đường cắt chéo đột ngột của nhóm cam là minh chứng cho thấy AI đang chiếm trọn các tác vụ rập khuôn, thiếu tính tự quyết nhưng hoàn toàn bất lực trước những công việc đòi hỏi chuyên môn cao và quyền kiểm soát cốt lõi của con người.*"
        )

# =========================================================================
# TAB 4: Trục thời gian và dự báo (Temporal & forecasting)
# =========================================================================
with tab4:
    st_header("Mô phỏng đà phát triển công nghệ và lộ trình chuyển dịch kỹ năng")
    st.write(
        "Năng lực tự động hóa của công nghệ không đứng yên mà phát triển theo quy luật số mũ. Dựa trên phân tích dự báo, "
        "chúng ta mô phỏng điểm giao thoa giữa khả năng của công nghệ và yêu cầu chuyên môn của con người, từ đó "
        "định hình lộ trình chuẩn bị kỹ năng đón đầu làn sóng biến động trước năm 2030."
    )
    
    st_subheader("Phòng thí nghiệm mô phỏng đà tăng trưởng công nghệ")
    st.write(
        "Kéo thanh chọn năm bên dưới để mô phỏng đà phát triển của năng lực tự động hóa so với đường yêu cầu năng lực chuyên môn tĩnh của con người."
    )
    st.markdown(
        r"""
        **Mô hình tăng trưởng năng lực tự động hóa tích lũy:**
        Năng lực tự động hóa của AI được giả định tăng trưởng lũy tiến theo cấp số mũ với tỷ lệ tăng trưởng $15\%$ mỗi năm ($g = 0.15$), giới hạn tối đa ở điểm số $5.0$ (năng lực tự động hóa hoàn toàn):
        """
    )
    st.latex(r"AI_{cap}(t) = \min\left(AI_{cap}(2025) \times (1 + g)^{t - 2025},\ 5.0\right)")
    st.markdown(
        r"""
        *Trong đó:*
        * $AI_{cap}(t)$: Năng lực tự động hóa mô phỏng tại năm dự báo $t$.
        * $AI_{cap}(2025)$: Điểm đánh giá năng lực tự động hóa thực tế ban đầu từ chuyên gia.
        * $g = 0.15$: Tốc độ tăng trưởng giả định của công nghệ mỗi năm.
        """
    )
    
    selected_year = st.slider("Chọn năm dự báo:", min_value=2025, max_value=2030, value=2025, step=1, key="forecasting_slider")
    sim_N = selected_year - 2025
    
    years_range = list(range(2025, 2031))
    ai_caps = []
    human_caps = []
    for y in years_range:
        n = y - 2025
        sim_cap = (df_model['Khả năng tự động hóa (chuyên gia)'] * (1.15 ** n)).clip(upper=5.0)
        ai_caps.append(sim_cap.mean())
        human_caps.append(df_model['Domain Expertise Requirement'].mean())
        
    df_trend = pd.DataFrame({
        'Năm': years_range,
        'Năng lực tự động hóa': ai_caps,
        'Yêu cầu chuyên môn': human_caps
    })
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=df_trend['Năm'], 
        y=df_trend['Năng lực tự động hóa'], 
        name='Năng lực tự động hóa mô phỏng', 
        line=dict(color=THEME_PALETTE[5], width=3)
    ))
    fig_trend.add_trace(go.Scatter(
        x=df_trend['Năm'], 
        y=df_trend['Yêu cầu chuyên môn'], 
        name='Yêu cầu chuyên môn của con người', 
        line=dict(color=THEME_PALETTE[0], width=3, dash='dash')
    ))
    fig_trend.add_vline(x=selected_year, line_dash="dot", line_color="#64748b")
    apply_chart_style(fig_trend, "Mô phỏng đà phát triển tự động hóa so với năng lực chuyên môn")
    st.plotly_chart(fig_trend, use_container_width=True)
    st_analysis(
        "*Đường biểu diễn tiến hóa mô phỏng tốc độ phát triển của tự động hóa so với yêu cầu chuyên môn. "
        "Khi kéo thanh trượt năm về phía tương lai, khoảng cách giữa đường **năng lực tự động hóa** (cam nhạt) và **yêu cầu "
        "chuyên môn của con người** (xanh đậm) thu hẹp dần, cho thấy số lượng tác vụ rơi vào **vùng rủi ro tự động hóa cao** "
        "tăng lên nhanh chóng, đặt ra yêu cầu cấp bách về kế hoạch chuyển đổi kỹ năng chủ động.*"
    )
    
    # Tính toán tác vụ rủi ro tại thời điểm được chọn
    df_simulated = df_model.copy()
    df_simulated['Năng lực mô phỏng'] = (df_simulated['Khả năng tự động hóa (chuyên gia)'] * (1.15 ** sim_N)).clip(upper=5.0)
    
    danger_tasks_count = len(df_simulated[df_simulated['Năng lực mô phỏng'] >= 4.0])
    danger_percentage = (danger_tasks_count / len(df_simulated)) * 100
    
    st.write(
        f"Tại năm dự báo {selected_year}, mô phỏng ghi nhận có {danger_tasks_count} trên tổng số {len(df_simulated)} tác vụ "
        f"({danger_percentage:.1f}%) rơi vào trạng thái rủi ro tự động hóa cao (năng lực công cụ đạt từ 4.0 trở lên)."
    )
    
    st_subheader("La bàn chuyển đổi kỹ năng và lộ trình chuyển dịch tác vụ")
    st.write(
        "Chọn ngành nghề và tác vụ hiện tại của bạn để tìm kiếm các tác vụ chuyển dịch an toàn hơn "
        "(năng lực công cụ thấp, quyền tự quyết cao) trong cùng ngành nghề dựa trên sự tương thích về mặt thuộc tính kỹ năng."
    )
    
    col_sel_job, col_sel_task = st.columns(2)
    with col_sel_job:
        selected_occupation = st.selectbox("Chọn ngành nghề của bạn:", sorted(df_simulated['Ngành nghề'].unique()), key="job_dropdown")
    with col_sel_task:
        job_specific_tasks = df_simulated[df_simulated['Ngành nghề'] == selected_occupation]
        selected_task_name = st.selectbox("Chọn tác vụ bạn đang làm:", sorted(job_specific_tasks['Tác vụ'].unique()), key="task_dropdown")
        
    chosen_task = job_specific_tasks[job_specific_tasks['Tác vụ'] == selected_task_name].iloc[0]
    
    # Đưa ra các gợi ý an toàn
    safe_recs = job_specific_tasks.sort_values(
        by=['Human Agency Scale Rating', 'Năng lực mô phỏng'], 
        ascending=[False, True]
    ).head(3)
    
    st.write("Trạng thái hiện tại của tác vụ được chọn:")
    c1, c2, c3 = st.columns(3)
    with c1:
        st_kpi_card("Năng lực công cụ hiện tại", f"{chosen_task['Khả năng tự động hóa (chuyên gia)']:.2f}/5.0", "green")
    with c2:
        st_kpi_card(f"Năng lực công cụ tại năm {selected_year}", f"{chosen_task['Năng lực mô phỏng']:.2f}/5.0", "amber")
    with c3:
        st_kpi_card("Quyền tự chủ con người", f"{chosen_task['Human Agency Scale Rating']:.2f}/5.0", "green")
    
    st.write("Đề xuất lộ trình chuyển dịch sang các tác vụ có độ bảo vệ cao:")
    rec_cols = st.columns(3)
    for idx, row in safe_recs.reset_index(drop=True).iterrows():
        with rec_cols[idx]:
            with st.container(border=True):
                st.markdown(f"<p style='font-size: 14px; color: {THEME_PALETTE[1]}; font-weight: bold; margin-bottom: 4px;'>Đề xuất {idx+1}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 15px; font-weight: bold; margin-top: 0; margin-bottom: 8px;'>{row['Tác vụ']}</p>", unsafe_allow_html=True)
                st.write(f"Kỹ năng: {row['Skill (O*NET Work Activity)']}")
                st.write(f"Tự chủ: {row['Human Agency Scale Rating']:.2f}/5.0")
                st.write(f"Năng lực AI dự báo: {row['Năng lực mô phỏng']:.2f}/5.0")

# =========================================================================
# TAB 5: Phân khúc và định hình chân dung (Human segmentation)
# =========================================================================
with tab5:
    st_header("Phòng thử nghiệm nhân sự và mô phỏng chiến lược tương lai")
    st.write(
        "Chào mừng bạn đến với Phòng thử nghiệm nhân sự. Tại đây, bạn có thể tự đánh giá vị thế sự nghiệp của chính mình "
        "thông qua la bàn chân dung cá nhân, hoặc đóng vai trò nhà quản trị để mô phỏng mức độ rủi ro công nghệ "
        "của tổ chức dựa trên cấu trúc đội ngũ phòng ban."
    )
    
    st_subheader("Hệ thống phân loại chân dung nhân sự trong kỷ nguyên AI")
    st.write(
        "Hệ thống phân loại này bổ trợ cho mô hình phân cụm K-Means (ở Trang 2), giúp chuyển dịch góc nhìn từ "
        "'rủi ro tự động hóa của tác vụ' sang 'khả năng thích ứng thực tế của con người'. Lực lượng lao động "
        "được phân chia làm 4 chân dung đặc trưng dựa trên các yếu tố thâm niên kinh nghiệm, mức lương và hành vi ứng dụng AI thực tế:"
    )
    
    st.markdown(
        """
        <table style="width:100%; border-collapse: collapse; margin-bottom: 25px; font-size: 14.5px;">
            <thead>
                <tr style="background-color: #0d5c3a; color: #ffffff; text-align: left;">
                    <th style="padding: 12px; border: 1px solid #e2e8f0; font-weight: 700;">Chân dung nhân sự</th>
                    <th style="padding: 12px; border: 1px solid #e2e8f0; font-weight: 700;">Kinh nghiệm</th>
                    <th style="padding: 12px; border: 1px solid #e2e8f0; font-weight: 700;">Mức lương</th>
                    <th style="padding: 12px; border: 1px solid #e2e8f0; font-weight: 700;">Hành vi ứng dụng AI</th>
                </tr>
            </thead>
            <tbody>
                <tr style="background-color: #f8fafc;">
                    <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold; color: #0d5c3a;">Chuyên gia tích hợp chiến lược<br><small style="color: #64748b; font-style: italic;">(Strategic power user)</small></td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">Cao (trên 3 năm, thường >10 năm)</td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">Cao ($86K+)</td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">Sử dụng AI thường xuyên (hàng ngày/tuần) cho các tác vụ phức tạp như Thiết kế hệ thống và Phân tích dữ liệu.</td>
                </tr>
                <tr>
                    <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold; color: #3a8d67;">Chuyên gia truyền thống<br><small style="color: #64748b; font-style: italic;">(Traditional domain expert)</small></td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">Cao (trên 3 năm)</td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">Trung bình - Cao</td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">Hầu như chưa từng dùng AI. Dựa hoàn toàn vào năng lực chuyên môn và quy trình làm việc truyền thống lâu năm.</td>
                </tr>
                <tr style="background-color: #f8fafc;">
                    <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold; color: #b45309;">Nhân sự nhạy bén công nghệ<br><small style="color: #64748b; font-style: italic;">(Adaptive tech adopter)</small></td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">Thấp - Trung bình (dưới 3 năm)</td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">Trung bình</td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">Thích ứng cực nhanh, sử dụng AI thường xuyên cho các tác vụ kỹ thuật như Viết mã và Thiết kế hệ thống.</td>
                </tr>
                <tr>
                    <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold; color: #c2410c;">Nhân sự lệ thuộc công nghệ<br><small style="color: #64748b; font-style: italic;">(Replaceable tech dependent)</small></td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">Thấp (dưới 3 năm)</td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">Thấp ($0-60K)</td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">Sử dụng AI thường xuyên nhưng chỉ cho các tác vụ đơn giản (như viết mã lặp lại), thiếu năng lực tự quyết và tư duy hệ thống độc lập.</td>
                </tr>
            </tbody>
        </table>
        """,
        unsafe_allow_html=True
    )
    
    st_subheader("La bàn chân dung sự nghiệp cá nhân")
    st.write(
        "Hãy nhập thông tin thâm niên, mức thu nhập và tần suất sử dụng LLM thực tế của bạn đối với 5 nhóm tác vụ cốt lõi. "
        "Hệ thống sẽ định vị chân dung nghề nghiệp của bạn, đối chiếu khoảng cách kỹ năng với hình mẫu chuyên gia và đưa ra lời khuyên phát triển."
    )
    
    col_input, col_radar = st.columns([1, 1.2])
    with col_input:
        user_exp = st.selectbox(
            "Thâm niên kinh nghiệm của bạn:",
            options=['Dưới 1 năm', '1-2 năm', '3-5 năm', '6-10 năm', 'Trên 10 năm'],
            key="user_exp"
        )
        user_income = st.selectbox(
            "Mức thu nhập hàng năm của bạn (USD):",
            options=['Dưới $30K', '$30K - $60K', '$60K - $86K', '$86K - $165K', '$165K - $209K', '$209K - $529K', 'Trên $529K'],
            key="user_income"
        )
        st.write("**Tần suất bạn sử dụng LLM cho các tác vụ:**")
        user_coding = st.selectbox("1. Viết mã (Coding):", options=['Chưa từng dùng', 'Thỉnh thoảng', 'Hàng tuần', 'Hàng ngày'], key="u_coding")
        user_sysdesign = st.selectbox("2. Thiết kế hệ thống (System Design):", options=['Chưa từng dùng', 'Thỉnh thoảng', 'Hàng tuần', 'Hàng ngày'], key="u_sys")
        user_dataproc = st.selectbox("3. Xử lý dữ liệu (Data Processing):", options=['Chưa từng dùng', 'Thỉnh thoảng', 'Hàng tuần', 'Hàng ngày'], key="u_data")
        user_analysis = st.selectbox("4. Phân tích (Analysis):", options=['Chưa từng dùng', 'Thỉnh thoảng', 'Hàng tuần', 'Hàng ngày'], key="u_ana")
        user_ideagen = st.selectbox("5. Tạo ý tưởng (Idea Generation):", options=['Chưa từng dùng', 'Thỉnh thoảng', 'Hàng tuần', 'Hàng ngày'], key="u_idea")
        
        exp_mapping = {
            'Dưới 1 năm': 'Less than 1 year',
            '1-2 năm': '1-2 year',
            '3-5 năm': '3-5 years',
            '6-10 năm': '6-10 years',
            'Trên 10 năm': 'More than 10 years'
        }
        income_mapping = {
            'Dưới $30K': '0-30K',
            '$30K - $60K': '30-60K',
            '$60K - $86K': '60-86K',
            '$86K - $165K': '86K-165K',
            '$165K - $209K': '165K-209K',
            '$209K - $529K': '209K-529K',
            'Trên $529K': '529K+'
        }
        freq_db_mapping = {
            'Chưa từng dùng': 'Never',
            'Thỉnh thoảng': 'Occasionally',
            'Hàng tuần': 'Weekly',
            'Hàng ngày': 'Daily'
        }
        
        user_row = {
            'Income': income_mapping[user_income],
            'Experience': exp_mapping[user_exp],
            'LLM Usage by Type - Coding': freq_db_mapping[user_coding],
            'LLM Usage by Type - System Design': freq_db_mapping[user_sysdesign],
            'LLM Usage by Type - Data Processing': freq_db_mapping[user_dataproc],
            'LLM Usage by Type - Analysis': freq_db_mapping[user_analysis],
            'LLM Usage by Type - Idea Generation': freq_db_mapping[user_ideagen]
        }
        user_persona = classify_worker_persona(user_row)
        
        st.markdown("### Kết quả định vị:")
        color_type = "green" if "Strategic" in user_persona or "Traditional" in user_persona else "amber"
        border_color = '#0d5c3a' if color_type == 'green' else '#f59e0b'
        text_color = '#0d5c3a' if color_type == 'green' else '#b45309'
        st.markdown(
            f"""
            <div style="
                border: 2px solid {border_color};
                border-radius: 12px;
                padding: 16px 20px;
                background-color: #ffffff;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                margin-bottom: 24px;
                width: 100%;
            ">
                <p style='font-size: 13px; color: #64748b; margin-top: 0; margin-bottom: 6px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;'>Chân dung AI của bạn</p>
                <h4 style='font-size: 18px; color: {text_color}; margin-top: 0; margin-bottom: 0; font-weight: 700; line-height: 1.4;'>{user_persona}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_radar:
        freq_mapping = {'Daily': 4, 'Weekly': 3, 'Occasionally': 2, 'Never': 1}
        df_radar_calc = df_user_it.copy()
        for col in llm_cols:
            df_radar_calc[col] = df_radar_calc[col].map(freq_mapping).fillna(1)
        
        benchmark_data = df_radar_calc[df_radar_calc['Chân dung nhân sự'] == 'Chuyên gia tích hợp chiến lược (Strategic power user)'][llm_cols].mean()
        benchmark_scores = [benchmark_data[col] for col in llm_cols]
        
        user_scores = [
            freq_mapping[freq_db_mapping[user_coding]],
            freq_mapping[freq_db_mapping[user_sysdesign]],
            freq_mapping[freq_db_mapping[user_dataproc]],
            freq_mapping[freq_db_mapping[user_analysis]],
            freq_mapping[freq_db_mapping[user_ideagen]]
        ]
        
        skills_labels = ['Viết mã', 'Thiết kế hệ thống', 'Xử lý dữ liệu', 'Phân tích', 'Tạo ý tưởng']
        skills_closed = skills_labels + [skills_labels[0]]
        benchmark_closed = benchmark_scores + [benchmark_scores[0]]
        user_closed = user_scores + [user_scores[0]]
        
        fig_overlay = go.Figure()
        fig_overlay.add_trace(go.Scatterpolar(
            r=benchmark_closed,
            theta=skills_closed,
            fill='toself',
            name="Hình mẫu: Chuyên gia chiến lược",
            line=dict(color='#0d5c3a', width=2),
            opacity=0.3
        ))
        fig_overlay.add_trace(go.Scatterpolar(
            r=user_closed,
            theta=skills_closed,
            fill='toself',
            name="Hồ sơ của bạn",
            line=dict(color='#f59e0b', width=3),
            opacity=0.75
        ))
        
        apply_chart_style(fig_overlay, "Đối chiếu tần suất sử dụng LLM của bạn và hình mẫu chuyên gia")
        fig_overlay.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[1, 4], 
                    tickvals=[1, 2, 3, 4], 
                    ticktext=['Chưa từng', 'Thỉnh thoảng', 'Hàng tuần', 'Hàng ngày']
                ),
                domain=dict(x=[0.15, 0.85], y=[0.0, 0.8])
            ),
            legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5),
            margin=dict(t=120, b=80, l=40, r=40)
        )
        st.plotly_chart(fig_overlay, use_container_width=True)
        
    if 'Strategic' in user_persona:
        advice_text = (
            "*Chúc mừng bạn! Bạn đã đạt chân dung **Chuyên gia tích hợp chiến lược (Strategic power user)**. "
            "Hồ sơ của bạn cho thấy sự cân bằng xuất sắc khi sử dụng AI không chỉ cho viết mã mà cả các tác vụ phức tạp như **thiết kế hệ thống và phân tích dữ liệu**. "
            "Khuyến nghị dành cho bạn là **tiếp tục nghiên cứu các mô hình AI mới** và đóng vai trò hạt nhân dẫn dắt, chia sẻ quy trình làm việc chuẩn cho đội ngũ xung quanh.*"
        )
    elif 'Traditional' in user_persona:
        advice_text = (
            "*Bạn được phân loại vào nhóm **Chuyên gia chuyên môn truyền thống (Traditional domain expert)**. "
            "Mặc dù bạn có thâm niên vững vàng, việc **chưa khai thác thế mạnh của AI** có thể khiến bạn mất nhiều thời gian cho các tác vụ thủ công. "
            "Hãy bắt đầu tích hợp LLM vào quy trình làm việc hằng ngày, đặc biệt là ở khâu **tạo ý tưởng hoặc xử lý dữ liệu thô** để tối ưu hóa năng suất vốn có của bạn.*"
        )
    elif 'Adaptive' in user_persona:
        advice_text = (
            "*Bạn thuộc nhóm **Nhân sự nhạy bén công nghệ (Adaptive tech adopter)**. "
            "Bạn đang thích ứng rất nhanh với công nghệ mới và sử dụng AI thường xuyên ở các tác vụ kỹ thuật. "
            "Tuy nhiên, để thăng tiến lên nhóm Chiến lược, bạn cần tích lũy thêm **kinh nghiệm chuyên môn sâu** và học cách sử dụng AI "
            "để **thiết kế kiến trúc hệ thống và phân tích chuyên sâu**, tránh phụ thuộc quá đà vào việc tạo mã nguồn ngắn hạn.*"
        )
    else:
        advice_text = (
            "*Bạn được xếp vào nhóm **Nhân sự lệ thuộc công nghệ (Replaceable tech dependent)**. "
            "Tần suất sử dụng AI của bạn cao nhưng chủ yếu tập trung vào việc tạo mã lặp lại, trong khi thâm niên và thu nhập còn khiêm tốn. "
            "Hồ sơ này cảnh báo **nguy cơ bị thay thế cao** khi công nghệ AI nâng cấp. Hãy chủ động học hỏi **tư duy kiến trúc hệ thống**, "
            "tham gia các tác vụ đòi hỏi sự bất định cao, và nâng cao kỹ năng tương tác phi kỹ thuật để củng cố vị thế cốt lõi của mình.*"
        )
    st_analysis(advice_text)
    
    st_header("Mô phỏng sức khỏe nhân sự tổ chức (Organizational AI Synergy Sandbox)")
    st.write(
        "Nhà quản lý có thể điều chỉnh tỷ lệ phần trăm phân bổ của 4 chân dung nhân sự trong phòng ban "
        "để đánh giá mức độ rủi ro thích ứng công nghệ của tổ chức, phát hiện nguy cơ và nhận đề xuất lộ trình chiến lược tương ứng."
    )
    st.markdown(
        r"""
        **Công thức tính Chỉ số rủi ro thích ứng công nghệ:**
        Điểm số rủi ro thô ($Score_{raw}$) của tổ chức được tính bằng trung bình trọng số mức độ rủi ro thích ứng của các nhóm nhân sự, sau đó chuẩn hóa về thang đo phần trăm ($Risk_{index}$):
        """
    )
    st.latex(r"Score_{raw} = \frac{p_{strategic} \cdot 1.0 + p_{traditional} \cdot 3.0 + p_{adaptive} \cdot 5.0 + p_{replaceable} \cdot 9.0}{100}")
    st.latex(r"Risk_{index} = \frac{Score_{raw} - 1.0}{8.0} \times 100\%")
    st.markdown(
        r"""
        *Trong đó:*
        * $p_{strategic}, p_{traditional}, p_{adaptive}, p_{replaceable}$ là tỷ lệ phần trăm tương ứng của 4 nhóm chân dung.
        * Các hệ số $1.0, 3.0, 5.0, 9.0$ lần lượt là trọng số rủi ro thích ứng của từng chân dung (thấp nhất đối với nhóm tích hợp chiến lược và cao nhất đối với nhóm lệ thuộc công nghệ).
        """
    )
    
    col_sim_input, col_sim_output = st.columns([1, 1])
    with col_sim_input:
        st.write("**Điều chỉnh cơ cấu nhân sự phòng ban (Tổng phải bằng 100%):**")
        p_strategic = st.slider("Chuyên gia tích hợp chiến lược (%)", min_value=0, max_value=100, value=25, step=5, key="sim_str")
        p_traditional = st.slider("Chuyên gia truyền thống (%)", min_value=0, max_value=100, value=25, step=5, key="sim_tra")
        p_adaptive = st.slider("Nhân sự nhạy bén công nghệ (%)", min_value=0, max_value=100, value=25, step=5, key="sim_ada")
        p_replaceable = st.slider("Nhân sự lệ thuộc công nghệ (%)", min_value=0, max_value=100, value=25, step=5, key="sim_rep")
        
        total_pct = p_strategic + p_traditional + p_adaptive + p_replaceable
        if total_pct == 100:
            st.markdown(f"**Tổng tỷ lệ cơ cấu**: `{total_pct}%` (Đạt chuẩn 100%)")
        else:
            st.markdown(f"**Tổng tỷ lệ cơ cấu**: `{total_pct}%` <span style='color: #c2410c; font-weight: bold;'>(Vui lòng điều chỉnh tổng về đúng 100%)</span>", unsafe_allow_html=True)
        
    with col_sim_output:
        if total_pct != 100:
            st.markdown(
                """
                <div style="
                    background-color: #f8fafc;
                    border: 1px solid #e2e8f0;
                    padding: 16px;
                    border-radius: 8px;
                    color: #64748b;
                    font-size: 14.5px;
                ">
                    Vui lòng điều chỉnh tổng tỷ lệ phần trăm của 4 nhóm nhân sự ở cột bên trái về đúng 100% để bắt đầu chạy mô phỏng.
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            raw_score = (p_strategic * 1.0 + p_traditional * 3.0 + p_adaptive * 5.0 + p_replaceable * 9.0) / 100.0
            vul_index = ((raw_score - 1.0) / 8.0) * 100.0
            
            if vul_index < 35:
                risk_level = "An toàn cao (Low Vulnerability)"
                color_type = "green"
            elif vul_index < 65:
                risk_level = "Trung bình (Moderate Vulnerability)"
                color_type = "amber"
            else:
                risk_level = "Nguy hiểm (High Vulnerability)"
                color_type = "amber"
                
            border_col = '#0d5c3a' if color_type == 'green' else '#f59e0b'
            text_col = '#0d5c3a' if color_type == 'green' else '#b45309'
            
            st.markdown(
                f"""
                <div style="
                    border: 2px solid {border_col};
                    border-radius: 12px;
                    padding: 16px 20px;
                    background-color: #ffffff;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                    margin-bottom: 16px;
                    width: 100%;
                ">
                    <p style='font-size: 13px; color: #64748b; margin-top: 0; margin-bottom: 6px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;'>Chỉ số rủi ro thích ứng công nghệ</p>
                    <h2 style='font-size: 32px; color: {text_col}; margin-top: 0; margin-bottom: 0; font-weight: 800;'>{vul_index:.1f}%</h2>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(f"**Trạng thái rủi ro:** `{risk_level}`")
            
            alerts = []
            if p_replaceable > 40:
                alerts.append(
                    "**Rủi ro Nợ kỹ thuật (Tech Debt Risk):** Nhóm lệ thuộc công nghệ quá đông (trên 40%). "
                    "Nhân sự có thể lạm dụng sinh mã tự động mà không hiểu sâu sắc mã nguồn, tạo lỗ hổng bảo mật và tích tụ nợ kỹ thuật cho sản phẩm."
                )
            if p_traditional > 40:
                alerts.append(
                    "**Rủi ro Tụt hậu Công nghệ (Tech Lag Risk):** Nhóm chuyên môn truyền thống chiếm hơn 40%. "
                    "Tổ chức đang lãng phí cơ hội gia tăng hiệu suất từ AI. Tốc độ thực thi và đổi mới sáng tạo có thể chậm hơn đối thủ."
                )
            if p_strategic < 15:
                alerts.append(
                    "**Thiếu hụt Hạt nhân Chiến lược (Strategic Void):** Số lượng chuyên gia tích hợp dưới 15%. "
                    "Thiếu người dẫn dắt quy chuẩn sử dụng công cụ AI ở cấp độ kiến trúc hệ thống, dẫn đến việc ứng dụng AI tự phát manh mún."
                )
            if p_adaptive > 50:
                alerts.append(
                    "**Rủi ro Quá tải Thử nghiệm (Chaotic Innovation):** Nhóm nhạy bén công nghệ chiếm hơn 50%. "
                    "Dễ dẫn đến tình trạng áp dụng công cụ tràn lan, thiếu kiểm soát quy trình và làm suy yếu độ ổn định của sản phẩm lõi."
                )
                
            if alerts:
                st.markdown("### Các cảnh báo rủi ro:")
                for alert in alerts:
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #fffbeb;
                            border-left: 4px solid #f59e0b;
                            padding: 12px 16px;
                            border-radius: 4px;
                            margin-bottom: 12px;
                            color: #78350f;
                            font-size: 14px;
                            line-height: 1.5;
                        ">
                            {alert}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    """
                    <div style="
                        background-color: #f0fdf4;
                        border-left: 4px solid #0d5c3a;
                        padding: 12px 16px;
                        border-radius: 4px;
                        margin-bottom: 12px;
                        color: #14532d;
                        font-size: 14px;
                        line-height: 1.5;
                        font-weight: 500;
                    ">
                        Hệ thống vận hành cân bằng: Cơ cấu nhân sự ổn định, các chỉ số rủi ro nằm trong giới hạn kiểm soát an toàn.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            st.markdown("### Lộ trình chiến lược khuyến nghị:")
            recommendations = []
            if p_replaceable > 40:
                recommendations.append("Thiết lập quy trình kiểm duyệt mã nguồn nghiêm ngặt, bắt buộc qua sự phê duyệt của các chuyên gia tích hợp chiến lược.")
                recommendations.append("Tổ chức đào tạo có hệ thống về kiến thức nền tảng (như cấu trúc dữ liệu, giải thuật, thiết kế hệ thống) thay vì chỉ sử dụng AI viết code thô.")
            if p_traditional > 40:
                recommendations.append("Tạo cơ chế khuyến khích, khen thưởng cho các chuyên gia truyền thống khi họ tích hợp thành công công cụ AI vào quy trình làm việc.")
                recommendations.append("Tổ chức các buổi chia sẻ tri thức nội bộ để nhóm Chuyên gia tích hợp chiến lược chuyển giao kinh nghiệm thực chiến cho nhóm truyền thống.")
            if p_strategic < 15:
                recommendations.append("Đẩy mạnh chính sách thu hút hoặc bồi dưỡng nội bộ để gia tăng tỷ lệ Chuyên gia tích hợp chiến lược thông qua các bài toán R&D đầy thử thách.")
                recommendations.append("Xây dựng bộ quy tắc ứng dụng AI (AI Playbook) chuẩn của công ty để dẫn dắt hành vi ứng dụng công cụ.")
            
            if not recommendations:
                recommendations.append("Tiếp tục duy trì cơ cấu nhân sự hiện tại và tổ chức định kỳ các chương trình chia sẻ tri thức liên tục giữa các nhóm.")
                
            for rec in recommendations:
                st.markdown(f"* {rec}")
                
            st_analysis(
                f"*Kết quả mô phỏng cấu trúc đội ngũ chỉ ra mức độ rủi ro thích ứng công nghệ của tổ chức đạt **{vul_index:.1f}%**. "
                f"Sự phân bổ này đòi hỏi ban quản lý phải có chiến lược đào tạo và luân chuyển tri thức phù hợp. "
                f"Nhóm **Chuyên gia tích hợp chiến lược** cần đóng vai trò là hạt nhân chuyển giao công nghệ cho nhóm **Chuyên gia truyền thống**, "
                f"đồng thời thiết lập bộ khung kiểm soát chất lượng chặt chẽ để giảm thiểu rủi ro nợ kỹ thuật từ nhóm **Nhân sự lệ thuộc công nghệ**.*"
            )

