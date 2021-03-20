
from nba_api.stats.endpoints import playergamelog
import pandas as pd
import datetime
from nba_api.stats.static import players
import time

nbaTeams = ['Houston Rockets','Detroit Pistons','Cleveland Cavaliers','San Antonio Spurs','Memphis Grizzlies','Golden State Warriors','Chicago Bulls','Denver Nuggets','Miami Heat','Indiana Pacers','Boston Celtics','Sacramento Kings','Brooklyn Nets','New York Knicks','Philidelpia 76ers','Toronto Raptors','Chicago Bulls','Milwaukee Bucks','Washington Wizards','Orlando Magic','Charlotte Hornets','Atlanta Hawks','Minnesota Timberwolves','Oklahoma City Thunder','Portland Trail Blazers','Utah Jazz','LA Clippers','Los Angeles Lakers','Phoenix Suns','New Orleans Pelicans']

def getStatsByPlayerAndGame(playerID, gameDate):
    games = playergamelog.PlayerGameLog(player_id=playerID)
    #it returns a list
    df = games.get_data_frames()[0]
    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'], utc=True)
    #filter to just the correct date
    df = df.loc[df['GAME_DATE'] == gameDate]
    return df.squeeze()
    
    
def openAndFindResult(dataFrameURL, playersDF):
    
    translationDict = {'Total Points, Rebounds and Assists':'PRA','Double-Double':'DD','Total Turnovers':'TOV','Total Assists':'AST','Total Made 3 Point Shots':'FG3M','Total Blocks':'BLK','Total Points':'PTS','Total Rebounds':'REB','Total Blocks and Steals':'BS'}
    df = pd.read_csv(dataFrameURL)
    df['result'] = None
    df['startTime'] = pd.to_datetime(df['startTime'], utc=True)
    for i,row in df.iterrows():
        if(df.at[i,'home'] in nbaTeams):
            
            print("Index: " + str(i))
            betType = df.at[i,'betType']
            if(' - ' in betType):
                #Then its a prop bet
                metric = betType.split(' - ')[0]
                playerName = betType.split(' - ')[1]
                tempPlayersDF = playersDF.loc[playersDF['full_name'] == playerName]
                if(len(tempPlayersDF)>0):
                    playerID = tempPlayersDF.squeeze()['id']
                    print("getting stats for playerID")
                    print(playerID)
                    print(playerName)
                    statsObj = getStatsByPlayerAndGame(playerID,df.at[i,'startTime'])
                    if(len(statsObj) >0): #if not, it hasnt found a matching game. Which is ok, it might not be played yet
                        statsTranslation = translationDict[metric]
                        print("Value is:")
                        print(df.at[i,'points'])
                        if(statsTranslation == 'PRA'):
                            statsObj['PRA'] = statsObj['PTS'] + statsObj['REB'] + statsObj['AST']
                        if(statsTranslation == 'DD'):
                            statsObj['DD'] = 0 #not implemented
                        if(statsTranslation == 'BS'):
                            statsObj['BS'] = statsObj['BLK'] + statsObj['STL']
                        if(statsObj[statsTranslation] > float(df.at[i,'points']) and df.at[i,'designation'] == 'over'):
                            print("set 1")
                            df.at[i,'result'] = 1
                            print(df.at[i,'result'])
                        elif(statsObj[statsTranslation] < float(df.at[i,'points']) and df.at[i,'designation'] == 'under'):
                            print("set 1")
                            df.at[i,'result'] = 1
                        elif(statsObj[statsTranslation] == df.at[i,'points']):
                            df.at[i,'result'] = 0.5
                        else:
                            df.at[i,'result'] = 0
                    
                    else:
                        print("Empty stats DF, game probably hasn't been played yet.")
                else:
                    print("empty players df, player likely does not play in NBA. Name is: " + str(playerName))
                time.sleep(2)
            else:
                print("Wasn't a props bet.")
    print(df)
    df.to_csv('savedStats.csv')
    
playerList = players.get_players()
playerListDF = pd.DataFrame.from_records(playerList)

url = '/Users/brocklumbard/Desktop/PinnacleOutputbasketball03182021201530.csv'
openAndFindResult(url,playerListDF)
