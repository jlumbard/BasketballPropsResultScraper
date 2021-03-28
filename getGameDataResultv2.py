import pandas as pd
import datetime
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import time

nbaTeams = ['Houston Rockets','Detroit Pistons','Cleveland Cavaliers','San Antonio Spurs','Memphis Grizzlies','Golden State Warriors','Chicago Bulls','Denver Nuggets','Miami Heat','Indiana Pacers','Boston Celtics','Sacramento Kings','Brooklyn Nets','New York Knicks','Philidelpia 76ers','Toronto Raptors','Chicago Bulls','Milwaukee Bucks','Washington Wizards','Orlando Magic','Charlotte Hornets','Atlanta Hawks','Minnesota Timberwolves','Oklahoma City Thunder','Portland Trail Blazers','Utah Jazz','LA Clippers','Los Angeles Lakers','Phoenix Suns','New Orleans Pelicans']
translationDict = {'Half-Time':'','Total Rebounds and Assists' :'RA','Total Points and Rebounds':'PR','Total Points, Rebounds and Assists':'PRA','Double-Double':'DD','Total Turnovers':'TOV','Total Assists':'AST','Total Made 3 Point Shots':'FG3M','Total Blocks':'BLK','Total Blocked Shots':'BLK','Total Points':'PTS','Total Rebounds':'REB','Total Steals':'STL','Total Blocks and Steals':'BS'}


def addOutcomesToDF(df, gameDate):
    

    df['result'] = None
    df['playerName'] = ""
    df['statName'] = ""
    df['startTime'] = pd.to_datetime(df['startTime'], utc=True)


    for i,row in df.iterrows():
        if(df.at[i,'home'] in nbaTeams):
            betType = df.at[i,'betType']
            if(' - ' in betType):
                #Then its a prop bet
                metric = betType.split(' - ')[0]
                playerName = betType.split(' - ')[1]
                df.at[i,'playerName'] = playerName
                df.at[i,'statName'] = translationDict[metric]
        else:
            df.drop(i, inplace=True)

    playerNamesOnly = df['playerName'].unique()
    print(playerNamesOnly)
    print(type(playerNamesOnly))



    def getStatsByPlayerAndGame(playerID, gameDate):
        time.sleep(1)
        games = playergamelog.PlayerGameLog(player_id=playerID)
        #it returns a list
        df = games.get_data_frames()[0]
        df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'], utc=True)
        #filter to just the correct date
        df = df.loc[df['GAME_DATE'] == gameDate]
        if(len(df)>0):
            df['PR'] = df['PTS'] + df['REB']
            df['PRA'] = df['PTS'] + df['REB'] + df['AST']
            df['BS'] = df['BLK'] + df['STL']
            df['PR'] = df['PTS'] + df['REB']
            df['RA'] = df['REB'] + df['AST']
        return df.squeeze()

    playerStatsDF = pd.DataFrame()

    #This contains their IDs
    playerList = players.get_players()
    playerListDF = pd.DataFrame.from_records(playerList)

    #Get them all in one DF
    for player in playerNamesOnly:
        print("SCRAPING:")
        print(player)
        playerIDList = playerListDF.loc[playerListDF['full_name'] == player]

        if(len(playerIDList)>0):
            playerStatsRow = getStatsByPlayerAndGame(playerIDList.squeeze()['id'],gameDate)
            playerStatsRow['name'] = player 
            print(playerStatsRow)
            playerStatsDF = playerStatsDF.append(playerStatsRow,ignore_index=True)
        

    print(playerStatsDF)

    #now join the above df of the stats and player names with the big df

    #melt turns it into having columns of each statname, statvalue combo rather than a column for each stat
    if('name' in playerStatsDF.columns):
        meltedPlayerStats = playerStatsDF.melt(id_vars='name',var_name="Stat",value_name="Value")
        mergedDF = df.merge(meltedPlayerStats, how='inner', left_on=['playerName','statName'], right_on=['name','Stat'])

        print(mergedDF)

        mergedDF['result'] = 0
        for i,row in mergedDF.iterrows():
            if(mergedDF.at[i,'Value'] > float(mergedDF.at[i,'points']) and mergedDF.at[i,'designation'] == 'over'):
                print("set 1")
                mergedDF.at[i,'result'] = 1
                # print(mergedDF.at[i,'result'])
            elif(mergedDF.at[i,'Value'] < float(mergedDF.at[i,'points']) and mergedDF.at[i,'designation'] == 'under'):
                print("set 1")
                mergedDF.at[i,'result'] = 1
            elif(mergedDF.at[i,'Value'] == mergedDF.at[i,'points']):
                mergedDF.at[i,'result'] = 0.5
            else:
                mergedDF.at[i,'result'] = 0

        return mergedDF
    else:
        print("RETURNED FALSE, NO PLAYERS IN THE DF")
        return pd.DataFrame()

#iterate through cwd and update all files With new names

import os

print("Current working directory:")
print(os.getcwd())
dirToUse = 'sampleData'
dirToMoveTo = 'sampleDataDone'
dirToUseAlternate = '/Users/brocklumbard/OneDrive - Ivey Business School/SEAFinalProject'


for filename in os.listdir(dirToUse):
    if filename.endswith(".csv") and 'basketball' in filename:
        print("Now processing: ")
        print(filename)
        print("scrape date is:")
        gameDate = datetime.datetime.strptime(filename.split('basketball')[1].replace('.csv',''),"%m%d%Y%H%M%S").replace(hour=0,minute=0,second=0,tzinfo=datetime.timezone.utc)
        print(gameDate)
        dfToModify = pd.read_csv(dirToUse+'/'+filename)
        #Sometimes the DF's starttimes will be later than the 
        #Datetime that is passed in...Depends on the time that it was produced

        dfToModify['startTime'] = pd.to_datetime(dfToModify['startTime'], utc=True)
        print(dfToModify['startTime'].unique())
        dfToModify['startTime'].unique()

        lowestDate = dfToModify['startTime'].unique()[0]
        for iterdate in dfToModify['startTime'].unique():
            if(lowestDate > iterdate):
                print("SET NEW DATE")
                lowestDate = iterdate

        if(lowestDate > gameDate):
            gameDate = lowestDate
        dateTranslationDict = {}

        dfToModify['scrapeMergeDate'] = gameDate
        print(gameDate)
        returnedDF = addOutcomesToDF(dfToModify, gameDate)
        returnedDF.to_csv('mergedData/ResultsAdded'+filename)
        print("Done file")
        print(filename)
        print("moving")
        os.rename(dirToUse+'/'+filename, dirToMoveTo+'/'+filename)

print("Done.")
