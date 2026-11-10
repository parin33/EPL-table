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
def get_status(row, table):
    """Return a short label for one team, e.g. 'Champion'."""
    # --- Prepare the numbers you'll compare (compute once, reuse) ---
    my_points = row['points']               
    my_max = max_points(row)                
    rival_maxes = []                      
    for r in table:
        if r['team']['name'] != row['team']['name']:                         
            rival_maxes.append(max_points(r))
    rival_best_max = max(rival_maxes) 
    leader = leader_points(table)
    safety = safety_points(table)


    if my_points > rival_best_max:
        return f'CHAMPION'
    if my_max < safety:
            return f'Relegated'
    relegation_zone = [max_points(row) for row in table if row['position'] in (18,19,20)]
    if my_points > max(relegation_zone):
        return 'Safe'
    if my_max < leader:
        return f'out of the title race'
    else: return "In progress"



def add_statuses(table):
    """Return a list of statuses, one per team, in table order."""
    for row in table:
        row['status'] = get_status(row,table)
    return table


# ---------- Test area: only runs with `python calculations.py` ----------
if __name__ == "__main__":
    from api import get_standings

    table = get_standings()
    for row in table:
       print(row["team"]["name"], games_left(row), max_points(row),'Status: ',get_status(row,table))
    print(f'The leader has {leader_points(table)} points now.') 
    print(f'The safety point is {safety_points(table)} points now.')
