import numpy as np
import pandas as pd
from scipy import stats

stat_categories = ['FGM', 'FGA', 'FG_PCT', 'FG3M','FG3A', \
'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', \
'AST','STL', 'BLK', 'TOV', 'PTS']

def _get_scores(list_data_games, game):
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
    #diff["TOV"] = diff["TOV"]*-1

    one_big_thing["absolute"] = {"stat": diff.index[abs_idx], "score": diff.iloc[abs_idx]}
    one_big_thing["positive"] = {"stat": diff.index[pos_idx], "score": diff.iloc[pos_idx]}
    one_big_thing["negative"] = {"stat": diff.index[neg_idx], "score": diff.iloc[neg_idx]}

    game = {k:game[k] for k in game.keys() if k not in stat_categories}
    #response["data"]=data
    #response["portion"]=portion
    response["scores"]=diff.to_dict()
    response["stats"]=game_stat.to_dict()
    response["game"]=game
    response["obt"]=one_big_thing
    return response

# each obt object in the list should have the "WL" set
def _get_team_season_summary(obt_list, stat_list):
    obt_df = pd.DataFrame(obt_list)
    wins = obt_df[obt_df["WL"] == "W"]["absolute"].apply(pd.Series)
    loss = obt_df[obt_df["WL"] == "L"]["absolute"].apply(pd.Series)
    wins_mode = stats.mode(wins["stat"]).mode[0]
    loss_mode = stats.mode(loss["stat"]).mode[0]

    stats_df = pd.DataFrame(stat_list)
    wins_mode_stat_list = list(stats_df[stats_df["WL"] == "W"][wins_mode])
    wins_mode_stat_avg = np.mean(stats_df[wins_mode])
    wins_mode_stat_win_avg = np.mean(stats_df[stats_df["WL"] == "W"][wins_mode])
    wins_mode_stat_loss_avg = np.mean(stats_df[stats_df["WL"] == "L"][wins_mode])
    loss_mode_stat_list = list(stats_df[stats_df["WL"] == "L"][loss_mode])
    loss_mode_stat_avg = np.mean(stats_df[loss_mode])
    loss_mode_stat_win_avg = np.mean(stats_df[stats_df["WL"] == "W"][loss_mode])
    loss_mode_stat_loss_avg = np.mean(stats_df[stats_df["WL"] == "L"][loss_mode])

    summary = {}
    wins_response = {}
    wins_response["stat"] = wins_mode
    wins_response["stat_list"] = wins_mode_stat_list
    wins_response["stat_avg"] = wins_mode_stat_avg
    wins_response["stat_win_avg"] = wins_mode_stat_win_avg
    wins_response["stat_loss_avg"] = wins_mode_stat_loss_avg
    loss_response = {}
    loss_response["stat"] = loss_mode
    loss_response["stat_list"] = loss_mode_stat_list
    loss_response["stat_avg"] = loss_mode_stat_avg
    loss_response["stat_win_avg"] = loss_mode_stat_win_avg
    loss_response["stat_loss_avg"] = loss_mode_stat_loss_avg
    summary["wins_stats"] = wins_response
    summary["loss_stats"] = loss_response
    summary["record"] = str(len(wins))+"-"+str(len(loss))
    return summary

def _get_default_data(season_id_int, game):
    portion = None
    # if playoffs, use the regular season
    if (season_id_int > 40000):
        season_id_int -= 20000
        data = str(season_id_int)

    # if at "beginning" of season, use last season as data
    #elif (game["GAME_NUM"] < 10):
    #    data = str(season_id_int-1)

    # else, take that season's games.
    else:
        data = str(season_id_int)
        #portion = "before"
    return data, portion
