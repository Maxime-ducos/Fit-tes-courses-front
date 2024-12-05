
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import os

def map_mood(df):
    df['name'] = df['name'].fillna('')
    df['tags'] = df['tags'].fillna('')
    df['ingredients'] = df['ingredients'].fillna('')
    df['description'] = df['description'].fillna('')
    def concat_columns_to_text(row):
        # Fonction pour transformer une colonne en texte
        def column_to_text(value):
            if isinstance(value, list):  # Si la valeur est une liste, on joint les éléments par un espace
                return " ".join(map(str, value))
            elif isinstance(value, str):  # Si c'est une chaîne, on la retourne telle quelle
                return value
            else:  # Si c'est NaN ou autre, retourner une chaîne vide
                return ""

        # Concaténer les colonnes
        name_text = column_to_text(row['name'])
        tags_text = column_to_text(row['tags'])
        ingredients_text = column_to_text(row['ingredients'])
        description_text = column_to_text(row['description'])

        return f"{name_text} {tags_text} {ingredients_text} {description_text}".strip()

    # Appliquer cette fonction à chaque ligne du DataFrame
    df['text'] = df.apply(concat_columns_to_text, axis=1)

    # Etape 15 : Préparer la vectorisation TF-IDF de la colonne 'text'
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(df['text'])

    # Etape 16 : PCA - Appliquer la PCA pour réduire à 200 dimensions
    pca = PCA(n_components=200, random_state=42)
    X_pca = pca.fit_transform(X.toarray())  # Convertir X en tableau dense car PCA ne supporte pas les matrices sparse

    # Étape 4 : Charger les centroïdes sauvegardés
    centroids = np.load(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + '/raw_data/kmeans_centroids.npy')

    # Étape 5 : Initialiser le modèle K-Means avec les centroïdes pré-sauvegardés
    kmeans = KMeans(n_clusters=len(centroids), init=centroids, n_init=1, random_state=42)

    df['mood'] = kmeans.fit_predict(X)
    return df
