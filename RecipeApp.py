import streamlit as st
from helper import load_recipes, get_all_recipes_summary, get_random_recipe, search_by_ingredient,add_recipe,save_recipes,filter_by_category,rate_recipe,sort_by_rating,split_ingredients,return_ingredients,scale_recipe


# Load recipe from CSV
recipes = load_recipes("apprecipes.csv")

# App title
st.title("👨🏼‍🍳 Abdulla's Recipe Manager App")
st.write("Store, retrieve, and manage your favorite recipes.")

# Sidebar menu
menu = st.sidebar.radio("Choose an option:",
                         [ "➕ Add New Recipe", "🕵🏼 Search by Ingredient", "📖 View All Recipes", "🎲 Random Recipe","🔎 Browse by Category","⭐ Rate a Recipe"])

#-------------
# ADD RECIPE
#--------------

if menu == "➕ Add New Recipe":
    st.header("➕ Add New Recipe")

    # Collect inputs of the new recipe
    name=st.text_input("Recipe Name")
    ingredients=st.text_area("Ingredients (format: name:quantity:unit, separated by commas)",placeholder="Flour:200:g, milk:300:ml, eggs:2:whole")
    prep_time= st.number_input("Preparation Time (in minutes)", min_value=1)
    instructions=st.text_area("Instructions")
    difficulty= st.selectbox("Difficulty",["Easy","Medium","Hard"])
    category= st.selectbox("Category",['Breakfast', 'Lunch', 'Dinner', 'Dessert'])

    # Add recipe button and validation of empty boxes
    if st.button("Add Recipe"):
        if name.strip()=='' or ingredients.strip()=='' or instructions.strip()=='':
            st.warning("⛔ Please Fill in all the requirements.")

        # Add(in dataframe),save, and display new recipe
        else:    
            recipes=add_recipe(recipes,name,ingredients,prep_time,instructions,difficulty,category)
            save_recipes(recipes,"apprecipes.csv")
            st.success("Recipe added successfully")

            new_recipe=recipes.iloc[-1]
            st.subheader(f"{new_recipe['name']}")
            st.write(f"🕰️ Preparation Time: {new_recipe['prep_time']} minutes")
            st.write(f"📈 Difficulty: {new_recipe['difficulty']}")
            st.write(f"📊 Category: {new_recipe['category']}")
            st.write(f"🧀 Ingredients: {new_recipe['ingredients']}")
            st.write(f"🧾 Instructions: {new_recipe['instructions']}")
            
    
#---------------------
# SEARCH BY INGREDIENT
#---------------------

elif menu== "🕵🏼 Search by Ingredient":
    st.header("🕵🏼 Search by Ingredient")
    ingredient=st.text_input("Enter an ingredient: ")
    if st.button("Search"):

        # Reject empty boxes and searching for matching recipes
        if ingredient.strip()=='':
            st.warning("⛔ Please enter an ingredient.")
        else:
            matching=search_by_ingredient(recipes,ingredient)
            if matching.empty:
                st.info("ℹ️ No recipes found containing this ingredient.")
            else:
                st.success(f"Found {len(matching)} recipe/recipes.")
                st.dataframe(matching)
                
# ----------------
# VIEW ALL RECIPES
# ----------------

elif menu == "📖 View All Recipes":
    st.header("📖 View All Recipes")
    summary=get_all_recipes_summary(recipes)
    st.dataframe(summary)
# ----------------------------
# RANDOM RECIPE with SCALLING
# ----------------------------
elif menu=="🎲 Random Recipe":
    st.header("🎲 Random Recipe")
   
    # Generate random recipe
    if st.button("Give me a random recipe"):
        st.session_state.random_recipe=get_random_recipe(recipes).iloc[0]
    
    # Display the random recipe    
    if 'random_recipe' in st.session_state:
        recipe=st.session_state.random_recipe
        st.subheader(f"{recipe['name']}")
        
        st.write(f"🕰️ Preparation Time: {recipe['prep_time']} minutes")
        st.write(f"📈 Difficulty: {recipe['difficulty']}")
        st.write(f"🧀 Ingredients: {recipe['ingredients']}")
        st.write(f"🧾 Instructions: {recipe['instructions']}")
       
        # Scale recipe based on servings
        desired_servings=st.number_input("How many servings do you want?", min_value=1, value=int(recipe['servings']))
        scaled=scale_recipe(recipe['ingredients'],recipe['servings'], desired_servings)
        st.write(f"Scaled Ingredients: {scaled}")
        
# ------------------
# BROWSE BY CATEGORY
# ------------------

elif menu=="🔎 Browse by Category":
    st.header("🔎 Browse by Category")
    category= st.selectbox("Category",['Breakfast', 'Lunch', 'Dinner', 'Dessert'])
    if st.button("Show Recipes"):
        matching=filter_by_category(recipes, category)
        if matching.empty:
            st.info("ℹ️ No recipes found in this category.")
        else:
            st.success(f"Found {len(matching)} recipe/recipes.")
            st.dataframe(matching)
            
# -----------
# RATE RECIPE
# -----------

elif menu== "⭐ Rate a Recipe":
    st.header("⭐ Rate a Recipe")
    recipe_lst=recipes['name'].tolist()
    selected_recipe=st.selectbox("Choose a recipe:",recipe_lst)
    rating= st.slider("Rating: ", 1,5,3)
    if st.button("Submit Rating"):
        selected_id=None
        for index in recipes.index:
            if recipes.loc[index, 'name']==selected_recipe:
                selected_id=recipes.loc[index, 'recipe_id']
        recipes=rate_recipe(recipes, selected_id, rating)
        save_recipes(recipes, "apprecipes.csv")
        st.success(f"Rated {selected_recipe} as {rating} stars.")
        st.dataframe(sort_by_rating(recipes))  


        


    









        



        