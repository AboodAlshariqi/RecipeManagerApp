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

    
#=================
# COOKING HISTORY
#=================

def mark_as_cooked(data,recipe_id,cooked_date=None):
    """
    Updates the cooking history of a recipe.

    Parameter:
    data(dataframe):All recipes
    recipe_id(int): ID of the recipe that was cooked
    cooked_date(date): Date the recipe was cooked. If not provided use today's date

    Returns:
    data(dataframe):All recipes with the updated cooking count and last cooked date
    """
    if cooked_date is None:
        cooked_date=str(date.today())
    for index in data.index:
        if data.loc[index, 'recipe_id']==recipe_id:
            data.loc[index, 'times_cooked']=data.loc[index, 'times_cooked']+1
            data.loc[index,'last_cooked_date']=cooked_date
    return data

def suggest_stale_recipes(data, days_threshold=30):

    """
    Finds recipes that have never been cooked or have not been cooked recently (30 days)

    Parameter:
    data(dataframe):All recipes
    days_threshold(int): Number of days after which a recipe is considered stale
    
    Returns:
    stale(dataframe): Recipes that needs to be cooked again
    """
    dates=pd.to_datetime(data['last_cooked_date'], format='mixed', errors='coerce')
    never_cooked=dates.isna()
    today=pd.to_datetime(date.today())
    days_since_cooked=(today-dates).dt.days
    not_cooked_recently=days_since_cooked>days_threshold
    stale_recipes=[]
    
    for index in data.index:
        if never_cooked[index] or not_cooked_recently[index]:
            stale_recipes.append(index)

    stale=data.loc[stale_recipes]
    return stale    

    
#=================
# SHOPPING LIST
#=================
def generate_shopping_list(data, recipe_ids):

    """
    Generates a list of ingredients from selected recipes.

    Parameters:
    data(dataframe): All recipes
    recipe_ids(list): List of recipe IDs selected by the user

    Returns:
    all_ingredients(list): List containing all ingredients from selected recipes
    """
    all_ingredients=[]

    for recipe_id in recipe_ids:
        for index in data.index:
            
            if data.loc[index,'recipe_id']==recipe_id:
                ingredient_string=data.loc[index,'ingredients']
                ingredient_list=split_ingredients(ingredient_string)
                all_ingredients.extend(ingredient_list)
                break

    return all_ingredients


def merge_ingredients(ingredient_list):

    """
    Combines duplicated ingredients and calculates the total quantity required.

    Parameters:
    ingredient_list(list): List of ingredient dictionaries containing name, quantity, and unit

    Returns:
    result(list): Combined ingredient list with total quantities
    """
    
    ingredients_df=pd.DataFrame(ingredient_list)
    combined=ingredients_df.groupby(['name','unit'],as_index=False)['quantity'].sum()
    result=combined.to_dict('records')
    return result




    
