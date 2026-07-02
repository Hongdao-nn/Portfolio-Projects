import streamlit as st
import pandas as pd
from src.ui_components import (
    st_header, st_subheader, st_analysis, THEME_PALETTE
)

def render_tab_recommendation(data):
    """
    Render Tab 4: Hệ thống khuyến nghị dịch chuyển nghề nghiệp và nâng cao kỹ năng
    """
    df_model = data['df_model']
    
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
    
    # Đồng bộ hóa từ Trang 3
    session_occ = st.session_state.get("forecasting_job_dropdown", "Tất cả các ngành")
    selected_year = st.session_state.get("forecasting_year_slider", 2025)
    
    if session_occ == "Tất cả các ngành":
        selected_occ = sorted(df_model['Ngành nghề'].unique().tolist())[0]
    else:
        selected_occ = session_occ
        
    st.success(f"Ngành nghề đang phân tích (đồng bộ từ Trang 3): **{selected_occ}** (Năm mô phỏng: **{selected_year}**)")
        
    # Tính toán các thông số của ngành nguồn
    df_src_tasks = df_model[df_model['Ngành nghề'] == selected_occ]
    skills_src = set(df_src_tasks['Skill (O*NET Work Activity)'].dropna().unique())
    src_wage = df_src_tasks['Occupation Mean Annual Wage'].mean()
    
    K_READINESS = 59.98 / 88.36
    g_vn = 0.20
    n_sel = selected_year - 2025
    src_caps = (df_src_tasks['Khả năng tự động hóa (chuyên gia)'] * K_READINESS * ((1 + g_vn) ** n_sel)).clip(upper=5.0)
    src_avg_risk = src_caps.mean()
    
    # Tìm kiếm các ứng viên dịch chuyển phù hợp
    candidates = []
    for occ in sorted(df_model['Ngành nghề'].unique()):
        if occ == selected_occ:
            continue
            
        df_occ_tasks = df_model[df_model['Ngành nghề'] == occ]
        occ_wage = df_occ_tasks['Occupation Mean Annual Wage'].mean()
        occ_caps = (df_occ_tasks['Khả năng tự động hóa (chuyên gia)'] * K_READINESS * ((1 + g_vn) ** n_sel)).clip(upper=5.0)
        occ_avg_risk = occ_caps.mean()
        
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
                'Kỹ năng': skills_tgt
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
            occ_caps = (df_occ_tasks['Khả năng tự động hóa (chuyên gia)'] * K_READINESS * ((1 + g_vn) ** n_sel)).clip(upper=5.0)
            occ_avg_risk = occ_caps.mean()
            skills_tgt = set(df_occ_tasks['Skill (O*NET Work Activity)'].dropna().unique())
            union_skills = skills_src.union(skills_tgt)
            jaccard = len(skills_src.intersection(skills_tgt)) / len(union_skills) if len(union_skills) > 0 else 0
            
            if occ_avg_risk < src_avg_risk and occ_wage >= 0.85 * src_wage and jaccard >= 0.10:
                candidates.append({
                    'Ngành nghề': occ,
                    'Rủi ro': occ_avg_risk,
                    'Lương': occ_wage,
                    'Jaccard': jaccard,
                    'Kỹ năng': skills_tgt
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
            occ_caps = (df_occ_tasks['Khả năng tự động hóa (chuyên gia)'] * K_READINESS * ((1 + g_vn) ** n_sel)).clip(upper=5.0)
            occ_avg_risk = occ_caps.mean()
            skills_tgt = set(df_occ_tasks['Skill (O*NET Work Activity)'].dropna().unique())
            union_skills = skills_src.union(skills_tgt)
            jaccard = len(skills_src.intersection(skills_tgt)) / len(union_skills) if len(union_skills) > 0 else 0
            
            if occ_avg_risk < src_avg_risk and occ_wage >= 0.70 * src_wage and jaccard >= 0.10:
                candidates.append({
                    'Ngành nghề': occ,
                    'Rủi ro': occ_avg_risk,
                    'Lương': occ_wage,
                    'Jaccard': jaccard,
                    'Kỹ năng': skills_tgt
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
            occ_caps = (df_occ_tasks['Khả năng tự động hóa (chuyên gia)'] * K_READINESS * ((1 + g_vn) ** n_sel)).clip(upper=5.0)
            occ_avg_risk = occ_caps.mean()
            skills_tgt = set(df_occ_tasks['Skill (O*NET Work Activity)'].dropna().unique())
            union_skills = skills_src.union(skills_tgt)
            jaccard = len(skills_src.intersection(skills_tgt)) / len(union_skills) if len(union_skills) > 0 else 0
            
            if occ_avg_risk < src_avg_risk and jaccard >= 0.10:
                candidates.append({
                    'Ngành nghề': occ,
                    'Rủi ro': occ_avg_risk,
                    'Lương': occ_wage,
                    'Jaccard': jaccard,
                    'Kỹ năng': skills_tgt
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
            occ_caps = (df_occ_tasks['Khả năng tự động hóa (chuyên gia)'] * K_READINESS * ((1 + g_vn) ** n_sel)).clip(upper=5.0)
            occ_avg_risk = occ_caps.mean()
            skills_tgt = set(df_occ_tasks['Skill (O*NET Work Activity)'].dropna().unique())
            union_skills = skills_src.union(skills_tgt)
            jaccard = len(skills_src.intersection(skills_tgt)) / len(union_skills) if len(union_skills) > 0 else 0
            
            if occ_avg_risk < src_avg_risk:
                candidates.append({
                    'Ngành nghề': occ,
                    'Rủi ro': occ_avg_risk,
                    'Lương': occ_wage,
                    'Jaccard': jaccard,
                    'Kỹ năng': skills_tgt
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
            occ_caps = (df_occ_tasks['Khả năng tự động hóa (chuyên gia)'] * K_READINESS * ((1 + g_vn) ** n_sel)).clip(upper=5.0)
            occ_avg_risk = occ_caps.mean()
            skills_tgt = set(df_occ_tasks['Skill (O*NET Work Activity)'].dropna().unique())
            union_skills = skills_src.union(skills_tgt)
            jaccard = len(skills_src.intersection(skills_tgt)) / len(union_skills) if len(union_skills) > 0 else 0
            
            candidates.append({
                'Ngành nghề': occ,
                'Rủi ro': occ_avg_risk,
                'Lương': occ_wage,
                'Jaccard': jaccard,
                'Kỹ năng': skills_tgt
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
                # 1. Vẽ card thông tin đẹp mắt sử dụng custom CSS class rec-card
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
                            <span class="rec-metric-label">Rủi ro AI (VN - {selected_year}):</span>
                            <span class="rec-metric-val" style="color: {'#ef4444' if cand['Rủi ro'] >= 4.0 else '#f59e0b' if cand['Rủi ro'] >= 2.5 else '#10b981'};">{cand['Rủi ro']:.2f}/5.0</span>
                        </div>
                        <div class="rec-metric" style="border-bottom: none; margin-bottom: 0;">
                            <span class="rec-metric-label">Mức lương trung bình:</span>
                            <span class="rec-metric-val" style="color: #0d5c3a;">${cand['Lương']:,.0f}/năm</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # 2. Phân loại tác vụ (nằm dưới card)
                df_tgt_tasks = df_model[df_model['Ngành nghề'] == cand['Ngành nghề']].copy()
                df_similar = df_tgt_tasks[df_tgt_tasks['Skill (O*NET Work Activity)'].isin(skills_src)]
                df_new = df_tgt_tasks[~df_tgt_tasks['Skill (O*NET Work Activity)'].isin(skills_src)]
                
                with st.expander(f"💼 Tác vụ tương đồng (Kỹ năng sẵn có) - {len(df_similar)}", expanded=False):
                    if len(df_similar) > 0:
                        for t_idx, t_row in df_similar.reset_index().iterrows():
                            st.markdown(f"- **{t_row['Tác vụ']}**")
                            st.caption(f"Kỹ năng sở hữu: {t_row['Skill (O*NET Work Activity)']}")
                    else:
                        st.write("Không có tác vụ tương đồng.")
                        
                with st.expander(f"📚 Tác vụ mới cần học (Kỹ năng bổ sung) - {len(df_new)}", expanded=False):
                    if len(df_new) > 0:
                        for t_idx, t_row in df_new.reset_index().iterrows():
                            st.markdown(f"- **{t_row['Tác vụ']}**")
                            st.caption(f"Kỹ năng cần bổ sung: {t_row['Skill (O*NET Work Activity)']}")
                    else:
                        st.write("Không có tác vụ mới cần học.")
        
        # Phân tích kết quả
        recs_names = [c['Ngành nghề'] for c in top_3]
        recs_str = ", ".join([f"**{r}**" for r in recs_names])
        analysis_text = f"""
*   **Chiến lược dịch chuyển chủ động:** Đối với ngành nghề nguồn là **{selected_occ}**, việc dịch chuyển sang các vị trí như {recs_str} sẽ giúp giảm thiểu đáng kể mức độ rủi ro bị thay thế bởi AI tại Việt Nam vào năm {selected_year}, đồng thời vẫn đảm bảo bảo vệ tối ưu mức thu nhập của bạn (không thấp hơn 85% lương gốc).
*   **Chương trình nâng cao kỹ năng trọng tâm:** Để chuyển đổi sự nghiệp thành công, bạn nên ưu tiên học bổ sung các kỹ năng tương ứng với các tác vụ được liệt kê trong mục **"Tác vụ mới cần học (Kỹ năng bổ sung)"** của từng ngành nghề đề xuất. Sự đầu tư học tập này giúp thu hẹp khoảng cách kỹ năng một cách nhanh chóng và hiệu quả.
"""
        st_analysis(analysis_text)
    else:
        st.write("Không tìm thấy đề xuất dịch chuyển phù hợp.")
