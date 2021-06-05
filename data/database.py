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
    [tov] integer NOT NULL,
    [tov_opp] integer NOT NULL,
    [fta] integer NOT NULL,
    [fta_opp] integer NOT NULL,
    [drb] integer NOT NULL,
    [drb_opp] integer NOT NULL, 
    [orb] integer NOT NULL,
    [orb_opp] integer NOT NULL,
    [three] integer NOT NULL,
    [three_opp] integer NOT NULL,
    [three_a] integer NOT NULL,
    [three_opp_a] integer NOT NULL,
    [team_id] integer NOT NULL,
    FOREIGN KEY ("team_id") REFERENCES teams (id)
) """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS odds (
    [id] integer PRIMARY KEY,
    [season] text NOT NULL,
    [date] text NOT NULL,
    [team_away] text NOT NULL,
    [team_home] text NOT NULL,
    [spread_open_away] text NOT NULL,
    [spread_open_home] text NOT NULL, 
    [spreadOdds_open_away] text NOT NULL, 
    [spreadOdds_open_home] text NOT NULL, 
    [total_open] text NOT NULL, 
    [spread_away] text NOT NULL,
    [spread_home] text NOT NULL, 
    [spreadOdds_away] text NOT NULL, 
    [spreadOdds_home] text NOT NULL, 
    [total] text NOT NULL
)""")

conn.commit()