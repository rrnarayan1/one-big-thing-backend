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
    season_id = request.form.get('seasonId')
    team_id = request.form.get('teamId')
    game_id = request.form.get('gameId')
    if (not season_id or not team_id or not game_id):
        return flask.abort(400)

    game = _get_game(season_id, team_id, game_id)
    if not game:
        return flask.abort(404)
    return flask.jsonify(game)

@app.route('/score')
def score():
    season_id = request.form.get('seasonId')
    team_id = request.form.get('teamId')
    game_id = request.form.get('gameId')
    data = request.form.get('data')
    portion = request.form.get('portion')

    if (not season_id or not team_id or not game_id):
        return flask.abort(400)

    game = _get_game(season_id, team_id, game_id)
    if (not game):
        return flask.abort(404)

    # if data not defined, provide a default
    if (not data):
        data_season_id = int(game[u"SEASON_ID"])
        # if playoffs, use the regular season
        if (data_season_id > 40000):
            data_season_id -= 20000
            data = str(data_season_id)

        # if at beginning of season, use last season as data
        elif (game["GAME_NUM"] < 10):
            data = str(data_season_id-1)
        
        # else, take that season's games up to that point
        else:
            data = str(data_season_id)
            portion = "before"

    # only use portion = before if data is for that year
    if (portion == "before" and game[u"SEASON_ID"] != data):
        return flask.abort(422)

    data_season_collection = seasons[data]
    if (portion == "before"):
        data_games = db.collection(data_season_collection) \
            .where(u"TEAM_ID", u"==", team_id) \
            .where(u"GAME_NUM", u"<", game[u"GAME_NUM"]).get()
    else:
        data_games = db.collection(data_season_collection) \
            .where(u"TEAM_ID", u"==",team_id).get()

    if (not data_games):
        return flask.abort(404)

    list_data_games = []
    for data_game in data_games:
        list_data_games.append(data_game.to_dict())

    response = {}
    game_stat = pd.Series(game)[stat_categories]
    df = pd.DataFrame(list_data_games)
    df = df[stat_categories]
    mean = df.mean()
    std = df.std()
    diff = (game_stat - mean) / std

    response["data"] = data;
    response["portion"] = portion;
    response["scores"]=diff.to_dict()
    response["game"]=game
    return flask.jsonify(response)

# returns the game as a dictionary. if not present, returns None
def _get_game(season_id, team_id, game_id):
    season_collection = seasons[season_id]
    doc_ref = db.document(season_collection,team_id + "-" + game_id)
    try:
        doc = doc_ref.get().to_dict()
        return doc
    except:
        return None
