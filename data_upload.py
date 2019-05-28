import firebase_admin
from firebase_admin import firestore
import csv
import json
from datetime import datetime

firebase_admin.initialize_app()
db = firestore.client()

db_keys = ['SEASON_ID','WL', 'TOV', 'TEAM_ID', 'REB', 'TEAM_NAME', 'FG3A', 'DREB', 'AST', 'TEAM_ABBREVIATION', 'FG3M', 'OREB', 'FGM', 'PF', 'PTS', 'FGA', 'PLUS_MINUS', 'STL', 'FTA', 'BLK', 'GAME_ID', 'MATCHUP', 'FTM', 'FT_PCT', 'FG_PCT', 'FG3_PCT', 'GAME_DATE']

float_keys = ['TOV', 'REB', 'FG3A', 'DREB', 'AST', 'FG3M', 'OREB', 'FGM', 'PF', 'PTS', 'FGA', 'PLUS_MINUS', 'STL', 'FTA', 'BLK', 'FTM', 'FT_PCT', 'FG_PCT', 'FG3_PCT']

def upload_file(csv_file):
    print(csv_file)
    with open(csv_file) as f:
        csv_reader = csv.DictReader(f)
        num_games = {}
        for row in csv_reader:
            team_id = row["TEAM_ID"]
            game_id = row["GAME_ID"]
            if team_id not in num_games.keys():
                num_games[team_id] = 0
            num_games[team_id] += 1
            doc_name = team_id + "-" + game_id
            db_dict = { unicode(k, 'utf-8'): unicode(row[k], 'utf-8') for k in db_keys }
            for key in float_keys:
                db_dict[key] = float(db_dict[key])
            db_dict[u"GAME_NUM"] = num_games[team_id]
            db_dict[u"GAME_DATE"] = datetime.strptime(db_dict[u"GAME_DATE"],"%Y-%m-%d")
            #print(db_dict)
            db.collection("18-19Reg").document(doc_name).set(db_dict)
            print("Wrote "+db_dict["MATCHUP"]+" "+str(db_dict["GAME_DATE"]))
            return

def upload_teams(json_file):
    print(json_file)
    with open(json_file) as f:
        teams = json.load(f)
        for team in teams:
            team_upload = {}
            team_upload[u"TEAM_ID"] = str(team["teamId"])
            team_upload[u"TEAM_ABBREVIATION"] = team["abbreviation"]
            team_upload[u"TEAM_NAME"] = team["teamName"]
            team_upload[u"SIMPLE_NAME"] = team["simpleName"]
            team_upload[u"LOCATION"] = team["location"]
            team_upload[u"LOGO"] = "https://stats.nba.com/media/img/teams/logos/"+team["abbreviation"]+"_logo.svg"
            db.collection("teams").document(team_upload[u"TEAM_ID"]).set(team_upload)
upload_teams("./data/teams.json")
#upload_file("../scripts/data/2018-19-RegularSeason-nba.csv")
