import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.ui_components import (
    st_header, st_subheader, st_analysis, apply_chart_style, 
    THEME_PALETTE
)
from src.data_loader import LLM_COLS

def render_tab_risk(data):
    """
    Render Tab 2: Động lực chuyển giao và Tấm khiên phòng ngự con người
    """
    df_model = data['df_model']
    df_meta_it = data['df_meta_it']
    df_worker_it = data['df_worker_it']
    
    st_header("Động lực chuyển giao và Tấm khiên phòng ngự con người")
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
        
    st_subheader("Bẫy năng lực từ AI Agent: Mối đe dọa đến tấm khiên chuyên môn")
    col_radar_text, col_radar_chart = st.columns([1, 1.2])
    with col_radar_text:
        st_analysis(
            "*Đây là mối đe dọa trực tiếp đối với tấm khiên phòng ngự. Mặc dù ngành công nghiệp có nền tảng Senior vững chắc, "
            "nhưng biểu đồ mạng nhện phát hiện một nghịch lý: nhóm Junior (dưới 3 năm kinh nghiệm) lại có tỷ lệ sử dụng AI "
            "cho các tác vụ vĩ mô như thiết kế hệ thống và tạo ý tưởng cao hơn hẳn so với Senior. Junior đang dùng AI "
            "như một lối tắt để nhảy cóc kinh nghiệm. Nhưng đây chính là 'Bẫy năng lực AI' — khi công cụ đi trước tư duy thực tế, "
            "nó dễ tạo ra ảo tưởng về năng lực trong khi tích lũy các lỗ hổng hệ thống và nợ kỹ thuật. Điều này cảnh báo chúng ta "
            "rằng không được bỏ qua quá trình tích lũy chuyên môn sâu nếu muốn giữ vững tấm khiên phòng ngự cốt lõi.*"
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
