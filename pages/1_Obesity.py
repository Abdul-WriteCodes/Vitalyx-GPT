# -*- coding: utf-8 -*-
from gpt_advice_openrouter import get_health_advice_openrouter
import streamlit as st
from utils.calculators import calculate_bmi, obesity_risk, bmi_status
from utils.charting import show_risk_chart

st.set_page_config("🩺 Vitalyx-GPT - Obesity Module", layout="centered")

# --- Header ---

st.markdown("""
<div style='text-align: center;'>
    <h1>🩺 Vitalyx-GPT</h1>
    <p style='font-size: 16px; color: gray;'>An Intelligent Health Risk Analyzer</p>
</div>
""", unsafe_allow_html=True)

st.title("🏋️ Obesity Risk Analyzer")

# --- Input Section ---
weight_str = st.text_input("⚖️ Weight (kg)", placeholder="e.g. 70")
height_str = st.text_input("📏 Height (cm)", placeholder="e.g. 170")

# --- Analysis Logic ---
if st.button("🔍 Analyze"):
    try:
        weight = float(weight_str)
        height = float(height_str)

        bmi = calculate_bmi(weight, height)
        risk, emoji = obesity_risk(bmi)

        st.success(f"✅ Your BMI is **{bmi:.2f}** — {bmi_status(bmi)} ({emoji} **{risk}**)")

        show_risk_chart("Obesity", risk)

        st.session_state["obesity_result"] = {
            "Condition": "Obesity",
            "Risk Level": risk,
            "Score": round(bmi, 2)
        }
        st.session_state["bmi_ready"] = True
        st.session_state["bmi_value"] = round(bmi, 2)

    except ValueError:
        st.error("❌ Please enter valid numeric values for weight and height.")
        st.session_state["bmi_ready"] = False

# --- GPT Advice Button (conditionally visible) ---
if st.session_state.get("bmi_ready"):
    if st.button("💬 Get GPT Advice"):
        with st.spinner("Analyzing your result and preparing advice..."):
            advice = get_health_advice_openrouter("obesity", st.session_state["bmi_value"])

        if advice and isinstance(advice, str):
            st.markdown("### 💡 GPT Advice")
            st.markdown(f"""
            <div style='padding:15px; border-radius:10px; border: 1px solid #dcedc8;'>
                {advice}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ GPT advice could not be fetched at the moment.")
