import sqlite3
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect('NBA.db')
cursor = conn.cursor()

def getID(name):
    cursor.execute('SELECT * FROM teams WHERE name=:name', {'name': name})
    team = cursor.fetchone()
    return team[0]

season = "2020/2021"
year = 2021
month = 5
day = 1
date = f'{month}-{day}-{year}'

#Check if date is already entered
cursor.execute('SELECT date FROM stats WHERE date=?', (date,))
data = cursor.fetchone()
if data is not None:
    print('Data from date already entered.')
    exit()

address = "https://www.basketball-reference.com"
date_extension = f"/boxscores/?month={month}&day={day}&year={year}"
headers={
    "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
}
game_links = []

#build list of all game links
link_data = requests.get(address + date_extension, headers=headers)
soup_links = BeautifulSoup(link_data.text, 'lxml')
for links in soup_links.find_all('p', class_="links"):
    link = links.find('a')
    game_links.append(link['href'])

#Loop through all links and collect data 
for i in range(0, len(game_links)):
    game_data = requests.get(address + game_links[i], headers=headers)
    soup_games = BeautifulSoup(game_data.text, 'lxml')

    team1_stats = []
    team2_stats = []
    opponent = 8

    #Get team names
    scorebox = soup_games.find('div', class_='scorebox')
    teams = scorebox.find_all('strong')
    team1_name = teams[0].find('a').text
    team1_name = team1_name.split(' ')[-1:][0]
    team2_name = teams[1].find('a').text
    team2_name = team2_name.split(' ')[-1:][0]
    if team1_name == 'Blazers':
        team1_name = 'Trail Blazers'
    if team2_name == 'Blazers':
        team2_name = 'Trail Blazers'

    #Collect game stats
    team1_stats.append(season)
    team1_stats.append(date,)
    table1 = soup_games.find_all('tfoot')
    if len(table1) == 18:
        opponent = 10
    team1_pts = table1[0].find('td', attrs={'data-stat': 'pts'}).text
    team1_stats.append(int(team1_pts))
    team1_pts_opp = table1[opponent].find('td', attrs={'data-stat': 'pts'}).text
    team1_stats.append(int(team1_pts_opp))
    team1_fg = table1[0].find('td', attrs={'data-stat': 'fg'}).text
    team1_stats.append(int(team1_fg))
    team1_fg_opp = table1[opponent].find('td', attrs={'data-stat': 'fg'}).text
    team1_stats.append(int(team1_fg_opp))
    team1_fga = table1[0].find('td', attrs={'data-stat': 'fga'}).text
    team1_stats.append(int(team1_fga))
    team1_fga_opp = table1[opponent].find('td', attrs={'data-stat': 'fga'}).text
    team1_stats.append(int(team1_fga_opp))
    team1_to = table1[0].find('td', attrs={'data-stat': 'tov'}).text
    team1_stats.append(int(team1_to))
    team1_to_opp = table1[opponent].find('td', attrs={'data-stat': 'tov'}).text
    team1_stats.append(int(team1_to_opp))
    team1_fta = table1[0].find('td', attrs={'data-stat': 'fta'}).text
    team1_stats.append(int(team1_fta))
    team1_fta_opp = table1[opponent].find('td', attrs={'data-stat': 'fta'}).text
    team1_stats.append(int(team1_fta_opp))
    team1_drb = table1[0].find('td', attrs={'data-stat': 'drb'}).text
    team1_stats.append(int(team1_drb))
    team1_drb_opp = table1[opponent].find('td', attrs={'data-stat': 'drb'}).text
    team1_stats.append(int(team1_drb_opp))
    team1_orb = table1[0].find('td', attrs={'data-stat': 'orb'}).text
    team1_stats.append(int(team1_orb))
    team1_orb_opp = table1[opponent].find('td', attrs={'data-stat': 'orb'}).text
    team1_stats.append(int(team1_orb_opp))
    team1_3p = table1[0].find('td', attrs={'data-stat': 'fg3'}).text
    team1_stats.append(int(team1_3p))
    team1_3p_opp = table1[opponent].find('td', attrs={'data-stat': 'fg3'}).text
    team1_stats.append(int(team1_3p_opp))
    team1_3pa = table1[0].find('td', attrs={'data-stat': 'fg3a'}).text
    team1_stats.append(int(team1_3pa))
    team1_3pa_opp = table1[opponent].find('td', attrs={'data-stat': 'fg3a'}).text
    team1_stats.append(int(team1_3pa_opp))
    team1_stats.append(getID(team1_name))

    team2_stats.append(season)
    team2_stats.append(date,)
    team2_stats.append(int(team1_pts_opp))
    team2_stats.append(int(team1_pts))
    team2_stats.append(int(team1_fg_opp))
    team2_stats.append(int(team1_fg))
    team2_stats.append(int(team1_fga_opp))
    team2_stats.append(int(team1_fga))
    team2_stats.append(int(team1_to_opp))
    team2_stats.append(int(team1_to))
    team2_stats.append(int(team1_fta_opp))
    team2_stats.append(int(team1_fta))
    team2_stats.append(int(team1_drb_opp))
    team2_stats.append(int(team1_drb))
    team2_stats.append(int(team1_orb_opp))
    team2_stats.append(int(team1_orb))
    team2_stats.append(int(team1_3p_opp))
    team2_stats.append(int(team1_3p))
    team2_stats.append(int(team1_3pa_opp))
    team2_stats.append(int(team1_3pa))
    team2_stats.append(getID(team2_name))

    sql = '''INSERT INTO stats(
            season, date, 
            points, points_opp, 
            fg, fg_opp, 
            fga, fga_opp, 
            tov, tov_opp, 
            fta, fta_opp, 
            drb, drb_opp, 
            orb, orb_opp, 
            three, three_opp, 
            three_a, three_opp_a, 
            team_id) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

    cursor.execute(sql, tuple(team1_stats))
    cursor.execute(sql, tuple(team2_stats))
    conn.commit()
    print(f'Data entered for {team1_name} vs {team2_name}')