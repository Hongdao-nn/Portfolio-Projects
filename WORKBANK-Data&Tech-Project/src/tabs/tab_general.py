import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.ui_components import (
    st_header, st_subheader, st_kpi_card, st_analysis, 
    apply_chart_style, THEME_PALETTE
)
from src.data_loader import LLM_COLS

def render_tab_general(data):
    """
    Render Tab 1: Bức tranh toàn cảnh (Industry overview)
    """
    df_model = data['df_model']
    df_meta_it = data['df_meta_it']
    
    st_header("Bức tranh toàn cảnh về bộ dữ liệu và thực trạng công nghiệp")
    st.write(
        "Nhằm đảm bảo tính đại diện và khách quan khi định hình chân dung phân khúc dữ liệu và công nghệ, "
        "phần trình bày đã áp dụng kỹ thuật lọc dữ liệu dựa trên văn bản từ tổng thể dữ liệu Work Bank. "
        "Quy trình trích xuất mẫu sử dụng bộ lọc danh mục nghề nghiệp chứa các từ khóa trọng tâm: "
        "**computer, software, data, information, network, web, programmer, developer, analyst, systems, ai, "
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
    for col in LLM_COLS:
        df_meta_it_temp[col] = df_meta_it_temp[col].fillna('Never').astype(str).str.strip()
        
    df_meta_it_temp['LLM Usage Overall'] = df_meta_it_temp[LLM_COLS].apply(
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
    
    st_subheader("Nghịch lý Dunning-Kruger trong việc ứng dụng công nghệ")
    col_radar_text, col_radar_chart = st.columns([1, 1.2])
    with col_radar_text:
        st_analysis(
            "Biểu đồ mạng nhện chỉ ra hiện tượng <strong>Dunning-Kruger kỹ thuật số</strong>: Nhóm nhân sự trẻ (<strong>Junior dưới 3 năm</strong>) có tỷ lệ sử dụng "
            "công nghệ tự động hóa cho các công việc vĩ mô như <strong>thiết kế hệ thống và tạo ý tưởng cao hơn hẳn</strong> so với "
            "đội ngũ <strong>Senior (trên 6 năm)</strong>. Sự phụ thuộc sớm vào công cụ khi chưa tích lũy đủ kinh nghiệm thực tế có thể dẫn đến "
            "<strong>rủi ro tích tụ nợ kỹ thuật</strong> và làm suy yếu khả năng tự thẩm định hệ thống của nhân sự tập sự."
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
