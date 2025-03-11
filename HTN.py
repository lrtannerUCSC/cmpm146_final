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
                'ingredients': [ingredient[0].strip().lower() for ingredient in ingredients],
                'cooking_time': 30  # Placeholder for cooking time (you can extract this from instructions if available)
            }
            recipes.append(recipe)
    return recipes

# Define the state
class State:
    def __init__(self, recipes, ingredients):
        self.recipes = recipes  # List of recipe objects
        self.ingredients = ingredients
        self.matched_recipes = []  # List of matched recipes

    def __repr__(self):
        return "State(recipes={}, ingredients={}, matched_recipes={})".format(
            len(self.recipes), self.ingredients, len(self.matched_recipes)
        )


# Define methods for task decomposition
def method_find_recipes(state, ingredients):
    print(f"Running method_find_recipes with ingredients: {ingredients}")
    matching_recipes = []
    for recipe in state.recipes:
        # Check if at least one user ingredient is in the recipe ingredients
        if any(ingredient in recipe['ingredients'] for ingredient in ingredients):
            matching_recipes.append(recipe['name'])  # Add only the recipe name
    print(f"Matching recipes: {matching_recipes}")
    state.matched_recipes = matching_recipes  # Update the matched_recipes list
    return []  # Return an empty list to indicate task completion


# Register the methods properly
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


# Main function to run the HTN planner
def find_recipes(csv_file, user_ingredients, common_ingredients):
    # Combine user ingredients with assumed ingredients
    all_ingredients = user_ingredients + common_ingredients

    # Load recipes from CSV
    recipes = load_recipes_from_csv(csv_file)

    # Initialize the state
    state = State(recipes, all_ingredients)

    # Run the HTN planner
    plan = pyhop.pyhop(state, [('find_recipes', all_ingredients)], verbose=3)
    
    # Check if the plan was successful and return the result
    if plan is not False:  # If the plan is not False, it succeeded
        print("Valid plan found")
        return state.matched_recipes  # Return the matched recipes from the state
    else:
        print("No valid plan found")
        return []  # If no valid plan found, return an empty list


# Example usage
if __name__ == "__main__":
    # List of common ingredients
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

    # Find recipes
    recommended_recipes = find_recipes('recipes.csv', user_ingredients, common_ingredients)
    
    # If there are any recommended recipes, print them
    if recommended_recipes:
        print("Recommended Recipes:")
        for recipe_name in recommended_recipes:
            print(f"- {recipe_name}")
    else:
        print("No recommended recipes found.")