import numpy as np
import pandas as pd 

stat_categories = ['FGM', 'FGA', 'FG_PCT', 'FG3M','FG3A', \
'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', \
'AST','STL', 'BLK', 'TOV', 'PTS']

def get_scores(list_data_games, game, team, opp_team):
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
    #response["data"]=data
    #response["portion"]=portion
    response["scores"]=diff.to_dict()
    response["stats"]=game_stat.to_dict()
    response["game"]=game
    response["obt"]=one_big_thing
    response["team"]=team
    response["opp_team"]=opp_team
    return response