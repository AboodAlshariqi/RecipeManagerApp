import pandas as pd
from datetime import date

# ================
# FILE MANAGEMENT
# ================

def load_recipes(filepath): 
    """
    Loads recipes from CSV file, create one if it doesn't exist.

    Parameters:
    filepath(str): Path to the CSV file

    Returns:
    data(dataframe):The recipes in the csv file

    """
    columns=['recipe_id','name','ingredients','prep_time','instructions','difficulty', 'category', 'servings', 'rating', 'times_cooked','last_cooked_date']

    try:
        data=pd.read_csv(filepath)
    except FileNotFoundError:
        data=pd.DataFrame(columns=columns)
        data.to_csv(filepath, index=False)

    return data
    
def save_recipes(data, filepath):
    """
    Saves the current recipes to a CSV file

    Parameters:
    data(dataframe):The recipes to save
    filepath(str):The path to send the CSV file to


    """
    data.to_csv(filepath, index=False)

#===============
# VIEW RECIPES
#===============

def get_all_recipes_summary(data): # User stories 4
    """
    Displays the name and prep_time of every recipe

    Parameters:
    data(dataframe): All recipes

    Returns:
    summary(dataframe): name and prep_time of every recipe

    """
    summary=data[['name', 'prep_time']]
    return summary
    
def get_random_recipe(data): # User stories 5
    """
    Returns a random recipe

    Parameters:
    data(dataframe):All recipes

    Returns:
    recipe(dataframe): One random recipe

    """
    recipe=data.sample()
    return recipe
    
#==================
# SEARCHING RECIPES
#==================

def search_by_ingredient(data,ingredient_search): # User stories 3
    """
    Returns recipes that contain the searched ingredient

    Parameters:
    data(dataframe):All recipes
    ingredient_search(str): Searching for ingredients

    Returns:
    matching_data(dataframe): the matching recipes of the ingredients searched

    """
    searching=data['ingredients'].str.contains(ingredient_search,case=False)
    matching_data=data[searching]
    return matching_data

def filter_by_category(data, category):
    """
    Displays recipes matching the category selected

    Parameters:
    data(dataframe):All recipes
    category(str): the categories written

    Returns:
    matches(dataframe):All matching recipes

    """
    condition=data['category']==category
    matches=data[condition]
    return matches

#===============
# ADDING RECIPES
#===============


def generate_recipe_id(data): # Helper for User stories 2 id part
    """
    Generates new recipe id

    Parameters:
    data(dataframe):All recipes

    Returns:
    new_id(int): new id


    """
    if data.empty:
        new_id=1
    else:
        new_id=data['recipe_id'].max()+1
    return new_id

def validate_difficulty(value): # Helper for User stories 2 difficulties part
    """
    Checks if a difficulty is Easy, Medium, or Hard

    Parameters:
    value:'Easy,Medium,Hard' entered by the user

    Returns:
    is_valid(bool): True if the difficulty is valid


    """
    allowed=['Easy','Medium','Hard']
    if value.title() in allowed:
        is_valid=True
    else:
        is_valid=False
    return is_valid
    
def add_recipe(data,name,ingredients,prep_time,instructions,difficulty,category): # User stories 2
    """
    Adds a new recipe to the collection

    Parameters:
    data(dataframe):All recipes
    name(str): Recipe name
    ingredients(str): The ingredients in the format name:quantity:unit
    prep_time(int): Preparation time in minutes
    instructions(str): Cooking instructions
    difficulty(str): Easy,Medium, or Hard
    category(str): The recipe category

    Returns:
    data(dataframe):All recipes in addition to the new recipe added
    """
    if not validate_difficulty(difficulty):
        return data
    new_id=generate_recipe_id(data)
    new_index=len(data)
    new_recipe= {'recipe_id':new_id,'name':name,'ingredients':ingredients,'prep_time':prep_time,'instructions':instructions,'difficulty':difficulty, 'category':category, 'servings':1, 'rating':0, 'times_cooked':0,'last_cooked_date':''}
    data.loc[new_index]=new_recipe
    return data

#================
# RECIPES RATING
#================

def rate_recipe(data,recipe_id,rating):
    """
    Sets the rating for the selected recipe

    Parameters:
    data(dataframe):All recipes
    recipe_id(int): The id of the recipe to rate
    rating(int): The rating from 1 to 5 stars

    Returns:
    data(dataframe):All recipes with the updated rating

    """
    if rating<1 or rating>5:
        return data
    recipe=data['recipe_id']==recipe_id
    data.loc[recipe, "rating"]=rating
    return data

def sort_by_rating(data):
    """
    Sorts recipes by rating from highest to lowest

    Parameters:
    data(dataframe):All recipes

    Returns:
    sorted_data(dataframe): Recipes sorted by rating
    
    """
    sorted_data=data.sort_values('rating', ascending=False)

    return sorted_data

#=================
# SCALING RECIPES
#=================

def split_ingredients(ingredient_str):
    """
    Convert ingredients string to a list of dictionaries (ingredients,quantity,unit)

    Parameters:
    ingredient_str(str): Ingredients in the format of name:quantity:unit separated by a comma

    Returns:
    ingredient_lst(list): A list of dictionaries with the format of name,quantity,unit

    """
    ingredient_lst=[]
    for i in ingredient_str.split(','):
        part=i.strip().split(':')
        ingredient={'name':part[0], 'quantity':float(part[1]), 'unit':part[2]}
        ingredient_lst.append(ingredient)
    return ingredient_lst

def return_ingredients(ingredient_lst):
    """
    Combines a list of ingredients into one string

    Parameters:
    ingredient_lst(list): A list of dictionaries with the format of name,quantity,unit

    Returns:
    result(str): The combined ingredients string

    """
    lst=[]
    for ingredient in ingredient_lst:
        text=f"{ingredient['name']}:{ingredient['quantity']}:{ingredient['unit']}"
        lst.append(text)
    result=', '.join(lst)
    return result

def scale_recipe(ingredient_str,original_servings,desired_servings):
    """
    Scales the ingredients of a recipe based on the selected number

    Parameters:
    ingredients_str(str): The original ingredients string
    original_servings(int): The recipe's original number of servings
    desired_servings(int): The number of servings to scale to

    Returns:
    scaled_string(str): The scaled ingredients string


    """
    if original_servings==0:
        return ingredient_str
    scale_factor=desired_servings/original_servings
    ingredients_lst=split_ingredients(ingredient_str)

    for ingredient in ingredients_lst:
        ingredient['quantity']=ingredient['quantity']*scale_factor

    scaled_string=return_ingredients(ingredients_lst)
    return scaled_string

    
    





    
