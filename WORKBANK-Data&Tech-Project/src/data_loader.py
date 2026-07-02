import pandas as pd
import numpy as np
import os
import re
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Tech keywords used to filter occupations
TECH_KEYWORDS = [
    'computer', 'software', 'data', 'information', 'network', 'web', 'programmer',
    'developer', 'analyst', 'systems', 'ai', 'artificial intelligence',
    'machine learning', 'algorithm'
]

def is_tech_job(job):
    job_lower = str(job).lower()
    for kw in TECH_KEYWORDS:
        if kw == 'ai':
            if re.search(r'\bai\b', job_lower):
                return True
        else:
            if kw in job_lower:
                return True
    return False

# LLM Usage columns
LLM_COLS = [
    'LLM Usage by Type - Coding', 
    'LLM Usage by Type - System Design', 
    'LLM Usage by Type - Data Processing', 
    'LLM Usage by Type - Analysis', 
    'LLM Usage by Type - Idea Generation'
]

def classify_worker_persona(row):
    """
    Classify worker persona based on income, experience, and LLM usage.
    """
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


def load_and_preprocess_data(data_dir="data"):
    """
    Load raw CSV data, filter for tech occupations, execute K-Means clustering,
    label vulnerability zones, and classify worker personas.
    """
    # Load raw data
    df_worker = pd.read_csv(os.path.join(data_dir, "domain_worker_desires.csv"))
    df_worker_meta = pd.read_csv(os.path.join(data_dir, "domain_worker_metadata.csv"))
    df_expert = pd.read_csv(os.path.join(data_dir, "expert_rated_technological_capability.csv"))
    df_task = pd.read_csv(os.path.join(data_dir, "task_statement_with_metadata.csv"))
    
    # Filter tech occupations
    all_jobs = df_worker_meta['Occupation (O*NET-SOC Title)'].dropna().unique()
    tech_jobs = [job for job in all_jobs if is_tech_job(job)]
    
    df_meta_it = df_worker_meta[df_worker_meta['Occupation (O*NET-SOC Title)'].isin(tech_jobs)].copy()
    df_tasks_it = df_task[df_task['Occupation (O*NET-SOC Title)'].isin(tech_jobs)].copy()
    df_worker_it = df_worker[df_worker['Occupation (O*NET-SOC Title)'].isin(tech_jobs)].copy()
    df_expert_it = df_expert[df_expert['Occupation (O*NET-SOC Title)'].isin(tech_jobs)].copy()
    
    # Build df_model
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
    
    # Calculate Risk Score
    df_model['Risk_Score'] = (
        df_model['Khả năng tự động hóa (chuyên gia)'] * (6 - df_model['Involved Uncertainty']) *
        (6 - df_model['Interpersonal Communication Requirement']) / 25
    )
    
    # K-Means clustering
    features_cluster = [
        'Khả năng tự động hóa (chuyên gia)', 'Mong muốn tự động hóa (người lao động)',
        'Domain Expertise Requirement', 'Involved Uncertainty',
        'Interpersonal Communication Requirement', 'Occupation Mean Annual Wage'
    ]
    X = df_model[features_cluster].fillna(df_model[features_cluster].median())
    X_scaled = StandardScaler().fit_transform(X)
    
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df_model['Cluster'] = kmeans.fit_predict(X_scaled)
    
    # Rank clusters based on Risk Score
    cluster_risk_rank = df_model.groupby('Cluster')['Risk_Score'].mean().sort_values().index.tolist()
    ordered_persona_names = [
        "Vùng an toàn (Safe zone)",
        "Vùng ổn định (Stable zone)",
        "Vùng tiềm ẩn nguy cơ (At-risk zone)",
        "Vùng báo động (Alert zone)"
    ]
    persona_labels = {cluster_id: ordered_persona_names[rank] for rank, cluster_id in enumerate(cluster_risk_rank)}
    df_model['Vùng rủi ro'] = df_model['Cluster'].map(persona_labels)
    
    # Worker aggregate survey details
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
    
    for col in LLM_COLS:
        df_user_it[col] = df_user_it[col].fillna('Never')
        
    df_user_it['Chân dung nhân sự'] = df_user_it.apply(classify_worker_persona, axis=1)
    
    return {
        'df_model': df_model,
        'df_user_it': df_user_it,
        'df_meta_it': df_meta_it,
        'df_worker_it': df_worker_it,
        'tech_jobs': tech_jobs
    }
