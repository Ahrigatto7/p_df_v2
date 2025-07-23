import streamlit as st
import pandas as pd
import requests

API_BASE = "http://localhost:8000"

st.header("📜 히스토리 로그")

try:
    res = requests.get(f"{API_BASE}/history_logs")
    logs = res.json()
    df = pd.DataFrame(logs)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    st.dataframe(df.sort_values("timestamp", ascending=False))
except Exception as e:
    st.error(f"로그 불러오기 실패: {e}")

