import pyhop
import csv


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
    def __init__(self, recipes, ingredients):
        self.recipes = recipes  # List of recipe objects
        self.ingredients = ingredients
        self.matched_recipes = []  # List of matched recipes

    def __repr__(self):
        return "State(recipes={}, ingredients={}, matched_recipes={})".format(
            len(self.recipes), self.ingredients, len(self.matched_recipes)
        )


def method_find_recipes(state, ingredients):
    print(f"Running method_find_recipes with ingredients: {ingredients}")
    matching_recipes = []
    for recipe in state.recipes:
        # Check if at least one user ingredient is in the recipe ingredients
        if any(ingredient in [ing[0].lower() for ing in recipe['ingredients']] for ingredient in ingredients):
            matching_recipes.append(recipe)  # Add the full recipe object
    print(f"Matching recipes: {[recipe['name'] for recipe in matching_recipes]}")
    state.matched_recipes = matching_recipes  # Update the matched_recipes list
    return []  # Return an empty list to indicate task completion


pyhop.declare_methods('find_recipes', method_find_recipes)


# Function to display assumed ingredients
def display_assumed_ingredients(common_ingredients):
    print("Assumed Ingredients:")
    for i, ingredient in enumerate(common_ingredients, 1):
        print(f"{i}. {ingredient}")


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
            if new_ingredient not in common_ingredients:
                common_ingredients.append(new_ingredient)
                print(f"Added '{new_ingredient}' to the list.")
            else:
                print(f"'{new_ingredient}' is already in the list.")

        elif choice == "2":
            # Remove an ingredient
            ingredient_to_remove = input("Enter the ingredient to remove: ").strip().lower()
            if ingredient_to_remove in common_ingredients:
                common_ingredients.remove(ingredient_to_remove)
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
    for i, recipe in enumerate(recipes, 1):
        print(f"{i}. {recipe['name']}")


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


def find_recipes(csv_file, user_ingredients, common_ingredients):
    all_ingredients = user_ingredients + common_ingredients

    recipes = load_recipes_from_csv(csv_file)

    state = State(recipes, all_ingredients)

    plan = pyhop.pyhop(state, [('find_recipes', all_ingredients)], verbose=3)
    
    if plan is not False:
        print("Valid plan found")
        return state.matched_recipes
    else:
        print("No valid plan found")
        return []  # If no valid plan found, return an empty list


def main():
    common_ingredients = [
        "salt", "white sugar", "butter", "egg", "white rice", "olive oil", "vegetable oil",
    ]

    # Allow the user to view and edit the assumed ingredients
    print("Welcome to the Recipe Finder!")
    display_assumed_ingredients(common_ingredients)
    edit_assumed_ingredients(common_ingredients)

    # Get user-specific ingredients
    user_ingredients = input("Enter your ingredients (comma-separated): ").strip().lower().split(",")
    user_ingredients = [ingredient.strip() for ingredient in user_ingredients]

    recommended_recipes = find_recipes('recipes.csv', user_ingredients, common_ingredients)
    
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