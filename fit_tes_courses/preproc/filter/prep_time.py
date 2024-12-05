def map_code_time(minutes):

    if  minutes < 15 :
        return 0
    elif minutes < 30 :
        return 1
    elif minutes < 60 :
        return 2
    else:
        return 4

#df_reviews = pd.read_csv('../../RAW_data/RAW_interactions.csv')
#df_recipes = pd.read_csv('../../raw_data/RAW_recipes.csv')
#df['prep_time'] = df['minutes'].apply(map_code_time)
