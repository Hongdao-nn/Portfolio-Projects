with tab3:
    st_header("Mô phỏng đà phát triển AI và dự báo rủi ro tác vụ")
    st.write(
        "Năng lực tự động hóa của công nghệ không đứng yên mà phát triển theo thời gian. Ở phần này, chúng ta mô phỏng "
        "đà phát triển của AI tại Mỹ và Việt Nam từ năm 2025 đến 2030, tích hợp với các tấm khiên phòng ngự con người và mô hình phân cụm K-Means để dự báo rủi ro thực tế."
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
        ### 2. Mô hình dự báo quỹ đạo phát triển AI và Chỉ số Rủi ro Tích hợp (Risk Score)
        Năng lực tự động hóa tích lũy của AI đối với từng tác vụ tại năm $t$ ($t \in [2025, 2030]$) được mô phỏng theo tỷ lệ tăng trưởng kép hàng năm (CAGR). Điểm rủi ro thực tế được điều phối bởi các rào cản phòng vệ:
        *   **Quỹ đạo AI tại Mỹ (CAGR cố định ở mức 24.1%):**
        """
    )
    st.latex(r"AI_{US}(t) = \min\left(AI_{base} \times (1 + g_{US})^{t - 2025},\ 5.0\right)")
    st.markdown(
        r"""
        *   **Quỹ đạo AI tại Việt Nam (Việt Nam có độ trễ và CAGR cố định ở mức 20.0%):**
        """
    )
    st.latex(r"AI_{VN}(t) = \min\left(AI_{base} \times K_{readiness} \times (1 + g_{VN})^{t - 2025},\ 5.0\right)")
    st.markdown(
        r"""
        *   **Chỉ số Rủi ro Tích hợp (Risk Score) sau khi qua Tấm khiên phòng ngự:**
        """
    )
    st.latex(r"Risk\_Score(t) = \frac{AI(t) \times (6 - Uncertainty) \times (6 - Communication)}{25}")
    st.markdown(
        r"""
        *Trong đó:*
        *   $AI_{base}$: Điểm năng lực tự động hóa ban đầu do chuyên gia đánh giá (thang điểm 5.0).
        *   $g_{US} = 24.1\%$: Tốc độ tăng trưởng kép hàng năm của thị trường AI tại Mỹ.
        *   $g_{VN} = 20.0\%$: Tốc độ tăng trưởng kép hàng năm của thị trường AI tại Việt Nam.
        *   $Uncertainty$: Mức độ bất định của tác vụ (1 - 5).
        *   $Communication$: Yêu cầu tương tác giao tiếp con người (1 - 5).
        
        ### 3. Phân vùng rủi ro động dựa trên K-Means
        Thay vì sử dụng ngưỡng cứng phiến diện, đặc trưng của từng tác vụ tại năm mô phỏng được cập nhật (điểm AI mô phỏng mới kết hợp với các rào cản bất định, giao tiếp và lương) và dự báo phân vùng bằng **mô hình K-Means** đã huấn luyện ở Trang 1:
        *   **Lệ thuộc AI (AI-Automated):** Tác vụ rơi vào cụm **Vùng báo động (Alert zone)**.
        *   **Cộng tác AI (AI-Collaborative):** Tác vụ rơi vào cụm **Vùng tiềm ẩn nguy cơ (At-risk zone)** hoặc **Vùng ổn định (Stable zone)**.
        *   **Lõi con người (Human Core):** Tác vụ rơi vào cụm **Vùng an toàn (Safe zone)**.
        """
    )
    st.markdown("---")
    
    st_subheader("Phòng thí nghiệm giả lập và phân tích lộ trình")
    
    # Widget điều khiển
    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        occ_options = ["Tất cả các ngành"] + sorted(df_model['Ngành nghề'].unique().tolist())
        selected_occ = st.selectbox("Chọn ngành nghề phân tích:", occ_options, key="forecasting_job_dropdown")
    with col_ctrl2:
        selected_year = st.slider(
            "Chọn năm mô phỏng:",
            min_value=2025,
            max_value=2030,
            value=2025,
            step=1,
            key="forecasting_year_slider"
        )
        
    # Lọc dữ liệu
    if selected_occ == "Tất cả các ngành":
        df_filtered = df_model.copy()
    else:
        df_filtered = df_model[df_model['Ngành nghề'] == selected_occ].copy()
        
    # Tính toán lộ trình rủi ro
    g_us = 0.241
    g_vn = 0.20
    K_READINESS = 59.98 / 88.36
    
    years_range = list(range(2025, 2031))
    us_trend = []
    vn_trend = []
    
    for yr in years_range:
        n = yr - 2025
        
        # Mỹ: tính AI và Risk Score
        us_cap_yr = (df_filtered['Khả năng tự động hóa (chuyên gia)'] * ((1 + g_us) ** n)).clip(upper=5.0)
        us_risk_yr = (us_cap_yr * (6 - df_filtered['Involved Uncertainty'].fillna(df_filtered['Involved Uncertainty'].median())) * 
                      (6 - df_filtered['Interpersonal Communication Requirement'].fillna(df_filtered['Interpersonal Communication Requirement'].median())) / 25)
        us_trend.append(us_risk_yr.mean())
        
        # Việt Nam: tính AI và Risk Score
        vn_cap_yr = (df_filtered['Khả năng tự động hóa (chuyên gia)'] * K_READINESS * ((1 + g_vn) ** n)).clip(upper=5.0)
        vn_risk_yr = (vn_cap_yr * (6 - df_filtered['Involved Uncertainty'].fillna(df_filtered['Involved Uncertainty'].median())) * 
                      (6 - df_filtered['Interpersonal Communication Requirement'].fillna(df_filtered['Interpersonal Communication Requirement'].median())) / 25)
        vn_trend.append(vn_risk_yr.mean())
        
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
        name='Risk Score tại Mỹ (CAGR 24.1%)',
        line=dict(color=THEME_PALETTE[5], width=3, shape='spline')
    ))
    fig_trend.add_trace(go.Scatter(
        x=df_chart_data['Năm'],
        y=df_chart_data['Việt Nam'],
        name='Risk Score tại Việt Nam (CAGR 20.0%)',
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
    
    apply_chart_style(fig_trend, f"So sánh lộ trình điểm rủi ro tích hợp (Risk Score): Mỹ vs Việt Nam ({selected_occ})")
    fig_trend.update_yaxes(range=[0.0, 5.2], title="Điểm rủi ro tích hợp trung bình (Risk Score)")
    fig_trend.update_xaxes(tickmode='linear', tick0=2025, dtick=1, title="Năm")
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Tính toán rủi ro tác vụ cho VN tại năm được chọn bằng K-Means
    n_sel = selected_year - 2025
    df_sim = df_filtered.copy()
    df_sim['AI_VN_sim'] = (df_sim['Khả năng tự động hóa (chuyên gia)'] * K_READINESS * ((1 + g_vn) ** n_sel)).clip(upper=5.0)
    
    # Chuẩn bị dữ liệu để dự báo cụm động bằng K-Means
    X_sim = df_sim[features_cluster].copy()
    X_sim['Khả năng tự động hóa (chuyên gia)'] = df_sim['AI_VN_sim']
    X_sim = X_sim.fillna(df_model[features_cluster].median())
    
    X_sim_scaled = scaler.transform(X_sim)
    df_sim['Cluster_sim'] = kmeans.predict(X_sim_scaled)
    df_sim['Vùng rủi ro mô phỏng'] = df_sim['Cluster_sim'].map(persona_labels)
    
    # Phân nhóm tác vụ dựa trên kết quả phân cụm K-Means
    automated_tasks = df_sim[df_sim['Vùng rủi ro mô phỏng'] == "Vùng báo động (Alert zone)"]
    collaborative_tasks = df_sim[df_sim['Vùng rủi ro mô phỏng'].isin(["Vùng tiềm ẩn nguy cơ (At-risk zone)", "Vùng ổn định (Stable zone)"])]
    human_core_tasks = df_sim[df_sim['Vùng rủi ro mô phỏng'] == "Vùng an toàn (Safe zone)"]
    
    total_tasks = len(df_sim)
    pct_auto = (len(automated_tasks) / total_tasks) * 100 if total_tasks > 0 else 0
    pct_collab = (len(collaborative_tasks) / total_tasks) * 100 if total_tasks > 0 else 0
    pct_human = (len(human_core_tasks) / total_tasks) * 100 if total_tasks > 0 else 0
    
    st_subheader(f"Phân tích cấu trúc rủi ro tác vụ năm {selected_year} (Việt Nam - Dự báo bằng K-Means)")
    st.write(
        f"Tại năm dự báo {selected_year}, trong ngành **{selected_occ}**, tổng số {total_tasks} tác vụ được mô phỏng "
        f"và phân loại dựa trên phân cụm K-Means:"
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
    
    with st.expander(f"Danh sách tác vụ Lệ thuộc AI ({len(automated_tasks)}) - [Vùng báo động K-Means]", expanded=False):
        if len(automated_tasks) > 0:
            for idx, row in automated_tasks.sort_values(by='AI_VN_sim', ascending=False).reset_index().iterrows():
                st.markdown(f"**{idx+1}. {row['Tác vụ']}**")
                r_score = row['AI_VN_sim'] * (6 - row['Involved Uncertainty']) * (6 - row['Interpersonal Communication Requirement']) / 25
                st.caption(f"Yêu cầu kỹ năng: {row['Skill (O*NET Work Activity)']} | Điểm mô phỏng VN: {row['AI_VN_sim']:.2f}/5.0 | Điểm rủi ro: {r_score:.2f}/5.0 | Cụm K-Means: {row['Vùng rủi ro mô phỏng']}")
        else:
            st.write("Không có tác vụ nào thuộc nhóm này.")
            
    with st.expander(f"Danh sách tác vụ Cộng tác AI ({len(collaborative_tasks)}) - [Vùng tiềm ẩn nguy cơ / Ổn định K-Means]", expanded=False):
        if len(collaborative_tasks) > 0:
            for idx, row in collaborative_tasks.sort_values(by='AI_VN_sim', ascending=False).reset_index().iterrows():
                st.markdown(f"**{idx+1}. {row['Tác vụ']}**")
                r_score = row['AI_VN_sim'] * (6 - row['Involved Uncertainty']) * (6 - row['Interpersonal Communication Requirement']) / 25
                st.caption(f"Yêu cầu kỹ năng: {row['Skill (O*NET Work Activity)']} | Điểm mô phỏng VN: {row['AI_VN_sim']:.2f}/5.0 | Điểm rủi ro: {r_score:.2f}/5.0 | Cụm K-Means: {row['Vùng rủi ro mô phỏng']}")
        else:
            st.write("Không có tác vụ nào thuộc nhóm này.")
            
    with st.expander(f"Danh sách tác vụ Lõi con người ({len(human_core_tasks)}) - [Vùng an toàn K-Means]", expanded=False):
        if len(human_core_tasks) > 0:
            for idx, row in human_core_tasks.sort_values(by='AI_VN_sim', ascending=True).reset_index().iterrows():
                st.markdown(f"**{idx+1}. {row['Tác vụ']}**")
                r_score = row['AI_VN_sim'] * (6 - row['Involved Uncertainty']) * (6 - row['Interpersonal Communication Requirement']) / 25
                st.caption(f"Yêu cầu kỹ năng: {row['Skill (O*NET Work Activity)']} | Điểm mô phỏng VN: {row['AI_VN_sim']:.2f}/5.0 | Điểm rủi ro: {r_score:.2f}/5.0 | Cụm K-Means: {row['Vùng rủi ro mô phỏng']}")
        else:
            st.write("Không có tác vụ nào thuộc nhóm này.")
            
    st_analysis(
        f"""
**PHÂN TÍCH KHOẢNG CÁCH VẬN TỐC & RỦI RO ĐỨT GÃY GIA CÔNG TOÀN CẦU (GLOBAL OUTSOURCING DISRUPTION):**

1. **Khoảng cách vận tốc (Velocity Gap):** Bản chất sự nguy hại của AI nằm ở **vận tốc thay đổi**. Trong khi AI tại Mỹ tăng trưởng kép ở mức **24.1%/năm** và Việt Nam là **20.0%/năm** (hàm số mũ), thì chu kỳ đào tạo lại và chuyển dịch nghề nghiệp của một con người đòi hỏi từ **1 đến 2 năm** (tuyến tính). Vận tốc AI vượt xa khả năng thích ứng của con người tạo nên một cú sốc thất nghiệp cơ cấu mạnh mẽ.
2. **Rủi ro đứt gãy gia công ngoại sinh:** Tại sao Mỹ phát triển AI nhanh lại gây nguy hiểm cho Việt Nam? Cơ cấu CNTT Việt Nam chủ yếu là gia công phần mềm (Outsourcing) cho các thị trường phát triển như Mỹ. Khi các đối tác Mỹ đạt tốc độ tự động hóa nhanh, họ sẽ áp dụng AI Agent để tự viết mã, kiểm thử (QA/QC), hỗ trợ kỹ thuật tại nước họ (**Digital Reshoring**). Khi đó, các đơn hàng outsourcing tại Việt Nam sẽ bị cắt giảm đột ngột trước khi thị trường Việt Nam kịp áp dụng AI nội địa.
3. **Độ tin cậy từ K-Means & Tấm khiên phòng thủ:** Việc áp dụng trực tiếp mô hình phân cụm K-Means cho năm {selected_year} chỉ ra rằng, khi năng lực AI dịch chuyển lên, có đến **{pct_auto:.1f}%** tác vụ chuyển sang **Vùng báo động (Alert zone)** và **{pct_collab:.1f}%** rơi vào **Vùng tiềm ẩn nguy cơ/ổn định**. Đây là các tác vụ có tính lặp lại cao, giao tiếp thấp (như viết mã cơ bản, test case tự động). Ngược lại, **{pct_human:.1f}%** tác vụ **Lõi con người (Safe zone)** vẫn đứng vững nhờ hai tấm khiên phòng ngự: khả năng ứng biến linh hoạt trước sự bất định và giao tiếp liên cá nhân phức tạp.
"""
    )