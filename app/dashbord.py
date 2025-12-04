import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.title("Dashaalia Dashboard")

# --- Overview KPIs ---
overview = requests.get(f"{API_URL}/api/stats/overview").json()
st.subheader("Vue d'ensemble")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Sessions", overview["total_sessions"])
col2.metric("Durée moyenne", f"{overview['avg_duration']:.2f} min")
col3.metric("Note moyenne", f"{overview['avg_note']:.2f} / 5")
col4.metric("Qualité moyenne", f"{overview['avg_quality']:.2f}")

# --- Top langues ---
langs = requests.get(f"{API_URL}/api/stats/top-languages?limit=5").json()
langs_df = pd.DataFrame(langs)
st.subheader("Top langues")
st.bar_chart(langs_df.set_index("_id")["count"])

# --- Sessions par jour ---
daily = requests.get(f"{API_URL}/api/stats/daily").json()
daily_df = pd.DataFrame(daily)
st.subheader("Évolution du nombre de sessions")
st.line_chart(daily_df.set_index("date")["sessions_count"])

# --- Répartition par service ---
services = requests.get(f"{API_URL}/api/stats/by-service").json()
services_df = pd.DataFrame(services)
st.subheader("Répartition par service")
st.bar_chart(services_df.set_index("_id")["count"])

# --- Interactions ---
interactions = requests.get(f"{API_URL}/api/stats/interactions").json()
st.subheader("Interactions moyennes")
col5, col6, col7 = st.columns(3)
col5.metric("Patient", f"{interactions['avg_patient']:.2f}")
col6.metric("Praticien", f"{interactions['avg_praticien']:.2f}")
col7.metric("Total", f"{interactions['avg_total']:.2f}")

# --- Notes praticiens ---
notes = requests.get(f"{API_URL}/api/stats/notes").json()
notes_df = pd.DataFrame(notes)
st.subheader("Distribution des notes praticiens")
st.bar_chart(notes_df.set_index("_id")["count"])
