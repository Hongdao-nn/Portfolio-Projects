import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.ui_components import (
    st_header, st_subheader, st_kpi_card, st_analysis, 
    apply_chart_style, THEME_PALETTE
)
from src.data_loader import classify_worker_persona, LLM_COLS

def render_tab_sandbox(data):
    """
    Render Tab 5: Phân khúc và định hình chân dung (Human segmentation)
    """
    df_user_it = data['df_user_it']
    
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
        for col in LLM_COLS:
            df_radar_calc[col] = df_radar_calc[col].map(freq_mapping).fillna(1)
        
        benchmark_data = df_radar_calc[df_radar_calc['Chân dung nhân sự'] == 'Chuyên gia tích hợp chiến lược (Strategic power user)'][LLM_COLS].mean()
        benchmark_scores = [benchmark_data[col] for col in LLM_COLS]
        
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
