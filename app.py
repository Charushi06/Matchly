import streamlit as st
import pandas as pd
import os

import tempfile

from src.orchestrator import ScreeningOrchestrator

st.set_page_config(page_title="Resume Screening", layout="wide")

st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title(" Matchly: Resume Screening System")
st.markdown("### AI-Powered Resume Ranking & Analysis")

with st.sidebar:
    st.image("https://img.icons8.com/clouds/100/000000/resume.png", width=100)
    st.header("Mission Control")
    model_choice = st.selectbox("Scoring Strategy", ["TF-IDF (Cosine Similarity)", "Semantic Search (Coming Soon)"])
    st.info("Upload resumes and paste the job description to start the ranking process.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Job Description")
    jd_text = st.text_area("Paste JD here...", height=300, placeholder="Required skills: Python, Machine Learning...")

with col2:
    st.subheader("Candidate Resumes")
    uploaded_files = st.file_uploader("Upload PDF/DOCX/TXT", type=['pdf', 'docx', 'txt'], accept_multiple_files=True)

if st.button(" Launch Screening Mission"):
    if not jd_text:
        st.error("Please provide a Job Description.")
    elif not uploaded_files:
        st.error("Please upload potential candidate resumes.")
    else:
        status_text = st.empty()
        progress_bar = st.progress(0)
        
        status_text.text("Initiating Core System...")
        
        # Create a temporary directory to store uploaded files for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            status_text.text(f"Ingesting {len(uploaded_files)} documents...")
            saved_paths = []
            
            for i, uploaded_file in enumerate(uploaded_files):
                path = os.path.join(temp_dir, uploaded_file.name)
                with open(path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                saved_paths.append(path)
                progress_bar.progress((i + 1) / len(uploaded_files) * 0.3)
            
            status_text.text("Running NLP Analysis & Scoring...")
            progress_bar.progress(0.4)
            
            try:
                orchestrator = ScreeningOrchestrator()
                results = orchestrator.run_screening_mission(jd_text, temp_dir)
                progress_bar.progress(1.0)
                status_text.success("Mission Accomplished!")
                
                if results:
                    st.subheader(" Ranked Candidates")
                    
                    df = pd.DataFrame(results)
                    # Formatting for display
                    display_df = df[['score', 'filename', 'raw_text_preview']].copy()

                    st.dataframe(
                        display_df,
                        column_config={
                            "score": st.column_config.ProgressColumn(
                                "Match Score",
                                min_value=0.0,
                                max_value=1.0,
                                format="%.4f",
                            )
                        },
                        use_container_width=True
                    )

                    
                    st.subheader("Detailed Breakdown")
                    for i, row in df.head(5).iterrows():
                        with st.expander(f"#{i+1} {row['filename']} - Score: {row['score']:.4f}"):
                            st.write("**Extracted Text Preview:**")
                            st.caption(row['raw_text_preview'] + "...")
                            
                    # Download results
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Ranking Report",
                        data=csv,
                        file_name='resume_ranking.csv',
                        mime='text/csv',
                    )
                else:
                    st.warning("No matches found or parsing failed.")
                    
            except Exception as e:
                st.error(f"An error occurred during the mission: {str(e)}")
