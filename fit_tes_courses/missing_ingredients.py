# Liste des ingrédients communs
def list_common_ingredients_principal(recipe_ingredients, user_ingredients):
    return [ing for ing in recipe_ingredients if any(word in user_ingredients for word in ing.split())]

# Liste des ingrédients manquants
def list_missing_ingredients_principal(recipe_ingredients, user_ingredients):
    return [ing for ing in recipe_ingredients if all(word not in user_ingredients for word in ing.split())]

def create_df_with_common_ingredient(df,user_ingredients ):
    df['reused_ingredients'] = df['ingredients'].apply(
    lambda recipe_ingredients: list_common_ingredients_principal(recipe_ingredients, user_ingredients)
    )
    df['reused_ingredient'] = df['reused_ingredients'].apply(len)
    # Calcul des ingrédients communs

    df['missing_ingredients'] = df['ingredients'].apply(
        lambda recipe_ingredients: list_missing_ingredients_principal(recipe_ingredients, user_ingredients)
    )

    df['nbr_missing_ingredients_principal'] = df['missing_ingredients'].apply(len)

    df = df.sort_values(by=['reused_ingredient', 'nbr_missing_ingredients_principal'], ascending=[False, True]).reset_index()
    # Retourner les 10 premières recettes
    selected_columns = ['name', 'missing_ingredients','reused_ingredients',  'num_reviews', 'avg_rating', 'calories','minutes','mood', 'mood_manual', 'reused_ingredient', 'recipe_id']
    df = df[selected_columns]
    # Définir recipe_id comme index


    return df.head(10)



"""

# Liste des ingrédients manquants
def liste_missing_ingredients_exact(recipe_ingredients, user_ingredients ):
    return [ing for ing in recipe_ingredients if ing not in user_ingredients]

def liste_common_ingredients_exact(recipe_ingredients, user_ingredients ):
    return [ing for ing in recipe_ingredients if ing in user_ingredients]

df['common_ingredients_exact'] = df['ingredients'].apply(
        lambda recipe_ingredients: liste_common_ingredients_exact(recipe_ingredients, user_ingredients)
    )
df['nbr_common_ingredients_exact'] = df['common_ingredients_exact'].apply(len)
    # Calcul des ingrédients manquants
df['missing_ingredients_exact'] = df['ingredients'].apply(
        lambda recipe_ingredients: liste_missing_ingredients_exact (recipe_ingredients, user_ingredients)
)
df['nbr_missing_ingredients_exact'] = df['missing_ingredients_exact'].apply(len)

# Affichage des colonnes sélectionnées
df_exact = df[['ingredients', 'missing_ingredients_principal', 'nbr_missing_ingredients_principal', 'missing_ingredients_exact', 'nbr_missing_ingredients_exact']]
"""
