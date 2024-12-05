from transformers import pipeline
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import pandas as pd
import os

# Télécharger les ressources nécessaires pour VADER
nltk.download('vader_lexicon')

def top_review_transformers_vader_textblob(df):
    df_reviews = pd.read_csv(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/preproc_data/df_reviews_preproc.csv')

    # Convertir les `recipe_id` en entier
    df['recipe_id'] = df['recipe_id'].astype(int)

    # Convertir la colonne en liste
    recipe_ids = df['recipe_id'].tolist()

    df_reviews = df_reviews[df_reviews['recipe_id'].isin(recipe_ids)]

    # Initialisation des analyseurs de sentiment
    sia = SentimentIntensityAnalyzer()


    df_reviews['vader_sentiment_score'] = df_reviews['review'].apply(lambda x: sia.polarity_scores(x)['compound'])
    df_reviews['textblob_sentiment_score'] = df_reviews['review'].apply(lambda x: TextBlob(x).sentiment.polarity)

    recipe_scores = df_reviews.groupby('recipe_id').agg({
        'vader_sentiment_score': 'mean',
        'textblob_sentiment_score': 'mean'
    }).reset_index()

    df = pd.merge(df, recipe_scores, on='recipe_id')

    top_5_vader = df.sort_values('vader_sentiment_score', ascending=False).head(5)
    top_5_textblob = df.sort_values('textblob_sentiment_score', ascending=False).head(5)
    return top_5_vader, top_5_textblob


def top_review_transformers(df):
    # Charger les données
    df_reviews = pd.read_csv('../preproc_data/df_reviews_preproc.csv')

    # Extraire la liste de recipe_id
    recipe_ids = df['recipe_id'].tolist()

    # Filtrer les reviews relatives à ces recipe_ids
    df_reviews = df_reviews[df_reviews['recipe_id'].isin(recipe_ids)]

    # Initialisation des analyseurs de sentiment
    sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    # Ajouter les scores pour chaque méthode
    def safe_transformer_score(review):
        try:
            return sentiment_analyzer(review)[0]['score']
        except Exception as e:
            print(f"Erreur lors du traitement avec Transformers : {e}")
            return 0.0

    df_reviews['transformer_sentiment_score'] = df_reviews['review'].apply(safe_transformer_score)

    # Calculer les moyennes des scores par recette
    recipe_scores = df_reviews.groupby('recipe_id').agg({
        'transformer_sentiment_score': 'mean'
    }).reset_index()

    # Fusionner avec les informations de la recette
    df = pd.merge(df, recipe_scores, on='recipe_id')

    # Générer 3 DataFrames pour les top 5 recettes de chaque méthode
    top_5_transformer = df.sort_values('transformer_sentiment_score', ascending=False).head(5)

    return top_5_transformer
