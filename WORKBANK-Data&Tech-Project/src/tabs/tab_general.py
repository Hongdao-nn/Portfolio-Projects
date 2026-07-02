import streamlit as st
import pandas as pd
import plotly.express as px
from src.ui_components import (
    st_header, st_subheader, st_kpi_card, st_analysis, 
    apply_chart_style, THEME_PALETTE, CLUSTER_COLORS
)
from src.data_loader import LLM_COLS

def render_tab_general(data):
    """
    Render Tab 1: Hiện trạng nhân sự và Bản đồ rủi ro công nghiệp
    """
    df_model = data['df_model']
    df_meta_it = data['df_meta_it']
    
    st_header("Hiện trạng nhân sự và Bản đồ rủi ro công nghiệp")
    st.write(
        "Nhằm phân tích ảnh hưởng của trí tuệ nhân tạo đối với thị trường lao động, báo cáo khảo sát lực lượng lao động công nghệ "
        "và ánh xạ các tác vụ công việc vào các phân vùng rủi ro khác nhau. Bộ dữ liệu tập trung vào các nhóm nghề nghiệp liên quan đến "
        "phát triển phần mềm, phân tích hệ thống, xử lý dữ liệu và an ninh mạng, được trích xuất từ dữ liệu khảo sát gốc bằng bộ lọc "
        "tên ngành nghề chứa các từ khóa trọng tâm: **computer, software, data, information, network, web, programmer, developer, "
        "analyst, systems, ai, artificial intelligence, machine learning, algorithm**."
    )
    
    ai_usage_pct = (df_meta_it[LLM_COLS].apply(lambda r: any(r != 'Never'), axis=1).mean() * 100)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st_kpi_card("Tổng số nhân sự khảo sát", f"{len(df_meta_it)}", "green")
    with col2:
        st_kpi_card("Số ngành khảo sát", f"{df_model['Ngành nghề'].nunique()}", "amber")
    with col3:
        st_kpi_card("Số lượng tác vụ phân tích", f"{len(df_model)}", "green")
    with col4:
        st_kpi_card("Tỷ lệ nhân sự dùng AI", f"{ai_usage_pct:.1f}%", "amber")
        
    st.write("")
    
    st_subheader("Phân bố thâm niên lực lượng lao động")
    col_donut_text, col_donut_chart = st.columns([1, 1.2])
    with col_donut_text:
        st_analysis(
            "*Để bắt đầu câu chuyện, chúng ta hãy nhìn vào chân dung lực lượng lao động - những người trực tiếp đối đầu với làn sóng AI. "
            "Biểu đồ tròn chỉ ra rằng đây là một ngành công nghiệp được dẫn dắt bởi những bộ não giàu kinh nghiệm, với hơn **77.9%** nhân sự "
            "có thâm niên từ **3 năm trở lên** (trong đó nhóm từ **3–5 năm** và **trên 10 năm** chiếm tỷ lệ cao nhất lần lượt là **28.5%** và **26.7%**). "
            "Sự áp đảo của nhóm Senior khẳng định rằng bất kỳ sự thay đổi công nghệ nào ở đây cũng sẽ tác động trực tiếp đến những cột trụ cốt lõi của hệ thống IT. "
            "Tuy nhiên, sự vững vàng về mặt kinh nghiệm này đang chuẩn bị đối mặt với một biến số mới đến từ thói quen công nghệ của thế hệ tiếp nối.*"
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
        df_donut = df_meta_it['Experience'].value_counts().reset_index()
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
        apply_chart_style(fig_donut, "Tỷ lệ phân bổ thâm niên kinh nghiệm làm việc")
        st.plotly_chart(fig_donut, use_container_width=True)
    
        
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
        st_analysis(
            "*Chương này đi sâu vào cấp độ tác vụ công việc để đối chiếu mong muốn của lập trình viên và năng lực thực tế của AI. "
            "Ma trận phân cụm chỉ ra rằng hầu hết các tác vụ trong ngành công nghệ thông tin đều đã bị kéo mạnh về phía bên phải, "
            "tập trung dày đặc trong vùng báo động (Alert zone) và vùng tiềm ẩn nguy cơ (At-risk zone) với điểm tự động hóa từ 3.0 đến 5.0. "
            "Vùng an toàn (Safe zone) ở phía bên trái ngày càng trở nên thưa thớt. Điều này báo hiệu rằng áp lực tự động hóa "
            "đang ở sát sườn và việc AI thay thế các công việc lập trình kỹ thuật không còn là dự báo xa vời, mà là thực tế đang diễn ra trực diện.*"
        )
    with col_scatter_chart:
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
