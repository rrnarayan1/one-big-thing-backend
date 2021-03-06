from Teams import get_team_by_id, get_all_teams
from Score import _get_scores, _get_team_season_summary
import pandas as pd


seasons = {
  "22016": "16-17Reg",
  "42016": "16-17Playoffs",
  "22017": "17-18Reg",
  "42017": "17-18Playoffs",
  "22018": "18-19Reg"
}

game_info = ['GAME_DATE', 'GAME_ID', 'MATCHUP', 'GAME_NUM','PTS', \
'PLUS_MINUS', 'SEASON_ID', 'TEAM_ABBREVIATION', 'TEAM_ID', 'TEAM_NAME', 'WL']

stat_categories = ['FGM', 'FGA', 'FG_PCT', 'FG3M','FG3A', \
'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', \
'AST','STL', 'BLK', 'TOV', 'PTS']

# returns the game as a dictionary. if not present, returns None
def get_game(db, season_id, team_id, game_id):
    season_collection = seasons[season_id]
    doc_ref = db.document(season_collection,team_id + "-" + game_id)
    try:
        game_doc = doc_ref.get().to_dict()
        return game_doc
    except:
        return None

#returns game for the team not listed in the team_id
def get_opp_game(db, season_id, team_id, game_id):
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

def get_games_stats(db, data, portion, team_id, game):
    data_season_collection = seasons[data]
    try:
        if (portion == "before"):
            data_games = db.collection(data_season_collection) \
                .where(u"TEAM_ID", u"==", team_id) \
                .where(u"GAME_NUM", u"<", game[u"GAME_NUM"]).get()
        else:
            data_games = db.collection(data_season_collection) \
                .where(u"TEAM_ID", u"==",team_id).get()
            list_data_games = []
            for data_game in data_games:
                list_data_games.append(data_game.to_dict())
            return list_data_games
    except:
        return None

def get_games_info_by_team_and_season(db, season_id, team_id, with_obt, with_summary):
    season_collection = seasons[season_id]
    games = get_games_stats(db, season_id, None, team_id, None)
    teams = get_all_teams(db)
    response = {}
    response["team"] = get_team_by_id(db, team_id)
    game_info_list = []
    game_stat_list = []
    obt_list = []
    for game in games:
        info_dict = {k : game[k] for k in game_info}
        stat_dict = {k : game[k] for k in stat_categories}
        if (with_obt):
            scores = _get_scores(games, game)
            obt = scores["obt"]
            info_dict["OBT"] = obt
            if (with_summary):
                obt["WL"] = info_dict["WL"]
                stat_dict["WL"] = info_dict["WL"]

            obt_list.append(obt)
        info_dict["OPP_TEAM"] = teams[info_dict["MATCHUP"][-3:]]
        game_info_list.append(info_dict)
        game_stat_list.append(stat_dict)
    response["games"] = game_info_list

    if (with_summary and with_obt):
        summary = _get_team_season_summary(obt_list, game_stat_list)
        response["summary"] = summary

    return response


