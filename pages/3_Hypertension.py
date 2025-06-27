# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 23:05:23 2025
@author: HP
"""

import streamlit as st
from utils.calculators import hypertension_risk
from utils.charting import show_risk_chart
from gpt_advice_openrouter import get_health_advice_openrouter  # ✅ GPT integration

# --- Page Config ---
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

st.title("❤️ Hypertension Risk Analyzer")

# --- Session flag ---
if "hypertension_analyzed" not in st.session_state:
    st.session_state.hypertension_analyzed = False

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
        st.session_state["bp_for_advice"] = avg_bp
        st.session_state.hypertension_analyzed = True

    except ValueError:
        st.error("❌ Please enter valid numeric values for both systolic and diastolic BP.")

# --- GPT Advice Section ---
if st.session_state.hypertension_analyzed:
    if st.button("💬 Get GPT Advice"):
        with st.spinner("Fetching personalized health advice..."):
            advice = get_health_advice_openrouter("hypertension", st.session_state["bp_for_advice"])

        if advice and isinstance(advice, str):
            st.markdown("### 💡 GPT Advice")
            st.markdown(f"""
            <div style='padding:15px; border-radius:10px; border: 1px solid #dcedc8; font-size:16px; line-height:1.6;'>
                {advice}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ GPT advice could not be fetched at the moment.")
