# calculations.py
# Purpose: all the maths for "what does each team need?"
# This file has NO Streamlit display code, only calculations.

TOTAL_GAMES = 38          # games per team in a Premier League season
RELEGATION_LINE = 17      # 17th place is the last safe position


# ---------- Building block 1: one team's numbers ----------
def games_left(row):
    """Return how many games this team still has to play."""
    return TOTAL_GAMES - row['playedGames']

def max_points(row):
    """Return the most points this team can still finish with."""
    return games_left(row)*3 + row['points']


# ---------- Building block 2: reference points in the table ----------
def leader_points(table):
    """Return the current points of the team in 1st place."""
    point = []
    for row in table:
        team_point = row['points']
        point.append(team_point)
    return max(point) 


def safety_points(table):
    """Return the current points of the team in 17th place."""
    return table[RELEGATION_LINE - 1]['points']

def points_behind_leader(row,table):
    """How many points to leader"""
    diff = leader_points(table) - row['points']
    if diff == 0:
        return '-'
    else: return diff

def points_above_safety(row,table):
    """How many points to safety"""
    return row['points'] - safety_points(table)
# ---------- Building block 3: the status of one team ----------
def best_rival_max(row, table):
    """Highest max_points among all the OTHER teams."""
    return max(max_points(r) for r in table
               if r['team']['name'] != row['team']['name'])


def title_status(row, table):
    """Where does this team stand in the title race?"""
    if row['points'] > best_rival_max(row, table):
        return 'Champion'
    if max_points(row) < leader_points(table):
        return 'Out of title race'
    return 'Title race'


def survival_status(row, table):
    """Where does this team stand in the fight against relegation?"""
    if max_points(row) < safety_points(table):
        return 'Relegated'
    bottom_three_max = max(max_points(r) for r in table
                           if r['position'] > RELEGATION_LINE)
    if row['points'] > bottom_three_max:
        return 'Safe'
    return 'Not yet safe'


def add_statuses(table):
    """Add a 'title' and a 'survival' label to each row."""
    for row in table:
        row['title'] = title_status(row, table)
        row['survival'] = survival_status(row, table)
    return table


# ---------- Test area: only runs with `python calculations.py` ----------
if __name__ == "__main__":
    from api import get_standings

    table = get_standings()
    #for row in table:
       #print(row["team"]["name"], games_left(row), max_points(row),'Status: ',get_status(row,table))
    #print(f'The leader has {leader_points(table)} points now.') 
    #print(f'The safety point is {safety_points(table)} points now.')
    import copy
    fake = copy.deepcopy(table)
    for r in fake:
        r["playedGames"] = 37
    for r in add_statuses(fake):
        print(r["position"], r["team"]["name"], r["title"], r["survival"])