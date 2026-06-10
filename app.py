import streamlit as st

from utils.pdf_parser import extract_text_from_pdf
from utils.text_preprocessing import clean_text
from utils.skill_extractor import extract_skills
from utils.similarity import calculate_similarity
from utils.recommendations import get_skill_recommendations
from utils.ats_score import calculate_skill_match, calculate_ats_score

st.set_page_config(page_title="AI Resume Screening", layout="wide")

st.title("AI Resume Screening System")
st.write("Upload a resume and compare it against a job description or predefined role.")

resume_file = st.file_uploader("Upload Resume", type=["pdf"])

job_input = st.radio(
    "Choose Job Input Method",
    ["Select Role", "Paste Job Description"]
)

jd_text = ""

if job_input == "Select Role":

    role = st.selectbox(
        "Select Role",
        [
            "Data Scientist",
            "Machine Learning Engineer",
            "Data Analyst",
            "Computer Vision Engineer",
            "NLP Engineer"
        ]
    )

    role_jds = {
        "Data Scientist": """
        Python SQL Statistics Machine Learning
        Data Visualization Pandas NumPy
        """,
        "Machine Learning Engineer": """
        Python TensorFlow PyTorch Docker AWS
        Machine Learning Deep Learning
        """,
        "Data Analyst": """
        SQL Excel Power BI Statistics
        Data Visualization Tableau
        """,
        "Computer Vision Engineer": """
        Python OpenCV YOLO CNN Deep Learning
        Object Detection Image Processing
        """,
        "NLP Engineer": """
        Python NLP Transformers BERT
        Hugging Face LLMs
        """
    }

    jd_text = role_jds[role]

else:
    jd_text = st.text_area(
        "Paste Job Description",
        height=250
    )

if st.button("Analyze Resume"):

    if resume_file is None:
        st.error("Please upload a resume.")

    elif not jd_text.strip():
        st.error("Please provide a job description.")

    else:

        resume_text = extract_text_from_pdf(resume_file)

        resume_text = clean_text(resume_text)
        jd_text = clean_text(jd_text)

        semantic_score = calculate_similarity(
            resume_text,
            jd_text
        )

        with open(
            "data/skills.txt",
            "r",
            encoding="utf-8"
        ) as f:

            skills = [
                skill.strip()
                for skill in f.readlines()
            ]

        resume_skills = extract_skills(
            resume_text,
            skills
        )

        jd_skills = extract_skills(
            jd_text,
            skills
        )

        missing_skills = list(
            set(jd_skills) - set(resume_skills)
        )

        skill_match = calculate_skill_match(
            resume_skills,
            jd_skills
        )

        ats_score = calculate_ats_score(
            skill_match,
            semantic_score
        )

        st.subheader("ATS Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "ATS Score",
                f"{ats_score}%"
            )

        with col2:
            st.metric(
                "Skill Match",
                f"{skill_match}%"
            )

        with col3:
            st.metric(
                "Semantic Match",
                f"{semantic_score:.2f}%"
            )

        st.progress(min(int(ats_score), 100))

        if ats_score >= 80:
            st.success("Excellent match for this role.")
        elif ats_score >= 60:
            st.warning("Moderate match. Improve a few skills.")
        else:
            st.error("Low match. Add more relevant skills and projects.")

        st.subheader("Detected Skills")

        if resume_skills:
            st.write(sorted(resume_skills))
        else:
            st.warning("No skills detected.")

        st.subheader("Missing Skills")

        if missing_skills:
            st.write(sorted(missing_skills))
        else:
            st.success("No missing skills found.")

        recommendations = get_skill_recommendations(
            missing_skills
        )

        st.subheader("Learning Recommendations")

        if recommendations:

            for skill, recommendation in recommendations.items():

                st.markdown(
                    f"**{skill.title()}**"
                )

                st.write(recommendation)

        else:
            st.success("No recommendations needed.")
