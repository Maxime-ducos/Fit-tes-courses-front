import pandas as pd
import numpy as np
import nltk
import logging
logging.getLogger('nltk').setLevel(logging.ERROR)
nltk.download('wordnet', quiet=True)
from nltk.stem import WordNetLemmatizer
import os
from fit_tes_courses.model.model_Max_cos_similary import model_Max_cos_similary_recette
#from preproc.filter.string_to_liste import string_to_list
#from model.model_by_substraction import find_recipes_with_fridge_ingredients
from fit_tes_courses.model.model_cosin_js import model_cosin_js
from fit_tes_courses.model.knn_model import find_similar_recipes

#from preproc.mormalize_word import normalize_word
from fit_tes_courses.missing_ingredients import create_df_with_common_ingredient


def recipe_recommendation_1(df, healthy, season, dish_type, prep_time, origin, categories,user_ingredients, mood, mood_manual):
    recipe_recommendation_1 = create_df_with_common_ingredient(df, user_ingredients)
    ingredients_1 = recipe_recommendation_1.get('ingredients', [])
    return {'recommended_recipe_1_as': ingredients_1}, recipe_recommendation_1

def recipe_recommendation_2(df, healthy, season, dish_type, prep_time, origin,categories, user_ingredients, mood, mood_manual):
    recipe_recommendation_2 = model_Max_cos_similary_recette(df, user_ingredients)
    recipe_recommendation_2 = create_df_with_common_ingredient(recipe_recommendation_2, user_ingredients)
    print(recipe_recommendation_2[['missing_ingredients', 'reused_ingredient' ]])

    ingredients_2 = recipe_recommendation_2.get('ingredients', [])
    return {'recipe_recommendation_2_md': ingredients_2}, recipe_recommendation_2

def recipe_recommendation_3(df, healthy, season, dish_type, prep_time, origin, categories, user_ingredients, mood, mood_manual):
    recipe_recommendation_3 = model_cosin_js(df, user_ingredients)
    recipe_recommendation_3 = create_df_with_common_ingredient(recipe_recommendation_3, user_ingredients)
    ingredients_3 = recipe_recommendation_3.get('ingredients', [])
    return {'recipe_recommendation_3_js': ingredients_3}, recipe_recommendation_3

def recipe_recommendation_4(df, healthy, season, dish_type, prep_time, origin,categories, user_ingredients, mood,mood_manual, n_neighbors=5):
    recipe_recommendation_4 = find_similar_recipes(df, user_ingredients, n_neighbors )
    recipe_recommendation_4 = create_df_with_common_ingredient(recipe_recommendation_4, user_ingredients)
    ingredients_4 = recipe_recommendation_4.get('ingredients', [])
    return {'recipe_recommendation_4_KNN': ingredients_4} , recipe_recommendation_4


# ATTENTION : METTRE EN COMMENTAIRE SI NON UTILISER
# Creation du nouveau DataFrame dans le dossier "preproc_data"


# from preproc.data import create_preproc_data, create_full_preproc_data
# print("Création du nouveau DataFrame...")
# print(create_preproc_data())


# print("Création du nouveau DataFrame...")
# print(create_full_preproc_data())

# Test Moedels

# healthy = None
# season =None
# dish_type =None
# prep_time =None
# origin =None
# categories = None
# user_ingredients = ["pasta", "chili", "chocolat", 'salsa']

# pd.set_option('display.max_colwidth', None)
# df = pd.read_csv('../preproc_data/df_preproc.csv')
# df['ingredients'] = df['ingredients'].apply(string_to_list)
# filtered_df = filter_dataframe(df, healthy, season, dish_type, prep_time, origin, categories)
# user_ingredients_normalized = [normalize_word(ingredient) for ingredient in user_ingredients]

# result1 = recipe_recommendation_1(df, healthy, season, dish_type, prep_time, origin, categories, user_ingredients_normalized)
# result2 = recipe_recommendation_2(df, healthy, season, dish_type, prep_time, origin, categories, user_ingredients_normalized)
# result3 = recipe_recommendation_3(df, healthy, season, dish_type, prep_time, origin, categories, user_ingredients_normalized)
# result4 = recipe_recommendation_4(df, healthy, season, dish_type, prep_time, origin, categories, user_ingredients_normalized, n_neighbors=5)
# print(result1)
# print("-" * 20)
# print(result2)
# print("-" * 20)
# print(result3)
# print("-" * 20)
# print(result4)


#df.to_csv("redf_final_filtered.csv", header=True, index=False)
