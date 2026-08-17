# Recipe Manager App

A digital recipe book built with Python and Streamlit. Store, search, scale, rate, and track your favorite recipes—all backed by a simple CSV file, no database required. It also connects to an online recipe API for new ideas, and to an LLM that suggests what to cook from what you already have.

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
- **Cooking history** — track recipes that have been cooked, record the number of times each recipe was made, and store the latest cooking date. The app can also suggest recipes that have not been cooked recently.
- **Shopping list generation** — select multiple recipes and automatically generate a combined shopping list by extracting ingredients and merging duplicate items with their total quantities.

### API Features
- **Search Online** — search [TheMealDB](https://www.themealdb.com/api.php) for new recipe ideas by dish name. Results show the meal photo, category, area of origin, and full instructions. No API key needed for this one.
- **Ask the AI Chef** — type in what you have in your kitchen and an LLM reads your saved recipe collection, picks the recipe that best matches, and tells you what you still need to buy. Runs through [OpenRouter](https://openrouter.ai/); requires an API key (see Setup below).

## DEMO and APP link

   Here is the link to the app (https://recipemanagerapp-ircwshrxwzc4wfhs49ecnh.streamlit.app/)

## Tech Used

- **Python** — core logic
- **Streamlit** — interactive web interface
- **pandas** — data storage and manipulation
- **CSV** — persistent recipe storage, no database needed
- **requests** — calls TheMealDB recipe API
- **openai** — client library used to reach the LLM through OpenRouter
- **python-dotenv** — loads the API key from a local `.env` file instead of hard-coding it

## Project Structure

```
functions.py          # All core logic — loading, saving, searching, adding, rating,
                      # scaling, cooking history, shopping list, and both API calls
recipemanagerapp.py   # Streamlit app — the user interface
apprecipes.csv        # Recipe data storage (created automatically on first run)
.env                  # Your API key (not committed — see Setup)
```

## How to Run

1. Clone this repository and open the `Project 1` folder.

2. Install the required packages. `requirements.txt` lives in the repository root:
   ```
   pip install -r ../requirements.txt
   ```

3. Set up your API key. Create a file named `.env` next to `recipemanagerapp.py` containing:
   ```
   OPENROUTER_KEY="your-key-here"
   ```
   Get a free key at [openrouter.ai/keys](https://openrouter.ai/keys).

   This step is only needed for the **Ask the AI Chef** feature. The other nine features work without it — the app will still run and simply show an error message inside that one section.

4. Run the app:
   ```
   streamlit run recipemanagerapp.py
   ```

## Notes

- `.env` is listed in `.gitignore` on purpose, so the API key is never pushed to GitHub. Anyone cloning this repository needs to create their own.
- Ingredients are stored in the format `name:quantity:unit`, separated by commas — for example `Flour:200:g, Milk:300:ml, Eggs:2:whole`. This is what allows the app to scale recipes and merge duplicate items into a shopping list.

## Author

Abdulla Alsharqi
