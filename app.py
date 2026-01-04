import streamlit as st
import re

# ------------------- CONFIG -------------------

multi_skills = {
    "data analysis": "dataanalysis",
    "machine learning": "machinelearning",
    "deep learning": "deeplearning",
    "cloud computing": "cloudcomputing",
    "artificial intelligence": "artificialintelligence",
    "web development": "webdevelopment"
}

synonyms = {
    "ml": "machinelearning",
    "ai": "artificialintelligence",
    "js": "javascript"
}

stopwords = {
    "and","or","the","a","an","with","for","to","of","in","on","at",
    "looking","developer","engineer","experience","skills","role",
    "we","you","is","are","be","this","that","as","by","from"
}

weights = {
    "python": 3,
    "sql": 2,
    "dataanalysis": 4,
    "machinelearning": 5,
    "deeplearning": 6,
    "artificialintelligence": 6,
    "cloudcomputing": 4,
    "webdevelopment": 3
}

skill_set = {
    "python","sql","javascript","html","css",
    "dataanalysis","machinelearning","deeplearning",
    "artificialintelligence","cloudcomputing",
    "powerbi","excel","java","react","nodejs",
    "webdevelopment","aws","azure","docker","git"
}


# ------------------- ENGINE -------------------

def clean(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    for phrase, token in multi_skills.items():
        if phrase in text:
            text = text.replace(phrase, token)

    words = text.split()
    normalized = set()

    for w in words:
        if w in synonyms:
            w = synonyms[w]

        if w in skill_set:
            normalized.add(w)

    return normalized


def resume_match(resume, job_desc):
    r = clean(resume)
    j = clean(job_desc)

    matched = r & j
    missing = j - r

    total_weight = 0
    obtained_weight = 0

    for skill in j:
        w = weights.get(skill, 1)
        total_weight += w
        if skill in matched:
            obtained_weight += w

    score = obtained_weight / total_weight * 100

    return score, matched, missing

# ------------------- UI -------------------

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("🧠 AI Resume Analyzer")

resume = st.text_area("📄 Paste Your Resume")
job = st.text_area("🧾 Paste Job Description")

if st.button("Analyze Resume"):
    score, matched, missing = resume_match(resume, job)

    st.metric("Match Score", f"{round(score,2)}%")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Skills")
        st.write(sorted(list(matched)))

    with col2:
        st.subheader("❌ Missing Skills")
        st.write(sorted(list(missing)))
