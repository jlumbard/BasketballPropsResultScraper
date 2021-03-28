import os
import pandas as pd
import datetime

nbaTeams = ['Houston Rockets','Detroit Pistons','Cleveland Cavaliers','San Antonio Spurs','Memphis Grizzlies','Golden State Warriors','Chicago Bulls','Denver Nuggets','Miami Heat','Indiana Pacers','Boston Celtics','Sacramento Kings','Brooklyn Nets','New York Knicks','Philidelpia 76ers','Toronto Raptors','Chicago Bulls','Milwaukee Bucks','Washington Wizards','Orlando Magic','Charlotte Hornets','Atlanta Hawks','Minnesota Timberwolves','Oklahoma City Thunder','Portland Trail Blazers','Utah Jazz','LA Clippers','Los Angeles Lakers','Phoenix Suns','New Orleans Pelicans']


print("Current working directory:")
print(os.getcwd())
dirToUse = '/Users/brocklumbard/OneDrive - Ivey Business School/SEAFinalProject'
#for testing
#dirToUse = 'sampleData' 

aggregatedDF = pd.DataFrame()

for filename in os.listdir(dirToUse):
    if filename.endswith(".csv") and 'basketball' in filename:
        print("Now processing: ")
        print(filename)
        print("scrape date is:")
        gameDate = datetime.datetime.strptime(filename.split('basketball')[1].replace('.csv',''),"%m%d%Y%H%M%S").replace(hour=0,minute=0,second=0,tzinfo=datetime.timezone.utc)
        print(gameDate)
        dfToModify = pd.read_csv(dirToUse+'/'+filename)

        dfToModify['result'] = None
        dfToModify['playerName'] = ""
        dfToModify['startTime'] = pd.to_datetime(dfToModify['startTime'], utc=True)


        for i,row in dfToModify.iterrows():
            if(dfToModify.at[i,'home'] in nbaTeams):
                betType = dfToModify.at[i,'betType']
                if(' - ' in betType):
                    #Then its a prop bet
                    metric = betType.split(' - ')[0]
                    playerName = betType.split(' - ')[1]
                    dfToModify.at[i,'playerName'] = playerName

        print(dfToModify)

        print(dfToModify['playerName'])
        aggregatedDF = aggregatedDF.append(pd.DataFrame(dfToModify['playerName']))
        
print(aggregatedDF)
print(aggregatedDF['playerName'])
aggregatedDF = pd.DataFrame(aggregatedDF['playerName'].unique())
print(aggregatedDF)

import getGoogleAmount

#eliminate a couple random bugs
aggregatedDF['searchResult'] = 0
aggregatedDF['searchResultBettingOnTerms'] = 0
for i, row in aggregatedDF.iterrows():
    if('Half' in aggregatedDF.at[i,0] or 'Quarter' in aggregatedDF.at[i,0] or aggregatedDF.at[i,0] == ""):
            aggregatedDF.drop(i, inplace=True)
    else:
        if('Jr.' in aggregatedDF.at[i,0]):
            aggregatedDF.at[i,0] = aggregatedDF.at[i,0].replace('Jr.','Jr')

        print('Searching') 
        print(aggregatedDF.at[i,0])
        try:
            aggregatedDF.at[i,'searchResult'] = getGoogleAmount.getNumOfResults(aggregatedDF.at[i,0])
            aggregatedDF.at[i,'searchResultBettingOnTerms'] = getGoogleAmount.getNumOfResults('Betting On ' + aggregatedDF.at[i,0])
        except Exception as e:
            print("Excepted")
            print(e)


aggregatedDF.to_csv('aggregatedDFNames.csv')
print("Done.")