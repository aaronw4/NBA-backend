import sqlite3
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect('NBA.db')
cursor = conn.cursor()

def getID(name):
    cursor.execute('SELECT * FROM teams WHERE name=:name', {'name': name})
    team = cursor.fetchone()
    return team[0]

# teamID = getID('Bulls')
season = "2020/2021"
year = 2020
month = 12
day = 22
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
    team1_stats.append(f'{month}-{day}-{year}')
    table1 = soup_games.find_all('tfoot')
    team1_pts = table1[0].find('td', attrs={'data-stat': 'pts'}).text
    team1_stats.append(int(team1_pts))
    team1_pts_opp = table1[8].find('td', attrs={'data-stat': 'pts'}).text
    team1_stats.append(int(team1_pts_opp))



    team2_stats.append(season)
    team2_stats.append(f'{month}-{day}-{year}')
    team2_stats.append(int(team1_pts_opp))
    team2_stats.append(int(team1_pts))

    # print()
    print(team1_stats)
    print(team2_stats)