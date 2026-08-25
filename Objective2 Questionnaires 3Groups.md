# Data Collection Questionnaires — Objective 2
## Decision Quality Experiment: Group A (Raw Predictions) / Group B (SHAP Visualizations) / Group C (XAI Narrative Reports)

**Instructions for use:** Each participant is randomly assigned to ONE group only (between-subjects design). Copy the relevant section into Google Forms / Qualtrics / Streamlit. All three groups share the same screening, instructions structure, and post-survey — only the stimulus per case differs.

---

# SECTION 0 — Screening Questions (ALL GROUPS)

1. What is your current role/status?
   - Graduate student (MBA/MSBA/Data Science/related)
   - Early-career ML/Data professional (0–2 years experience)
   - Other *(if Other, participant is screened out)*

2. Do you have prior coursework or work experience involving machine learning or data analysis?
   - Yes
   - No *(if No, participant is screened out)*

3. Have you worked with SHAP or similar model explanation tools before?
   - Yes, frequently
   - Yes, a little
   - No, not yet
   *(Used as a covariate in analysis, not for screening)*

4. Informed consent: "I understand this is a research study for an MBA project, my responses will be anonymized, and I can withdraw at any time." 
   - I agree and wish to proceed
   - I do not agree *(exits survey)*

---

# SECTION 1 — General Instructions (shown once, before Case 1)

*"You will be shown [15–20] business cases involving an employee attrition prediction made by a machine learning model. For each case, you will [see the model's output / see the model's output and SHAP chart / see the model's output and a plain-English explanation], and you must decide: **Will this employee leave the company or not?** After each decision, rate how confident you are. There are no right or wrong answers being judged about you personally — we are studying the tool, not you. Please work at your natural pace."*

---

# GROUP A — Raw Predictions Only

### Per-Case Format (repeat for each of the 15–20 cases)

**Case [X] of [N]**

> Employee Profile: [Age, Department, Job Role, Monthly Income, Years at Company, OverTime status, etc. — key input features, NOT the SHAP values]
>
> Model Prediction: **[Will Leave / Will Stay]**
> Model Confidence Score: **[XX%]**

**Q1.** Based on this information, what is your decision — will this employee leave the company?
   - Yes, will leave
   - No, will stay

**Q2.** How confident are you in this decision?
   - 1 – Not at all confident
   - 2
   - 3
   - 4 – Neutral
   - 5
   - 6
   - 7 – Extremely confident

*(Timestamp auto-logged: time from case display to Q1 submission = decision time)*

---

# GROUP B — SHAP Visualizations

### Per-Case Format (repeat for each of the 15–20 cases)

**Case [X] of [N]**

> Employee Profile: [same input features as Group A]
>
> Model Prediction: **[Will Leave / Will Stay]**
> Model Confidence Score: **[XX%]**
>
> [Embedded SHAP waterfall/force plot image showing top feature contributions for this case]

**Q1.** Based on this information, what is your decision — will this employee leave the company?
   - Yes, will leave
   - No, will stay

**Q2.** How confident are you in this decision?
   - 1 – Not at all confident
   - 2
   - 3
   - 4 – Neutral
   - 5
   - 6
   - 7 – Extremely confident

**Q3.** (Group B & C only) How clear was the explanation provided?
   - 1 – Very unclear
   - 2
   - 3
   - 4 – Neutral
   - 5
   - 6
   - 7 – Very clear

*(Timestamp auto-logged: time from case display to Q1 submission = decision time)*

---

# GROUP C — XAI Narrative Reports

### Per-Case Format (repeat for each of the 15–20 cases)

**Case [X] of [N]**

> Employee Profile: [same input features as Group A]
>
> Model Prediction: **[Will Leave / Will Stay]**
> Model Confidence Score: **[XX%]**
>
> **Narrative Explanation (LLM-generated):**
> *"This employee is predicted to leave primarily because of [top feature 1], combined with [top feature 2] and [top feature 3]. If [key feature] were reduced/increased by [X], the model's prediction would likely change to [alternate outcome], based on counterfactual analysis."*

**Q1.** Based on this information, what is your decision — will this employee leave the company?
   - Yes, will leave
   - No, will stay

**Q2.** How confident are you in this decision?
   - 1 – Not at all confident
   - 2
   - 3
   - 4 – Neutral
   - 5
   - 6
   - 7 – Extremely confident

**Q3.** (Group B & C only) How clear was the explanation provided?
   - 1 – Very unclear
   - 2
   - 3
   - 4 – Neutral
   - 5
   - 6
   - 7 – Very clear

**Q4.** (Group C only) How actionable did the explanation feel — did it suggest what could realistically be changed?
   - 1 – Not actionable at all
   - 2
   - 3
   - 4 – Neutral
   - 5
   - 6
   - 7 – Highly actionable

*(Timestamp auto-logged: time from case display to Q1 submission = decision time)*

---

# SECTION 2 — Post-Survey (ALL GROUPS, after final case)

**Trust / AI Adoption Intent (adapted TAM scale, 1–7 Likert: Strongly Disagree → Strongly Agree)**

1. I found the information provided useful for making my decisions.
2. I would trust this type of tool if I encountered it in my actual work.
3. I would want to use a tool like this again in the future.
4. The format I was shown made me more confident in my decisions overall.
5. I found it easy to understand why the model made its predictions.
6. I believe this tool would improve decision-making in a real organization.

**Open-ended (optional, all groups):**
7. What, if anything, made your decisions easier or harder in this study?
8. Do you have any suggestions to improve how this information was presented?

**Demographics (all groups, end of survey):**
9. Age range: [18–24 / 25–34 / 35–44 / 45+]
10. Years of ML/data experience: [0–1 / 1–2 / 2+]
11. Highest education level: [Bachelor's / Master's in progress / Master's completed / Other]

---

# Notes for Implementation

- **Case content must be identical in substance across groups** — only the *format of explanation* differs (raw vs. SHAP vs. narrative). This isolates the variable you're testing.
- **Randomize case order** within each group to control for ordering/fatigue effects.
- **Q3 and Q4 are intentionally absent from Group A** — there's no "explanation" to rate, so this preserves internal validity.
- Export raw responses to CSV with columns: `participant_id, group, case_id, decision, ground_truth, correct(0/1), confidence, clarity_rating(B/C only), actionability_rating(C only), decision_time_sec`.
- This structure feeds directly into your ANOVA: accuracy and confidence as dependent variables, group (A/B/C) as the independent variable.
