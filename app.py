import streamlit as st

st.set_page_config(
    page_title="SkillSync",
    page_icon="💼",
    layout="wide"
)

st.title("💼 SkillSync")
st.subheader("AI-Powered Job & Candidate Matching Platform")

st.write("Choose how you want to use the platform.")

st.markdown("---")

col1, col2 = st.columns(2)

# Recruiter Box
with col1:
    st.markdown("### 🧑‍💼 For Recruiters")
    
    st.info(
        """
        Find the **best candidates** for your job postings using AI-powered matching.
        
        ✔ Upload job description  
        ✔ Get top candidate matches  
        ✔ Skill & experience based ranking
        """
    )
    
    if st.button("Find Candidates"):
        st.switch_page("pages/recruiter_page.py")


# Freelancer Box
with col2:
    st.markdown("### 👩‍💻 For Job Seekers")
    
    st.info(
        """
        Discover the **best jobs** that match your skills and experience.
        
        ✔ Upload your profile  
        ✔ Get recommended jobs  
        ✔ Personalized job matching
        """
    )
    
    if st.button("Find Jobs"):
        st.switch_page("pages/candidate_page.py")