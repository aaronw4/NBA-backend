# NBA-backend
The is a python back-end created with Flask. The database was populated by using Beautiful Soup to scrape websites to collect NBA statistics and sports betting lines for the 2020/2021 season.

## Endpoints
Base URL: 

Method | Endpoint | Description | Query String
-------|----------|-------------|-------------
GET | /api/nba-scores-all | Returns scores for every game | 
GET | /api/nba-odds-all | Returns betting lines for every game | 
GET | /api/nba-odds-all | Returns average teams stats for entire season | 
GET | /api/nba-season-league-avg | Returns leagues average stats for entire season | 
GET | /api/nba-season-league-avg-location | Returns leagues average home/away stats for entire season | location
GET | /api/nba-season | Returns average teams stats for entire season at a given date | date
GET | /api/nba-season-location | Returns average teams home/away stats for entire season at a given date | date and location
GET | /api/nba-last10 | Returns average teams stats for the last ten games at a given date | date
GET | /api/nba-last10-location | Returns average teams home/away stats for the last ten home/away games at a given date | date and location
GET | /api/nba-season/all | Returns average team stats for all prior games for every game | 
GET | /api/nba-season-location/all | Returns average team home/away stats for all prior home/away games for every game | location
GET | /api/nba-last10/all | Returns average team stats covering the last ten games for every game | 
GET | /api/nba-last10-location/all | Returns average team home/away stats covering the last ten home/away games for every game | location


Query String | Key=Value Pairs
-------------|----------------
location | ?location=home or ?location=away
date | ?date='2021-05-01'