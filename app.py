"""
Streamlit App — XAI Decision Quality Experiment (Objective 2)
Groups: A = Raw Predictions | B = SHAP Visualizations | C = LLM Narrative Reports

Multiple responses from the same person ARE allowed in this version —
no participant ID de-duplication or single-attempt lock is enforced.
Each new session (new browser tab / new "Restart" click) is treated as
an independent submission and randomly re-assigned to a group.
"""

import streamlit as st
import pandas as pd
import random
import time
import os
from datetime import datetime

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------
DATA_FILE = "responses.csv"
GROUPS = ["A", "B", "C"]

# ---------------------------------------------------------------------
# 18 CASES (synthetic — swap fields with real model/SHAP/LLM output later)
# ---------------------------------------------------------------------
CASES = [
    dict(id=1, profile="Age 29, Sales Executive, Monthly Income ₹42,000, 2 yrs at company, OverTime: Yes, Job Satisfaction: Low",
         prediction="Will Leave", confidence=82, ground_truth="Left",
         shap=["OverTime (+0.31, increases leave risk)", "Low Job Satisfaction (+0.24)", "Short Tenure (+0.12)"],
         narrative="This employee is predicted to leave mainly due to frequent overtime combined with low reported job satisfaction. If overtime were reduced, the model estimates the leave probability would drop by roughly 20 percentage points."),
    dict(id=2, profile="Age 45, Research Scientist, Monthly Income ₹95,000, 14 yrs at company, OverTime: No, Job Satisfaction: High",
         prediction="Will Stay", confidence=91, ground_truth="Stayed",
         shap=["Long Tenure (+0.28, decreases leave risk)", "High Job Satisfaction (+0.22)", "No Overtime (+0.10)"],
         narrative="This employee is predicted to stay largely because of long tenure and high job satisfaction. No single factor suggests elevated flight risk at this time."),
    dict(id=3, profile="Age 24, Lab Technician, Monthly Income ₹22,000, 1 yr at company, OverTime: Yes, Job Satisfaction: Medium",
         prediction="Will Leave", confidence=64, ground_truth="Stayed",
         shap=["Short Tenure (+0.26)", "Low Income relative to role (+0.18)", "OverTime (+0.14)"],
         narrative="This employee is flagged as a moderate risk due to short tenure and relatively low income for the role, though job satisfaction is not a strong negative factor. Confidence is moderate rather than high."),
    dict(id=4, profile="Age 51, Manager, Monthly Income ₹180,000, 20 yrs at company, OverTime: No, Job Satisfaction: Medium",
         prediction="Will Stay", confidence=88, ground_truth="Stayed",
         shap=["Long Tenure (+0.35)", "High Income (+0.20)", "Senior Role (+0.09)"],
         narrative="Long tenure, high income, and seniority strongly outweigh the moderate job satisfaction score, resulting in a low predicted risk of leaving."),
    dict(id=5, profile="Age 31, Sales Representative, Monthly Income ₹28,000, 3 yrs at company, OverTime: Yes, Job Satisfaction: Low",
         prediction="Will Leave", confidence=77, ground_truth="Left",
         shap=["Low Job Satisfaction (+0.29)", "OverTime (+0.22)", "Low Income (+0.15)"],
         narrative="Low job satisfaction combined with frequent overtime and comparatively low income are the primary drivers behind this leave prediction."),
    dict(id=6, profile="Age 38, HR Specialist, Monthly Income ₹55,000, 8 yrs at company, OverTime: No, Job Satisfaction: High",
         prediction="Will Stay", confidence=58, ground_truth="Left",
         shap=["High Job Satisfaction (+0.20, decreases risk)", "Long Tenure (+0.15)", "Recent Manager Change (+0.13, increases risk)"],
         narrative="Job satisfaction and tenure suggest stability, but a recent change in reporting manager introduces some uncertainty. Confidence in this prediction is only moderate."),
    dict(id=7, profile="Age 26, Sales Executive, Monthly Income ₹35,000, 1.5 yrs at company, OverTime: Yes, Job Satisfaction: Medium",
         prediction="Will Leave", confidence=70, ground_truth="Left",
         shap=["Short Tenure (+0.25)", "OverTime (+0.19)", "Distance From Home High (+0.11)"],
         narrative="Short tenure and consistent overtime, combined with a long commute, together push this case toward a leave prediction."),
    dict(id=8, profile="Age 42, Research Director, Monthly Income ₹150,000, 12 yrs at company, OverTime: No, Job Satisfaction: Medium",
         prediction="Will Stay", confidence=85, ground_truth="Stayed",
         shap=["Long Tenure (+0.30)", "High Income (+0.18)", "No Overtime (+0.08)"],
         narrative="Despite only moderate job satisfaction, this employee's long tenure and high compensation strongly favor staying."),
    dict(id=9, profile="Age 33, Laboratory Technician, Monthly Income ₹26,000, 4 yrs at company, OverTime: Yes, Job Satisfaction: Low",
         prediction="Will Leave", confidence=73, ground_truth="Stayed",
         shap=["Low Job Satisfaction (+0.24)", "OverTime (+0.20)", "Low Income (+0.13)"],
         narrative="Low job satisfaction and frequent overtime are the leading indicators here, though tenure of 4 years provides some counterbalancing stability."),
    dict(id=10, profile="Age 55, Manager, Monthly Income ₹200,000, 25 yrs at company, OverTime: No, Job Satisfaction: High",
         prediction="Will Stay", confidence=94, ground_truth="Stayed",
         shap=["Long Tenure (+0.33)", "High Income (+0.24)", "High Job Satisfaction (+0.15)"],
         narrative="Every major factor — tenure, income, and satisfaction — points toward strong retention. This is a very low-risk case."),
    dict(id=11, profile="Age 27, Sales Representative, Monthly Income ₹24,000, 2 yrs at company, OverTime: Yes, Job Satisfaction: Low",
         prediction="Will Leave", confidence=68, ground_truth="Left",
         shap=["Low Job Satisfaction (+0.27)", "OverTime (+0.18)", "Low Income (+0.14)"],
         narrative="Low satisfaction and overtime, paired with below-average income for this role, are the primary contributors to elevated leave risk."),
    dict(id=12, profile="Age 36, Research Scientist, Monthly Income ₹68,000, 6 yrs at company, OverTime: No, Job Satisfaction: Medium",
         prediction="Will Stay", confidence=61, ground_truth="Left",
         shap=["Moderate Tenure (+0.14, decreases risk)", "No Overtime (+0.10)", "Stagnant Promotion History (+0.16, increases risk)"],
         narrative="While tenure and workload appear favorable, the lack of a promotion in several years introduces meaningful uncertainty. Model confidence is only moderate."),
    dict(id=13, profile="Age 30, HR Representative, Monthly Income ₹30,000, 3 yrs at company, OverTime: Yes, Job Satisfaction: Medium",
         prediction="Will Leave", confidence=55, ground_truth="Stayed",
         shap=["OverTime (+0.18)", "Short-Moderate Tenure (+0.12)", "Medium Job Satisfaction (+0.08, slight increase)"],
         narrative="Overtime is the dominant factor here, though satisfaction is not strongly negative. This is a borderline case with relatively low model confidence."),
    dict(id=14, profile="Age 48, Manufacturing Director, Monthly Income ₹165,000, 18 yrs at company, OverTime: No, Job Satisfaction: High",
         prediction="Will Stay", confidence=90, ground_truth="Stayed",
         shap=["Long Tenure (+0.31)", "High Income (+0.21)", "High Job Satisfaction (+0.17)"],
         narrative="Strong tenure, compensation, and satisfaction combine to produce a confidently low leave-risk prediction."),
    dict(id=15, profile="Age 25, Sales Executive, Monthly Income ₹27,000, 1 yr at company, OverTime: Yes, Job Satisfaction: Low",
         prediction="Will Leave", confidence=80, ground_truth="Left",
         shap=["Short Tenure (+0.28)", "Low Job Satisfaction (+0.24)", "OverTime (+0.16)"],
         narrative="A short tenure combined with low job satisfaction and frequent overtime places this employee in a high-risk category."),
    dict(id=16, profile="Age 40, Healthcare Representative, Monthly Income ₹72,000, 9 yrs at company, OverTime: No, Job Satisfaction: Medium",
         prediction="Will Stay", confidence=66, ground_truth="Stayed",
         shap=["Long-Moderate Tenure (+0.19)", "No Overtime (+0.13)", "Medium Job Satisfaction (+0.06)"],
         narrative="Tenure and manageable workload favor retention, though satisfaction is only moderate, keeping model confidence from being very high."),
    dict(id=17, profile="Age 34, Sales Executive, Monthly Income ₹50,000, 5 yrs at company, OverTime: Yes, Job Satisfaction: High",
         prediction="Will Stay", confidence=63, ground_truth="Left",
         shap=["High Job Satisfaction (+0.22, decreases risk)", "Moderate Tenure (+0.14)", "OverTime (+0.17, increases risk, partially offsetting)"],
         narrative="High job satisfaction is the main factor favoring retention, but consistent overtime is working against it, resulting in only moderate model confidence."),
    dict(id=18, profile="Age 29, Lab Technician, Monthly Income ₹25,000, 2.5 yrs at company, OverTime: No, Job Satisfaction: Medium",
         prediction="Will Stay", confidence=59, ground_truth="Stayed",
         shap=["No Overtime (+0.15)", "Moderate Tenure (+0.11)", "Medium Job Satisfaction (+0.07)"],
         narrative="No single strong risk factor is present, though satisfaction and tenure are both only moderate, keeping this prediction from being highly confident."),
]

POST_SURVEY_ITEMS = [
    "I found the information provided useful for making my decisions.",
    "I would trust this type of tool if I encountered it in my actual work.",
    "I would want to use a tool like this again in the future.",
    "The format I was shown made me more confident in my decisions overall.",
    "I found it easy to understand why the model made its predictions.",
    "I believe this tool would improve decision-making in a real organization.",
]

# ---------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------
def save_row(row: dict):
    df_row = pd.DataFrame([row])
    header = not os.path.exists(DATA_FILE)
    df_row.to_csv(DATA_FILE, mode="a", header=header, index=False)


def init_session():
    if "stage" not in st.session_state:
        st.session_state.stage = "screening"
    if "group" not in st.session_state:
        st.session_state.group = random.choice(GROUPS)  # re-randomized every new session
    if "case_index" not in st.session_state:
        st.session_state.case_index = 0
    if "responses" not in st.session_state:
        st.session_state.responses = []
    if "cases_order" not in st.session_state:
        order = CASES.copy()
        random.shuffle(order)  # randomize case order per participant
        st.session_state.cases_order = order
    if "case_start_time" not in st.session_state:
        st.session_state.case_start_time = None
    if "participant_id" not in st.session_state:
        st.session_state.participant_id = f"P{int(time.time() * 1000)}"  # auto-generated, non-blocking


def restart():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


# ---------------------------------------------------------------------
# APP
# ---------------------------------------------------------------------
st.set_page_config(page_title="XAI Decision Study", layout="centered")
init_session()

st.title("Explainable AI — Decision Study")

# ---------- STAGE 1: SCREENING ----------
if st.session_state.stage == "screening":
    st.subheader("Before we begin")

    role = st.radio(
        "What is your current role/status?",
        ["Graduate student (MBA/MSBA/Data Science/related)",
         "Early-career ML/Data professional (0–2 years experience)",
         "Other"],
    )
    ml_experience = st.radio(
        "Do you have prior coursework or work experience involving machine learning or data analysis?",
        ["Yes", "No"],
    )
    shap_familiarity = st.radio(
        "Have you worked with SHAP or similar model explanation tools before?",
        ["Yes, frequently", "Yes, a little", "No, not yet"],
    )
    consent = st.checkbox(
        "I understand this is a research study for an MBA project, my responses will be "
        "anonymized, and I can withdraw at any time. I agree to proceed."
    )

    if st.button("Start Study", disabled=not consent):
        if role == "Other" or ml_experience == "No":
            st.warning("Thank you for your interest — this study is currently scoped to "
                       "graduate students and early-career ML/data professionals.")
            st.stop()
        st.session_state.role = role
        st.session_state.shap_familiarity = shap_familiarity
        st.session_state.stage = "instructions"
        st.rerun()

# ---------- STAGE 2: INSTRUCTIONS ----------
elif st.session_state.stage == "instructions":
    st.subheader("Instructions")
    st.write(
        f"You are assigned to **Group {st.session_state.group}**. "
        "You will be shown 18 business cases involving an employee attrition prediction "
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

        st.progress((idx) / len(cases))
        st.subheader(f"Case {idx + 1} of {len(cases)}")
        st.markdown(f"**Employee Profile:** {case['profile']}")
        st.markdown(f"**Model Prediction:** {case['prediction']}  \n**Model Confidence:** {case['confidence']}%")

        if group == "B":
            st.markdown("**SHAP Top Feature Attributions:**")
            for f in case["shap"]:
                st.markdown(f"- {f}")
        elif group == "C":
            st.markdown("**Narrative Explanation:**")
            st.info(case["narrative"])

        with st.form(key=f"form_{idx}"):
            decision = st.radio("Your decision — will this employee leave?",
                                 ["Yes, will leave", "No, will stay"])
            confidence = st.slider("How confident are you in this decision?", 1, 7, 4)
            clarity = None
            actionability = None
            if group in ("B", "C"):
                clarity = st.slider("How clear was the explanation provided?", 1, 7, 4)
            if group == "C":
                actionability = st.slider(
                    "How actionable did the explanation feel?", 1, 7, 4
                )
            submitted = st.form_submit_button("Submit & Next")

        if submitted:
            elapsed = round(time.time() - st.session_state.case_start_time, 2)
            participant_decision = "Left" if decision.startswith("Yes") else "Stayed"
            correct = int(participant_decision == case["ground_truth"])

            save_row({
                "participant_id": st.session_state.participant_id,
                "group": group,
                "role": st.session_state.role,
                "shap_familiarity": st.session_state.shap_familiarity,
                "case_id": case["id"],
                "decision": participant_decision,
                "ground_truth": case["ground_truth"],
                "correct": correct,
                "confidence": confidence,
                "clarity": clarity,
                "actionability": actionability,
                "decision_time_sec": elapsed,
                "timestamp": datetime.now().isoformat(),
            })

            st.session_state.case_index += 1
            st.session_state.case_start_time = time.time()
            st.rerun()
    else:
        st.session_state.stage = "post_survey"
        st.rerun()

# ---------- STAGE 4: POST-SURVEY ----------
elif st.session_state.stage == "post_survey":
    st.subheader("A few final questions")

    with st.form("post_survey"):
        ratings = []
        for i, item in enumerate(POST_SURVEY_ITEMS):
            ratings.append(st.slider(item, 1, 7, 4, key=f"post_{i}"))
        open_1 = st.text_area("What, if anything, made your decisions easier or harder in this study?")
        open_2 = st.text_area("Any suggestions to improve how this information was presented?")
        age_range = st.selectbox("Age range", ["18–24", "25–34", "35–44", "45+"])
        experience = st.selectbox("Years of ML/data experience", ["0–1", "1–2", "2+"])
        education = st.selectbox("Highest education level",
                                  ["Bachelor's", "Master's in progress", "Master's completed", "Other"])
        submitted = st.form_submit_button("Submit Survey")

    if submitted:
        save_row({
            "participant_id": st.session_state.participant_id,
            "group": st.session_state.group,
            "record_type": "post_survey",
            **{f"post_item_{i+1}": r for i, r in enumerate(ratings)},
            "open_response_1": open_1,
            "open_response_2": open_2,
            "age_range": age_range,
            "experience": experience,
            "education": education,
            "timestamp": datetime.now().isoformat(),
        })
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
import os
import pandas as pd
import streamlit as st

# Admin / Researcher Access Section in Sidebar
st.sidebar.markdown("---")
admin_pass = st.sidebar.text_input("Admin Access", type="password")

if admin_pass == "research2026":  # Replace with your secret password
    st.sidebar.subheader("Researcher Dashboard")
    if os.path.exists("responses.csv"):
        df_responses = pd.read_csv("responses.csv")
        st.sidebar.write(f"Total entries: {len(df_responses)}")

        # View data table in an expander
        with st.expander("View Collected Data"):
            st.dataframe(df_responses)

        # Download button
        csv_data = df_responses.to_csv(index=False).encode("utf-8")
        st.sidebar.download_button(
            label="📥 Download responses.csv",
            data=csv_data,
            file_name="collected_xai_responses.csv",
            mime="text/csv",
        )
    else:
        st.sidebar.warning("No responses recorded yet.")
