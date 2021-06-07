import flask
from flask import request, jsonify
from flask_cors import CORS
from queries.seasonStatsAll import seasonStatsAll
from queries.last10StatsAll import last10StatsAll
from queries.seasonStats import seasonStats
from queries.last10Stats import last10Stats

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)

@app.route('/', methods=['GET'])
def home():
    return '<p>Server is alive!</p>'

@app.route('/api/nba-season/all', methods=['GET'])
def season_all():
    return jsonify(seasonStatsAll())

@app.route('/api/nba-last10/all', methods=['GET'])
def last10_all():
    return jsonify(last10StatsAll())

# date should have format: '2021-05-01'
@app.route('/api/nba-season', methods=['GET'])
def season_date():
    if 'date' in request.args:
        date = request.args['date']
    else:
        return "Error: No date field provided. Please specify an date."

    return jsonify(seasonStats(date))

@app.route('/api/nba-last10', methods=['GET'])
def last10_date():
    if 'date' in request.args:
        date = request.args['date']
    else:
        return "Error: No date field provided. Please specify an date."

    return jsonify(last10Stats(date))

app.run()
