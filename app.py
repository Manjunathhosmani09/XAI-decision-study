"""
Streamlit App — XAI Decision Quality Experiment (Objective 2)
Groups: A = Raw Predictions | B = SHAP Visualizations | C = LLM Narrative Reports
"""

import csv
from datetime import datetime
import os
import random
import time
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------
CASES_DATA_FILE = "responses_cases.csv"
SURVEY_DATA_FILE = "responses_survey.csv"
GROUPS = ["A", "B", "C"]

# ---------------------------------------------------------------------
# 10 CASES
# ---------------------------------------------------------------------
CASES = [
    dict(
        id=1,
        profile="Age 29, Sales Executive, Monthly Income ₹42,000, 2 yrs at company, OverTime: Yes, Job Satisfaction: Low",
        prediction="Will Leave",
        confidence=82,
        ground_truth="Left",
        shap=[
            "OverTime (+0.31, increases leave risk)",
            "Low Job Satisfaction (+0.24)",
            "Short Tenure (+0.12)",
        ],
        narrative="This employee is predicted to leave mainly due to frequent overtime combined with low reported job satisfaction. If overtime were reduced, the model estimates the leave probability would drop by roughly 20 percentage points.",
    ),
    dict(
        id=2,
        profile="Age 45, Research Scientist, Monthly Income ₹95,000, 14 yrs at company, OverTime: No, Job Satisfaction: High",
        prediction="Will Stay",
        confidence=91,
        ground_truth="Stayed",
        shap=[
            "Long Tenure (+0.28, decreases leave risk)",
            "High Job Satisfaction (+0.22)",
            "No Overtime (+0.10)",
        ],
        narrative="This employee is predicted to stay largely because of long tenure and high job satisfaction. No single factor suggests elevated flight risk at this time.",
    ),
    dict(
        id=3,
        profile="Age 24, Lab Technician, Monthly Income ₹22,000, 1 yr at company, OverTime: Yes, Job Satisfaction: Medium",
        prediction="Will Leave",
        confidence=64,
        ground_truth="Stayed",
        shap=[
            "Short Tenure (+0.26)",
            "Low Income relative to role (+0.18)",
            "OverTime (+0.14)",
        ],
        narrative="This employee is flagged as a moderate risk due to short tenure and relatively low income for the role, though job satisfaction is not a strong negative factor. Confidence is moderate rather than high.",
    ),
    dict(
        id=4,
        profile="Age 51, Manager, Monthly Income ₹180,000, 20 yrs at company, OverTime: No, Job Satisfaction: Medium",
        prediction="Will Stay",
        confidence=88,
        ground_truth="Stayed",
        shap=[
            "Long Tenure (+0.35)",
            "High Income (+0.20)",
            "Senior Role (+0.09)",
        ],
        narrative="Long tenure, high income, and seniority strongly outweigh the moderate job satisfaction score, resulting in a low predicted risk of leaving.",
    ),
    dict(
        id=5,
        profile="Age 31, Sales Representative, Monthly Income ₹28,000, 3 yrs at company, OverTime: Yes, Job Satisfaction: Low",
        prediction="Will Leave",
        confidence=77,
        ground_truth="Left",
        shap=[
            "Low Job Satisfaction (+0.29)",
            "OverTime (+0.22)",
            "Low Income (+0.15)",
        ],
        narrative="Low job satisfaction combined with frequent overtime and comparatively low income are the primary drivers behind this leave prediction.",
    ),
    dict(
        id=6,
        profile="Age 38, HR Specialist, Monthly Income ₹55,000, 8 yrs at company, OverTime: No, Job Satisfaction: High",
        prediction="Will Stay",
        confidence=58,
        ground_truth="Left",
        shap=[
            "High Job Satisfaction (+0.20, decreases risk)",
            "Long Tenure (+0.15)",
            "Recent Manager Change (+0.13, increases risk)",
        ],
        narrative="Job satisfaction and tenure suggest stability, but a recent change in reporting manager introduces some uncertainty. Confidence in this prediction is only moderate.",
    ),
    dict(
        id=7,
        profile="Age 26, Sales Executive, Monthly Income ₹35,000, 1.5 yrs at company, OverTime: Yes, Job Satisfaction: Medium",
        prediction="Will Leave",
        confidence=70,
        ground_truth="Left",
        shap=[
            "Short Tenure (+0.25)",
            "OverTime (+0.19)",
            "Distance From Home High (+0.11)",
        ],
        narrative="Short tenure and consistent overtime, combined with a long commute, together push this case toward a leave prediction.",
    ),
    dict(
        id=8,
        profile="Age 42, Research Director, Monthly Income ₹150,000, 12 yrs at company, OverTime: No, Job Satisfaction: Medium",
        prediction="Will Stay",
        confidence=85,
        ground_truth="Stayed",
        shap=[
            "Long Tenure (+0.30)",
            "High Income (+0.18)",
            "No Overtime (+0.08)",
        ],
        narrative="Despite only moderate job satisfaction, this employee's long tenure and high compensation strongly favor staying.",
    ),
    dict(
        id=9,
        profile="Age 33, Laboratory Technician, Monthly Income ₹26,000, 4 yrs at company, OverTime: Yes, Job Satisfaction: Low",
        prediction="Will Leave",
        confidence=73,
        ground_truth="Stayed",
        shap=[
            "Low Job Satisfaction (+0.24)",
            "OverTime (+0.20)",
            "Low Income (+0.13)",
        ],
        narrative="Low job satisfaction and frequent overtime are the leading indicators here, though tenure of 4 years provides some counterbalancing stability.",
    ),
    dict(
        id=10,
        profile="Age 55, Manager, Monthly Income ₹200,000, 25 yrs at company, OverTime: No, Job Satisfaction: High",
        prediction="Will Stay",
        confidence=94,
        ground_truth="Stayed",
        shap=[
            "Long Tenure (+0.33)",
            "High Income (+0.24)",
            "High Job Satisfaction (+0.15)",
        ],
        narrative="Every major factor — tenure, income, and satisfaction — points toward strong retention. This is a very low-risk case.",
    ),
]

POST_SURVEY_ITEMS = [
    "I found the information provided useful for making my decisions.",
    "I would trust this type of tool if I encountered it in my actual work.",
    "I would want to use a tool like this again in the future.",
    "The format I was shown made me more confident in my decisions overall.",
    "I found it easy to understand why the model made its predictions.",
    "I believe this tool would improve decision-making in a real organization.",
    "The explanations reduced the time and mental effort needed to evaluate cases.",
    "I felt capable of identifying potential errors or biases in the model's output.",
    "The level of detail in the explanations was sufficient and not overwhelming.",
    "I relied heavily on the AI's explanation rather than relying purely on intuition.",
    "The format helped me justify and defend my final decisions to others.",
    "Overall, having access to this AI assistance increased my decision-making speed.",
]

# ---------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------
def save_row_to_csv(filepath: str, row: dict):
    file_exists = os.path.exists(filepath)
    with open(filepath, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=list(row.keys()), quoting=csv.QUOTE_ALL
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def init_session():
    if "stage" not in st.session_state:
        st.session_state.stage = "screening"
    if "group" not in st.session_state:
        st.session_state.group = random.choice(GROUPS)
    if "case_index" not in st.session_state:
        st.session_state.case_index = 0
    if "cases_order" not in st.session_state:
        order = CASES.copy()
        random.shuffle(order)
        st.session_state.cases_order = order
    if "case_start_time" not in st.session_state:
        st.session_state.case_start_time = None
    if "participant_id" not in st.session_state:
        st.session_state.participant_id = f"P{int(time.time() * 1000)}"


def restart():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


# ---------------------------------------------------------------------
# APP CONFIG & ADMIN SIDEBAR
# ---------------------------------------------------------------------
st.set_page_config(page_title="XAI Decision Study", layout="centered")
init_session()

st.sidebar.markdown("---")
admin_pass = st.sidebar.text_input("Admin Access", type="password")

if admin_pass == "research2026":
    st.sidebar.subheader("Researcher Dashboard")

    if os.path.exists(CASES_DATA_FILE):
        try:
            df_cases = pd.read_csv(CASES_DATA_FILE, on_bad_lines="skip")
            st.sidebar.write(f"Task Rows: {len(df_cases)}")
            with st.sidebar.expander("View Cases Log"):
                st.dataframe(df_cases)
            st.sidebar.download_button(
                label="📥 Download Task Responses",
                data=df_cases.to_csv(index=False).encode("utf-8"),
                file_name="responses_cases.csv",
                mime="text/csv",
                key="dl_cases",
            )
        except Exception as e:
            st.sidebar.error(f"Error reading cases: {e}")
    else:
        st.sidebar.info("No case decisions logged yet.")

    if os.path.exists(SURVEY_DATA_FILE):
        try:
            df_survey = pd.read_csv(SURVEY_DATA_FILE, on_bad_lines="skip")
            st.sidebar.write(f"Surveys Completed: {len(df_survey)}")
            with st.sidebar.expander("View Survey Log"):
                st.dataframe(df_survey)
            st.sidebar.download_button(
                label="📥 Download Post-Surveys",
                data=df_survey.to_csv(index=False).encode("utf-8"),
                file_name="responses_survey.csv",
                mime="text/csv",
                key="dl_survey",
            )
        except Exception as e:
            st.sidebar.error(f"Error reading survey: {e}")
    else:
        st.sidebar.info("No surveys completed yet.")

# ---------------------------------------------------------------------
# STAGE ROUTING
# ---------------------------------------------------------------------
st.title("Explainable AI — Decision Study")

# ---------- STAGE 1: SCREENING ----------
if st.session_state.stage == "screening":
    st.subheader("Before we begin")

    participant_name = st.text_input("Full Name:")

    current_status = st.radio(
        "Current Status:",
        ["Student", "Working Professional"],
        index=None,
    )

    role = st.radio(
        "What is your domain / field of specialization?",
        [
            "Management / MBA / Business Analytics",
            "Data Science / Machine Learning / AI",
            "Software / Technology / Engineering",
            "Other",
        ],
        index=None,
    )
    ml_experience = st.radio(
        "Do you have prior coursework or work experience involving machine learning or data analysis?",
        ["Yes", "No"],
        index=None,
    )
    shap_familiarity = st.radio(
        "Have you worked with SHAP or similar model explanation tools before?",
        ["Yes, frequently", "Yes, a little", "No, not yet"],
        index=None,
    )
    consent = st.checkbox(
        "I understand this is a research study for an MBA project, my responses will be "
        "anonymized, and I can withdraw at any time. I agree to proceed."
    )

    if st.button("Start Study"):
        if not participant_name.strip():
            st.error("Please enter your name.")
        elif not current_status:
            st.error("Please select your current status.")
        elif not role:
            st.error("Please select your domain/specialization.")
        elif not ml_experience:
            st.error("Please select your ML experience status.")
        elif not shap_familiarity:
            st.error("Please select your familiarity with explanation tools.")
        elif not consent:
            st.error("Please check the consent box to proceed.")
        elif ml_experience == "No":
            st.warning(
                "Thank you for your interest — this study is currently scoped to "
                "participants with foundational exposure to data analytics or ML."
            )
        else:
            st.session_state.participant_name = participant_name.strip()
            st.session_state.current_status = current_status
            st.session_state.role = role
            st.session_state.shap_familiarity = shap_familiarity
            st.session_state.stage = "instructions"
            st.rerun()

# ---------- STAGE 2: INSTRUCTIONS ----------
elif st.session_state.stage == "instructions":
    st.subheader("Instructions")
    st.write(
        f"Hello **{st.session_state.participant_name}**, you are assigned to **Group {st.session_state.group}**. "
        "You will be shown 10 business cases involving an employee attrition prediction "
        "made by a machine learning model. For each case, decide: **Will this employee "
        "leave the company or not?** Then rate your confidence. There are no right or "
        "wrong answers being judged about you personally — we are studying the tool, not you."
    )
    if st.button("Begin Cases"):
        st.session_state.stage = "cases"
        st.session_state.case_start_time = time.time()
        st.rerun()

# ---------- STAGE 3: CASES ----------
elif st.session_state.stage == "cases":
    idx = st.session_state.case_index
    cases = st.session_state.cases_order

    if idx < len(cases):
        case = cases[idx]
        group = st.session_state.group

        st.progress(idx / len(cases))
        st.subheader(f"Case {idx + 1} of {len(cases)}")
        st.markdown(f"**Employee Profile:** {case['profile']}")
        st.markdown(
            f"**Model Prediction:** {case['prediction']}  \n**Model Confidence:** {case['confidence']}%"
        )

        if group == "B":
            st.markdown("**SHAP Top Feature Attributions:**")
            for f in case["shap"]:
                st.markdown(f"- {f}")
        elif group == "C":
            st.markdown("**Narrative Explanation:**")
            st.info(case["narrative"])

        with st.form(key=f"form_{idx}"):
            decision = st.radio(
                "Your decision — will this employee leave?",
                ["Yes, will leave", "No, will stay"],
                index=None,
            )
            confidence = st.select_slider(
                "How confident are you in this decision? (1 = Very Low, 7 = Very High)",
                options=[1, 2, 3, 4, 5, 6, 7],
                value=None,
            )
            clarity = None
            actionability = None
            if group in ("B", "C"):
                clarity = st.select_slider(
                    "How clear was the explanation provided? (1 = Very Unclear, 7 = Very Clear)",
                    options=[1, 2, 3, 4, 5, 6, 7],
                    value=None,
                )
            if group == "C":
                actionability = st.select_slider(
                    "How actionable did the explanation feel? (1 = Not Actionable, 7 = Highly Actionable)",
                    options=[1, 2, 3, 4, 5, 6, 7],
                    value=None,
                )
            submitted = st.form_submit_button("Submit & Next")

        if submitted:
            missing_fields = []
            if decision is None:
                missing_fields.append("Your decision (Will leave / Will stay)")
            if confidence is None:
                missing_fields.append("Confidence rating")
            if group in ("B", "C") and clarity is None:
                missing_fields.append("Explanation clarity rating")
            if group == "C" and actionability is None:
                missing_fields.append("Explanation actionability rating")

            if missing_fields:
                st.error(f"Please provide: {', '.join(missing_fields)}")
            else:
                elapsed = round(time.time() - st.session_state.case_start_time, 2)
                participant_decision = (
                    "Left" if decision.startswith("Yes") else "Stayed"
                )
                correct = int(participant_decision == case["ground_truth"])

                save_row_to_csv(
                    CASES_DATA_FILE,
                    {
                        "participant_id": st.session_state.participant_id,
                        "name": st.session_state.participant_name,
                        "status": st.session_state.current_status,
                        "group": group,
                        "role": st.session_state.role,
                        "shap_familiarity": st.session_state.shap_familiarity,
                        "case_id": case["id"],
                        "decision": participant_decision,
                        "ground_truth": case["ground_truth"],
                        "correct": correct,
                        "confidence": confidence,
                        "clarity": clarity if clarity is not None else "",
                        "actionability": (
                            actionability if actionability is not None else ""
                        ),
                        "decision_time_sec": elapsed,
                        "timestamp": datetime.now().isoformat(),
                    },
                )

                st.session_state.case_index += 1
                st.session_state.case_start_time = time.time()
                st.rerun()
    else:
        st.session_state.stage = "post_survey"
        st.rerun()

# ---------- STAGE 4: POST-SURVEY ----------
elif st.session_state.stage == "post_survey":
    st.subheader("Post-Study Survey: Decision Evaluation")
    st.write(
        "Please indicate your level of agreement with the following statements "
        "(1 = Strongly Disagree, 7 = Strongly Agree):"
    )

    with st.form("post_survey"):
        ratings = []
        for i, item in enumerate(POST_SURVEY_ITEMS):
            r = st.select_slider(
                f"{i + 1}. {item}",
                options=[1, 2, 3, 4, 5, 6, 7],
                value=None,
                key=f"post_{i}",
            )
            ratings.append(r)

        open_1 = st.text_area(
            "What, if anything, made your decisions easier or harder in this study?"
        )
        open_2 = st.text_area(
            "Any suggestions to improve how this explanation was presented?"
        )
        age_range = st.selectbox(
            "Age range",
            ["18–24", "25–34", "35–44", "45+"],
            index=None,
            placeholder="Choose an option",
        )
        experience = st.selectbox(
            "Years of ML/data experience",
            ["0–1", "1–2", "2+"],
            index=None,
            placeholder="Choose an option",
        )
        education = st.selectbox(
            "Highest education level",
            ["Bachelor's", "Master's in progress", "Master's completed", "Other"],
            index=None,
            placeholder="Choose an option",
        )
        submitted = st.form_submit_button("Submit Survey")

    if submitted:
        if any(r is None for r in ratings):
            st.error("Please provide a rating for all 12 evaluation questions.")
        elif not age_range:
            st.error("Please select your age range.")
        elif not experience:
            st.error("Please select your years of ML/data experience.")
        elif not education:
            st.error("Please select your highest education level.")
        else:
            survey_record = {
                "participant_id": st.session_state.participant_id,
                "name": st.session_state.participant_name,
                "status": st.session_state.current_status,
                "group": st.session_state.group,
                "age_range": age_range,
                "experience": experience,
                "education": education,
                "open_response_1": open_1,
                "open_response_2": open_2,
                "timestamp": datetime.now().isoformat(),
            }
            for i, r in enumerate(ratings):
                survey_record[f"post_item_{i+1}"] = r

            save_row_to_csv(SURVEY_DATA_FILE, survey_record)
            st.session_state.stage = "done"
            st.rerun()

# ---------- STAGE 5: DONE ----------
elif st.session_state.stage == "done":
    st.success("Thank you for participating! Your responses have been recorded.")
    st.write(
        "Multiple submissions are permitted in this version of the study — "
        "if you'd like to take part again, click below to restart and you "
        "will be randomly re-assigned to a group."
    )
    if st.button("Restart / Submit Another Response"):
        restart()
