import sqlite3

conn = sqlite3.connect('NBA.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS teams (
    id integer PRIMARY KEY,
    city text NOT NULL,
    name text NOT NULL
) """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS stats (
    [id] integer PRIMARY KEY,
    [season] text NOT NULL,
    [date] text NOT NULL,
    [points] integer NOT NULL,
    [points_opp] integer NOT NULL,
    [fg] integer NOT NULL,
    [fg_opp] integer NOT NULL,
    [fga] integer NOT NULL,
    [fga_opp] integer NOT NULL,
    [to] integer NOT NULL,
    [to_opp] integer NOT NULL,
    [fta] integer NOT NULL,
    [fta_opp] integer NOT NULL,
    [drb] integer NOT NULL,
    [drb_opp] integer NOT NULL, 
    [orb] integer NOT NULL,
    [orb_opp] integer NOT NULL,
    [three] integer NOT NULL,
    [three_opp] integer NOT NULL,
    [team_id] integer NOT NULL,
    FOREIGN KEY ("team_id") REFERENCES teams (id)
) """)

conn.commit()