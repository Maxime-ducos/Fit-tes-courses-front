import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
#from rapidfuzz import fuzz
from nltk.corpus import stopwords

# Charger le DataFrame
#df = joblib.load('df_final.pkl')
#print(df["ingredients"])

def model_cosin_js(df, search_words):
    # Initialisation des stopwords


    df.copy()
    # Créer un vecteur de recherche pour les ingrédients utilisateur
    vectorizer = CountVectorizer(tokenizer=lambda x: x.split(','))
    ingredient_matrix = vectorizer.fit_transform(df['ingredients'].apply(lambda x: ', '.join(x)))

    # Créer un vecteur pour les ingrédients utilisateur
    user_vector = vectorizer.transform([', '.join(search_words)])

    # Calculer la similarité cosinus entre le vecteur utilisateur et la matrice des ingrédients
    cosine_sim = cosine_similarity(user_vector, ingredient_matrix)

    # Ajouter la similarité cosinus aux recettes filtrées
    df['cosine_similarity'] = cosine_sim[0]
    df = df.sort_values(by='cosine_similarity', ascending=False).head(30)

    return df

"""
    # Fonction pour calculer le nombre d'ingrédients manquants par rapport aux mots recherchés
    def count_ingredients_not_in_search(ingredients, search_words):
        # Convertir les ingrédients en un ensemble de mots uniques
        ingredients_set = set(word.lower() for word in ingredients)

        # Compter le nombre de mots de ingredients_set qui ne sont pas dans search_words
        missing_count = sum(1 for word in ingredients_set if word not in [search_word.lower() for search_word in search_words])

        return missing_count


    # Appliquer la fonction pour calculer le nombre d'ingrédients non présents dans search_words
    df['missing_ingredients_count'] = df['cleaned_ingredients'].apply(lambda x: count_ingredients_not_in_search(x, search_words))

    df['missing_ingredients_count']

    # Calculer 'count_word', l'écart entre les mots de la recette et les mots recherchés
    df['count_word'] = df['ingredients_words'].apply(lambda x: len(x) - len(search_words))

    # Trier les recettes d'abord par le nombre d'ingrédients manquants (ordre croissant), puis par la similarité cosinus (ordre décroissant)
    df_sorted = df.sort_values(by=['missing_ingredients_count', 'cosine_similarity', 'count_word'], ascending=[True, False, True])
"""

    # Afficher les résultats finaux


# Définir les mots recherchés
"""
df_final = pd.read_csv("/Users/maxdu/code/Maxime-ducos/Fit-tes-courses/raw_data/df_final_filtered.csv")

def string_to_list(col_str):
    clean_str = col_str.strip("[]").replace("'", "")
    ingredients_list = [item.strip() for item in clean_str.split(',')]
    return ingredients_list
df_final['ingredients'] = df_final['ingredients'].apply(string_to_list)


search_words = ["onion", "salad", "salt"]
suggested_ingredients = model_cosin_js(df_final, search_words)
print(suggested_ingredients)
"""
