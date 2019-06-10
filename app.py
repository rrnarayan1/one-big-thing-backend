import firebase_admin
from firebase_admin import firestore
import flask
from flask import request
import pandas as pd
from flask_cors import CORS
import numpy as np
from Teams import get_team_by_id
from Games import get_game, get_opp_game, get_games_stats, get_games_info_by_team_and_season
from Score import _get_scores, _get_default_data

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

    game = get_game(db, season_id, team_id, game_id)
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

    game = get_game(db, season_id, team_id, game_id)
    opp_game = get_opp_game(db, season_id, team_id, game_id)
    if (not game):
        return flask.abort(404)

    team = get_team_by_id(db, game[u"TEAM_ID"])
    opp_team = get_team_by_id(db, opp_game[u"TEAM_ID"])
    if (not team or not opp_team):
        return flask.abort(404)

    # if data not defined, provide a default
    if (not data):
        data_season_id = int(game[u"SEASON_ID"])
        data, portion = _get_default_data(data_season_id, game)

    # only use 'portion = before' if data is for that year
    if (portion == "before" and game[u"SEASON_ID"] != data):
        return flask.abort(422)

    list_data_games = get_games_stats(db, data, portion, team_id, game)

    if (not list_data_games):
        return flask.abort(404)

    response = _get_scores(list_data_games, game)
    response["team"]=team
    response["opp_team"]=opp_team
    return flask.jsonify(response)

@app.route('/games')
def games():
    season_id = request.args.get('seasonId')
    team_id = request.args.get('teamId')
    with_obt = request.args.get('withOBT')
    if (not season_id or not team_id):
        return flask.abort(400)

    games = get_games_info_by_team_and_season(db, season_id, team_id, with_obt)

    return flask.jsonify(games)
