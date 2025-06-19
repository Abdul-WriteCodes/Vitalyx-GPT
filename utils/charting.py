# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 22:55:51 2025

@author: HP
"""

import altair as alt
import pandas as pd
import streamlit as st

RISK_SCORES = {'Low': 1, 'Moderate': 2, 'High': 3}
RISK_COLORS = {'Low': 'green', 'Moderate': 'orange', 'High': 'red'}

def show_risk_chart(condition, risk):
    df = pd.DataFrame([[condition, risk, RISK_SCORES[risk], RISK_COLORS[risk]]],
                      columns=["Condition", "Risk Level", "Score", "Color"])
    chart = alt.Chart(df).mark_bar().encode(
        x='Condition',
        y='Score',
        color=alt.Color('Risk Level', scale=alt.Scale(
            domain=list(RISK_COLORS.keys()), range=list(RISK_COLORS.values())))
    ).properties(height=300)
    st.altair_chart(chart, use_container_width=True)
