# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 23:03:16 2025
@author: HP
"""

import streamlit as st
from utils.calculators import calculate_bmi, diabetes_risk
from utils.charting import show_risk_chart

st.set_page_config("🩺 Vitalyx-GPT - Diabetes Module", layout="centered")

st.markdown("""
<div style='text-align: center;'>
    <h1>🩺 Vitalyx-GPT</h1>
    <p style='font-size: 16px; color: gray;'>
        An Intelligent Health Risk Analyzer
    </p>
</div>
""", unsafe_allow_html=True)

st.title("🧪 Diabetes Risk Analysis")

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

        bmi = calculate_bmi(weight, height)
        risk, emoji = diabetes_risk(age, bmi, fam_hist, glucose)

        st.success(f"✅ Your calculated BMI is **{bmi}**")
        st.markdown(f"### Diabetes Risk\n{emoji} **{risk}**")
        show_risk_chart("Diabetes", risk)

        st.session_state["diabetes_result"] = {
            "Condition": "Diabetes",
            "Risk Level": risk,
            "Score": glucose
        }

    except ValueError:
        st.error("❌ Please enter valid numeric values for all fields.")
