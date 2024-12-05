import ast

def filter_dataframe(df, healthy, season, dish_type, prep_time, origin, categories, cluster, mood_manual):
    """
    Filtre un DataFrame en fonction des critères fournis.

    Args:
        df (pd.DataFrame): DataFrame contenant les recettes.
        criteria (dict): Dictionnaire des critères de filtrage.

    Returns:
        pd.DataFrame: DataFrame filtré contenant les recettes correspondant aux critères.
    """
    filtered_df = df
    criteria = {'healthy': healthy,
                'season': season,
                'dish_type': dish_type,
                'prep_time': prep_time,
                'origin': origin,
                'categories': categories,
                'mood': cluster,
                'mood_manual' : mood_manual
                }

    # Appliquer les filtres un par un, seulement si le critère est spécifié et la colonne existe
    if criteria.get('healthy') is not None and 'healthy' in df.columns:
        filtered_df = filtered_df[filtered_df['healthy'] == criteria['healthy']]

    if criteria.get('season') is not None and criteria['season'] != 0 and 'season' in df.columns:
        filtered_df = filtered_df[filtered_df['season'] == criteria['season']]

    if criteria.get('dish_type') is not None and criteria['dish_type'] != 0 and 'dish_type' in df.columns:
        filtered_df = filtered_df[filtered_df['dish_type'] == criteria['dish_type']]

    if criteria.get('prep_time') is not None and criteria['prep_time'] != 0 and 'prep_time' in df.columns:
        filtered_df = filtered_df[filtered_df['prep_time'] == criteria['prep_time']]

    if criteria.get('origin') and 'origin' in df.columns:
        # Vérifier si l'origine correspond à l'une des origines listées dans la colonne
        filtered_df = filtered_df[filtered_df['origin'].str.lower().apply(
            lambda origins: criteria['origin'] in [o.strip() for o in origins.split(",")]
        )]

    if criteria.get('categories') and 'categories' in df.columns:
        # Vérifier si l'origine correspond à l'une des origines listées dans la colonne
        filtered_df = filtered_df[filtered_df['categories'].str.lower().apply(
            lambda categories: criteria['categories'] in [c.strip() for c in categories.split(",")]
        )]

    if criteria.get('mood') is not None and 'mood' in df.columns:
        # Extraire la valeur de mood
        mood_value = int(criteria['mood'][0]) if isinstance(criteria['mood'], list) else int(criteria['mood'])
        filtered_df = filtered_df[filtered_df['mood'] == mood_value ]

    if criteria.get('mood_manual') is not None and 'mood_manual' in df.columns:
        # Extraire la valeur de mood_manual
        mood_manual_value = int(criteria['mood_manual'][0]) if isinstance(criteria['mood_manual'], list) else int(criteria['mood_manual'])

        # Convertir les chaînes en listes si nécessaire pour mood_manual
        filtered_df['mood_manual'] = filtered_df['mood_manual'].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else x
        )

        # Appliquer le filtre "ou" sur mood et mood_manual
        filtered_df = filtered_df[filtered_df['mood_manual'].apply(lambda x: mood_manual_value in x)]

    return filtered_df
