import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.ui_components import (
    st_header, st_subheader, st_analysis, apply_chart_style, 
    THEME_PALETTE
)

def render_tab_risk(data):
    """
    Render Tab 3: Động lực và rào cản (Drivers & barriers)
    """
    df_model = data['df_model']
    df_worker_it = data['df_worker_it']
    
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
        
        top_5 = df_model.nlargest(5, 'Khả năng tự động hóa (chuyên gia)').copy()
        worst_5 = df_model.nsmallest(5, 'Khả năng tự động hóa (chuyên gia)').copy()
        df_extreme = pd.concat([top_5, worst_5])
        
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
