import streamlit as st
from utils.calculators import calculate_bmi, diabetes_risk
from utils.charting import show_risk_chart
from gpt_advice_openrouter import get_health_advice_openrouter  # GPT module

# --- Page Config ---
st.set_page_config("🩺 Vitalyx-GPT - Diabetes Module", layout="centered")

# --- Header ---
st.markdown("""
<div style='text-align: center;'>
    <h1>🩺 Vitalyx-GPT</h1>
    <p style='font-size: 16px; color: gray;'>
        An Intelligent Health Risk Analyzer
    </p>
</div>
""", unsafe_allow_html=True)

st.title("💉 Diabetes Risk Analyzer")

# --- Session flag to check if analysis was done ---
if "diabetes_analyzed" not in st.session_state:
    st.session_state.diabetes_analyzed = False

# --- Input Form ---
with st.form("diabetes_form"):
    age_str = st.text_input("🎂 Age", placeholder="e.g. 45")
    weight_str = st.text_input("⚖️ Weight (kg)", placeholder="e.g. 75")
    height_str = st.text_input("📏 Height (cm)", placeholder="e.g. 170")
    glucose_str = st.text_input("🩸 Fasting Glucose (mg/dL)", placeholder="e.g. 90")
    family_history = st.radio("👨‍👩‍👧 Family history of diabetes?", ["No", "Yes"])
    submitted = st.form_submit_button("🔍 Analyze")

# --- Risk Analysis ---
if submitted:
    try:
        age = int(age_str)
        weight = float(weight_str)
        height = float(height_str)
        glucose = float(glucose_str)
        fam_hist = family_history == "Yes"

        # Calculate BMI and Risk
        bmi = calculate_bmi(weight, height)
        risk, emoji = diabetes_risk(age, bmi, fam_hist, glucose)

        # Display results
        st.success(f"✅ Your calculated BMI is **{bmi}**")
        st.markdown(f"### Diabetes Risk\n{emoji} **{risk}**")
        show_risk_chart("Diabetes", risk)

        # Store results for summary page
        st.session_state["diabetes_result"] = {
            "Condition": "Diabetes",
            "Risk Level": risk,
            "Score": glucose
        }

        st.session_state["glucose_for_advice"] = glucose
        st.session_state.diabetes_analyzed = True

    except ValueError:
        st.error("❌ Please enter valid numeric values for all fields.")

# --- GPT Advice Section ---
if st.session_state.diabetes_analyzed:
    if st.button("💬 Get GPT Advice"):
        with st.spinner("Fetching AI advice based on your glucose level..."):
            advice = get_health_advice_openrouter("diabetes", st.session_state["glucose_for_advice"])

        if advice and isinstance(advice, str):
            st.markdown("### 💡 GPT Advice")
            st.markdown(f"""
            <div style='padding:15px; border-radius:10px; border: 1px solid #dcedc8; font-size:16px; line-height:1.6;'>
                {advice}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ GPT advice could not be fetched at the moment.")
