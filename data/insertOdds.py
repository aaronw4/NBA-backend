import sqlite3
import requests
from bs4 import BeautifulSoup
from changeName import changeName

conn = sqlite3.connect('NBA.db')
cursor = conn.cursor()
# for day in range(1, 17):
season = "2020/2021"
year = 2021
month = 5
day = 10

if month < 10:
    month_db = f'0{month}'
else:
    month_db = month
if day < 10:
    day_db = f'0{day}'
else:
    day_db = day
date = f'{year}{month_db}{day_db}'
date_db = f'{year}-{month_db}-{day_db}'

#Check if date is already entered
cursor.execute('SELECT date FROM odds WHERE date=?', (date_db,))
data = cursor.fetchone()
if data is not None:
    print('Data from date already entered.')
    exit()

address = "https://classic.sportsbookreview.com"
date_extension_odds = f"/betting-odds/nba-basketball/?date={date}"
date_extension_totals = f"/betting-odds/nba-basketball/totals/?date={date}"
USER_SETTINGS = "bbuserid=10017271; bbpassword=7274d03eb3521d19e02cd7871f6b345c; bb_userid=10017271; bb_password=7274d03eb3521d19e02cd7871f6b345c; sbrSession=aaronw4"
headers={
    "cookie" : USER_SETTINGS,
    "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
}

TEAMS_LIST = []
SPREADS_LIST = []
ODDS_LIST = []
OPENING_ODDS_LIST = []
OPENING_SPREAD_LIST = []
OPENING_TOTAL_LIST = []
TOTALS_LIST = []
RESULTS_DATA = []

html_data = requests.get(
    address + date_extension_odds,
    headers=headers
)

soup = BeautifulSoup(html_data.text, 'lxml')
# Create list of all team names
for teams in soup.find_all('span', class_='team-name'):
    city = teams.text
    if city[0] == "(":
        city = city.split(')')[1][1:]
    name = changeName(city)
    TEAMS_LIST.append(name)

# Create list of opening lines
for opening in soup.find_all('div', class_='eventLine-opener'):
    opening_lines = opening.text.split()
    if len(opening_lines) > 2:
        opening_spread1 = opening_lines[0]
        opening_spread1 = opening_spread1.replace('\u00BD', '.5')
        opening_odds1 = opening_lines[1][:4]
        opening_spread2 = opening_lines[1][4:]
        opening_spread2 = opening_spread2.replace('\u00BD', '.5')
        opening_odds2 = opening_lines[2]
    elif len(opening_lines) == 1:
        opening_spread1 = '0'
        opening_spread2 = '0'
        opening_odds1 = opening_lines[0][2:6]
        opening_odds2 = opening_lines[0][8:]
    else:
        opening_spread1 = ''
        opening_spread2 = ''
        opening_odds1 = ''
        opening_odds2 = ''
    OPENING_SPREAD_LIST.append(opening_spread1)
    OPENING_SPREAD_LIST.append(opening_spread2)
    OPENING_ODDS_LIST.append(opening_odds1)
    OPENING_ODDS_LIST.append(opening_odds2)

# Create list of game lines
for lines in soup.find_all('div', rel='1096'):
    game_lines = lines.find_all('b')
    if len(game_lines) == 0:
        continue
    game_line1 = game_lines[0].text
    game_line2 = game_lines[1].text
    spread1 = game_line1[:-5]
    spread1 = spread1.replace('\u00BD', '.5')
    if spread1 == 'P':
        spread1 = '0'
    spread2 = game_line2[:-5]
    spread2 = spread2.replace('\u00BD', '.5')
    if spread2 == 'P':
        spread2 = '0'
    odds1 = game_line1[-4:]
    odds2 = game_line2[-4:]
    SPREADS_LIST.append(spread1)
    SPREADS_LIST.append(spread2)
    ODDS_LIST.append(odds1)
    ODDS_LIST.append(odds2)

# Collect totals lines
html_data = requests.get(
    address + date_extension_totals,
    headers=headers
)
soup = BeautifulSoup(html_data.text, 'lxml')

for opening in soup.find_all('div', class_='eventLine-opener'):
    opening_lines = opening.text.split()
    if len(opening_lines) > 2:
        opening_total1 = opening_lines[0]
        opening_total1 = opening_total1.replace('\u00BD', '.5')
        opening_total2 = opening_lines[1]
        opening_total2 = opening_total2.replace('\u00BD', '.5')
    elif len(opening_lines) == 1:
        opening_total1 = '0'
        opening_total2 = '0'
    else:
        opening_total1 = ''
        opening_total2 = ''
    OPENING_TOTAL_LIST.append(opening_total1)
    OPENING_TOTAL_LIST.append(opening_total2)

for lines in soup.find_all('div', rel='1096'):
    total_lines = lines.find_all('b')
    if len(total_lines) == 0:
        continue
    total_line1 = total_lines[0].text
    total_line2 = total_lines[1].text
    total1 = total_line1[:-5]
    total1 = total1.replace('\u00BD', '.5')
    total2 = total_line2[:-5]
    total2 = total2.replace('\u00BD', '.5')
    TOTALS_LIST.append(total1)
    TOTALS_LIST.append(total2)

# Create object with data
for i in range(0, len(TEAMS_LIST), 2):
    team_stats = []
    if SPREADS_LIST[i] == '':
        continue
    team_stats.append(season)
    team_stats.append(date_db)
    team_stats.append(TEAMS_LIST[i])
    team_stats.append(TEAMS_LIST[i+1])
    team_stats.append(OPENING_SPREAD_LIST[i])
    team_stats.append(OPENING_SPREAD_LIST[i+1])
    team_stats.append(OPENING_ODDS_LIST[i])
    team_stats.append(OPENING_ODDS_LIST[i+1])
    team_stats.append(OPENING_TOTAL_LIST[i])
    team_stats.append(SPREADS_LIST[i])
    team_stats.append(SPREADS_LIST[i+1])
    team_stats.append(ODDS_LIST[i])
    team_stats.append(ODDS_LIST[i+1])
    team_stats.append(TOTALS_LIST[i])

    sql = '''INSERT INTO odds(
        season, date, team_away, team_home, 
        spread_open_away, spread_open_home, 
        spreadOdds_open_away, spreadOdds_open_home, 
        total_open, spread_away, spread_home, 
        spreadOdds_away, spreadOdds_home, total)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    '''
    cursor.execute(sql, tuple(team_stats))
    conn.commit()
    # print(team_stats)
    print(f'Data entered for {TEAMS_LIST[i]} vs {TEAMS_LIST[i+1]}')