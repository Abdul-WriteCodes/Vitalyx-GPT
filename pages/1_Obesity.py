# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 22:56:57 2025
@author: HP
"""

import streamlit as st
from utils.calculators import calculate_bmi, obesity_risk, bmi_status
from utils.charting import show_risk_chart

st.set_page_config("🩺 Vitalyx-GPT - Obesity Module", layout="centered")

st.title("⚖️ Obesity Risk Analysis")

# Use text_input with placeholder only — no default, no stepper
weight_str = st.text_input("⚖️ Weight (kg)", placeholder="e.g. 70")
height_str = st.text_input("📏 Height (cm)", placeholder="e.g. 170")

if st.button("Analyze"):
    try:
        weight = float(weight_str)
        height = float(height_str)

        bmi = calculate_bmi(weight, height)
        risk, emoji = obesity_risk(bmi)

        st.success(f"✅ Your BMI is **{bmi}** — {bmi_status(bmi)} ({emoji} **{risk}**)")
        show_risk_chart("Obesity", risk)

        st.session_state["obesity_result"] = {
            "Condition": "Obesity",
            "Risk Level": risk,
            "Score": round(bmi, 2)
        }

    except ValueError:
        st.error("❌ Please enter valid numeric values for weight and height.")
