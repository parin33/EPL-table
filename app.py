import streamlit as st
from api import get_standings
from calculations import add_statuses, points_behind_leader, points_above_safety

st.set_page_config(page_title="EPL Dashboard", page_icon="⚽", layout="wide")

st.title("⚽ Premier League Dashboard")
st.caption("Data: football-data.org · refreshes every 5 minutes")

# ---------- Settings (edit these if the European spots change) ----------
ZONES = [
    (4, "rgba(46, 204, 113, 0.25)", "🟩 Champions League"),
    (6, "rgba(52, 152, 219, 0.25)", "🟦 Europa League"),
    (7, "rgba(241, 196, 15, 0.25)", "🟨 Conference League"),
]
RELEGATION_FROM = 18
RELEGATION_COLOR = "rgba(231, 76, 60, 0.30)"

# ---------- Load data ----------
try:
    table = get_standings()
except Exception as e:
    st.error(f"Couldn't load data: {e}")
    st.stop()

table = add_statuses(table)
# ---------- Helper: pick a row colour from league position ----------
def zone_color(pos):
    if pos >= RELEGATION_FROM:
        return RELEGATION_COLOR
    for last_pos, colour, _ in ZONES:
        if pos <= last_pos:
            return colour
    return "transparent"

# ---------- Build the HTML table ----------
headers = ["Pos", "Team", "P", "W", "D", "L", "GF", "GA", "GD", "Pts",
           "Behind", "Vs safety", "Status"]

head_html = "".join(f"<th>{h}</th>" for h in headers)

rows_html = ""
for r in table:
    cells = [
    r["position"], r["team"]["name"], r["playedGames"], r["won"],
    r["draw"], r["lost"], r["goalsFor"], r["goalsAgainst"],
    r["goalDifference"], r["points"],
    points_behind_leader(r, table),
    points_above_safety(r, table),
    r["status"],
]
    cells_html = "".join(f"<td>{c}</td>" for c in cells)
    rows_html += f'<tr style="background-color:{zone_color(r["position"])}">{cells_html}</tr>'

css = """
<style>
.epl-table { width: 100%; border-collapse: collapse; font-size: 16px; }
.epl-table th, .epl-table td {
    text-align: center;            /* centres every cell */
    padding: 10px 8px;
    border-bottom: 1px solid rgba(255,255,255,0.12);
}
.epl-table th { color: #00ff85; border-bottom: 2px solid #00ff85; }
</style>
"""

html = f'{css}<table class="epl-table"><thead><tr>{head_html}</tr></thead><tbody>{rows_html}</tbody></table>'
st.markdown(html, unsafe_allow_html=True)

# ---------- Legend ----------
st.write("")
legend = [label for _, _, label in ZONES] + ["🟥 Relegation"]
st.markdown(" &nbsp; ".join(legend))
st.caption("Qualification spots are approximate and can shift with cup results.")