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
# day = 22

for day in range(1, 17):
    if month < 10:
        month_db = f'0{month}'
    else:
        month_db = month
    if day < 10:
        day_db = f'0{day}'
    else:
        day_db = day
    date_db = f'{year}-{month_db}-{day_db}'

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
            
        #Collect ot games
        table1 = soup_games.find_all('tfoot')
        if len(table1) >= 18:
            id1 = getID(team1_name)
            id2 = getID(team2_name)

            cursor.execute( '''
                UPDATE stats
                SET overtime = "yes"
                WHERE date = :date AND team_id = :id
            ''', ({'date':date_db, 'id':id1}))

            cursor.execute( '''
                UPDATE stats
                SET overtime = "yes"
                WHERE date = :date AND team_id = :id
            ''', ({'date':date_db, 'id':id2}))

            conn.commit()
            print(date_db, team1_name, team2_name)