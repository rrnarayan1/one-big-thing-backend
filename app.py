import firebase_admin
from firebase_admin import firestore
import flask
from flask import request
import pandas as pd

app = flask.Flask(__name__)

firebase_admin.initialize_app()
db = firestore.client()

seasons = {
  "22016": "16-17Reg",
  "42016": "16-17Playoffs",
  "22017": "17-18Reg",
  "42017": "17-18Playoffs",
  "22018": "18-19Reg"
}

stat_categories = ['FGM', 'FGA', 'FG_PCT', 'FG3M','FG3A', \
'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', \
'AST','STL', 'BLK', 'TOV', 'PTS']


@app.route('/')
def hello():
    return "Hello World"


@app.route('/game')
def game():
    season_id = request.args.get('seasonId')
    team_id = request.args.get('teamId')
    game_id = request.args.get('gameId')
    if (not season_id or not team_id or not game_id):
        return flask.abort(400)

    game = _get_game(season_id, team_id, game_id)
    if not game:
        return flask.abort(404)
    return flask.jsonify(game)

@app.route('/score')
def score():
    season_id = request.args.get('seasonId')
    team_id = request.args.get('teamId')
    game_id = request.args.get('gameId')
    data = request.args.get('data')
    data_type = request.args.get('dataType')
    if (not season_id or not team_id or not game_id or not data):
        return flask.abort(400)

    game = _get_game(season_id, team_id, game_id)
    if (not game):
        return flask.abort(404)

    # assume the data is for the whole season
    data_season_collection = seasons[data]
    team_unicode = (team_id).encode("utf-8")
    data_games = db.collection(data_season_collection) \
        .where(u"TEAM_ID", u"==",team_id).get()
    if (not data_games):
        return flask.abort(404)

    list_data_games = []
    for data_game in data_games:
        list_data_games.append(data_game.to_dict())

    game_stat = pd.Series(game)[stat_categories]
    df = pd.DataFrame(list_data_games)
    df = df[stat_categories]
    mean = df.mean()
    std = df.std()
    diff = (game_stat - mean) / std
    diff_dict = diff.to_dict()
    print(diff_dict)
    return flask.jsonify(diff_dict)

# returns the game as a dictionary
def _get_game(season_id, team_id, game_id):
    season_collection = seasons[season_id]
    doc_ref = db.document(season_collection,team_id + "-" + game_id)
    try:
        doc = doc_ref.get().to_dict()
        return doc
    except:
        return None
