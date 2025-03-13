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


def method_find_recipes(state, ingredients):
    print(f"Running method_find_recipes with ingredients: {ingredients}")
    matching_recipes = []
    added_recipe_ids = set()  # Track IDs of recipes already added to avoid duplicates
    
    for recipe in state.recipes:
        # Skip if recipe is already in the list
        if recipe['id'] in added_recipe_ids:
            continue
        
        # Extract ingredient names from the recipe
        recipe_ingredients = [ing[0].lower() for ing in recipe['ingredients']]
        
        # Check "must use" constraint
        if state.must_use and not all(must_ingredient in recipe_ingredients for must_ingredient in state.must_use):
            continue  # Skip if recipe doesn't include all "must use" ingredients
        
        # Check "exclude" constraint
        if state.exclude and any(exclude_ingredient in recipe_ingredients for exclude_ingredient in state.exclude):
            continue  # Skip if recipe contains any "exclude" ingredient
        
        # Check if the user has enough of each ingredient
        has_enough_ingredients = True
        for ingredient, recipe_quantity in recipe['ingredients']:
            if ingredient.lower() in ingredients:
                # Skip quantity check if the user has an infinite amount
                if ingredients[ingredient.lower()] == 'infinite':
                    continue
                # Extract numeric values from quantities
                user_quantity_numeric = extract_numeric_value(ingredients[ingredient.lower()])
                recipe_quantity_numeric = extract_numeric_value(recipe_quantity)
                # Compare numeric values
                if user_quantity_numeric < recipe_quantity_numeric:
                    has_enough_ingredients = False
                    break
        
        if has_enough_ingredients:
            matching_recipes.append(recipe)  # Add the full recipe object
            added_recipe_ids.add(recipe['id'])  # Track the recipe ID to avoid duplicates
    
    print(f"Matching recipes: {[recipe['name'] for recipe in matching_recipes]}")
    state.matched_recipes = matching_recipes  # Update the matched_recipes list
    return []  # Return an empty list to indicate task completion


pyhop.declare_methods('find_recipes', method_find_recipes)


# Function to display assumed ingredients
def display_assumed_ingredients(common_ingredients):
    print("Assumed Ingredients:")
    for i, (ingredient, quantity) in enumerate(common_ingredients.items(), 1):
        print(f"{i}. {ingredient}: {quantity}")


# Function to allow the user to edit the list of assumed ingredients
def edit_assumed_ingredients(common_ingredients):
    while True:
        print("\nOptions:")
        print("1. Add an ingredient")
        print("2. Remove an ingredient")
        print("3. View current list")
        print("4. Done editing")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
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

        elif choice == "2":
            # Remove an ingredient
            ingredient_to_remove = input("Enter the ingredient to remove: ").strip().lower()
            if ingredient_to_remove in common_ingredients:
                del common_ingredients[ingredient_to_remove]
                print(f"Removed '{ingredient_to_remove}' from the list.")
            else:
                print(f"'{ingredient_to_remove}' is not in the list.")

        elif choice == "3":
            # View current list
            display_assumed_ingredients(common_ingredients)

        elif choice == "4":
            # Exit editing
            print("Finished editing the list.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


# Function to display the list of recommended recipes
def display_recipe_list(recipes):
    print("\nRecommended Recipes:")
    # Define column widths
    name_width = 80
    cuisine_width = 20
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


def find_recipes(csv_file, all_ingredients, must_use=None, exclude=None):
    recipes = load_recipes_from_csv(csv_file)

    state = State(recipes, all_ingredients, must_use, exclude)

    plan = pyhop.pyhop(state, [('find_recipes', all_ingredients)], verbose=3)
    
    if plan is not False:
        print("Valid plan found")
        return state.matched_recipes
    else:
        print("No valid plan found")
        return []  # If no valid plan found, return an empty list


def main():
    # Common ingredients as a dictionary (ingredient: quantity or 'infinite')
    common_ingredients = {
        "salt": "infinite",
        "white sugar": "infinite",
        "butter": "infinite",
        "white rice": "infinite",
        "olive oil": "infinite",
        "vegetable oil": "infinite",
    }

    # Allow the user to view and edit the assumed ingredients
    print("Welcome to the Recipe Finder!")
    display_assumed_ingredients(common_ingredients)
    edit_assumed_ingredients(common_ingredients)

    # Get user-specific ingredients
    user_ingredients = {}
    ingredients_input = input("Enter your ingredients (e.g., 'flour - 200g, eggs'): ").strip().lower()
    for item in ingredients_input.split(','):
        if item.strip():
            if '-' in item:
                ingredient, quantity = item.strip().split('-')
                user_ingredients[ingredient.strip()] = quantity.strip()
            else:
                user_ingredients[item.strip()] = 'infinite'  # Assume infinite if no quantity is specified

    # Combine user_ingredients and common_ingredients (user_ingredients takes precedence)
    all_ingredients = {**common_ingredients, **user_ingredients}

    # Get "must use" ingredients
    must_use = input("Enter ingredients that MUST be used (comma-separated, leave blank if none): ").strip().lower().split(",")
    must_use = [ingredient.strip() for ingredient in must_use if ingredient.strip()]

    # Get "exclude" ingredients
    exclude = input("Enter ingredients to EXCLUDE (comma-separated, leave blank if none): ").strip().lower().split(",")
    exclude = [ingredient.strip() for ingredient in exclude if ingredient.strip()]

    recommended_recipes = find_recipes('recipes.csv', all_ingredients, must_use, exclude)
    
    if recommended_recipes:
        while True:
            display_recipe_list(recommended_recipes)
            
            # Allow the user to select a recipe
            selected_recipe = select_recipe(recommended_recipes)
            if selected_recipe is None:
                break  # Exit if the user chooses to exit

            display_recipe_details(selected_recipe)

            # Ask the user if they want to go back to the list or exit
            print("\nOptions:")
            print("1. Go back to the list of recipes")
            print("2. Exit")
            choice = input("Choose an option (1-2): ").strip()
            if choice == "2":
                break  # Exit the loop and end the program
    else:
        print("No recommended recipes found.")


if __name__ == "__main__":
    main()