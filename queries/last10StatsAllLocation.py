import sqlite3

def last10StatsAllLocation(location):
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
        avg(stats.points) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as points, 
        avg(stats.points_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as points_opp, 
        avg(stats.fg) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as fg, 
        avg(stats.fg_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as fg_opp, 
        avg(stats.fga) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as fga, 
        avg(stats.fga_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as fga_opp, 
        avg(stats.tov) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as tov, 
        avg(stats.tov_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as tov_opp, 
        avg(stats.fta) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as fta, 
        avg(stats.fta_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as fta_opp, 
        avg(stats.drb) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as drb, 
        avg(stats.drb_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as drb_opp, 
        avg(stats.orb) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as orb, 
        avg(stats.orb_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as orb_opp, 
        avg(stats.three) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as three, 
        avg(stats.three_opp) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as three_opp, 
        avg(stats.three_a) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as three_a, 
        avg(stats.three_opp_a) OVER(PARTITION BY teams.name ORDER BY stats.date ROWS BETWEEN 10 PRECEDING and 1 PRECEDING) as three_a_opp
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
