# API Documentation 

## /  GET
**Params:** None

**Return:** str: "Hello World"

## /game GET

**Params**
* str: seasonId (Which season?)
* str: teamId (Which team's stats?)
* str: gameId (Which game?)

**Return:** JSON: with [gameInfo and gameStats](#column-info "Goto column-info")–oppTeam not provided

**Example:**
`/game?seasonId=22016&teamId=1610612737&gameId=0021600927`
```
{
    "AST": 21,
    "BLK": 1,
    "DREB": 33,
    "FG3A": 27,
    "FG3M": 9,
    "FG3_PCT": 0.333,
    "FGA": 77,
    "FGM": 34,
    "FG_PCT": 0.442,
    "FTA": 31,
    "FTM": 19,
    "FT_PCT": 0.613,
    "GAME_DATE": "Sun, 05 Mar 2017 00:00:00 GMT",
    "GAME_ID": "0021600927",
    "GAME_NUM": 62,
    "MATCHUP": "ATL vs. IND",
    "OREB": 11,
    "PF": 19,
    "PLUS_MINUS": -1,
    "PTS": 96,
    "REB": 44,
    "SEASON_ID": "22016",
    "STL": 12,
    "TEAM_ABBREVIATION": "ATL",
    "TEAM_ID": "1610612737",
    "TEAM_NAME": "Atlanta Hawks",
    "TOV": 15,
    "WL": "L"
}
```

## /score GET

**Params**
* str: seasonId (Which season?)
* str: teamId (Which team's stats?)
* str: gameId (Which game?)
* OPTIONAL: str: data 
  * Corresponds to a seasonId (e.g. '22016')
  * If provided, that season's data is used to compute z-scores
* OPTIONAL: str: portion 
  * Only `portion='before'` is currently supported
  * If provided, the game season is played in must correspond to the `data` parameter. `data` param must be provided

**Return:** JSON
* 'game'
  * [gameInfo](#game-info "Goto game-info") is provided
  * 'OPP_TEAM' is an added parameter
* 'obt'
  * Given: most positive, negative, and the most extreme (absolute value) z-scores for the game
  * Each object is given a 'score' (z-score) and a 'stat' (stat name associated with the score)
  * "default" value is "positive" if team won, "negative" if team lost
* 'scores'
  * Z-scores of all [game stats](#column-info "Goto column-info"), based on `data` and `portion`
* 'stats'
  * Raw stats of all [game stats](#column-info "Goto column-info")
* 'team'
  * Team statistics

**Example:**
`/score?seasonId=22016&teamId=1610612737&gameId=0021600927`
```
{
    "game": {
        "GAME_DATE": "Sun, 05 Mar 2017 00:00:00 GMT",
        "GAME_ID": "0021600927",
        "GAME_NUM": 62,
        "MATCHUP": "ATL vs. IND",
        "OPP_TEAM": {
            "LOCATION": "Indiana",
            "LOGO": "https://stats.nba.com/media/img/teams/logos/IND_logo.svg",
            "SIMPLE_NAME": "Pacers",
            "TEAM_ABBREVIATION": "IND",
            "TEAM_ID": "1610612754",
            "TEAM_NAME": "Indiana Pacers"
        },
        "PF": 19,
        "PLUS_MINUS": -1,
        "SEASON_ID": "22016",
        "TEAM_ABBREVIATION": "ATL",
        "TEAM_ID": "1610612737",
        "TEAM_NAME": "Atlanta Hawks",
        "WL": "L"
    },
    "obt": {
        "absolute": {
            "score": -1.67,
            "stat": "BLK"
        },
        "default": {
            "score": -1.67,
            "stat": "BLK"
        },
        "negative": {
            "score": -1.67,
            "stat": "BLK"
        },
        "positive": {
            "score": 1.23,
            "stat": "STL"
        }
    },
    "scores": {
        "AST": -0.52,
        "BLK": -1.67,
        "DREB": -0.2,
        "FG3A": 0.21,
        "FG3M": 0.04,
        "FG3_PCT": -0.1,
        "FGA": -0.96,
        "FGM": -0.76,
        "FG_PCT": -0.18,
        "FTA": 0.74,
        "FTM": 0.14,
        "FT_PCT": -1.05,
        "OREB": 0.19,
        "PTS": -0.58,
        "REB": -0.05,
        "STL": 1.23,
        "TOV": 0.2
    },
    "stats": {
        "AST": 21,
        "BLK": 1,
        "DREB": 33,
        "FG3A": 27,
        "FG3M": 9,
        "FG3_PCT": 0.333,
        "FGA": 77,
        "FGM": 34,
        "FG_PCT": 0.442,
        "FTA": 31,
        "FTM": 19,
        "FT_PCT": 0.613,
        "OREB": 11,
        "PTS": 96,
        "REB": 44,
        "STL": 12,
        "TOV": 15
    },
    "team": {
        "LOCATION": "Atlanta",
        "LOGO": "https://stats.nba.com/media/img/teams/logos/ATL_logo.svg",
        "SIMPLE_NAME": "Hawks",
        "TEAM_ABBREVIATION": "ATL",
        "TEAM_ID": "1610612737",
        "TEAM_NAME": "Atlanta Hawks"
    }
}
```

## /games GET

**Params**
* str: seasonId (Which season?)
* str: teamId (Which team's stats?)
* str: gameId (Which game?)
* bool: withOBT (Determines if OBT is computed)
* bool: withSummary (Determines if team season summary is computed)

**Return:** JSON
* 'games'
  * List of `game`s
  * Each game has [gameInfo](#game-info "Goto game-info"), `OBT` if asked for, and `OPP_TEAM`
* 'team'
  * Team statistics
* 'summary'
  * 'loss_stats'
    * 'stat' (Calculated by finding the mode of the negative OBTs of the games played that season)
    * 'stat_avg' (That stat's average in all games that season)
    * 'stat_loss_avg' (That stat's average in games lost that season)
    * 'stat_win_avg' (That stat's average in games won that season)
    * 'stat_list' (That stat's value in all games lost that season)
  * 'wins_stats'
    * Same format as 'loss_stats'
  * 'record'
    * Record for that season


**Example:**
`/games?seasonId=22016&teamId=1610612737&withSummary=True&withOBT=True`
```
{
  "games": [
        {
            "GAME_DATE": "Thu, 27 Oct 2016 00:00:00 GMT",
            "GAME_ID": "0021600014",
            "GAME_NUM": 1,
            "MATCHUP": "ATL vs. WAS",
            "OBT": {
                ...
            },
            "OPP_TEAM": {
                ...
            },
            "PLUS_MINUS": 15,
            "PTS": 114,
            "SEASON_ID": "22016",
            "TEAM_ABBREVIATION": "ATL",
            "TEAM_ID": "1610612737",
            "TEAM_NAME": "Atlanta Hawks",
            "WL": "W"
        },...
   ],
  "summary": {
        "loss_stats": {
            "stat": "FT_PCT",
            "stat_avg": 0.7260609756097561,
            "stat_list": [0.793, 0.639, ...],
            "stat_loss_avg": 0.7012307692307693,
            "stat_win_avg": 0.7485813953488372
        },
        "record": "43-39",
        "wins_stats": {
            "stat": "FG3M",
            "stat_avg": 8.890243902439025,
            "stat_list": [12,5,...],
            "stat_loss_avg": 8.35897435897436,
            "stat_win_avg": 9.372093023255815
        }
   }
   "team": {
        ...
   }
}
```

### column-info
```
game_info = ['GAME_DATE', 'GAME_ID', 'MATCHUP', 'GAME_NUM','PTS', 'PLUS_MINUS', 'SEASON_ID', 'TEAM_ABBREVIATION', 'TEAM_ID', 'TEAM_NAME', 'WL']

stat_categories = ['FGM', 'FGA', 'FG_PCT', 'FG3M','FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST','STL', 'BLK', 'TOV', 'PTS']
```
