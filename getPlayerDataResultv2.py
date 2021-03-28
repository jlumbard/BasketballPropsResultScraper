import os
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog
import pandas as pd

teamsList = teams.get_teams()
abbrNameTransList = {}
teamGameLogs = {}
for x in teamsList:
    abbrNameTransList[x['abbreviation']] = x['full_name']
    print(x['abbreviation'])
    teamGameLogs[x['abbreviation']] = (teamgamelog.TeamGameLog(x['id']))

print(teamsList)
df = pd.DataFrame()
for key, value in teamGameLogs.items():
    df = df.append(pd.DataFrame(
        value.team_game_log.get_data_frame()), ignore_index=True)

homeDf = df.loc[df['MATCHUP'].str.contains('@')]
homeDf[['team','ignore']] = homeDf['MATCHUP'].str.split(' @ ', expand=True)

awayDf = df.loc[df['MATCHUP'].str.contains(' vs. ')]
awayDf[['team','ignore']] = awayDf['MATCHUP'].str.split(' vs. ',expand=True)

matchupDF = homeDf.merge(
    awayDf, how="inner", on="Game_ID", suffixes=('_away', '_home'))

matchupDF['abbr_home'] = matchupDF['team_home']
matchupDF['abbr_away'] = matchupDF['team_away']

matchupDF = matchupDF.replace({'team_home':abbrNameTransList})
matchupDF = matchupDF.replace({'team_away':abbrNameTransList})

betsDF = pd.read_csv('finalDFNoProps.csv')

matchupDF.to_csv('matchups.csv')

betsDF['startTime'] = pd.to_datetime(betsDF['startTime'], utc=True)
betsDF['OGscrapeDate'] = pd.to_datetime(betsDF['OGscrapeDate'], utc=True)
matchupDF['GAME_DATE_home'] = pd.to_datetime(matchupDF['GAME_DATE_home'], utc=True)
doubleMergeDF = pd.merge(betsDF, matchupDF, how="left", left_on=['home','OGscrapeDate'], right_on=['team_home','GAME_DATE_home'])

print(betsDF['startTime'].unique())
print(matchupDF['GAME_DATE_home'].unique())

print(betsDF['home'].unique())
print(matchupDF['team_home'].unique())

print(doubleMergeDF)
print(doubleMergeDF['ignore_away'].count())
doubleMergeDF.to_csv('doubleMergeDF.csv')
print(matchupDF.loc[138])

# Have to join, need to split out abbreviations
