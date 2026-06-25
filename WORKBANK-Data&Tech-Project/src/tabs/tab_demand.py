import streamlit as st
import pandas as pd
import plotly.express as px
from src.ui_components import (
    st_header, st_subheader, st_analysis, apply_chart_style, 
    CLUSTER_COLORS, THEME_PALETTE
)

def render_tab_demand(data):
    """
    Render Tab 2: Kỳ vọng và thực tế (Expectation vs. reality)
    """
    df_model = data['df_model']
    
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
