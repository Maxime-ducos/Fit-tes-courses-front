
def string_to_list(col_str):
    clean_str = col_str.strip("[]").replace("'", "")
    ingredients_list = [item.strip() for item in clean_str.split(',')]
    return ingredients_list
