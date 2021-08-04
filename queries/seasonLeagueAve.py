import sqlite3

def seasonLeagueAve():
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
        avg(stats.points) OVER (ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as points, 
        avg(stats.fg) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as fg, 
        avg(stats.fga) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as fga, 
        avg(stats.tov) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as tov, 
        avg(stats.fta) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as fta, 
        avg(stats.drb) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as drb, 
        avg(stats.orb) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as orb, 
        avg(stats.three) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as three, 
        avg(stats.three_a) OVER(ORDER BY stats.date RANGE UNBOUNDED PRECEDING) as three_a
        FROM stats WHERE stats.overtime = "no"
        '''
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
