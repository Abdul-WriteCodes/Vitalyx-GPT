# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 23:00:10 2025
@author: HP
"""

import streamlit as st
import pandas as pd
import altair as alt
from utils.charting import RISK_SCORES, RISK_COLORS

# --- Page Title ---
st.set_page_config("🩺 Vitalyx-GPT - Summary Dashboard", layout="centered")
st.title("📊 Summary Dashboard")
st.markdown("Compare your health risk analysis across all assessed conditions.")

# --- Collect Results from Session ---
conditions = ["obesity_result", "diabetes_result", "hypertension_result"]
results = []

for cond in conditions:
    if cond in st.session_state:
        result = st.session_state[cond].copy()
        result["Score"] = RISK_SCORES[result["Risk Level"]]
        result["Color"] = RISK_COLORS[result["Risk Level"]]
        results.append(result)

# --- Display Results ---
if results:
    df = pd.DataFrame(results)

    st.markdown("### 📝 Analysis Summary Table")
    st.dataframe(
        df[["Condition", "Risk Level", "Score"]],
        use_container_width=True
    )

    st.markdown("### 📊 Comparative Risk Levels")
    chart = alt.Chart(df).mark_bar(size=60).encode(
        x=alt.X("Condition:N", title="Health Condition"),
        y=alt.Y("Score:Q", title="Risk Score (1 = Low, 3 = High)", scale=alt.Scale(domain=[0, 3])),
        color=alt.Color("Risk Level:N",
            scale=alt.Scale(domain=list(RISK_COLORS.keys()), range=list(RISK_COLORS.values())),
            legend=alt.Legend(title="Risk Level")
        ),
        tooltip=["Condition", "Risk Level", "Score"]
    ).properties(
        height=350,
        title="🧬 Condition Risk Comparison"
    )

    st.altair_chart(chart, use_container_width=True)

    # Health insight tips
    st.markdown("### 💡 Health Insight")
    for result in results:
        if result["Risk Level"] == "High":
            st.error(f"🔴 **{result['Condition']}**: High risk detected — please consult a healthcare professional.")
        elif result["Risk Level"] == "Moderate":
            st.warning(f"🟠 **{result['Condition']}**: Moderate risk — consider regular monitoring and lifestyle adjustments.")
        else:
            st.success(f"🟢 **{result['Condition']}**: Low risk — great job maintaining your health!")

else:
    st.info("⚠️ No analysis data yet. Please analyze at least one condition from the sidebar modules.")
