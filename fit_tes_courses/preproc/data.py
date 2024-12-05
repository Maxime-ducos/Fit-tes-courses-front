import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from fit_tes_courses.preproc.filter.dish_type import map_recipe_type
from fit_tes_courses.preproc.filter.healthy_score  import calculate_healthy_score
from fit_tes_courses.preproc.filter.origin import map_origin
from fit_tes_courses.preproc.filter.season import map_season
from fit_tes_courses.preproc.filter.prep_time import  map_code_time
from fit_tes_courses.preproc.filter.categories import map_categories
from fit_tes_courses.preproc.mormalize_word import normalize_word
from fit_tes_courses.preproc.filter.mood import map_mood
from fit_tes_courses.preproc.filter.mood_manual import manual_mood

# from filter.string_to_liste import string_to_list

def preproc(df_recipes, df_reviews):
    # Définir les étapes du processus
    steps = [
        "Merge recipes and reviews",
        "Filter recipes with minimum reviews and ratings",
        "Remove cocktails",
        "Convert ingredients and tags to lists",
        "Split nutrition information into columns",
        "Calculate health scores",
        "Add origin information",
        "Add ingredient categories",
        "Add seasonal information",
        "Add dish types",
        "Add preparation time",
        "Calculate weighted scores",
        "Drop unnecessary columns",
        "Normalize ingredients"
    ]

    # Initialiser la barre de progression
    with tqdm(
        total=len(steps),
        desc="Processing DataFrame",
        unit="step",
        ncols=100,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
        dynamic_ncols=True,
        leave=True
    ) as pbar:
        # Étape 1 : Fusion des recettes et des reviews
        pbar.set_description(steps[-1])
        recipe_metrics = df_reviews.groupby('recipe_id').agg(
            num_reviews=('rating', 'count'),
            avg_rating=('rating', 'mean'),
            median_rating=('rating', 'median')
        ).reset_index()
        df = pd.merge(df_recipes, recipe_metrics, how='left', left_on='id', right_on='recipe_id')
        df.set_index('id', inplace=True)
        df[['num_reviews', 'avg_rating', 'median_rating']] = df[['num_reviews', 'avg_rating', 'median_rating']].fillna(0)
        pbar.update(1)

        # Étape 2 : Filtrer les recettes
        pbar.set_description(steps[0])
        min_vote = 5
        min_avg_rate = 4
        df = df[df['num_reviews'] > min_vote]
        df = df[df['avg_rating'] > min_avg_rate]
        pbar.update(1)

        # Étape 3 : Supprimer les cocktails, sauces, tea, dressing, coffee, alcoholic
        pbar.set_description(steps[1])
        cocktail_recipes = df[df['tags'].apply(lambda x: 'cocktails' in x)]
        df = df.drop(cocktail_recipes.index)
        sauce_recipes = df[df['name'].str.contains('sauce', case=False, na=False)]
        df = df.drop(sauce_recipes.index)
        tea_recipes = df[df['name'].str.contains('tea', case=False, na=False)]
        df = df.drop(tea_recipes.index)
        dressing_recipes = df[df['name'].str.contains('dressing', case=False, na=False)]
        df = df.drop(dressing_recipes.index)
        coffee_recipes = df[df['name'].str.contains('coffee', case=False, na=False)]
        df = df.drop(coffee_recipes.index)
        alcoholic_recipes = df[df['name'].str.contains('alcoholic', case=False, na=False)]
        df = df.drop(alcoholic_recipes.index)
        pbar.update(1)

        # Étape 4 : Convertir les colonnes en listes
        pbar.set_description(steps[2])
        def string_to_list(col_str):
            clean_str = col_str.strip("[]").replace("'", "")
            ingredients_list = [item.strip() for item in clean_str.split(',')]
            return ingredients_list
        df['ingredients'] = df['ingredients'].apply(string_to_list)
        df['tags'] = df['tags'].apply(string_to_list)
        pbar.update(1)

        # Étape 5 : Diviser les informations nutritionnelles
        pbar.set_description(steps[3])
        df[['calories','total fat (PDV)','sugar (PDV)','sodium (PDV)','protein (PDV)','saturated fat (PDV)','carbohydrates (PDV)']] = df.nutrition.str.split(",", expand=True)
        df['calories'] = df['calories'].apply(lambda x: x.replace('[', ''))
        df['carbohydrates (PDV)'] = df['carbohydrates (PDV)'].apply(lambda x: x.replace(']', ''))
        df[['calories','total fat (PDV)','sugar (PDV)','sodium (PDV)','protein (PDV)','saturated fat (PDV)','carbohydrates (PDV)']] = df[['calories','total fat (PDV)','sugar (PDV)','sodium (PDV)','protein (PDV)','saturated fat (PDV)','carbohydrates (PDV)']].astype('float')
        pbar.update(1)

        # Étape 6 : Calculer le score santé
        pbar.set_description(steps[4])
        df['Healthy Score'] = df.apply(calculate_healthy_score, axis=1)
        df['healthy'] = df['Healthy Score'].apply(lambda x: 1 if x >= 8 else 0)
        pbar.update(1)

        # Étape 7 : Ajouter l'origine
        pbar.set_description(steps[5])
        df['origin'] = df['tags'].apply(map_origin)
        pbar.update(1)

        # Étape 8 : Ajouter les catégories d'ingrédients
        pbar.set_description(steps[6])
        df['categories'] = df['tags'].apply(map_categories)
        pbar.update(1)

        # Étape 9 : Ajouter les informations saisonnières
        pbar.set_description(steps[7])
        df['season'] = df['tags'].apply(map_season)
        pbar.update(1)

        # Étape 10 : Ajouter les types de plats
        pbar.set_description(steps[8])
        # df['tags'] = df['tags'].apply(lambda ingredients: [normalize_word(ing) for ing in ingredients])
        df = map_recipe_type(df)
        pbar.update(1)

        # Étape 11 : Ajouter les temps de préparation
        pbar.set_description(steps[9])
        df['prep_time'] = df['minutes'].apply(map_code_time)
        pbar.update(1)

        # Étape 12 : Calculer les scores pondérés
        pbar.set_description(steps[10])
        Mean = df['avg_rating'].mean()
        def weighted_rating(x, min_vote=min_vote, Mean=Mean):
            v = x['num_reviews']
            R = x['avg_rating']
            return (v / (v + min_vote) * R) + (min_vote / (min_vote + v) * Mean)
        df['score'] = df.apply(weighted_rating, axis=1)
        pbar.update(1)

        # Étape 13 : Normaliser les ingrédients
        pbar.set_description(steps[11])
        df['ingredients'] = df['ingredients'].apply(lambda ingredients: [normalize_word(ing) for ing in ingredients])
        pbar.update(1)

        # Étape 14 : Concaténer les données textuelles (name, description, ingredients, tags)
        pbar.set_description(steps[12])
        df = map_mood(df)

        pbar.set_description(steps[13])
        df = df[df["n_ingredients"] > 2]
        df = manual_mood(df)


        # Étape 15 : Supprimer les colonnes inutiles
        columns_to_drop = [ 'contributor_id', 'submitted', 'nutrition', 'steps', 'total fat (PDV)',
                           'sugar (PDV)', 'sodium (PDV)', 'protein (PDV)',
                           'saturated fat (PDV)', 'carbohydrates (PDV)', 'Healthy Score']
        df_preproc = df.drop(columns=columns_to_drop)
        pbar.update(1)



    return df_preproc, df

def create_preproc_data():
    # Chemins relatifs
    output_dir = '../preproc_data'
    output_file1 = os.path.join(output_dir, 'df_preproc.csv')
    output_file2 = os.path.join(output_dir, 'df_reviews_preproc.csv')

    # Création du dossier `preproc_data` s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)

    # Chargement des données brutes
    df_reviews = pd.read_csv('../raw_data/RAW_interactions.csv')
    df_recipes = pd.read_csv('../raw_data/RAW_recipes.csv')

    # Traitement des données
    df = preproc(df_recipes, df_reviews)[0]
    # Extraire la liste de recipe_id depuis result2
    recipe_ids = df['recipe_id'].tolist()

# Filtrer les reviews relatives à ces recipe_ids
    df_reviews = df_reviews[df_reviews['recipe_id'].isin(recipe_ids)]

    # Sauvegarde du DataFrame dans le dossier `preproc_data`
    df.to_csv(output_file1, header=True, index=False)
    df_reviews.to_csv(output_file2, header=True, index=False)
    print(f"Nouveau DataFrame créé à  : {output_file1} ,{output_file2} ")
    return df

def create_full_preproc_data():
    # Chemins relatifs
    output_dir = '../preproc_data'
    output_file = os.path.join(output_dir, 'df_full_preproc.csv')

    # Création du dossier `preproc_data` s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)

    # Chargement des données brutes
    df_reviews = pd.read_csv('../raw_data/RAW_interactions.csv')
    df_recipes = pd.read_csv('../raw_data/RAW_recipes.csv')

    # Traitement des données
    df = preproc(df_recipes, df_reviews)[1]

    # Sauvegarde du DataFrame dans le dossier `preproc_data`
    df.to_csv(output_file, header=True, index=False)

    print(f"Nouveau DataFrame créé à  : {output_file}")
    return df
