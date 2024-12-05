# Importer les bibliothèques nécessaires
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier  # Import du modèle XGBoost
import os

def manual_mood(df):
    #intégration fichier excel Jeremy
    mood = pd.read_csv(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + '/raw_data/402_recettes_mood_manual_input.csv', sep=';')
    mood.columns = mood.columns.str.strip()  # Supprime les espaces au début/fin

    # sélection de recette de df_preproc et merge avec les moods
    df_mood = pd.merge(df, mood, on='name', how='right')
    moods_liste = [
        "Gourmand / Savoureux", "Sain / Équilibré", "Exotique / Curieux",
        "Confort / Réconfortant", "Festif / Ludique", "Épicé / Intense",
        "Fruité / Rafraîchissant", "Familial / Convivial", "Énergisant / Vitalisant", "Aphrodisiaque / Envoûtant"
    ]
    # Nettoyer la colonne Mood (supprimer les espaces et les valeurs vides)
    df_mood['Mood'] = df_mood['Mood'].str.split(',')
    # Créer des colonnes pour chaque mood
    for mood in moods_liste:
        df_mood[mood] = df_mood['Mood'].apply(lambda x: 1 if mood in x else 0)

    # Remplacer les NaN dans la colonne 'text'
    df_mood['text'] = df_mood['text'].fillna('')
    # Stocker les résultats pour chaque mood
    vectorizers = {}
    models = {}
    for mood in moods_liste:
        # Définir X et y
        X = df_mood['text']
        y = df_mood[mood]  # La colonne correspondant au mood actuel
        vectorizer = TfidfVectorizer(max_features=5000)
        X_tfidf = vectorizer.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)
        model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        vectorizers[mood] = vectorizer
        models[mood] = model

    for mood in moods_liste:
        df_tfidf = vectorizers[mood].transform(df['text'])
        df[mood] = models[mood].predict(df_tfidf)
    # Dictionnaire des correspondances

    mood_mapping = {
        "Gourmand / Savoureux": 0,
        "Confort / Réconfortant": 1,
        "Sain / Équilibré": 2,
        "Familial / Convivial": 3,
        "Épicé / Intense" : 4,
        "Festif / Ludique": 5,
        "Fruité / Rafraîchissant": 6,
        "Aphrodisiaque / Envoûtant": 7,
        "Exotique / Curieux" : 8 ,
        "Énergisant / Vitalisant": 9
        }

# Nouvelle colonne pour stocker la liste des moods
    df['mood_manual'] = df.apply(lambda row: [
        numeric_value for mood, numeric_value in mood_mapping.items() if row[mood] == 1
    ], axis=1)


    return df
