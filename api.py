import requests
import streamlit as st

BASE = "https://api.football-data.org/v4"

@st.cache_data(ttl=300)  # remember the result for 5 minutes
def get_standings(league="PL"):
    r = requests.get(
        f"{BASE}/competitions/{league}/standings",
        headers={"X-Auth-Token": st.secrets["API_KEY"]},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["standings"][0]["table"]