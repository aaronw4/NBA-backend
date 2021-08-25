import sqlite3

def seasonLeagueAveLoc(location):
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
        SELECT stats.date,         
        avg(CASE WHEN stats.overtime = "no" THEN stats.points ELSE NULL END) OVER (ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as points, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fg ELSE NULL END) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as fg, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fga ELSE NULL END) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as fga, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.tov ELSE NULL END) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as tov, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.fta ELSE NULL END) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as fta, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.drb ELSE NULL END) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as drb, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.orb ELSE NULL END) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as orb, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.three ELSE NULL END) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as three, 
        avg(CASE WHEN stats.overtime = "no" THEN stats.three_a ELSE NULL END) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as three_a
        FROM stats
        WHERE stats.home_away = :location
        ''', ({'location':location})
    )

    results = cursor.fetchall()

    new_result = {}
    for row in results:
        date = row['date']
        result_keys = list(row.keys())
        result_keys = result_keys[1:]

        if date not in new_result:
            new_result[row['date']] = {}
        new_dict = {x:row[x] for x in result_keys}            
        new_result[row['date']] = new_dict
        
    return new_result