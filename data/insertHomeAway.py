import sqlite3

conn = sqlite3.connect('NBA.db')
cursor = conn.cursor()

for id in range(1, 2161): 
    if id % 2 == 0:
        location = 'home'
    else:
        location = 'away'

    cursor.execute(
        '''UPDATE stats
        SET home_away = :location
        WHERE id = :id
        ''', ({'location':location, 'id':id})
    )
    conn.commit()
    # print(f'{id} is {location}')
