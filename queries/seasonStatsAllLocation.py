import sqlite3

def seasonStatsAllLocation(location):
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
        SELECT stats.date, teams.name,  
        avg(CASE WHEN stats.overtime = "no" THEN stats.points ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as points, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.points_opp ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as points_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fg ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as fg, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fg_opp ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as fg_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fga ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as fga, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fga_opp ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as fga_opp,
        avg(CASE WHEN stats.overtime = "no" THEN stats.tov ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as tov, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.tov_opp ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as tov_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fta ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as fta, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fta_opp ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as fta_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.drb ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as drb, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.drb_opp ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as drb_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.orb ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as orb, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.orb_opp ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as orb_opp,
        avg(CASE WHEN stats.overtime = "no" THEN stats.three ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as three, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.three_opp ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as three_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.three_a ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as three_a, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.three_opp_a ELSE NULL END) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN UNBOUNDED PRECEDING and 1 PRECEDING) as three_a_opp
        FROM teams INNER JOIN stats ON teams.id = stats.team_id
        WHERE stats.home_away = :location
        ''', ({"location":location})
    )

    results = cursor.fetchall()
    
    new_result = {}
    for row in results:
        date = row['date']
        result_keys = list(row.keys())
        result_keys = result_keys[2:]

        if date not in new_result:
            new_result[row['date']] = {}
        new_dict = {x:row[x] for x in result_keys}            
        new_result[row['date']][row['name']] = new_dict
        
    return new_result
