# 💼 SkillSync - AI-Powered Job & Candidate Matching Platform

## 📌 Overview
SkillSync is an AI-powered platform designed to intelligently match freelancers and job seekers with relevant job opportunities based on their skills and requirements.

Instead of relying on keyword-based matching, SkillSync uses **semantic similarity and vector search** to understand the true meaning of job descriptions and candidate profiles, enabling more accurate and efficient hiring.

---

## 🚀 Features
- 🔍 Semantic job-candidate matching using embeddings
- ⚡ Fast similarity search using FAISS
- 📊 Real-time matching with similarity scores
- 🧠 Context-aware recommendations (not just keyword matching)
- 💻 Interactive dashboard for recruiters and candidates
- 📈 Scalable pipeline for large datasets

---

## 🛠️ Tech Stack

**Languages**
- Python

**Libraries & Frameworks**
- Sentence Transformers
- FAISS (Facebook AI Similarity Search)
- NumPy
- Pandas
- Scikit-learn
- Streamlit

---

## 🧠 How It Works

### 1. Data Input
- Candidate profiles (skills, experience, interests)
- Job descriptions (requirements, responsibilities)

---

### 2. Embedding Generation
- Convert text data into dense vector embeddings using **Sentence Transformers**
- Captures semantic meaning instead of just keywords

---

### 3. Vector Indexing
- Store embeddings in **FAISS index**
- Enables fast similarity search even for large datasets

---

### 4. Matching Algorithm
- Compute similarity between job and candidate embeddings
- Rank results based on cosine similarity

---

### 5. Output
- Top matching jobs for candidates
- Best candidate recommendations for recruiters
- Display similarity scores for transparency

---

## 📊 Example Workflow

1. User inputs a job description  
2. System converts it into embeddings  
3. FAISS retrieves top matching candidate profiles  
4. Results are ranked and displayed with similarity scores  

---

## Project Structure
```
AI-Based-Recommendation-System
│
├── Dataset_cleaning_and_embedding
│ └── datasets_cleaning_and_embedding.ipynb
│
├── datasets
│ ├── preprocessed_datasets
│ │ ├── candidates_preprocessed.csv
│ │ ├── jobs_preprocessed.csv
│ │
│ ├── job_dataset.csv
│ └── upwork_data_scientists.csv
│
├── embeddings
│ ├── candidate_index.faiss
│ └── job_index.faiss
│
├── pages
│ ├── candidate_page.py
│ └── recruiter_page.py
│
├── app.py
├── new_profile_preprocessing.py
├── requirements.txt
└── README.md
```



---


---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/SkillSync.git
cd SkillSync
```
### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Run the App
```bash
streamlit run app.py
```
### 4️⃣ Open in Browser
```bash
http://localhost:8501
```

##⚠️ Notes
- Ensure datasets are in correct folders

- Make sure FAISS index is created before running

- Install FAISS if needed:

```bash
pip install faiss-cpu
```


