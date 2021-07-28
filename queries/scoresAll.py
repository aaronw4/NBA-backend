import sqlite3

def scoresAll():
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
        SELECT stats.date, teams.name, stats.points
        FROM teams INNER JOIN stats ON teams.id = stats.team_id
        '''
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
