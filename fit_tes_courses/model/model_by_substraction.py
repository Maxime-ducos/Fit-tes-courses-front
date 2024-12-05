
def find_recipes_with_fridge_ingredients(df, user_ingredients):
    """
    Trouve les recettes réalisables avec les ingrédients disponibles dans le frigo de l'utilisateur,
    et les classe par le nombre d'ingrédients en commun, puis par le nombre d'ingrédients manquants.

    Args:
        df (pd.DataFrame): DataFrame contenant les recettes. Doit inclure une colonne 'ingredients' (listes d'ingrédients).

    Returns:
        pd.DataFrame: Les 10 premières recettes triées par priorité.
    """

    # Calculer le nombre d'ingrédients en commun
    def count_common_ingredients(recipe_ingredients):
        return len([ing for ing in recipe_ingredients if ing in user_ingredients])

    df['common_ingredients'] = df['ingredients'].apply(count_common_ingredients)

    # Calculer le nombre d'ingrédients manquants
    def count_missing_ingredients(recipe_ingredients):
        return len([ing for ing in recipe_ingredients if ing not in user_ingredients])

    df['missing_ingredients'] = df['ingredients'].apply(count_missing_ingredients)

    # Filtrer les recettes pour garder uniquement celles avec au moins un ingrédient commun
    df = df[df['common_ingredients'] > 0]
    # Trier les recettes :
    # 1. Par nombre d'ingrédients en commun (décroissant)
    # 2. Par nombre d'ingrédients manquants (croissant)
    df_sorted = df.sort_values(by=['common_ingredients', 'missing_ingredients'], ascending=[False, True]).reset_index()
    # Retourner les 10 premières recettes
    return df_sorted.head(10)


#tests
#df_final = pd.read_csv("../raw_data/df_final.csv")
#df_final['ingredients'] = df_final['ingredients'].apply(ast.literal_eval)

#def string_to_list(col_str):
    #clean_str = col_str.strip("[]").replace("'", "")
    #ingredients_list = [item.strip() for item in clean_str.split(',')]
    #return ingredients_list
#df_final['ingredients'] = df_final['ingredients'].apply(string_to_list)

#result = find_recipes_with_fridge_ingredients(df_final)
#print("result", result)
