import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

def normalize_word(word):
    """
    Normalise un mot en utilisant la lemmatisation.

    Args:
        word (str): Mot à normaliser.

    Returns:
        str: Mot normalisé.
    """

    # Initialisation du lemmatizer
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(word.lower().strip())
