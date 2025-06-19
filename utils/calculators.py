# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 22:54:25 2025

@author: HP
"""

# --- Calculation Functions ---
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return round(weight / (height_m ** 2), 2)

def obesity_risk(bmi):
    if bmi >= 30: return 'High', '🔴'
    elif bmi >= 25: return 'Moderate', '🟡'
    return 'Low', '🟢'

def diabetes_risk(age, bmi, fam_hist, glucose):
    score = sum([age >= 45, bmi >= 25, fam_hist, glucose >= 100])
    if score >= 3: return 'High', '🔴'
    elif score == 2: return 'Moderate', '🟡'
    return 'Low', '🟢'

def hypertension_risk(systolic, diastolic):
    if systolic >= 140 or diastolic >= 90: return 'High', '🔴'
    elif systolic >= 130 or diastolic >= 85: return 'Moderate', '🟡'
    return 'Low', '🟢'

def bmi_status(bmi):
    if bmi < 18.5: return "Underweight"
    elif bmi < 25: return "Normal"
    elif bmi < 30: return "Overweight"
    else: return "Obese"