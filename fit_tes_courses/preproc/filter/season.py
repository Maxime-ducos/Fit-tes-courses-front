def map_season(tags):

    if "summer" in tags:
        return 1
    elif "winter" in tags:
        return 3
    elif "spring" in tags:
        return 2
    elif "fall" in tags:
        return 4
    else:
        return  0

#df_reviews = pd.read_csv('../../RAW_data/RAW_interactions.csv')
#df_recipes = pd.read_csv('../../raw_data/RAW_recipes.csv')
#df['season'] = df['tags'].apply(map_season)
#print(df)
