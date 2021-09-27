# NBA-backend
The is a python back-end created with Flask. The database was populated by using Beautiful Soup to scrape websites to collect NBA statistics and sports betting lines for the 2020/2021 season. This backend is deployed on Heroku and AWS.

## Endpoints
Heroku Base URL: https://arw-nba-backend.herokuapp.com/  

AWS Base URL: http://nba-backend.eba-mc4zbfx6.us-west-1.elasticbeanstalk.com/

Method | Endpoint | Description | Query String
-------|----------|-------------|-------------
GET | /api/nba-scores-all | Returns points scored for each game | 
GET | /api/nba-odds-all | Returns betting lines for every game | 
GET | /api/nba-season-league-avg | Returns leagues average stats for all prior games for every game | 
GET | /api/nba-season-league-avg-location | Returns leagues average home/away stats for all prior games for every game | location
GET | /api/nba-season | Returns average teams stats for entire season at a given date | date
GET | /api/nba-season-location | Returns average teams home/away stats for entire season at a given date | date and location
GET | /api/nba-last10 | Returns average teams stats from the last ten games at a given date | date
GET | /api/nba-last10-location | Returns average teams home/away stats from the last ten home/away games at a given date | date and location
GET | /api/nba-season/all | Returns average team stats from all prior games for every game | 
GET | /api/nba-season-location/all | Returns average team home/away stats from all prior home/away games for every game | location
GET | /api/nba-last10/all | Returns average team stats covering the last ten games for every game | 
GET | /api/nba-last10-location/all | Returns average team home/away stats covering the last ten home/away games for every game | location


Query String | Key=Value Pairs
-------------|----------------
location | ?location=home or ?location=away
date | ?date=2021-05-01