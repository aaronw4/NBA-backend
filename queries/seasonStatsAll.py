import sqlite3
import json

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect('NBA.db')
conn.row_factory = dict_factory
cursor = conn.cursor()

cursor.execute(
    '''
    SELECT teams.name, stats.date, 
    avg(stats.points) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as points, 
    avg(stats.points_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as points_opp, 
    avg(stats.fg) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as fg, 
    avg(stats.fg_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as fg_opp, 
    avg(stats.fga) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as fga, 
    avg(stats.fga_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as fga_opp,
    avg(stats.tov) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as tov, 
    avg(stats.tov_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as tov_opp, 
    avg(stats.fta) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as fta, 
    avg(stats.fta_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as fta_opp, 
    avg(stats.drb) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as drb, 
    avg(stats.drb_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as drb_opp, 
    avg(stats.orb) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as orb, 
    avg(stats.orb_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as orb_opp,
    avg(stats.three) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as three, 
    avg(stats.three_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as three_opp, 
    avg(stats.three_a) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as three_a, 
    avg(stats.three_opp_a) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and CURRENT ROW) as three_a_opp
    FROM teams INNER JOIN stats ON teams.id = stats.team_id
    '''
)

result = cursor.fetchall()
data = json.dumps(result)

print(data)