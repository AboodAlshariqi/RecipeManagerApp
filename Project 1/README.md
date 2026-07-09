# Recipe Manager App

A digital recipe book built with Python and Streamlit. Store, search, scale, rate, and track your favorite recipes—all backed by a simple CSV file, no database required.

## Problem Statement

This app gives you one simple place to store your recipes, search them by ingredient, get random meal inspiration, and rate them based on what you liked the most.

## Features

### Core Features
- **Add a new recipe** — name, ingredients, prep time, instructions, and difficulty level
- **Search by ingredient** — find every recipe that uses a specific ingredient
- **View all recipes** — see every recipe's name and prep time at a glance
- **Random recipe suggestion and scaling** — can't decide what to cook? Let the app pick for you, adjust a random recipe's ingredient quantities to match your desired number of servings.
- **Categorization** — tag recipes as Breakfast, Lunch, Dinner, or Dessert, and browse by category
- **Ingredient scaling** — adjust any recipe's ingredient quantities to match your desired number of servings
- **Ratings** — rate recipes 1–5 stars and sort your collection by rating
- Cooking history — track recipes that have been cooked, record the number of times each recipe was made, and store the latest cooking date. The app can also suggest recipes that have not been cooked recently.
- Shopping list generation — select multiple recipes and automatically generate a combined shopping list by extracting ingredients and merging duplicate items with their total quantities.


## Tech Used

- **Python** — core logic
- **Streamlit** — interactive web interface
- **pandas** — data storage and manipulation
- **CSV** — persistent recipe storage, no database needed

## Project Structure

helper.py         # All core logic — functions for loading, saving, searching,
                   adding, rating, and scaling recipes
                    
recipeapp.py       # Streamlit app — the user interface
apprecipes.csv     # Recipe data storage (created automatically on first run)


## How to Run

1. Clone this repository
2. Install the required packages:
   pip install streamlit pandas
3. Run the app:
   streamlit run recipeapp.py
   Here is the link to the app (https://recipemanagerapp-fat37gqdwiqnaktktoevd7.streamlit.app/)




## Author

Abdulla Alsharqi
