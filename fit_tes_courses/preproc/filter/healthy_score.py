# Fonction pour calculer le score Healthy
def calculate_healthy_score(row):
    score = 0

    # 1. Calories
    if row['calories'] < 400:
        score += 2
    elif 400 <= row['calories'] <= 600:
        score += 1
    # Sinon, 0 point (au-delà de 600 kcal)

    # 2. Graisses saturées (Saturated Fat)
    if row['saturated fat (PDV)'] < 5:
        score += 2
    elif 5 <= row['saturated fat (PDV)'] <= 10:
        score += 1
    # Sinon, 0 point (au-delà de 10% PDV)

    # 3. Sucres (Sugar)
    if row['sugar (PDV)'] < 5:
        score += 2
    elif 5 <= row['sugar (PDV)'] <= 10:
        score += 1
    # Sinon, 0 point (au-delà de 10% PDV)

    # 4. Sodium
    if row['sodium (PDV)'] < 5:
        score += 2
    elif 5 <= row['sodium (PDV)'] <= 10:
        score += 1
    # Sinon, 0 point (au-delà de 10% PDV)

    # 5. Protéines (Protein)
    if row['protein (PDV)'] >= 10:
        score += 2
    elif 5 <= row['protein (PDV)'] < 10:
        score += 1
    # Sinon, 0 point (en dessous de 5% PDV)

    return score

# df['Healthy Score'] = df.apply(calculate_healthy_score, axis=1)

# # Ajouter la classification basée sur le score
# df['Health Classification'] = df['Healthy Score'].apply(lambda x: 1 if x >= 8 else 0)

# # Appliquer la classification sur le score existant
# df['Health Classification'] = df['Healthy Score'].apply(classify_recipe)

# # Afficher un aperçu des données avec la nouvelle classification
# print(df[['calories', 'total fat (PDV)', 'sugar (PDV)', 'sodium (PDV)',
#                          'protein (PDV)', 'saturated fat (PDV)', 'Healthy Score', 'Health Classification']].head())
