import sqlite3

conn = sqlite3.connect('NBA.db')
cursor = conn.cursor()

cursor.execute(
    '''SELECT teams.name, avg(stats.points), avg(stats.points_opp), 
    avg(stats.fg), avg(stats.fg_opp), avg(stats.fga), avg(stats.fga_opp),
    avg(stats.tov), avg(stats.tov_opp), avg(stats.fta), avg(stats.fta_opp), 
    avg(stats.drb), avg(stats.drb_opp), avg(stats.orb), avg(stats.orb_opp),
    avg(stats.three), avg(stats.three_opp), avg(stats.three_a), avg(stats.three_opp_a)
    FROM teams INNER JOIN stats ON teams.id = stats.team_id
    GROUP BY teams.name'''
)

result = cursor.fetchall()
print(result)