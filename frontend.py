import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="FoodChain AI", layout="wide")

st.title("🍱 FoodChain AI – AI + Blockchain Redistribution")

# -----------------------------
# SURPLUS SECTION
# -----------------------------

st.header("🧠 Surplus Detection")

if st.button("Load Surplus Data"):
    response = requests.get(f"{BACKEND_URL}/surplus")
    if response.status_code == 200:
        surplus_data = response.json()
        st.json(surplus_data)
    else:
        st.error("Failed to fetch surplus data")

# -----------------------------
# URGENCY SECTION
# -----------------------------

st.header("📊 Hunger Urgency Zones")

if st.button("Load Urgency Zones"):
    response = requests.get(f"{BACKEND_URL}/urgency")
    if response.status_code == 200:
        urgency_data = response.json()
        st.json(urgency_data)
    else:
        st.error("Failed to fetch urgency data")

# -----------------------------
# REDISTRIBUTION SECTION
# -----------------------------

st.header("🔁 Run Redistribution")

if st.button("Run AI Redistribution"):
    response = requests.get(f"{BACKEND_URL}/redistribute")
    if response.status_code == 200:
        result = response.json()
        st.success("Redistribution Completed!")
        st.json(result)
    else:
        st.error("Redistribution failed")

# -----------------------------
# BLOCKCHAIN VIEWER
# -----------------------------

st.header("🔗 Blockchain Ledger")

if st.button("View Blockchain"):
    response = requests.get(f"{BACKEND_URL}/blockchain")
    if response.status_code == 200:
        chain = response.json()
        st.json(chain)
    else:
        st.error("Failed to fetch blockchain data")
