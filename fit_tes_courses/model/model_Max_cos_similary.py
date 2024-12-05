import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
# Créer une chaîne de caractères pour chaque liste d'ingrédients

def model_Max_cos_similary_recette(df, user_ingredients):
    df.copy()
    vectorizer = CountVectorizer()

    df['ingredients_str'] = df['ingredients'].apply(lambda x: ' '.join(x))
    ingredients_matrix = vectorizer.fit_transform(df['ingredients_str'])

    print("\nVotre liste d'ingrédients normalisée :", user_ingredients)
    user_ingredients_str = ' '.join(user_ingredients)
    user_vector = vectorizer.transform([user_ingredients_str])

    similarities = cosine_similarity(user_vector, ingredients_matrix).flatten()

    df['cosine_similarity'] = similarities


    # Trier par similarité cosinus, puis par nombre d'ingrédients correspondants
    df = df.sort_values(by='cosine_similarity', ascending=False).head(20)
    return df

def model_Max_cos_similary_ingrédients(df, user_ingredients):

    vectorizer = CountVectorizer()
    df.copy()

    df['ingredients_str'] = df['ingredients'].apply(lambda x: ' '.join(x))
    ingredients_matrix = vectorizer.fit_transform(df['ingredients_str'])

    print("\nVotre liste d'ingrédients normalisée :", user_ingredients)
    user_ingredients_str = ' '.join(user_ingredients)
    user_vector = vectorizer.transform([user_ingredients_str])

    similarities = cosine_similarity(user_vector, ingredients_matrix).flatten()

    similar_recipes_indices = similarities.argsort()[-10:][::-1]
    # Obtenir les indices des recettes similaires

    recommended_ingredients = []

    # Vérifier les indices avec `iloc`
    for index in similar_recipes_indices:
        try:
            recipe_ingredients = df.iloc[index]['ingredients']
            for ingredient in recipe_ingredients:
                if not any(user_ing.lower() in ingredient.lower() for user_ing in user_ingredients):
                    recommended_ingredients.append(ingredient)
        except IndexError:
            print(f"Index {index} invalide.")
            continue

    # Filtrer les doublons dans les recommandations
    filtered_ingredients = []
    for ingredient in recommended_ingredients:
        if not any(ingredient.lower() in other.lower() for other in recommended_ingredients if ingredient != other):
            filtered_ingredients.append(ingredient)

    return list(set(filtered_ingredients))

#tests
"""
df_final = pd.read_csv("/Users/maxdu/code/Maxime-ducos/Fit-tes-courses/raw_data/df_final_filtered.csv")

def string_to_list(col_str):
    clean_str = col_str.strip("[]").replace("'", "")
    ingredients_list = [item.strip() for item in clean_str.split(',')]
    return ingredients_list
df_final['ingredients'] = df_final['ingredients'].apply(string_to_list)


user_fridge = ['chocolat, rice','brocoli']
suggested_ingredients = model_Max_cos_similary(df_final, user_fridge)
print(suggested_ingredients)"""
