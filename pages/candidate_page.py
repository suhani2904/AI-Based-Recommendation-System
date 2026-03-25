import streamlit as st
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from new_profile_preprocessing import clean_text

st.set_page_config(page_title="Candidate", layout="wide")

st.title("👨‍💻 Candidate Dashboard")



@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()


@st.cache_resource
def load_job_index():
    return faiss.read_index("embeddings/job_index.faiss")

job_index = load_job_index()

@st.cache_resource
def load_candidate_index():
    return faiss.read_index("embeddings/candidate_index.faiss")

candidate_index = load_candidate_index()


@st.cache_data
def load_jobs():
    return pd.read_csv(
        "datasets/preprocessed_datasets/jobs_preprocessed.csv"
    )

jobs_df = load_jobs()



def get_embedding(text):

    emb = model.encode(text)
    emb = np.array([emb]).astype("float32")
    faiss.normalize_L2(emb)

    return emb


# -------------------------
# UI
# -------------------------

st.subheader("Create Your Profile")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name")
    title = st.text_input("Title")
    country = st.text_input("Country")
    locality = st.text_input("Locality")
    experience_level = st.selectbox(
        "Experience Level",
        ["Fresher", "Junior", "Mid", "Mid-Senior", "Senior"]
    )


with col2:
    hourly_rate = st.text_input("Hourly Rate")
    total_jobs = st.text_input("Total Jobs Completed")
    total_hours = st.text_input("Total Hours Worked")
    jobSuccess = st.text_input("Job Success")

    skills = st.text_area("Skills")

description = st.text_area("Description")

# -------------------------
# Button
# -------------------------

if st.button("Find Matching Jobs"):

    candidates_path = "datasets/preprocessed_datasets/candidates_preprocessed.csv"

    new_candidate = pd.DataFrame({
        "title": [title],
        "description": [description],
        "skills": [skills],
        "ExperienceLevel": [experience_level],
        "hourlyRate": [hourly_rate],
        "jobSuccess" : [jobSuccess],
        "totalJobs": [total_jobs],
        "totalHours": [total_hours],
        "name" : [name],
        "country" : [country],
        "locality" : [locality]
    })

    candidates_df = pd.read_csv(candidates_path)

    candidates_df = pd.concat([candidates_df, new_candidate], ignore_index=True)

    candidates_df.to_csv(candidates_path, index=False)

    profile_text = clean_text(
        " ".join([
            title,
            description,
            skills,
            experience_level
        ])
    )

    candidate_embedding = get_embedding(profile_text)

    candidate_index.add(candidate_embedding)

    faiss.write_index(candidate_index, "embeddings/candidate_index.faiss")

    scores, indices = job_index.search(candidate_embedding, 15)

    jobs_df = pd.read_csv("datasets/preprocessed_datasets/jobs_preprocessed.csv")

    st.subheader("Top Job Matches")

    cols = st.columns(2)

    for i, (score, idx) in enumerate(zip(scores[0], indices[0])):

        if idx == -1 or idx >= len(jobs_df):
            continue

        job = jobs_df.iloc[idx]

        with cols[i % 2]:
            with st.container(border=True):

                st.markdown(f"### {job['Title']}")

                match = score * 100
                st.progress(float(score))

                st.write(f"**Match:** {match:.2f}%")
                st.write(f"**Job ID:** {job['JobID']}")
                st.write(f"**Skills:** {job['Skills']}")
                st.write(f"**Experience:** {job['ExperienceLevel']}")
                st.write(f"**Years Required:** {job['YearsOfExperience']}")
                st.write(f"**Responsibilities:** {job['Responsibilities']}")