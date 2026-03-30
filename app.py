import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="UPI Fraud Detection Dashboard",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 UPI Fraud Detection Dashboard")
st.markdown("### 🔍 Detect whether a transaction is **Fraudulent** or **Legitimate**")

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("MyTransaction.csv")

# Clean data
df["Withdrawal"] = df["Withdrawal"].fillna(0)
df["Deposit"] = df["Deposit"].fillna(0)
df["Balance"] = df["Balance"].fillna(0)

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("💳 Enter Transaction Details")

withdrawal = st.sidebar.number_input(
    "Withdrawal Amount",
    min_value=0.0,
    value=500.0
)

deposit = st.sidebar.number_input(
    "Deposit Amount",
    min_value=0.0,
    value=0.0
)

balance = st.sidebar.number_input(
    "Current Balance",
    min_value=0.0,
    value=1000.0
)

# -----------------------------
# Dashboard Metrics
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("💸 Avg Withdrawal", f"{df['Withdrawal'].mean():,.2f}")
col2.metric("💰 Avg Deposit", f"{df['Deposit'].mean():,.2f}")
col3.metric("🏦 Avg Balance", f"{df['Balance'].mean():,.2f}")

# -----------------------------
# Transaction Chart
# -----------------------------
st.subheader("📊 Transaction Pattern Analysis")

fig, ax = plt.subplots(figsize=(8, 4))
df[["Withdrawal", "Deposit"]].sum().plot(kind="bar", ax=ax)
plt.xticks(rotation=0)
st.pyplot(fig)

# -----------------------------
# Fraud Detection Logic
# -----------------------------
st.subheader("🛡️ Fraud Detection Result")

if st.button("🔍 Check Transaction"):
    fraud_score = 0

    avg_withdrawal = df["Withdrawal"].mean()

    # Rule 1: unusually high withdrawal
    if withdrawal > avg_withdrawal * 3:
        fraud_score += 40

    # Rule 2: withdrawal > balance
    if withdrawal > balance:
        fraud_score += 40

    # Rule 3: no deposit + high withdrawal
    if deposit == 0 and withdrawal > avg_withdrawal * 2:
        fraud_score += 20

    # Final decision
    if fraud_score >= 50:
        st.error(f"🚨 Fraudulent Transaction Detected! (Risk Score: {fraud_score}%)")
    else:
        st.success(f"✅ Legitimate Transaction (Risk Score: {fraud_score}%)")
