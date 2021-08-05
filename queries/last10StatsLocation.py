import sqlite3

def last10StatsLocation(date, location):
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
        avg(CASE WHEN stats.overtime = "no" THEN stats.points ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as points, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.points_opp ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as points_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fg ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as fg, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fg_opp ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as fg_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fga ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as fga, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fga_opp ELSE NULL END OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as fga_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.tov ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as tov, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.tov_opp ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as tov_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fta ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as fta, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fta_opp ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as fta_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.drb ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as drb, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.drb_opp ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as drb_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.orb ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as orb, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.orb_opp ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as orb_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.three ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as three,  
        avg(CASE WHEN stats.overtime = "no" THEN stats.three_opp ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as three_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.three_a ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as three_a, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.three_opp_a ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 9 PRECEDING and CURRENT ROW)as three_a_opp
        FROM teams INNER JOIN stats ON teams.id = stats.team_id
        WHERE stats.date <:date AND stats.home_away = :location
        ''', ({"location":location, "date":date})
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

    return last10
