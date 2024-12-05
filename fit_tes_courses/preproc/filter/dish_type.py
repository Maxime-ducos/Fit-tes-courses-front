# def map_recipe_type(row):
#     recipe_type_keywords = {
#         '1': [
#             'appetizer', 'hors d’oeuvre', 'starter', 'entrée', 'amuse-bouche', 'finger food',
#             'small plate', 'first course', 'snack', 'dip', 'canapé', 'crudités', 'antipasto'
#         ],

#         '3': [
#             'dessert', 'pudding', 'pastry', 'cake', 'ice cream', 'sorbet', 'pie', 'tart',
#             'mousse', 'custard', 'sweet', 'cookies', 'brownies', 'cheesecake', 'macarons',
#             'sundae', 'biscuit', 'doughnut', 'trifle'
#         ],
#         '4': [
#             'party', 'buffet', 'potluck', 'cocktail', 'celebration', 'gathering', 'festive',
#             'party food', 'snacks', 'finger food', 'party platter', 'canapé', 'nibbles',
#             'chips', 'popcorn', 'cheese board', 'charcuterie', 'crudités', 'tapas',
#             'mini sandwiches', 'cocktail sausages', 'punch', 'sliders', 'dips', 'wings',
#             'nachos', 'pizza bites', 'bite-sized'
#         ],
#             '2': [
#             'main course', 'entrée', 'meal', 'dish', 'side dish', 'main dish', 'platter',
#             'serving', 'second course', 'plate', 'portion', 'serving', 'course'
#         ]
#     }
#     # Combiner toutes les colonnes en une seule chaîne (ignorer les NaN)
#     combined_text = ' '.join(row.dropna().astype(str)).lower()
#     for recipe_type, keywords in recipe_type_keywords.items():
#         if any(keyword in combined_text for keyword in keywords):
#             return recipe_type
#     return 'None'

# # Application de la fonction à chaque ligne du DataFrame
# #df['code_type'] = df.apply(map_recipe_type, axis=1)
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier  # Import du modèle XGBoost

#0, entrée
#1, main course
#2, dessert
#3, apéritif

def map_recipe_type(df):
    # Charger les fichiers
    recipes_with_dish_type = pd.read_csv('../raw_data/df_manual_dishtype.csv')

    # Étape 1 : Préparation des données
    recipes_with_dish_type['text'] = (
        recipes_with_dish_type['name'].fillna('').apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x).replace('[', '').replace(']', '').replace("'", '')) + ' ' +
        recipes_with_dish_type['tags'].fillna('').apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x).replace('[', '').replace(']', '').replace("'", '')) + ' ' +
        recipes_with_dish_type['description'].fillna('') + ' ' +
        recipes_with_dish_type['ingredients'].fillna('').apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x).replace('[', '').replace(']', '').replace("'", ''))
    )

    df['text'] = (
        df['name'].fillna('').apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x).replace('[', '').replace(']', '').replace("'", '')) + ' ' +
        df['tags'].fillna('').apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x).replace('[', '').replace(']', '').replace("'", '')) + ' ' +
        df['description'].fillna('') + ' ' +
        df['ingredients'].fillna('').apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x).replace('[', '').replace(']', '').replace("'", ''))
    )

    # Extraire les colonnes pertinentes
    X = recipes_with_dish_type['text']
    y = recipes_with_dish_type['num_dish_type']

    # Vectorisation TF-IDF
    vectorizer = TfidfVectorizer(max_features=5000)
    X_tfidf = vectorizer.fit_transform(X)

    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

    # Étape 2 : Entraîner le modèle avec XGBoost
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)  # Modèle XGBoost
    model.fit(X_train, y_train)

    # Évaluer le modèle
    y_pred = model.predict(X_test)
    #print(classification_report(y_test, y_pred))

    # Étape 3 : Prédiction pour df_final_final
    df_tfidf = vectorizer.transform(df['text'])

    df['dish_type'] = model.predict(df_tfidf)
    return df
