# Study Cases (n=18) — Synthetic Data for Objective 2 Experiment

These are made-up cases (not from a real trained model) styled after the IBM HR Attrition dataset. Each case includes: employee profile (shown to all groups), model prediction + confidence (shown to all groups), top-3 SHAP-style feature attributions (Group B), and a narrative explanation (Group C), plus the **ground truth label** used for scoring accuracy.

A mix of correct and incorrect model predictions is included deliberately — this is what allows you to actually detect differences in decision quality across groups (if the model were always right, participants would just learn to copy it).

---

**Case 1**
- Profile: Age 29, Sales Executive, Monthly Income ₹42,000, 2 years at company, OverTime: Yes, Job Satisfaction: Low
- Model Prediction: **Will Leave** | Confidence: 82%
- Ground Truth: **Left**
- Top SHAP Features: OverTime (+0.31, increases leave risk), Low Job Satisfaction (+0.24), Short Tenure (+0.12)
- Narrative: *"This employee is predicted to leave mainly due to frequent overtime combined with low reported job satisfaction. If overtime were reduced, the model estimates the leave probability would drop by roughly 20 percentage points."*

**Case 2**
- Profile: Age 45, Research Scientist, Monthly Income ₹95,000, 14 years at company, OverTime: No, Job Satisfaction: High
- Model Prediction: **Will Stay** | Confidence: 91%
- Ground Truth: **Stayed**
- Top SHAP Features: Long Tenure (+0.28, decreases leave risk), High Job Satisfaction (+0.22), No Overtime (+0.10)
- Narrative: *"This employee is predicted to stay largely because of long tenure and high job satisfaction. No single factor suggests elevated flight risk at this time."*

**Case 3**
- Profile: Age 24, Lab Technician, Monthly Income ₹22,000, 1 year at company, OverTime: Yes, Job Satisfaction: Medium
- Model Prediction: **Will Leave** | Confidence: 64%
- Ground Truth: **Stayed**
- Top SHAP Features: Short Tenure (+0.26), Low Income relative to role (+0.18), OverTime (+0.14)
- Narrative: *"This employee is flagged as a moderate risk due to short tenure and relatively low income for the role, though job satisfaction is not a strong negative factor. Confidence is moderate rather than high."*

**Case 4**
- Profile: Age 51, Manager, Monthly Income ₹180,000, 20 years at company, OverTime: No, Job Satisfaction: Medium
- Model Prediction: **Will Stay** | Confidence: 88%
- Ground Truth: **Stayed**
- Top SHAP Features: Long Tenure (+0.35), High Income (+0.20), Senior Role (+0.09)
- Narrative: *"Long tenure, high income, and seniority strongly outweigh the moderate job satisfaction score, resulting in a low predicted risk of leaving."*

**Case 5**
- Profile: Age 31, Sales Representative, Monthly Income ₹28,000, 3 years at company, OverTime: Yes, Job Satisfaction: Low
- Model Prediction: **Will Leave** | Confidence: 77%
- Ground Truth: **Left**
- Top SHAP Features: Low Job Satisfaction (+0.29), OverTime (+0.22), Low Income (+0.15)
- Narrative: *"Low job satisfaction combined with frequent overtime and comparatively low income are the primary drivers behind this leave prediction."*

**Case 6**
- Profile: Age 38, HR Specialist, Monthly Income ₹55,000, 8 years at company, OverTime: No, Job Satisfaction: High
- Model Prediction: **Will Stay** | Confidence: 58%
- Ground Truth: **Left**
- Top SHAP Features: High Job Satisfaction (+0.20, decreases risk), Long Tenure (+0.15), Recent Manager Change (+0.13, increases risk)
- Narrative: *"Job satisfaction and tenure suggest stability, but a recent change in reporting manager introduces some uncertainty. Confidence in this prediction is only moderate."*

**Case 7**
- Profile: Age 26, Sales Executive, Monthly Income ₹35,000, 1.5 years at company, OverTime: Yes, Job Satisfaction: Medium
- Model Prediction: **Will Leave** | Confidence: 70%
- Ground Truth: **Left**
- Top SHAP Features: Short Tenure (+0.25), OverTime (+0.19), Distance From Home High (+0.11)
- Narrative: *"Short tenure and consistent overtime, combined with a long commute, together push this case toward a leave prediction."*

**Case 8**
- Profile: Age 42, Research Director, Monthly Income ₹150,000, 12 years at company, OverTime: No, Job Satisfaction: Medium
- Model Prediction: **Will Stay** | Confidence: 85%
- Ground Truth: **Stayed**
- Top SHAP Features: Long Tenure (+0.30), High Income (+0.18), No Overtime (+0.08)
- Narrative: *"Despite only moderate job satisfaction, this employee's long tenure and high compensation strongly favor staying."*

**Case 9**
- Profile: Age 33, Laboratory Technician, Monthly Income ₹26,000, 4 years at company, OverTime: Yes, Job Satisfaction: Low
- Model Prediction: **Will Leave** | Confidence: 73%
- Ground Truth: **Stayed**
- Top SHAP Features: Low Job Satisfaction (+0.24), OverTime (+0.20), Low Income (+0.13)
- Narrative: *"Low job satisfaction and frequent overtime are the leading indicators here, though tenure of 4 years provides some counterbalancing stability."*

**Case 10**
- Profile: Age 55, Manager, Monthly Income ₹200,000, 25 years at company, OverTime: No, Job Satisfaction: High
- Model Prediction: **Will Stay** | Confidence: 94%
- Ground Truth: **Stayed**
- Top SHAP Features: Long Tenure (+0.33), High Income (+0.24), High Job Satisfaction (+0.15)
- Narrative: *"Every major factor — tenure, income, and satisfaction — points toward strong retention. This is a very low-risk case."*

**Case 11**
- Profile: Age 27, Sales Representative, Monthly Income ₹24,000, 2 years at company, OverTime: Yes, Job Satisfaction: Low
- Model Prediction: **Will Leave** | Confidence: 68%
- Ground Truth: **Left**
- Top SHAP Features: Low Job Satisfaction (+0.27), OverTime (+0.18), Low Income (+0.14)
- Narrative: *"Low satisfaction and overtime, paired with below-average income for this role, are the primary contributors to elevated leave risk."*

**Case 12**
- Profile: Age 36, Research Scientist, Monthly Income ₹68,000, 6 years at company, OverTime: No, Job Satisfaction: Medium
- Model Prediction: **Will Stay** | Confidence: 61%
- Ground Truth: **Left**
- Top SHAP Features: Moderate Tenure (+0.14, decreases risk), No Overtime (+0.10), Stagnant Promotion History (+0.16, increases risk)
- Narrative: *"While tenure and workload appear favorable, the lack of a promotion in several years introduces meaningful uncertainty. Model confidence is only moderate."*

**Case 13**
- Profile: Age 30, HR Representative, Monthly Income ₹30,000, 3 years at company, OverTime: Yes, Job Satisfaction: Medium
- Model Prediction: **Will Leave** | Confidence: 55%
- Ground Truth: **Stayed**
- Top SHAP Features: OverTime (+0.18), Short-Moderate Tenure (+0.12), Medium Job Satisfaction (+0.08, slight increase)
- Narrative: *"Overtime is the dominant factor here, though satisfaction is not strongly negative. This is a borderline case with relatively low model confidence."*

**Case 14**
- Profile: Age 48, Manufacturing Director, Monthly Income ₹165,000, 18 years at company, OverTime: No, Job Satisfaction: High
- Model Prediction: **Will Stay** | Confidence: 90%
- Ground Truth: **Stayed**
- Top SHAP Features: Long Tenure (+0.31), High Income (+0.21), High Job Satisfaction (+0.17)
- Narrative: *"Strong tenure, compensation, and satisfaction combine to produce a confidently low leave-risk prediction."*

**Case 15**
- Profile: Age 25, Sales Executive, Monthly Income ₹27,000, 1 year at company, OverTime: Yes, Job Satisfaction: Low
- Model Prediction: **Will Leave** | Confidence: 80%
- Ground Truth: **Left**
- Top SHAP Features: Short Tenure (+0.28), Low Job Satisfaction (+0.24), OverTime (+0.16)
- Narrative: *"A short tenure combined with low job satisfaction and frequent overtime places this employee in a high-risk category."*

**Case 16**
- Profile: Age 40, Healthcare Representative, Monthly Income ₹72,000, 9 years at company, OverTime: No, Job Satisfaction: Medium
- Model Prediction: **Will Stay** | Confidence: 66%
- Ground Truth: **Stayed**
- Top SHAP Features: Long-Moderate Tenure (+0.19), No Overtime (+0.13), Medium Job Satisfaction (+0.06)
- Narrative: *"Tenure and manageable workload favor retention, though satisfaction is only moderate, keeping model confidence from being very high."*

**Case 17**
- Profile: Age 34, Sales Executive, Monthly Income ₹50,000, 5 years at company, OverTime: Yes, Job Satisfaction: High
- Model Prediction: **Will Stay** | Confidence: 63%
- Ground Truth: **Left**
- Top SHAP Features: High Job Satisfaction (+0.22, decreases risk), Moderate Tenure (+0.14), OverTime (+0.17, increases risk, partially offsetting)
- Narrative: *"High job satisfaction is the main factor favoring retention, but consistent overtime is working against it, resulting in only moderate model confidence."*

**Case 18**
- Profile: Age 29, Lab Technician, Monthly Income ₹25,000, 2.5 years at company, OverTime: No, Job Satisfaction: Medium
- Model Prediction: **Will Stay** | Confidence: 59%
- Ground Truth: **Stayed**
- Top SHAP Features: No Overtime (+0.15), Moderate Tenure (+0.11), Medium Job Satisfaction (+0.07)
- Narrative: *"No single strong risk factor is present, though satisfaction and tenure are both only moderate, keeping this prediction from being highly confident."*

---

## Summary Table

| Case | Prediction | Ground Truth | Correct? | Confidence |
|------|-----------|---------------|----------|------------|
| 1 | Leave | Left | ✅ | 82% |
| 2 | Stay | Stayed | ✅ | 91% |
| 3 | Leave | Stayed | ❌ | 64% |
| 4 | Stay | Stayed | ✅ | 88% |
| 5 | Leave | Left | ✅ | 77% |
| 6 | Stay | Left | ❌ | 58% |
| 7 | Leave | Left | ✅ | 70% |
| 8 | Stay | Stayed | ✅ | 85% |
| 9 | Leave | Stayed | ❌ | 73% |
| 10 | Stay | Stayed | ✅ | 94% |
| 11 | Leave | Left | ✅ | 68% |
| 12 | Stay | Left | ❌ | 61% |
| 13 | Leave | Stayed | ❌ | 55% |
| 14 | Stay | Stayed | ✅ | 90% |
| 15 | Leave | Left | ✅ | 80% |
| 16 | Stay | Stayed | ✅ | 66% |
| 17 | Stay | Left | ❌ | 63% |
| 18 | Stay | Stayed | ✅ | 59% |

**Design notes:**
- 12 of 18 model predictions are correct (~67% accuracy), 6 are wrong — deliberately imperfect so participants can't just "trust the model blindly" and still score well. This is what makes the explanation format matter.
- Wrong predictions are spread across both classes (not all false leaves or all false stays) to avoid bias.
- Confidence scores vary from 55%–94% so participants also see genuine model uncertainty, not just extremes.
- These cases can be swapped for real model outputs later without changing any survey structure — just replace the profile/prediction/SHAP/narrative fields with actual outputs from your trained XGBoost + SHAP + LLM pipeline.
