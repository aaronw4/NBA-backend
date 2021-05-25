import sqlite3
import json

date = "2021-04-01"

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect('NBA.db')
conn.row_factory = dict_factory
cursor = conn.cursor()

cursor.execute(
    '''SELECT teams.name, avg(stats.points) as points, avg(stats.points_opp) as points_opp, 
    avg(stats.fg) as fg, avg(stats.fg_opp) as fg_opp, avg(stats.fga) as fga, avg(stats.fga_opp) as fga_opp,
    avg(stats.tov) as tov, avg(stats.tov_opp) as tov_opp, avg(stats.fta) as fta, avg(stats.fta_opp) as fta_opp, 
    avg(stats.drb) as drb, avg(stats.drb_opp) as drb_opp, avg(stats.orb) as orb, avg(stats.orb_opp) as orb_opp,
    avg(stats.three) as three, avg(stats.three_opp) as three_opp, avg(stats.three_a) as three_a, avg(stats.three_opp_a) as three_a_opp
    FROM teams INNER JOIN stats ON teams.id = stats.team_id
    WHERE stats.date <:date GROUP BY teams.name''', ({"date":date})
)

result = cursor.fetchall()
data = json.dumps(result)

print(data)