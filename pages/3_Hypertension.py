# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 23:05:23 2025
@author: HP
"""

import streamlit as st
from utils.calculators import hypertension_risk
from utils.charting import show_risk_chart

st.set_page_config("🩺 Vitalyx-GPT - Hypertension Module", layout="centered")

# --- Header ---
st.markdown("""
<div style='text-align: center;'>
    <h1>🩺 Vitalyx-GPT</h1>
    <p style='font-size: 16px; color: gray;'>
        An Intelligent Health Risk Analyzer
    </p>
</div>
""", unsafe_allow_html=True)

st.title("🩺 Hypertension Risk Analysis")

# --- Input Form ---
with st.form("hypertension_form"):
    systolic_str = st.text_input("🔼 Systolic BP (mmHg)", placeholder="e.g. 120")
    diastolic_str = st.text_input("🔽 Diastolic BP (mmHg)", placeholder="e.g. 80")
    submitted = st.form_submit_button("🔍 Analyze")

# --- Risk Analysis ---
if submitted:
    try:
        systolic = int(systolic_str)
        diastolic = int(diastolic_str)

        risk, emoji = hypertension_risk(systolic, diastolic)

        st.markdown(f"### Hypertension Risk\n{emoji} **{risk}**")
        show_risk_chart("Hypertension", risk)

        avg_bp = round((systolic + diastolic) / 2, 1)

        st.session_state["hypertension_result"] = {
            "Condition": "Hypertension",
            "Risk Level": risk,
            "Score": avg_bp
        }

    except ValueError:
        st.error("❌ Please enter valid numeric values for both systolic and diastolic BP.")
