import streamlit as st

# --- App Config ---
st.set_page_config(page_title="🩺 Vitalyx-GPT", layout="centered")

# --- Main UI ---
st.markdown("""
<div style='text-align: center;'>
    <h1>🩺 Vitalyx-GPT</h1>
    <p style='font-size: 16px; color: gray;'>
        An Intelligent Modular Health Risk Analyzer
    </p>
</div>
""", unsafe_allow_html=True)

st.image("https://cdn-icons-png.flaticon.com/512/2950/2950610.png", width=100)  # Optional logo

st.markdown("### 👋 Welcome!")
st.write("""
**Vitalyx-GPT** helps you analyze common health conditions like Obesity, Diabetes, and Hypertension based on your personal health data.

👉 Use the **sidebar** to select and analyze a health condition.

✅ Each analysis will display:
- Your calculated score (e.g., BMI, BP, Glucose)
- A risk level (Low / Moderate / High)
- A visual risk chart
- Personalized health tips (coming soon)

📊 Once you've completed one or more analyses, visit the **Summary Dashboard** to compare all results side-by-side.
""")

st.markdown("---")
st.info("ℹ️ This tool is for informational purposes only. Always consult a healthcare provider for professional advice.")
