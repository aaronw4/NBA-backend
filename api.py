import flask
from flask import request, jsonify
from flask_cors import CORS
from queries.seasonStatsAll import seasonStatsAll
from queries.last10StatsAll import last10StatsAll
from queries.seasonStats import seasonStats
from queries.last10Stats import last10Stats
from queries.last10StatsLocation import last10StatsLocation
from queries.seasonStatsLocation import seasonStatsLocation
from queries.last10StatsAllLocation import last10StatsAllLocation
from queries.seasonStatsAllLocation import seasonStatsAllLocation
from queries.oddsAll import oddsAll
from queries.seasonLeagueAve import seasonLeagueAve
from queries.seasonLeagueAveLoc import seasonLeagueAveLoc
from queries.scoresAll import scoresAll

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)

@app.route('/', methods=['GET'])
def home():
    return '<p>Server is alive!</p>'

@app.route('/api/nba-season/all', methods=['GET'])
def season_all():
    return jsonify(seasonStatsAll())

# date should have format: '2021-05-01'
@app.route('/api/nba-season-location/all', methods=['GET'])
def season_location_all():
    if 'location' in request.args:
        location = request.args['location']
    else:
        return "Error: No location field provided. Please specify home or away"

    return jsonify(seasonStatsAllLocation(location))

@app.route('/api/nba-last10/all', methods=['GET'])
def last10_all():
    return jsonify(last10StatsAll())

@app.route('/api/nba-last10-location/all', methods=['GET'])
def last10_location_all():
    if 'location' in request.args:
        location = request.args['location']
    else:
        return "Error: No location field provided. Please specify home or away"

    return jsonify(last10StatsAllLocation(location))

@app.route('/api/nba-season', methods=['GET'])
def season_date():
    if 'date' in request.args:
        date = request.args['date']
    else:
        return "Error: No date field provided. Please specify an date."

    return jsonify(seasonStats(date))

# &location=home or &location=away
@app.route('/api/nba-season-location', methods=['GET'])
def season_date_home():
    if 'date' in request.args:
        date = request.args['date']
    else:
        return "Error: No date field provided. Please specify an date."

    if 'location' in request.args:
        location = request.args['location']
    else:
        return "Error: No location field provided. Please specify home or away"

    return jsonify(seasonStatsLocation(date, location))
    
@app.route('/api/nba-last10', methods=['GET'])
def last10_date():
    if 'date' in request.args:
        date = request.args['date']
    else:
        return "Error: No date field provided. Please specify an date."

    return jsonify(last10Stats(date))

@app.route('/api/nba-last10-location', methods=['GET'])
def last10_date_home():
    if 'date' in request.args:
        date = request.args['date']
    else:
        return "Error: No date field provided. Please specify an date."

    if 'location' in request.args:
        location = request.args['location']
    else:
        return "Error: No location field provided. Please specify home or away"

    return jsonify(last10StatsLocation(date, location))

@app.route('/api/nba-odds-all', methods=['GET'])
def odds_All():
    return jsonify(oddsAll())

@app.route('/api/nba-season-league-avg', methods=['GET'])
def ave_All():
    return jsonify(seasonLeagueAve())

@app.route('/api/nba-season-league-avg-location', methods=['GET'])
def ave_All_loc():
    if 'location' in request.args:
        location = request.args['location']
    else:
        return "Error: No location field provided. Please specify home or away"

    return jsonify(seasonLeagueAveLoc(location))

@app.route('/api/nba-scores-all', methods=['GET'])
def scores_All():
    return jsonify(scoresAll())

app.run()
