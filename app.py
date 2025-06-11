import streamlit as st
import pandas as pd
import altair as alt

# --- Risk Scores ---
RISK_SCORES = {'Low': 1, 'Moderate': 2, 'High': 3}
RISK_COLORS = {'Low': 'green', 'Moderate': 'orange', 'High': 'red'}

# --- Calculation Functions ---
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return round(weight / (height_m ** 2), 2)

def obesity_risk(bmi):
    if bmi >= 30: return 'High', '🔴'
    elif bmi >= 25: return 'Moderate', '🟡'
    return 'Low', '🟢'

def diabetes_risk(age, bmi, fam_hist, glucose):
    score = sum([age >= 45, bmi >= 25, fam_hist, glucose >= 100])
    if score >= 3: return 'High', '🔴'
    elif score == 2: return 'Moderate', '🟡'
    return 'Low', '🟢'

def hypertension_risk(systolic, diastolic):
    if systolic >= 140 or diastolic >= 90: return 'High', '🔴'
    elif systolic >= 130 or diastolic >= 85: return 'Moderate', '🟡'
    return 'Low', '🟢'

def bmi_status(bmi):
    if bmi < 18.5: return "Underweight"
    elif bmi < 25: return "Normal"
    elif bmi < 30: return "Overweight"
    else: return "Obese"

# --- App Config ---
st.set_page_config("🩺Vitalyx-GPT", layout="centered")
st.markdown(
    """
    <div style='text-align: center;'>
        <h1>🩺 Vitalyx-GPT</h1>
        <p style='font-size: 16px; color: gray;'>
            An Intelligent Health Risk Analyzer
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# --- Sidebar Selection ---
with st.sidebar:
    st.title("⚙️ Settings")
    st.subheader("🩺Vitalyx-GPT.")
    analysis_option = st.sidebar.selectbox(
    "📌 Select Condition to Analyze",
    ("Obesity", "Diabetes", "Hypertension")
)


# Create a 3-column layout to center and constrain form width
left_col, center_col, right_col = st.columns([0.5, 2, 0.5])

with center_col:
    with st.form("input_form"):
        st.subheader(f"📋 Health Data for {analysis_option} Analysis")
        error = False  # Flag to check if input is valid

        if analysis_option == "Obesity":
            weight_str = st.text_input("⚖️ Weight (kg)", placeholder="e.g. 70")
            height_str = st.text_input("📏 Height (cm)", placeholder="e.g. 170")

        elif analysis_option == "Diabetes":
            age_str = st.text_input("🎂 Age", placeholder="e.g. 45")
            weight_str = st.text_input("⚖️ Weight (kg)", placeholder="e.g. 75")
            height_str = st.text_input("📏 Height (cm)", placeholder="e.g. 170")
            glucose_str = st.text_input("🧪 Fasting Glucose (mg/dL)", placeholder="e.g. 90")
            family_history = st.radio("👨‍👩‍👧 Family history of diabetes?", ["No", "Yes"])

        elif analysis_option == "Hypertension":
            systolic_str = st.text_input("🩺 Systolic BP", placeholder="e.g. 120")
            diastolic_str = st.text_input("🩺 Diastolic BP", placeholder="e.g. 80")

        submitted = st.form_submit_button(f"🔍 Analyze {analysis_option} Risk")


# --- Analysis Result ---
if submitted:
    try:
        if analysis_option == "Obesity":
            weight = float(weight_str)
            height = float(height_str)
            bmi = calculate_bmi(weight, height)
            risk, emoji = obesity_risk(bmi)
            st.success(f"✅ Your BMI is **{bmi}** — {bmi_status(bmi)}")
            st.progress(min(bmi / 40, 1.0))
            st.markdown(f"### Obesity Risk\n{emoji} **{risk}**")
            st.caption("💡 Tip: Improve your diet and increase physical activity.")
            risk_df = pd.DataFrame([["Obesity", risk, RISK_SCORES[risk], RISK_COLORS[risk]]],
                                   columns=["Condition", "Risk Level", "Score", "Color"])

        elif analysis_option == "Diabetes":
            age = int(age_str)
            weight = float(weight_str)
            height = float(height_str)
            glucose = float(glucose_str)
            fam_hist = family_history == "Yes"
            bmi = calculate_bmi(weight, height)
            risk, emoji = diabetes_risk(age, bmi, fam_hist, glucose)
            st.markdown(f"### Diabetes Risk\n{emoji} **{risk}**")
            st.caption("💡 Tip: Watch your carbohydrate intake and monitor glucose regularly.")
            risk_df = pd.DataFrame([["Diabetes", risk, RISK_SCORES[risk], RISK_COLORS[risk]]],
                                   columns=["Condition", "Risk Level", "Score", "Color"])

        elif analysis_option == "Hypertension":
            systolic = int(systolic_str)
            diastolic = int(diastolic_str)
            risk, emoji = hypertension_risk(systolic, diastolic)
            st.markdown(f"### Hypertension Risk\n{emoji} **{risk}**")
            st.caption("💡 Tip: Reduce salt, manage stress, and monitor blood pressure.")
            risk_df = pd.DataFrame([["Hypertension", risk, RISK_SCORES[risk], RISK_COLORS[risk]]],
                                   columns=["Condition", "Risk Level", "Score", "Color"])

        # --- Risk Chart ---
        st.markdown("### 📊 Risk Chart")
        chart = alt.Chart(risk_df).mark_bar().encode(
            x='Condition',
            y='Score',
            color=alt.Color('Risk Level', scale=alt.Scale(domain=list(RISK_COLORS.keys()), range=list(RISK_COLORS.values()))),
            tooltip=['Condition', 'Risk Level']
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)

        st.markdown("### ✅ Summary")
        st.write("This analysis is for informational purposes only. Consult your doctor for a full health evaluation.")

    except ValueError:
        st.error("❌ Please fill in all fields with valid numeric values.")
