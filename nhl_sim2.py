import streamlit as st
import numpy as np

# 2025 Round 1 matchups
round1 = [
    ("Toronto Maple Leafs", "Ottawa Senators"),
    ("Tampa Bay Lightning", "Florida Panthers"),
    ("Washington Capitals", "Montreal Canadiens"),
    ("Carolina Hurricanes", "New Jersey Devils"),
    ("Winnipeg Jets", "St. Louis Blues"),
    ("Dallas Stars", "Colorado Avalanche"),
    ("Vegas Golden Knights", "Minnesota Wild"),
    ("Los Angeles Kings", "Edmonton Oilers"),
]

# Dummy Elo ratings (adjust if you want)
elos = {team: 1550 for a, b in round1 for team in (a, b)}
elos.update({
    "Dallas Stars": 1580,
    "Florida Panthers": 1575,
    "Edmonton Oilers": 1570,
    "Toronto Maple Leafs": 1560,
    "Winnipeg Jets": 1590
})

def win_prob(team1, team2):
    e1, e2 = elos[team1], elos[team2]
    return 1 / (1 + 10 ** ((e2 - e1) / 400))

def simulate_series(t1, t2):
    p = win_prob(t1, t2)
    wins = {t1: 0, t2: 0}
    while max(wins.values()) < 4:
        winner = t1 if np.random.rand() < p else t2
        wins[winner] += 1
    return max(wins, key=wins.get)

def run_full_bracket():
    winners_r1 = [simulate_series(a, b) for a, b in round1]
    # Semis: pair by index
    winners_r2 = [
        simulate_series(winners_r1[0], winners_r1[1]),
        simulate_series(winners_r1[2], winners_r1[3]),
        simulate_series(winners_r1[4], winners_r1[5]),
        simulate_series(winners_r1[6], winners_r1[7]),
    ]
    # Finals
    finals = [
        simulate_series(winners_r2[0], winners_r2[1]),
        simulate_series(winners_r2[2], winners_r2[3])
    ]
    champion = simulate_series(finals[0], finals[1])
    return winners_r1, winners_r2, finals, champion

# Streamlit UI
st.title("NHL 2025 Bracket Simulator 🏒")
if st.button("Run One Full Playoff Bracket"):
    r1, r2, r3, champ = run_full_bracket()
    st.subheader("Round 1 Winners:")
    for w in r1: st.write(f"- {w}")
    st.subheader("Semifinals Winners:")
    for w in r2: st.write(f"- {w}")
    st.subheader("Conference Finals Winners:")
    for w in r3: st.write(f"- {w}")
    st.markdown(f"## 🏆 Champion: **{champ}**")
