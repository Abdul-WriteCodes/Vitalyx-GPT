import streamlit as st
import requests

# --- Risk Calculation Functions ---
def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 2)

def obesity_risk_category(bmi):
    if bmi >= 30:
        return 'high'
    elif bmi >= 25:
        return 'moderate'
    return 'low'

def diabetes_risk_score(age, bmi, family_history, fasting_glucose):
    score = sum([
        age >= 45,
        bmi >= 25,
        family_history,
        fasting_glucose >= 100
    ])
    return 'high' if score >= 3 else 'moderate' if score == 2 else 'low'

def hypertension_risk_category(systolic, diastolic):
    if systolic >= 140 or diastolic >= 90:
        return 'high'
    elif systolic >= 130 or diastolic >= 85:
        return 'moderate'
    return 'low'

def generate_alerts(obesity_risk, diabetes_risk, hypertension_risk):
    alert_levels = {
        'high': ("🔴", st.error),
        'moderate': ("🟡", st.warning),
        'low': ("🟢", st.success)
    }

    alerts = {
        'Obesity': {
            'high': "High risk of obesity. Consider lifestyle changes and professional guidance.",
            'moderate': "Moderate risk of obesity. Increase activity and watch diet.",
            'low': "Low obesity risk. Keep it up!"
        },
        'Diabetes': {
            'high': "High risk of diabetes. Please consult a healthcare provider.",
            'moderate': "Moderate diabetes risk. Improve diet and increase exercise.",
            'low': "Low diabetes risk. Great!"
        },
        'Hypertension': {
            'high': "High risk of hypertension. Monitor BP and reduce salt/stress.",
            'moderate': "Moderate hypertension risk. Improve lifestyle habits.",
            'low': "Low hypertension risk. Excellent!"
        }
    }

    for condition, risk in zip(['Obesity', 'Diabetes', 'Hypertension'], 
                               [obesity_risk, diabetes_risk, hypertension_risk]):
        icon, display_fn = alert_levels[risk]
        display_fn(f"**{condition} Alert:** {icon} {alerts[condition][risk]}")

# --- Local LLM with Ollama ---
def get_local_llm_response(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()['response']
    except Exception as e:
        return f"⚠️ Error getting local LLM response: {e}"

def generate_health_advice(risks):
    prompt = (
        f"As a health assistant, provide a warm, supportive explanation to a patient with the following risks:\n\n"
        f"- Obesity risk: {risks['obesity']}\n"
        f"- Diabetes risk: {risks['diabetes']}\n"
        f"- Hypertension risk: {risks['hypertension']}\n\n"
        "Explain what each risk means, how it affects health, and suggest lifestyle tips to manage or reduce each risk."
    )
    return get_local_llm_response(prompt)

# --- UI: Health Risk Analyzer ---
st.title("🧠 Health Risk Analyzer")

with st.form("risk_form"):
    st.subheader("Enter your health information:")
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, step=1.0)
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, step=1.0)
        age = st.number_input("Age", min_value=10, max_value=100, step=1)
    with col2:
        glucose = st.number_input("Fasting Glucose (mg/dL)", min_value=50.0, max_value=300.0, step=1.0)
        systolic = st.number_input("Systolic BP (mmHg)", min_value=80, max_value=200)
        diastolic = st.number_input("Diastolic BP (mmHg)", min_value=50, max_value=130)

    family_history = st.radio("Family history of diabetes?", ["No", "Yes"])

    submitted = st.form_submit_button("🔍 Analyze")

    if submitted:
        bmi = calculate_bmi(weight, height)
        obesity_risk = obesity_risk_category(bmi)
        diabetes_risk = diabetes_risk_score(age, bmi, family_history == "Yes", glucose)
        hypertension_risk = hypertension_risk_category(systolic, diastolic)

        st.session_state.risks = {
            "obesity": obesity_risk,
            "diabetes": diabetes_risk,
            "hypertension": hypertension_risk
        }

        st.success(f"✅ Your BMI is **{bmi}** — Obesity Risk: **{obesity_risk.upper()}**")
        generate_alerts(obesity_risk, diabetes_risk, hypertension_risk)

        with st.spinner("🧠 Talking to your virtual health assistant..."):
            gpt_advice = generate_health_advice(st.session_state.risks)

        st.subheader("🩺 Virtual Health Assistant Says:")
        st.markdown(gpt_advice)

# --- Chatbot Section ---
st.markdown("---")
st.header("💬 Talk to Your Health Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

risk_text = ""
if "risks" in st.session_state:
    r = st.session_state.risks
    risk_text = (
        f"Patient risk levels:\n"
        f"- Obesity risk: {r['obesity']}\n"
        f"- Diabetes risk: {r['diabetes']}\n"
        f"- Hypertension risk: {r['hypertension']}\n\n"
    )

system_prompt = (
    "You are a compassionate virtual health assistant. "
    "You provide supportive advice about lifestyle and wellness but do NOT provide medical diagnoses or treatment.\n\n"
    + risk_text +
    "Always be encouraging and informative."
)

# Display previous chat
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).markdown(msg["content"])

user_prompt = st.chat_input("Type your message here...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    with st.spinner("Health assistant is typing..."):
        full_prompt = system_prompt + "\nUser: " + user_prompt + "\nAssistant:"
        reply = get_local_llm_response(full_prompt)

    st.chat_message("assistant").markdown(reply)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
