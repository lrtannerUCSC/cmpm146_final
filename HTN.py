import pyhop
import csv

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
                'ingredients': [ingredient[0].strip().lower() for ingredient in ingredients],  # Get ingredient names
            }
            recipes.append(recipe)
    return recipes

class State:
    def __init__(self, recipes, ingredients):
        self.recipes = recipes  # List of recipe objects
        self.ingredients = ingredients  # List of ingredients
        self.matched_recipes = []  # List of matched recipes

    def __repr__(self):
        return "State(recipes={}, ingredients={}, matched_recipes={})".format(
            len(self.recipes), self.ingredients, len(self.matched_recipes)
        )


# Adds recipe to list if the recipe has at least one of the ingredients the user listed
# Prob change the filter to be more specific
def method_find_recipes(state, ingredients):
    print(f"Running method_find_recipes with ingredients: {ingredients}")
    matching_recipes = []
    for recipe in state.recipes:
        # Check if at least one user ingredient is in the recipe ingredients
        if any(ingredient.lower() in recipe['ingredients'] for ingredient in ingredients):
            matching_recipes.append(recipe['name'])  # Adding only name right now for clarity, maybe change later
    print(f"Matching recipes: {matching_recipes}")
    state.matched_recipes = matching_recipes
    return []  # Return empty list to indicate there are no more tasks

pyhop.declare_methods('find_recipes', method_find_recipes)

def find_recipes(csv_file, user_ingredients):

    recipes = load_recipes_from_csv(csv_file)

    state = State(recipes, user_ingredients)

    plan = pyhop.pyhop(state, [('find_recipes', user_ingredients)], verbose=3)
    
    if plan is not False:
        print("Valid plan found")
        return state.matched_recipes  # Return the matched recipes from the state
    else:
        print("No valid plan found")
        return []  # If no valid plan found, return an empty list

if __name__ == "__main__":
    user_ingredients = ['pork']  # Example user ingredients input

    # Find recipes
    recommended_recipes = find_recipes('recipes.csv', user_ingredients)
    
    # If there are any recommended recipes, print them
    if recommended_recipes:
        print("Recommended Recipes:")
        for recipe_name in recommended_recipes:
            print(f"- {recipe_name}")
    else:
        print("No recommended recipes found.")