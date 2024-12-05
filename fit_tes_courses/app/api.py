import os
import pandas as pd
from fastapi import FastAPI, Query
from typing import List, Optional
# from fit_tes_courses.model.model_by_substraction import find_recipes_with_fridge_ingredients
from fit_tes_courses.app.recipe_global_filter import filter_dataframe
from fastapi.responses import FileResponse
from fit_tes_courses.main import recipe_recommendation_1, recipe_recommendation_2, recipe_recommendation_3, recipe_recommendation_4
from fit_tes_courses.preproc.filter.string_to_liste import string_to_list
from fit_tes_courses.preproc.mormalize_word import normalize_word
from fastapi.responses import JSONResponse
from fit_tes_courses.model.top_reviews_positivity_by_bert import top_review_transformers_vader_textblob #top_review_transformers


"""
Launch the API: uvicorn app.api:app --reload
"""

app = FastAPI()

# Define a root `/` endpoint
@app.get('/')
def index():
    return {'oki': True}

@app.get('/predict')
def predict(
    user_ingredients: List[str] = Query(..., description="Liste des ingrédients disponibles"),
    healthy: Optional[int] = Query(None, description="Option healthy : 0=No, 1=Yes"),
    season: Optional[int] = Query(None, description="Saison : 0=Any, 1=Spring, 2=Summer, 3=Winter, 4=Fall"),
    dish_type: Optional[int] = Query(None, description="Type de plat : 0=Any, 1=Starter, 2=Main course, 3=Dessert, 4=Snack"),
    prep_time: Optional[int] = Query(None, description="Temps de préparation : 0=Any, 1=-15 min, 2=15-30 min, 3=30-60 min, 4=1-2h"),
    origin: Optional[str] = Query(None, description="Origine du plat : Ordinary, American, Italian, African..."),
    categories: Optional[str] = Query(None, description="Categorie : Vegan, Sans œufs, Végétarien, Sans lactose, Sans gluten"),
    mood: List[str] = Query(None, description="Mood : 2=Copieux & Généreux, 3=Réconfortant & Familier,   4=Salé & Polyvalent ,0=Sucré & Gourmand , 1 = Sain & Léger"),
    mood_manual : List[str] = Query(None, description= "Mood_manual : Gourmand & Savoureux = 0, Confort & Réconfortant = 1, Sain & Équilibré = 2 , Familial / Convivial = 3, Épicé / Intense = 4, Festif / Ludique =5 , Fruité / Rafraîchissant = 6, Aphrodisiaque / Envoûtant = 7, Exotique / Curieux = 8, Énergisant / Vitalisant = 9")
    ):
    # Compute recommended_recipe from user parameters
    # Load the recipes dataframe
    df = pd.read_csv(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/preproc_data/df_preproc.csv')

    df['ingredients'] = df['ingredients'].apply(string_to_list)

    filtered_df = filter_dataframe(df, healthy, season, dish_type, prep_time, origin, categories, mood, mood_manual)

    user_ingredients_normalized = [normalize_word(ingredient) for ingredient in user_ingredients]


    result1 = recipe_recommendation_1(filtered_df, healthy, season, dish_type, prep_time, origin,categories, user_ingredients_normalized, mood, mood_manual)
    result2 = recipe_recommendation_2(filtered_df, healthy, season, dish_type, prep_time, origin,categories, user_ingredients_normalized, mood, mood_manual)
    result4 = recipe_recommendation_4(filtered_df, healthy, season, dish_type, prep_time, origin,categories, user_ingredients_normalized, mood, mood_manual, n_neighbors=5)
    result3 = recipe_recommendation_3(filtered_df, healthy, season, dish_type, prep_time, origin, categories, user_ingredients_normalized, mood, mood_manual)
    dfs=[result1[1], result2[1], result3[1], result4[1]]
    combined_df = pd.concat(dfs).drop_duplicates(subset="recipe_id").reset_index(drop=True).sort_values(by='num_reviews', ascending=False)
    #combined_df.to_csv("combined_results.csv", header=True, index=False)


    result_json1 = result1[1].to_dict(orient="records")
    result_json2 = result2[1].to_dict(orient="records")
    result_json3 = result3[1].to_dict(orient="records")
    result_json4 = result4[1].to_dict(orient="records")
    result_combined_df = combined_df.to_dict(orient="records")

    top_5_vader, top_5_textblob = top_review_transformers_vader_textblob(combined_df)
    #top_5_transformer = top_review_transformers(combined_df)

    # Convertir les DataFrames des tops 5 en JSON
    #top_5_transformer_json = top_5_transformer.to_dict(orient="records")
    top_5_vader_json = top_5_vader.to_dict(orient="records")
    top_5_textblob_json = top_5_textblob.to_dict(orient="records")

    # Retourner les résultats en JSON
    return JSONResponse(content={
        "result1": result_json1,
        "result2": result_json2,
        "result3": result_json3,
        "result4": result_json4,
        "result_combined_df": result_combined_df,
        #"top_5_transformer": top_5_transformer_json,
        "top_5_vader": top_5_vader_json,
        "top_5_textblob": top_5_textblob_json
    })




    # Filter the recipes based on the user criteria
    #filtered_df = filter_dataframe(df, healthy, season, dish_type, prep_time, origin)

    # Recommend the best recipes based on the user's ingredients and criteria testing 3 models
    # Model 1: by substraction
    #recipe_recommendation_1 = find_recipes_with_fridge_ingredients(filtered_df, user_ingredients)
    #ingredients_1 = recipe_recommendation_1.get('ingredients', [])
    # Model 2: cosine
    #recipe_recommendation_2 =
    #ingredients_2 = recipe_recommendation_2.get('ingredients', [])

    # Model 3: KNN
    #recipe_recommendation_3 =
    #ingredients_3 = recipe_recommendation_2.get('ingredients', [])


    #return {'recommended_recipe_1': ingredients_1,
            #'recommended_recipe_2': ingredients_2,
            #'recommended_recipe_3': ingredients_3,
            #}
