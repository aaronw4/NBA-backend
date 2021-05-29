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
    '''
    SELECT teams.name, stats.date, avg(stats.points) 
    OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW) as points
    FROM teams INNER JOIN stats ON teams.id = stats.team_id
    WHERE stats.date <:date
    ''', ({"date":date})
)

results = cursor.fetchall()
last10 = []
for index in range(len(results)):
    if index == len(results)-1:
        last10.append(results[index])
    elif results[index]['date'] < results[index+1]['date']:
        continue
    else:
        last10.append(results[index])
data = json.dumps(last10)

print(data)