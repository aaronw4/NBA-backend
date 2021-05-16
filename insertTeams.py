import sqlite3

conn = sqlite3.connect('NBA.db')
cursor = conn.cursor()

teams = [
    (1, 'Atlanta', 'Hawks'),
    (2, 'Boston', 'Celtics'),
    (3, 'Charlotte', 'Hornets'),
    (4, 'Chicago', 'Bulls'),
    (5, 'Cleveland', 'Cavaliers'),
    (6, 'Detroit', 'Pistons'),
    (7, 'Indiana', 'Pacers'),
    (8, 'Miami', 'Heat'),
    (9, 'Milwaukee', 'Bucks'),
    (10, 'Brooklyn', 'Nets'),
    (11, 'New York', 'Knicks'),
    (12, 'Orlando', 'Magic'),
    (13, 'Philadelphia', '76ers'),
    (14, 'Toronto', 'Raptors'),
    (15, 'Washington', 'Wizards'),
    (16, 'Dallas', 'Mavericks'),
    (17, 'Denver', 'Nuggets'),
    (18, 'Golden State', 'Warriors'),
    (19, 'Houston', 'Rockets'),
    (20, 'Los Angeles', 'Clippers'),
    (21, 'Los Angeles', 'Lakers'),
    (22, 'Memphis', 'Grizzlies'),
    (23, 'Minnesota', 'Timberwolves'),
    (24, 'New Orleans', 'Pelicans'),
    (25, 'Oklahoma City', 'Thunder'),
    (26, 'Phoenix', 'Suns'),
    (27, 'Portland', 'Trail Blazers'),
    (28, 'Sacramento', 'Kings'),
    (29, 'San Antonio', 'Spurs'),
    (30, 'Utah', 'Jazz')
]

cursor.executemany('INSERT INTO teams VALUES(?,?,?)', teams)

conn.commit()