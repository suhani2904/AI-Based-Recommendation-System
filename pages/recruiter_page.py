import streamlit as st
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from new_profile_preprocessing import clean_text

st.set_page_config(page_title="Recruiter", layout="wide")

st.title("🧑‍💼 Recruiter Dashboard")




@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()


@st.cache_resource
def load_candidate_index():
    return faiss.read_index("embeddings/candidate_index.faiss")

candidate_index = load_candidate_index()


@st.cache_resource
def load_job_index():
    return faiss.read_index("embeddings/job_index.faiss")

job_index = load_job_index()


@st.cache_data
def load_candidates():
    return pd.read_csv(
        "datasets/preprocessed_datasets/candidates_preprocessed.csv"
    )

candidates_df = load_candidates()




if "scores" not in st.session_state:
    st.session_state.scores = None

if "indices" not in st.session_state:
    st.session_state.indices = None

if "selected_candidate" not in st.session_state:
    st.session_state.selected_candidate = None




def get_embedding(text):

    emb = model.encode(text)
    emb = np.array([emb]).astype("float32")
    faiss.normalize_L2(emb)

    return emb



st.subheader("Post a Job")

col1, col2 = st.columns(2)

with col1:
    job_id = st.text_input("Job Id")
    title = st.text_input("Job Title")

    experience_level = st.selectbox(
        "Experience Level",
        ["Fresher", "Junior", "Mid", "Mid-Senior", "Senior"]
    )

with col2:
    years_exp = st.text_input("Years of Experience")
    skills = st.text_area("Skills")

responsibilities = st.text_area("Responsibilities")
keywords = st.text_area("Keywords")



if st.button("Find Best Candidates"):

    jobs_path = "datasets/preprocessed_datasets/jobs_preprocessed.csv"

    new_job = pd.DataFrame({
        "JobID": [job_id],
        "Title": [title],
        "ExperienceLevel": [experience_level],
        "YearsOfExperience": [years_exp],
        "Skills": [skills],
        "Responsibilities": [responsibilities],
        "Keywords": [keywords]
    })

    jobs_df = pd.read_csv(jobs_path)

    jobs_df = pd.concat([jobs_df, new_job], ignore_index=True)

    jobs_df.to_csv(jobs_path, index=False)

    # Create embedding
    job_text = clean_text(
        " ".join([
            title,
            skills,
            responsibilities,
            keywords,
            experience_level
        ])
    )

    job_embedding = get_embedding(job_text)

    # Save job embedding
    job_index.add(job_embedding)
    faiss.write_index(job_index, "embeddings/job_index.faiss")

    # Search candidates
    scores, indices = candidate_index.search(job_embedding, 10)
    candidates_df= pd.read_csv("datasets/preprocessed_datasets/candidates_preprocessed.csv")

    st.session_state.scores = scores
    st.session_state.indices = indices




if st.session_state.selected_candidate is not None:

    candidate = candidates_df.iloc[st.session_state.selected_candidate]

    st.markdown("## Candidate Profile")

    with st.container(border=True):

        col1, col2 = st.columns([1,2])

        with col1:

            st.markdown(f"### {candidate['name']}")

            st.write(f"**Title:** {candidate['title']}")
            st.write(f"**Country:** {candidate['country']}")
            st.write(f"**Hourly Rate:** ${candidate['hourlyRate']}")

        with col2:

            st.write("**Skills:**")
            st.write(candidate['skills'])

            st.write("**Description:**")
            st.write(candidate['description'])

        st.markdown("### Performance")

        col3, col4, col5 = st.columns(3)

        with col3:
            st.metric("Job Success", f"{candidate['jobSuccess']}%")

        with col4:
            st.metric("Total Hours", candidate['totalHours'])

        with col5:
            st.metric("Total Jobs", candidate['totalJobs'])

        if st.button("Close Profile"):
            st.session_state.selected_candidate = None

    st.markdown("---")


# -------------------------
# Candidate Cards
# -------------------------

if st.session_state.scores is not None:

    scores = st.session_state.scores
    indices = st.session_state.indices

    st.subheader("Top Candidate Matches")

    cols = st.columns(2)

    for i, (score, idx) in enumerate(zip(scores[0], indices[0])):

        if idx == -1 or idx >= len(candidates_df):
            continue

        candidate = candidates_df.iloc[idx]

        with cols[i % 2]:

            with st.container(border=True):

                st.markdown(f"### {candidate['name']}")

                match = score * 100

                st.progress(float(score))

                st.write(f"**Match:** {match:.1f}%")
                st.write(f"**Title:** {candidate['title']}")
                st.write(f"**Skills:** {candidate['skills']}")
                st.write(f"**Experience Level:** {candidate['ExperienceLevel']}")

                if st.button("View Profile", key=f"profile_{i}"):
                    st.session_state.selected_candidate = idx