import pandas as pd
def map_origin(tags):
    region_keywords = {
        'American': [
            'american', 'north-american', 'south-american', 'southern-united-states',
            'northeastern-united-states', 'southwestern-united-states', 'midwestern',
            'tex-mex', 'californian', 'pacific-northwest', 'bbq', 'barbecue'
        ],
        'French': [
            'french', 'provence', 'parisian', 'bistro', 'brie', 'baguette', 'crepe',
            'ratatouille', 'croissant', 'souffle'
        ],
        'Asian': [
            'asian', 'chinese', 'japanese', 'thai', 'vietnamese', 'korean', 'indonesian',
            'malaysian', 'szechuan', 'cantonese', 'hunan', 'pakistani', 'philippine',
            'mongolian', 'ramen', 'sushi', 'kimchi'
        ],
        'Mexican': [
            'mexican', 'southwestern', 'baja', 'oaxacan', 'tacos', 'burritos', 'enchiladas',
            'quesadillas', 'guacamole', 'pozole', 'churros'
        ],
        'Italian': [
            'italian', 'pizza', 'pasta', 'spaghetti', 'lasagna',
            'risotto', 'gnocchi', 'bruschetta', 'focaccia', 'caprese'
        ],
        'Indian': [
            'indian', 'curry', 'masala', 'tikka', 'dal', 'naan', 'samosa', 'chai',
            'vindaloo', 'korma', 'paneer', 'biryani'
        ],
        'Mediterranean': [
            'mediterranean', 'greek', 'spanish', 'turkish', 'moroccan', 'lebanese',
            'israeli', 'falafel', 'hummus', 'paella', 'tapas', 'couscous'
        ],
        'African': [
            'african', 'south-african', 'north-african', 'ethiopian', 'nigerian',
            'moroccan', 'algerian', 'tunisian', 'kenyan', 'ghanaian', 'injera',
            'tagine', 'jollof'
        ],
        'Middle Eastern': [
            'middle-eastern', 'arabic', 'persian', 'iranian', 'syrian', 'palestinian',
            'iraqi', 'kuwaiti', 'saudi-arabian', 'lebanese', 'turkish', 'hummus',
            'falafel', 'shawarma', 'tabbouleh', 'baklava'
        ],
        'Caribbean': [
            'caribbean', 'jamaican', 'haitian', 'trinidadian', 'cuban', 'puerto-rican',
            'dominican', 'jerk', 'plantains', 'ackee', 'saltfish', 'rice-and-peas'
        ],
        'European': [
            'european', 'british', 'english', 'irish', 'scottish', 'welsh',
            'german', 'italian', 'french', 'spanish', 'portuguese', 'greek',
            'hungarian', 'polish', 'swiss', 'swedish', 'danish', 'norwegian',
            'russian', 'austrian', 'belgian', 'dutch', 'finnish', 'czech', 'slovakian'
        ],
        'Oceanian': [
            'australian', 'new-zealand', 'pacific', 'south-pacific', 'hawaiian',
            'polynesian', 'micronesian'
        ]
    }
    regions = []
    for tag in tags:
        tag_lower = tag.lower()  # Convertir le tag en minuscule
        for region, keywords in region_keywords.items():
            if any(keyword in tag_lower for keyword in keywords):
                regions.append(region)
    return ", ".join(set(regions)) or "Ordinary"  # Éliminer les doublons et retourner "Ordinary" si vide

# Appliquer la fonction à la colonne des tags
#df['Origin'] = df['tags'].apply(map_origin)
