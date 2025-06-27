import streamlit as st

# --- App Config ---
st.set_page_config(page_title="🩺 CARDIOMETRIX", layout="centered")

# --- Hero Section ---

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
# --- Intro Section ---
st.markdown("### 👋 Welcome to CARDIOMETRIX")
st.write("""
CARDIOMETRIX intelligently analyzes risks of:

- 🏋️ **Obesity** (BMI-based)
- 💉 **Diabetes** (Glucose-based)
- ❤️ **Hypertension** (Blood Pressure-based)

📍 Tap or click below to begin.
""")

# --- Navigation Buttons (Mobile/Responsive) ---
st.markdown("<div class='button-container' style='display: flex; justify-content: space-around; gap: 1rem; flex-wrap: wrap;'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏋️ Obesity"):
        st.session_state["page"] = "Obesity"

with col2:
    if st.button("💉 Diabetes"):
        st.session_state["page"] = "Diabetes"

with col3:
    if st.button("❤️ Hypertension"):
        st.session_state["page"] = "Hypertension"

st.markdown("</div>", unsafe_allow_html=True)

# --- Redirect if page clicked ---
if "page" in st.session_state:
    st.markdown(f"""
    <meta http-equiv="refresh" content="0; url=/{st.session_state['page']}" />
    """, unsafe_allow_html=True)

# --- Info Footer ---
st.markdown("---")
st.info("⚠️ This app provides informational guidance. For medical advice, consult your healthcare provider.")
