import pandas as pd
from datetime import date

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

def search_by_ingredient(data,ingredient_search): # User stories 3
    """
    Returns recipes that contain the searched ingredient

    Parameters:
    data(dataframe):All recipes
    ingredient_search(str): Searching for ingredients

    Returns:
    matching_data(dataframe): the mathcing recipes of the ingredients searched

    """
    searching=data['ingredients'].str.contains(ingredient_search,case=False)
    matching_data=data[searching]
    return matching_data

def filter_by_category(data, category):
    """
    Displays recipes mathcing the category selected

    Parameters:
    data(dataframe):All recipes
    category(str): the categories written

    Returns:
    data(dataframe):All matching recipes

    """
    condition=data['category']==category
    matches=data[condition]
    return matches

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
    value:Easy,Medium,Hard

    Returns:
    is_valid***


    """
    allowed=['Easy','Medium','Hard']
    if value.title() in allowed:
        is_valid=True
    else:
        is_valid=False
    return is_valid
    
def add_recipe(data,name,ingredients,prep_time,instructions,difficulty,category): # User stories 2
    if not validate_difficulty(difficulty):
        return data
    new_id=generate_recipe_id(data)
    new_index=len(data)
    new_recipe= {'recipe_id':new_id,'name':name,'ingredients':ingredients,'prep_time':prep_time,'instructions':instructions,'difficulty':difficulty, 'category':category, 'servings':1, 'rating':0, 'times_cooked':0,'last_cooked_date':''}
    data.loc[new_index]=new_recipe
    return data

#Strech goal 3
def rate_recipe(data,recipe_id,rating):
    if rating<1 or rating>5:
        return data
    recipe=data['recipe_id']==recipe_id
    data.loc[recipe, "rating"]=rating
    return data

#strech goal3
def sort_by_rating(data):
    sorted_data=data.sort_values('rating', ascending=False)

    return sorted_data

#stretch goal 2

def split_ingredients(ingredient_str):
    ingredient_lst=[]
    comma=ingredient_str.split(',')
    for i in comma:
        part=i.strip().split(':')
        ingredient={'name':part[0], 'quantity':float(part[1]), 'unit':part[2]}
        ingredient_lst.append(ingredient)
    return ingredient_lst

def return_ingredients(ingredient_lst):
    lst=[]
    for ingredient in ingredient_lst:
        text=f"{ingredient['name']}:{ingredient['quantity']}:{ingredient['unit']}"
        lst.append(text)
    result=', '.join(lst)
    return result

def scale_recipe(ingredient_str,original_servings,desired_servings):
    if original_servings==0:
        return ingredient_str
    scale_factor=desired_servings/original_servings
    ingredients_lst=split_ingredients(ingredient_str)

    for ingredient in ingredients_lst:
        ingredient['quantity']=ingredient['quantity']*scale_factor

    scaled_string=return_ingredients(ingredients_lst)
    return scaled_string


    
    





    
