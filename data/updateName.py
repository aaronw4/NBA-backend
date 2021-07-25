from os import name
import sqlite3
from sqlite3.dbapi2 import Cursor
from changeName import changeName

conn = sqlite3.connect('NBA.db')
cursor = conn.cursor()

for id in range (1, 712):
    if id == 163:
        continue

    cursor.execute(
        '''
            SELECT team_away FROM odds WHERE id = :id
        ''', ({'id':id})
    )
    result = cursor.fetchone()
    name_away = changeName(result[0])

    cursor.execute(
        '''
            SELECT team_home FROM odds WHERE id = :id
        ''', ({'id':id})
    )
    result2 = cursor.fetchone()
    name_home = changeName(result2[0])

    cursor.execute(
        '''
            UPDATE odds
            SET team_away = :name_away, team_home = :name_home
            WHERE id = :id
        ''', ({'name_away':name_away, 'name_home':name_home ,'id':id})
    )
    conn.commit()

    # print(result[0], name_away)
    # print(result2[0], name_home)