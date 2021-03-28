import os 
import pandas as pd
import datetime

dirToUse = '/Users/brocklumbard/OneDrive - Ivey Business School/SEAFinalProject'

nbaTeams = ['Houston Rockets','Detroit Pistons','Cleveland Cavaliers','San Antonio Spurs','Memphis Grizzlies','Golden State Warriors','Chicago Bulls','Denver Nuggets','Miami Heat','Indiana Pacers','Boston Celtics','Sacramento Kings','Brooklyn Nets','New York Knicks','Philidelpia 76ers','Toronto Raptors','Chicago Bulls','Milwaukee Bucks','Washington Wizards','Orlando Magic','Charlotte Hornets','Atlanta Hawks','Minnesota Timberwolves','Oklahoma City Thunder','Portland Trail Blazers','Utah Jazz','LA Clippers','Los Angeles Lakers','Phoenix Suns','New Orleans Pelicans']
finalDF = pd.DataFrame()

for filename in os.listdir(dirToUse):
    if filename.endswith(".csv") and 'basketball' in filename:
        print("Now processing: ")
        print(filename)
        print("scrape date is:")
        gameDate = datetime.datetime.strptime(filename.split('basketball')[1].replace('.csv',''),"%m%d%Y%H%M%S").replace(hour=0,minute=0,second=0,tzinfo=datetime.timezone.utc)
        print(gameDate)

        dfToModify = pd.read_csv(dirToUse+'/'+filename)

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

        dfToModify['OGscrapeDate'] = gameDate
        dfToModify['SiteName'] = filename.split('Output')[0]
        finalDF = finalDF.append(dfToModify, ignore_index=True)

finalDF = finalDF.loc[(finalDF['betType'] == 'total') | (finalDF['betType'] == 'awayTotal') | (finalDF['betType'] == 'homeTotal') | (finalDF['betType'] == 'spread') | (finalDF['betType'] == 'moneyline')]

finalDF = finalDF.loc[finalDF['home'].isin(nbaTeams)]
finalDF.to_csv('finalDFNoProps.csv')
print(finalDF)
print("Done.")