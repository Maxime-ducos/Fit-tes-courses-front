import pandas as pd

def map_categories(ingredients):


    categories_keyword = {
        'Végétarien': [
            'vegetarian'],
        'Vegan': [
            'vegan'],
        'Sans gluten': [
            'gluten-free'],
        'Sans œufs': [
            'egg-free', 'vegan'],
        'Sans lactose': [
            'lactose-free']
    }

    matched_categories = []
    for ingredient in ingredients:
        ingredient_lower = ingredient.lower()  # Convertir l'ingrédient en minuscule
        for category, keywords in categories_keyword.items():
            if any(keyword in ingredient_lower for keyword in keywords):
                matched_categories.append(category)
    return ", ".join(set(matched_categories)) or "Normal"  # Éliminer les doublons et retourner "Normal" si vide

#df_recipes['categories'] = df_recipes['ingredients'].map(classify_ingredients)

"""
    categories_keyword = {
        'Végétarien': [
            'vegetarian', 'tofu', 'paneer', 'vegetables', 'salad', 'lentils', 'legumes',
            'beans', 'pasta', 'quinoa', 'bulgur', 'chickpeas', 'veggie', 'soy', 'tempeh',
            'mushrooms', 'meat-free', 'dahl', 'eggplant', 'zucchini', 'avocado', 'cheese'
        ],
        'Vegan': [
            'vegan', 'plant-based', 'tofu', 'tempeh', 'seitan', 'lentils', 'beans',
            'chickpeas', 'quinoa', 'soy milk', 'almond milk', 'coconut milk', 'vegan cheese',
            'vegan butter', 'cashew cream', 'vegetables', 'fruits', 'greens', 'hummus',
            'falafel', 'dairy-free', 'egg-free'
        ],
        'Sans gluten': [
            'gluten-free', 'quinoa', 'rice', 'corn', 'polenta', 'buckwheat', 'millet',
            'sorghum', 'tapioca', 'arrowroot', 'gluten-free bread', 'gluten-free pasta',
            'potatoes', 'cassava', 'gluten-free flour', 'amaranth', 'legumes', 'lentils',
            'meat', 'seafood', 'vegetables', 'fruits', 'chia seeds', 'flaxseed'
        ],
        'Sans œufs': [
            'egg-free', 'vegan', 'tofu', 'applesauce', 'mashed banana', 'chia seeds',
            'flaxseed', 'egg replacer', 'baking powder', 'cornstarch', 'arrowroot', 'agar',
            'custard powder', 'potato starch', 'yogurt', 'cream cheese', 'non-dairy yogurt'
        ],
        'Sans lactose': [
            'lactose-free', 'dairy-free', 'almond milk', 'soy milk', 'coconut milk',
            'oat milk', 'rice milk', 'cashew milk', 'lactose-free cheese', 'lactose-free butter',
            'lactose-free yogurt', 'vegan cheese', 'vegan butter', 'coconut cream',
            'sorbet', 'lactose-free ice cream', 'tofu', 'plant-based cream'
        ]
    }
"""
