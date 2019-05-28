import firebase_admin
from firebase_admin import firestore
import flask
from flask import request
import pandas as pd
from flask_cors import CORS
import numpy as np

app = flask.Flask(__name__)
cors = CORS(app)

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
    portion = request.args.get('portion')

    if (not season_id or not team_id or not game_id):
        return flask.abort(400)

    game = _get_game(season_id, team_id, game_id)
    opp_game = _get_opp_game(season_id, team_id, game_id)
    if (not game):
        return flask.abort(404)

    team = _get_team(game[u"TEAM_ID"])
    opp_team = _get_team(opp_game[u"TEAM_ID"])
    if (not team or not opp_team):
        return flask.abort(404)

    # if data not defined, provide a default
    if (not data):
        data_season_id = int(game[u"SEASON_ID"])
        data, portion = _get_default_data(data_season_id, game)

    # only use 'portion = before' if data is for that year
    if (portion == "before" and game[u"SEASON_ID"] != data):
        return flask.abort(422)

    data_games = _get_games_stats(data, portion, team_id, game)

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
    diff = np.round(((game_stat - mean) / std).astype(np.double), 2)
    one_big_thing = {}

    diff["TOV"] = diff["TOV"]*-1
    pos_idx = np.array(diff).argmax()
    neg_idx = np.array(diff).argmin()
    abs_idx = np.array(np.abs(diff)).argmax()
    diff["TOV"] = diff["TOV"]*-1

    one_big_thing["absolute"] = {"stat": diff.index[abs_idx], "score": diff.iloc[abs_idx]}
    one_big_thing["positive"] = {"stat": diff.index[pos_idx], "score": diff.iloc[pos_idx]}
    one_big_thing["negative"] = {"stat": diff.index[neg_idx], "score": diff.iloc[neg_idx]}

    game = {k:game[k] for k in game.keys() if k not in stat_categories}
    print(game)
    #response["data"]=data
    #response["portion"]=portion
    response["scores"]=diff.to_dict()
    response["stats"]=game_stat.to_dict()
    response["game"]=game
    response["obt"]=one_big_thing
    response["team"]=team
    response["opp_team"]=opp_team
    return flask.jsonify(response)

def _get_games_stats(data, portion, team_id, game):
    data_season_collection = seasons[data]
    try:
        if (portion == "before"):
            data_games = db.collection(data_season_collection) \
                .where(u"TEAM_ID", u"==", team_id) \
                .where(u"GAME_NUM", u"<", game[u"GAME_NUM"]).get()
        else:
            data_games = db.collection(data_season_collection) \
                .where(u"TEAM_ID", u"==",team_id).get()
        return data_games
    except:
        return None

def _get_default_data(season_id_int, game):
    portion = None
    # if playoffs, use the regular season
    if (season_id_int > 40000):
        season_id_int -= 20000
        data = str(season_id_int)

    # if at "beginning" of season, use last season as data
    elif (game["GAME_NUM"] < 10):
        data = str(season_id_int-1)

    # else, take that season's games up to that point
    else:
        data = str(season_id_int)
        portion = "before"
    return data, portion

# returns the game as a dictionary. if not present, returns None
def _get_game(season_id, team_id, game_id):
    season_collection = seasons[season_id]
    doc_ref = db.document(season_collection,team_id + "-" + game_id)
    try:
        game_doc = doc_ref.get().to_dict()
        return game_doc
    except:
        return None

#returns game for the team not listed in the team_id
def _get_opp_game(season_id, team_id, game_id):
    season_collection = seasons[season_id]
    doc_ref = db.collection(season_collection).where(u"GAME_ID",u"==",game_id)
    try:
        games = doc_ref.get()
        for game in games:
            game_dict = game.to_dict()
            if (game_dict[u"TEAM_ID"] != team_id):
                return game_dict
    except:
        return None

def _get_team(team_id):
    doc_ref = db.document("teams",team_id)
    try:
        return doc_ref.get().to_dict()
    except:
        return None
