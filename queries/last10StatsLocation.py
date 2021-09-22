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
        SELECT teams.name, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.points ELSE NULL END) as points, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.points_opp ELSE NULL END) as points_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fg ELSE NULL END) as fg, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fg_opp ELSE NULL END) as fg_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fga ELSE NULL END) as fga, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fga_opp ELSE NULL END) as fga_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.tov ELSE NULL END) as tov, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.tov_opp ELSE NULL END) as tov_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fta ELSE NULL END) as fta, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fta_opp ELSE NULL END) as fta_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.drb ELSE NULL END) as drb, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.drb_opp ELSE NULL END) as drb_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.orb ELSE NULL END) as orb, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.orb_opp ELSE NULL END) as orb_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.three ELSE NULL END) as three,  
        avg(CASE WHEN stats.overtime = "no" THEN stats.three_opp ELSE NULL END) as three_opp, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.three_a ELSE NULL END) as three_a, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.three_opp_a ELSE NULL END) as three_a_opp
        FROM teams INNER JOIN stats ON teams.id = stats.team_id
        WHERE stats.date <:date AND stats.home_away = :location
        GROUP BY teams.name''', ({"location":location, "date":date})
    )

    results = cursor.fetchall()

    new_result = {}
    for row in results:
        name = row['name']
        result_keys = list(row.keys())
        result_keys = result_keys[1:]

        new_dict = {x:row[x] for x in result_keys}
        new_result[name] = new_dict

    return new_result
