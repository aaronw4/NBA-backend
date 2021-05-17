import sqlite3

conn = sqlite3.connect('NBA.db')
cursor = conn.cursor()

def getID(name):
    cursor.execute('SELECT * FROM teams WHERE name=:name', {'name': name})
    team = cursor.fetchone()
    return team[0]

teamID = getID('Bulls')

print(teamID)