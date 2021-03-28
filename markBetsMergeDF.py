import pandas as pd

df = pd.read_csv('doubleMergeDF.csv')
df['total'] = df['PTS_home'] +df['PTS_away']
df['result'] = 0

#will be negative if they win
df['homeSpread'] = df['PTS_away'] - df['PTS_home']
df['awaySpread'] = df['PTS_home'] - df['PTS_away'] 

#if canucks are +1.5 and they lose by one then they covered spread 
# its a win if the column above is smaller than that spread

# if canucks are -1.5 and they win by 2 then they covered the spread 
# its a win if the column above is smaller than that spread

#only fulltime bets. Most of them anyways
df = df.loc[df['period'] == 0]

df.points = df.points.astype(float)
df.awaySpread = df.awaySpread.astype(float)
df.homeSpread = df.homeSpread.astype(float)
df.PTS_away = df.PTS_away.astype(float)
df.PTS_home = df.PTS_home.astype(float)

for i, row in df.iterrows():
    #check totals 
    if(df.at[i,'betType'] == 'total'):

        if(df.at[i,'designation'] == 'over' and df.at[i,'points'] < df.at[i,'total']):
            df.at[i,'result'] = 1
        elif(df.at[i,'designation'] == 'under' and df.at[i,'points'] > df.at[i,'total']):
            df.at[i,'result'] = 1
        elif(df.at[i,'points'] == df.at[i,'total']):
            df.at[i,'result'] = 0.5
    if(df.at[i,'betType'] == 'homeTotal'):

        if(df.at[i,'designation'] == 'over' and df.at[i,'points'] < df.at[i,'PTS_home']):
            df.at[i,'result'] = 1
        elif(df.at[i,'designation'] == 'under' and df.at[i,'points'] > df.at[i,'PTS_home']):
            df.at[i,'result'] = 1
        elif(df.at[i,'points'] == df.at[i,'PTS_home']):
            df.at[i,'result'] = 0.5
    if(df.at[i,'betType'] == 'awayTotal'):

        if(df.at[i,'designation'] == 'over' and df.at[i,'points'] < df.at[i,'PTS_away']):
            df.at[i,'result'] = 1
        elif(df.at[i,'designation'] == 'under' and df.at[i,'points'] > df.at[i,'PTS_away']):
            df.at[i,'result'] = 1
        elif(df.at[i,'points'] == df.at[i,'PTS_away']):
            df.at[i,'result'] = 0.5

    if(df.at[i,'betType'] == 'spread'):

        if(df.at[i,'designation'] == df.at[i,'away'] and df.at[i,'awaySpread'] < df.at[i,'points']):
            df.at[i,'result'] = 1
        elif(df.at[i,'designation'] == df.at[i,'home'] and df.at[i,'homeSpread'] < df.at[i,'points']):
            df.at[i,'result'] = 1
        elif(df.at[i,'designation'] == df.at[i,'away'] and df.at[i,'awaySpread'] == df.at[i,'points']):
            df.at[i,'result'] = 0.5
        elif(df.at[i,'designation'] == df.at[i,'home'] and df.at[i,'homeSpread'] == df.at[i,'points']):
            df.at[i,'result'] = 0.5

    if(df.at[i,'betType'] == 'moneyline'):

        if(df.at[i,'designation'] == df.at[i,'away'] and df.at[i,'PTS_away'] > df.at[i,'PTS_home']):
            df.at[i,'result'] = 1
        elif(df.at[i,'designation'] == df.at[i,'home'] and df.at[i,'PTS_home'] > df.at[i,'PTS_away']):
            df.at[i,'result'] = 1
        

df.to_csv('MarkedWinMergeBetsNoProps.csv')

df['teamMergeColumn'] = df['designation']
df = df.loc[df['betType'] != 'total']
df = df.loc[df['designation'] != 'over']
df = df.loc[df['price'] >= 2.0]
for i, row in df.iterrows():
    if(df.at[i,'betType'] == 'homeTotal'):
        df.at[i,'teamMergeColumn'] = df.at[i,'home']
    elif(df.at[i,'betType'] == 'awayTotal'):
        df.at[i,'teamMergeColumn'] = df.at[i,'away']
        

socialMediaDF = pd.read_csv('NBATeamsFollowerCount.csv')

mergedSocialsDFNoProps = df.merge(socialMediaDF,how="inner",left_on="teamMergeColumn",right_on="TEAM")

mergedSocialsDFNoProps.to_csv('mergedSocialsDFNoProps.csv')

mergedSocialsDFNoProps['ROI'] = mergedSocialsDFNoProps['result'] * mergedSocialsDFNoProps['price']
mergedSocialsDFAgg = mergedSocialsDFNoProps.groupby(['teamMergeColumn']).mean()

mergedSocialsDFAgg.merge(socialMediaDF,how="inner",left_on="teamMergeColumn",right_on="TEAM").to_csv('mergedSocialsDFAggUnderdogs.csv')