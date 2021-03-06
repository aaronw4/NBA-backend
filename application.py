from flask import Flask, request, jsonify
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

# date should have format: '2021-05-01'
# &location=home or &location=away

application = Flask(__name__)
cors = CORS(application)

@application.route('/', methods=['GET'])
def home():
    return '<p>Server is alive!</p>'

@application.route('/api/nba-season/all', methods=['GET'])
def season_all():
    return jsonify(seasonStatsAll())

@application.route('/api/nba-season-location/all', methods=['GET'])
def season_location_all():
    if 'location' in request.args:
        location = request.args['location']
    else:
        return "Error: No location field provided. Please specify home or away"

    return jsonify(seasonStatsAllLocation(location))

@application.route('/api/nba-last10/all', methods=['GET'])
def last10_all():
    return jsonify(last10StatsAll())

@application.route('/api/nba-last10-location/all', methods=['GET'])
def last10_location_all():
    if 'location' in request.args:
        location = request.args['location']
    else:
        return "Error: No location field provided. Please specify home or away"

    return jsonify(last10StatsAllLocation(location))

@application.route('/api/nba-season', methods=['GET'])
def season_date():
    if 'date' in request.args:
        date = request.args['date']
    else:
        return "Error: No date field provided. Please specify an date."

    return jsonify(seasonStats(date))

@application.route('/api/nba-season-location', methods=['GET'])
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
    
@application.route('/api/nba-last10', methods=['GET'])
def last10_date():
    if 'date' in request.args:
        date = request.args['date']
    else:
        return "Error: No date field provided. Please specify an date."

    return jsonify(last10Stats(date))

@application.route('/api/nba-last10-location', methods=['GET'])
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

@application.route('/api/nba-odds-all', methods=['GET'])
def odds_All():
    return jsonify(oddsAll())

@application.route('/api/nba-season-league-avg', methods=['GET'])
def ave_All():
    return jsonify(seasonLeagueAve())

@application.route('/api/nba-season-league-avg-location', methods=['GET'])
def ave_All_loc():
    if 'location' in request.args:
        location = request.args['location']
    else:
        return "Error: No location field provided. Please specify home or away"

    return jsonify(seasonLeagueAveLoc(location))

@application.route('/api/nba-scores-all', methods=['GET'])
def scores_All():
    return jsonify(scoresAll())

if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0')
