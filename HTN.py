import pyhop
import csv
import re


# Helper function to extract numeric values from quantities
def extract_numeric_value(quantity):
    # Takes the 200 out of flour - 200g, for comparing amounts
    match = re.search(r'\d+\.?\d*', quantity)
    if match:
        return float(match.group())
    return 0  # Default to 0 if no numeric value is found


# Load recipes from CSV
def load_recipes_from_csv(filename):
    recipes = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Parse ingredients into a list of tuples (ingredient, quantity)
            ingredients = eval(row['ingredients'])  # Convert string to list of tuples
            recipe = {
                'id': row['id'],
                'name': row['name'],
                'category': row['category'],
                'area': row['area'],
                'instructions': row['instructions'],
                'ingredients': ingredients,  # Store as list of tuples
            }
            recipes.append(recipe)
    return recipes


class State:
    def __init__(self, recipes, ingredients, must_use=None, exclude=None):
        self.recipes = recipes  # List of recipe objects
        self.ingredients = ingredients  # User's available ingredients as a dictionary
        self.must_use = must_use if must_use else []  # Must-use ingredients
        self.exclude = exclude if exclude else []  # Exclude ingredients
        self.matched_recipes = []  # List of matched recipes
        self.meal_plan = []  # List of planned meals
        self.used_recipes = set()  # Track used recipes to ensure variety


# HTN method to plan meals for a given number of days
def method_plan_meals(state, meals_per_day, days, cuisines=None):
    print(f"Planning {meals_per_day} meals per day for {days} days...")
    for day in range(1, days + 1):
        pyhop.pyhop(state, [('plan_day', day, meals_per_day, cuisines)], verbose=3)
    display_meal_plan(state.meal_plan)
    return []


# HTN method to plan meals for a single day
def method_plan_day(state, day, meals_per_day, cuisines=None):
    print(f"\nPlanning Day {day}:")
    for meal in range(1, meals_per_day + 1):
        pyhop.pyhop(state, [('plan_meal', day, meal, cuisines)], verbose=3)
    return []


# HTN method to plan a single meal
def method_plan_meal(state, day, meal, cuisines=None):
    print(f"Planning Meal {meal} for Day {day}...")
    # Filter recipes by cuisine if specified
    if cuisines:
        filtered_recipes = [recipe for recipe in state.matched_recipes if recipe['area'].lower() in cuisines]
    else:
        filtered_recipes = state.matched_recipes
    if not filtered_recipes:
        print("No recipes match the specified cuisines.")
        return False
    # Select a recipe that hasn't been used too often
    for recipe in filtered_recipes:
        if recipe['id'] not in state.used_recipes:
            state.used_recipes.add(recipe['id'])
            state.meal_plan.append((day, meal, recipe))
            print(f"Selected: {recipe['name']} ({recipe['area']})")
            return []
    print("No unique recipes left for the specified constraints.")
    return False


# Declare HTN methods
pyhop.declare_methods('plan_meals', method_plan_meals)
pyhop.declare_methods('plan_day', method_plan_day)
pyhop.declare_methods('plan_meal', method_plan_meal)


# Function to display assumed ingredients
def display_assumed_ingredients(common_ingredients):
    print("Assumed Ingredients:")
    for i, (ingredient, quantity) in enumerate(common_ingredients.items(), 1):
        print(f"{i}. {ingredient}: {quantity}")


# Function to allow the user to edit the list of assumed ingredients
def edit_assumed_ingredients(common_ingredients):
    while True:
        print("\nOptions:")
        print("A. Add an ingredient")
        print("R. Remove an ingredient")
        print("V. View current list")
        print("D. Done editing")
        choice = input("Choose an option (A/R/V/D): ").strip().lower()

        if choice == "a":
            # Add an ingredient
            new_ingredient = input("Enter the ingredient to add: ").strip().lower()
            quantity = input("Enter the quantity (or leave blank for infinite): ").strip().lower()
            if not quantity:
                quantity = "infinite"
            if new_ingredient not in common_ingredients:
                common_ingredients[new_ingredient] = quantity
                print(f"Added '{new_ingredient}' to the list.")
            else:
                print(f"'{new_ingredient}' is already in the list.")

        elif choice == "r":
            # Remove an ingredient
            ingredient_to_remove = input("Enter the ingredient to remove: ").strip().lower()
            if ingredient_to_remove in common_ingredients:
                del common_ingredients[ingredient_to_remove]
                print(f"Removed '{ingredient_to_remove}' from the list.")
            else:
                print(f"'{ingredient_to_remove}' is not in the list.")

        elif choice == "v":
            # View current list
            display_assumed_ingredients(common_ingredients)

        elif choice == "d":
            # Exit editing
            print("Finished editing the list.")
            break

        else:
            print("Invalid choice. Please enter A, R, V, or D.")


# Function to display the list of recommended recipes
def display_recipe_list_console(recipes):
    print("\nRecommended Recipes:")
    # Define column widths
    name_width = 80
    cuisine_width = 30
    category_width = 20
    
    # Print the header
    print(
        f"{'#'.ljust(5)}"
        f"{'Recipe Name'.ljust(name_width)}"
        f"{'Cuisine'.ljust(cuisine_width)}"
        f"{'Category'.ljust(category_width)}"
    )
    print("-" * (5 + name_width + cuisine_width + category_width))
    
    # Print each recipe in a formatted row
    for i, recipe in enumerate(recipes, 1):
        print(
            f"{str(i).ljust(5)}"
            f"{recipe['name'].ljust(name_width)}"
            f"{recipe['area'].ljust(cuisine_width)}"
            f"{recipe['category'].ljust(category_width)}"
        )

# def display_recipe_list(recipes):
#     # Define column widths
#     name_width = 50
#     cuisine_width = 30
#     category_width = 20
    
#     # Create the header
#     recipe_list = (
#         f"{'Recipe'.ljust(name_width)}"
#         # f"{'Cuisine'.ljust(cuisine_width)}"
#         # f"{'Category'.ljust(category_width)}\n"
#     )
#     recipe_list += "-" * (5 + name_width + cuisine_width + category_width) + "\n"
#     recipe_list += "-" * (5 + name_width) + "\n"
    
#     # Add each recipe to the formatted string
#     for i, recipe in enumerate(recipes, 1):
#         recipe_list += (
#             f"{str(i).ljust(5)}"
#             f"{recipe['name'].ljust(name_width)}"
#             f"{recipe['area'].ljust(cuisine_width)}"
#             f"{recipe['category'].ljust(category_width)}\n"
#         )
    
#     return recipe_list

def display_recipe_list(recipes):
    # Create a formatted string with recipe names
    recipe_list = ""
    for i, recipe in enumerate(recipes, 1):
        recipe_list += f"{i}. {recipe['name']}\n"  # Add recipe name with numbering
    return recipe_list

# Function to allow the user to select a recipe
def select_recipe(recipes):
    while True:
        try:
            choice = int(input("Enter the number of the recipe you want to view (or 0 to exit): ").strip())
            if choice == 0:
                return None  # Exit
            elif 1 <= choice <= len(recipes):
                return recipes[choice - 1]  # Return the selected recipe
            else:
                print("Invalid choice. Please enter a number between 1 and", len(recipes))
        except ValueError:
            print("Invalid input. Please enter a number.")


# Function to display the full details of a recipe
def display_recipe_details(recipe):
    print("\nRecipe Details:")
    print(f"Name: {recipe['name']}")
    print(f"Category: {recipe['category']}")
    print(f"Cuisine: {recipe['area']}")
    print("\nIngredients:")
    for ingredient, measurement in recipe['ingredients']:
        print(f"- {ingredient}: {measurement}")
    print("\nInstructions:")
    print(recipe['instructions'])


# Function to filter recipes based on user constraints
# def find_recipes(recipes, all_ingredients, must_use=None, exclude=None):
    matching_recipes = []
    unique_recipe_ids = set()  # Track unique recipe IDs to avoid duplicates
    
    for recipe in recipes:
        # Skip if recipe ID has already been added
        if recipe['id'] in unique_recipe_ids:
            continue
            
        # Extract ingredient names from the recipe
        recipe_ingredients = [ing[0].lower() for ing in recipe['ingredients']]
        
        # Check "must use" constraint
        if must_use and not all(must_ingredient in recipe_ingredients for must_ingredient in must_use):
            continue
        
        # Check "exclude" constraint
        if exclude and any(exclude_ingredient in recipe_ingredients for exclude_ingredient in exclude):
            continue
        
        # Check ingredient availability and quantities
        has_enough_ingredients = True
        print(recipe['name'])
        print("\n", all_ingredients)
        for ingredient, recipe_quantity in recipe['ingredients']:
            ingredient_lower = ingredient.lower()
            if ingredient_lower not in all_ingredients:
                has_enough_ingredients = False
                break
            if all_ingredients[ingredient_lower] != 'infinite':
                user_qty = extract_numeric_value(all_ingredients[ingredient_lower])
                recipe_qty = extract_numeric_value(recipe_quantity)
                if user_qty < recipe_qty:
                    has_enough_ingredients = False
                    break
        
        if has_enough_ingredients:
            if recipe not in matching_recipes:
                matching_recipes.append(recipe)
            # unique_recipe_ids.add(recipe['id'])
    
    return matching_recipes
def find_recipes(recipes, all_ingredients, must_use=None, exclude=None):
    matching_recipes = []
    unique_recipe_ids = set()  # Track unique recipe IDs to avoid duplicates
    
    # Convert all_ingredients keys to lowercase for consistent lookup
    all_ingredients = {k.lower(): v for k, v in all_ingredients.items()}
    
    # Convert must_use and exclude to lowercase for consistent matching
    if must_use:
        must_use = [ingredient.lower() for ingredient in must_use]
    if exclude:
        exclude = [ingredient.lower() for ingredient in exclude]
    
    for recipe in recipes:
        # Skip if recipe ID has already been added
        if recipe['id'] in unique_recipe_ids:
            continue
            
        # Extract ingredient names from the recipe
        recipe_ingredients = [ing[0].lower() for ing in recipe['ingredients']]
        
        # Check "must use" constraint
        if must_use and not all(must_ingredient in recipe_ingredients for must_ingredient in must_use):
            continue
        
        # Check "exclude" constraint
        if exclude and any(exclude_ingredient in recipe_ingredients for exclude_ingredient in exclude):
            continue
        
        # Check if at least one ingredient is in all_ingredients
        has_at_least_one_ingredient = any(
            ingredient_lower in all_ingredients
            for ingredient_lower in recipe_ingredients
        )
        
        # If at least one ingredient is available, add the recipe to the list
        if has_at_least_one_ingredient:
            if recipe not in matching_recipes:
                matching_recipes.append(recipe)
            unique_recipe_ids.add(recipe['id'])
    
    return matching_recipes

# Function to get user-specific ingredients
def get_user_ingredients():
    user_ingredients = {}
    ingredients_input = input("Enter your ingredients (e.g., 'flour - 200g, eggs'): ").strip().lower()
    for item in ingredients_input.split(','):
        if item.strip():
            if '-' in item:
                ingredient, quantity = item.strip().split('-')
                user_ingredients[ingredient.strip()] = quantity.strip()
            else:
                user_ingredients[item.strip()] = 'infinite'  # Assume infinite if no quantity is specified
    return user_ingredients


# Function to display the meal plan
def display_meal_plan(meal_plan):
    print("\nMeal Plan:")
    for day, meal, recipe in meal_plan:
        print(f"Day {day}, Meal {meal}: {recipe['name']} ({recipe['area']})")

# Common ingredients as a dictionary (ingredient: quantity or 'infinite')
common_ingredients = {
    "salt": "infinite",
    "sugar": "infinite",
    "butter": "infinite",
    "rice": "infinite",
    "olive oil": "infinite",
    "vegetable oil": "infinite",
    "oil": "infinite",
}

def main():
    

    # Allow the user to view and edit the assumed ingredients
    print("Welcome to the Recipe Finder!")
    display_assumed_ingredients(common_ingredients)
    edit_assumed_ingredients(common_ingredients)

    # Get user-specific ingredients
    user_ingredients = get_user_ingredients()

    # Combine user_ingredients and common_ingredients (user_ingredients takes precedence)
    all_ingredients = {**common_ingredients, **user_ingredients}

    # Get "must use" ingredients
    must_use = input("Enter ingredients that MUST be used (comma-separated, leave blank if none): ").strip().lower().split(",")
    must_use = [ingredient.strip() for ingredient in must_use if ingredient.strip()]

    # Get "exclude" ingredients
    exclude = input("Enter ingredients to EXCLUDE (comma-separated, leave blank if none): ").strip().lower().split(",")
    exclude = [ingredient.strip() for ingredient in exclude if ingredient.strip()]

    while True:
        # Load recipes and filter based on user constraints
        recipes = load_recipes_from_csv('recipes.csv')
        matched_recipes = find_recipes(recipes, all_ingredients, must_use, exclude)
        
        if matched_recipes:
            # Display the recipe list after updating ingredients
            display_recipe_list_console(matched_recipes)
            
            while True:
                # Display basic options
                print("\nOptions:")
                print("V. View a recipe")
                print("U. Update ingredients and re-run search")
                print("P. Plan meals")
                print("E. Exit")
                choice = input("Choose an option (V/U/P/E): ").strip().lower()

                if choice == "v":
                    # Allow the user to select a recipe
                    selected_recipe = select_recipe(matched_recipes)
                    if selected_recipe is not None:
                        display_recipe_details(selected_recipe)
                elif choice == "u":
                    # Update ingredients and re-run search
                    print("\nUpdating ingredients...")
                    user_ingredients = get_user_ingredients()
                    all_ingredients = {**common_ingredients, **user_ingredients}
                    must_use = input("Enter ingredients that MUST be used (comma-separated, leave blank if none): ").strip().lower().split(",")
                    must_use = [ingredient.strip() for ingredient in must_use if ingredient.strip()]
                    exclude = input("Enter ingredients to EXCLUDE (comma-separated, leave blank if none): ").strip().lower().split(",")
                    exclude = [ingredient.strip() for ingredient in exclude if ingredient.strip()]
                    break  # Exit the inner loop and re-run the search
                elif choice == "p":
                    # Plan meals
                    meals_per_day = int(input("Enter the number of meals per day: ").strip())
                    days = int(input("Enter the number of days: ").strip())
                    cuisines = input("Enter cuisines to include (comma-separated, leave blank for any): ").strip().lower().split(",")
                    cuisines = [cuisine.strip() for cuisine in cuisines if cuisine.strip()]

                    # Create a state for HTN planning
                    state = State(recipes, all_ingredients, must_use, exclude)
                    state.matched_recipes = matched_recipes  # Assign matched_recipes to state.matched_recipes
                    meal_plan_found = pyhop.pyhop(state, [('plan_meals', meals_per_day, days, cuisines)], verbose=3)

                    if meal_plan_found is not False:
                        display_meal_plan(state.meal_plan)
                    else:
                        print("No valid meal plan found.")
                elif choice == "e":
                    # Exit the program
                    print("Goodbye!")
                    return
                else:
                    print("Invalid choice. Please enter V, U, P, or E.")
        else:
            print("No recommended recipes found.")
            # Allow the user to update ingredients and re-run the search
            print("\nOptions:")
            print("U. Update ingredients and re-run search")
            print("E. Exit")
            choice = input("Choose an option (U/E): ").strip().lower()
            if choice == "u":
                print("\nUpdating ingredients...")
                user_ingredients = get_user_ingredients()
                all_ingredients = {**common_ingredients, **user_ingredients}
                must_use = input("Enter ingredients that MUST be used (comma-separated, leave blank if none): ").strip().lower().split(",")
                must_use = [ingredient.strip() for ingredient in must_use if ingredient.strip()]
                exclude = input("Enter ingredients to EXCLUDE (comma-separated, leave blank if none): ").strip().lower().split(",")
                exclude = [ingredient.strip() for ingredient in exclude if ingredient.strip()]
            else:
                print("Goodbye!")
                return


if __name__ == "__main__":
    main()