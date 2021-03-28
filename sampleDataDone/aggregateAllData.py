import os 
import pandas as pd
import datetime

dirToUse = 'mergedData'
# dirToMoveTo = 'sampleDataDone'
# dirToUseAlternate = '/Users/brocklumbard/OneDrive - Ivey Business School/SEAFinalProject'

finalDF = pd.DataFrame()

for filename in os.listdir(dirToUse):
    if filename.endswith(".csv") and 'basketball' in filename:
        print("Now processing: ")
        print(filename)
        print("scrape date is:")
        gameDate = datetime.datetime.strptime(filename.split('basketball')[1].replace('.csv',''),"%m%d%Y%H%M%S").replace(hour=0,minute=0,second=0,tzinfo=datetime.timezone.utc)
        print(gameDate)
        dfToModify['startTime'] = pd.to_datetime(dfToModify['startTime'], utc=True)
        print(dfToModify['startTime'].unique())
        dfToModify['startTime'].unique()

        dfToModify['startTime'] = pd.to_datetime(dfToModify['startTime'], utc=True)
        lowestDate = dfToModify['startTime'].unique()[0]
        for iterdate in dfToModify['startTime'].unique():
            if(lowestDate > iterdate):
                print("SET NEW DATE")
                lowestDate = iterdate

        if(lowestDate > gameDate):
            gameDate = lowestDate
        dateTranslationDict = {}

        dfToModify['scrapeMergeDate'] = gameDate
        dfToModify = pd.read_csv(dirToUse+'/'+filename)
        dfToModify['OGscrapeDate'] = gameDate
        dfToModify['SiteName'] = filename.split('Output')[0]
        finalDF = finalDF.append(dfToModify, ignore_index=True)


finalDF.to_csv('finalDF.csv')
print("Done.")
