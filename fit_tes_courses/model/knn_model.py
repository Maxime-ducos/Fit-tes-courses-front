import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
import joblib

def find_similar_recipes(df, search_words, n_neighbors=5):
    """
    Trouve les recettes les plus similaires à partir de la recherche d'ingrédients.
    Arguments:
    df -- DataFrame contenant les recettes et leurs ingrédients
    search_words -- Liste des mots d'ingrédients recherchés
    n_neighbors -- Nombre de voisins à retourner (par défaut 5)
    Retour:
    DataFrame contenant les recettes les plus proches avec leur distance
    """
    # Préparation des ingrédients sous forme de chaîne de texte
    df.copy()
    if df.shape[0]<5:
        return None
    else :
        df['ingredients_str'] = df['ingredients'].apply(lambda x: ', '.join(x))

        # Vectorisation des ingrédients
        vectorizer = CountVectorizer(tokenizer=lambda x: x.split(', '))  # Tokenizer séparant par virgules
        ingredient_matrix = vectorizer.fit_transform(df['ingredients_str'])

        # Transformer les mots de recherche de l'utilisateur en vecteur
        search_vector = vectorizer.transform([', '.join(search_words)])

        # Créer le modèle KNN
        knn = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')  # Utilisation de la distance cosine

        # Entraîner le modèle KNN sur les ingrédients
        knn.fit(ingredient_matrix)

        # Trouver les voisins les plus proches des search_words
        distances, indices = knn.kneighbors(search_vector)

        # Extraire les recettes correspondant aux indices
        df_selected_recipes = df.iloc[indices[0]]  # Indices des n voisins les plus proches
        df_selected_recipes['distance'] = distances[0]  # Ajouter les distances à df_selected_recipes

        return df_selected_recipes.head(20)

"""
Test
from fit_tes_courses.preproc.filter.string_to_liste import string_to_list
df = pd.read_csv('../../preproc_data/df_preproc.csv')
df['ingredients'] = df['ingredients'].apply(string_to_list)
user_ingredients = ["eggs", "banana", "chocolat", "celery"]
df_selected_recipes = find_similar_recipes(df, user_ingredients, n_neighbors=5)
print(df_selected_recipes)
"""
