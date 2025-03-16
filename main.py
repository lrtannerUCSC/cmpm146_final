import tkinter as tk
import os
from tkinter import filedialog
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL
from HTN import load_recipes_from_csv, display_recipe_list, display_recipe_list_console, find_recipes, State, pyhop, display_meal_plan, common_ingredients

off_white = '#fbffe4'
light_green = '#3d8d7a'
dark_green = '#2B5B50'
temp_image_path = "temp_fridge.jpg"

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

ingredients_text = []
recipes = load_recipes_from_csv('recipes.csv')

def main():
    root = tk.Tk()
    root.title("Fridge Friend")
    root.geometry("1920x1080")
    root.configure(bg=off_white)

    canvas = tk.Canvas(root, width=1920, height=138)
    canvas.pack()

    ##############
    # Header bar #
    ##############

    # Add Header Background
    create_rounded_rectangle(canvas, 0, 0, 1920, 138, radius=20, fill=light_green)

    # Add Header Text
    canvas.create_text(230, 69, text="Fridge Friend", fill=off_white, font=('Helvetica', 50))
    canvas.create_text(1820, 110, text="V0.01 Demo", fill=off_white, font=('Helvetica', 20))

    ###############
    # Frame Setup #
    ###############
    
    frame_width = 0.25  # Each frame will take up 25% of the width

    frames = []
    for i in range(4):
        frame = tk.Frame(root, bg=off_white)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frames.append(frame)

    canvas_width = 0.25 * 1920
    canvas_height = 1080 - 138

    #####################
    # Center Left Frame #
    #####################

    canvas = tk.Canvas(frames[1], width=canvas_width, height=canvas_height, highlightthickness=0, bg=off_white)
    canvas.pack(expand=True)

    body_height = 700 
    body_vertical_offset = 50
    title_percentage = 0.3
    title_height = body_height * title_percentage   

    # Body Rectangle
    create_rounded_rectangle(
        canvas,
        (canvas_width - 450) / 2, 
        (canvas_height - body_height) / 2 - body_vertical_offset, 
        (canvas_width + 450) / 2, 
        (canvas_height + body_height) / 2 - body_vertical_offset, 
        radius=20,
        fill=light_green, 
        outline=''
    )
    
    # Title Bar
    create_rounded_rectangle(
        canvas,
        (canvas_width - 450) / 2, 
        (canvas_height - body_height) / 2 - body_vertical_offset, 
        (canvas_width + 450) / 2, 
        (canvas_height - (body_height - title_height)) / 2 - body_vertical_offset, 
        radius=20,
        fill=dark_green, 
        outline=''
    )

    # Title Text
    canvas.create_text(
        canvas_width / 2, 
        (canvas_height - body_height) / 2 - body_vertical_offset + title_height / 2 - 55, 
        text="Ingredients", 
        fill=off_white, 
        font=('Helvetica', 30)
    )

    # Ingredients Text Box
    ingredients_text_widget = tk.Text(
        frames[1], 
        font=('Helvetica', 14), 
        wrap=tk.WORD, 
        bg=off_white, 
        fg=dark_green, 
        height=10, 
        width=30,
    )
    ingredients_text_widget.place(
        x=(canvas_width - 450) / 2 + 20, 
        y=(canvas_height - body_height) / 2 - body_vertical_offset + title_height - 80, 
        width=410, 
        height=320
    )
    ingredients_text = "\n".join([f"{ingredient[0]} {ingredient[1] if ingredient[1] != 'infinite' else ''}" for ingredient in common_ingredients.items()])
    ingredients_text_widget.insert(tk.END, ingredients_text)

    # Must Include Text Box
    canvas.create_text(
        (canvas_width - 450) / 2 + 20, 
        (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 270, 
        text="Must Include", 
        anchor='w', 
        fill=off_white, 
        font=('Helvetica', 20)
    )
    must_include_text_widget = tk.Text(
        frames[1], 
        font=('Helvetica', 14), 
        wrap=tk.WORD, 
        bg=off_white, 
        fg=dark_green, 
        height=3, 
        width=30
    )
    must_include_text_widget.place(
        x=(canvas_width - 450) / 2 + 20, 
        y=(canvas_height - body_height) / 2 - body_vertical_offset + title_height + 300, 
        width=410, 
        height=60
    )

    # Must Exclude Text Box
    canvas.create_text(
        (canvas_width - 450) / 2 + 20, 
        (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 380, 
        text="Must Exclude", 
        anchor='w', 
        fill=off_white, 
        font=('Helvetica', 20)
    )
    must_exclude_text_widget = tk.Text(
        frames[1], 
        font=('Helvetica', 14), 
        wrap=tk.WORD, 
        bg=off_white, 
        fg=dark_green, 
        height=3, 
        width=30
    )
    must_exclude_text_widget.place(
        x=(canvas_width - 450) / 2 + 20, 
        y=(canvas_height - body_height) / 2 - body_vertical_offset + title_height + 410, 
        width=410, 
        height=60
    )

    # Add and Remove Buttons
    button_spread = 114  # Horizontal spacing between buttons
    button_width = 12    # Width of the buttons
    button_vertical_offset = 110  # Vertical offset from the bottom of the frame

    # Add Button
    add_button = tk.Button(
        frames[1], 
        text="Add", 
        bg=light_green, 
        fg=off_white, 
        font=('Helvetica', 20), 
        width=button_width
    )
    canvas.create_window(
        canvas_width / 2 - button_spread, 
        (canvas_height + 450) / 2 + button_vertical_offset, 
        window=add_button
    )
    add_button.config(command=lambda: open_popup("add", ingredients_text_widget))

    # Remove Button
    remove_button = tk.Button(
        frames[1], 
        text="Remove", 
        bg=light_green, 
        fg=off_white, 
        font=('Helvetica', 20), 
        width=button_width
    )
    canvas.create_window(
        canvas_width / 2 + button_spread, 
        (canvas_height + 450) / 2 + button_vertical_offset, 
        window=remove_button
    )
    remove_button.config(command=lambda: open_popup("remove", ingredients_text_widget))

    ######################
    # Center Right Frame #
    ######################

    canvas = tk.Canvas(frames[2], width=canvas_width, height=canvas_height, bg=off_white, highlightthickness=0)
    canvas.pack(expand=True)

    body_height = 700 
    body_vertical_offset = 50
    title_percentage = 0.3
    title_height = body_height * title_percentage   

    # Body Rectangle
    create_rounded_rectangle(
        canvas,
        (canvas_width - 450) / 2, 
        (canvas_height - body_height) / 2 - body_vertical_offset, 
        (canvas_width + 450) / 2, 
        (canvas_height + body_height) / 2 - body_vertical_offset, 
        radius=20,
        fill=light_green, 
        outline=''
    )
    
    # Title Bar
    create_rounded_rectangle(
        canvas,
        (canvas_width - 450) / 2, 
        (canvas_height - body_height) / 2 - body_vertical_offset, 
        (canvas_width + 450) / 2, 
        (canvas_height - (body_height - title_height)) / 2 - body_vertical_offset, 
        radius=20,
        fill=dark_green, 
        outline=''
    )

    # Title Text
    canvas.create_text(
        canvas_width / 2, 
        (canvas_height - body_height) / 2 - body_vertical_offset + title_height / 2 - 55, 
        text="Meal Plan Settings", 
        fill=off_white, 
        font=('Helvetica', 30)
    )

    # Body Text and Input
    canvas.create_text(
        (canvas_width - 450) / 2 + 20, 
        (canvas_height - body_height) / 2 - body_vertical_offset + title_height - 80, 
        text="Meals per day", 
        anchor='w', 
        fill=off_white, 
        font=('Helvetica', 20)
    )
    entry_meals_per_day = tk.Entry(frames[2], font=('Helvetica', 20), width=27, bg=off_white)
    entry_meals_per_day_window = canvas.create_window(
        (canvas_width - 450) / 2 + 20, 
        (canvas_height - body_height) / 2 - body_vertical_offset + title_height - 40, 
        anchor='w', 
        window=entry_meals_per_day
    )

    canvas.create_text(
        (canvas_width - 450) / 2 + 20, 
        (canvas_height - body_height) / 2 - body_vertical_offset + title_height, 
        text="Number of days", 
        anchor='w', 
        fill=off_white, 
        font=('Helvetica', 20)
    )
    entry_number_of_days = tk.Entry(frames[2], font=('Helvetica', 20), width=27, bg=off_white)
    entry_number_of_days_window = canvas.create_window(
        (canvas_width - 450) / 2 + 20, 
        (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 40, 
        anchor='w', 
        window=entry_number_of_days
    )

    canvas.create_text(
        (canvas_width - 450) / 2 + 20, 
        (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 80, 
        text="Cuisine preference", 
        anchor='w', 
        fill=off_white, 
        font=('Helvetica', 20)
    )
    entry_cuisine_preference = tk.Entry(frames[2], font=('Helvetica', 20), width=27, bg=off_white)
    entry_cuisine_preference_window = canvas.create_window(
        (canvas_width - 450) / 2 + 20, 
        (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 120, 
        anchor='w', 
        window=entry_cuisine_preference
    )

    canvas.create_text(
        (canvas_width - 450) / 2 + 20, 
        (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 160, 
        text="Categories", 
        anchor='w', 
        fill=off_white, 
        font=('Helvetica', 20)
    )
    text_categories = tk.Text(frames[2], font=('Helvetica', 20), height=9, width=27, bg=off_white)
    text_categories_window = canvas.create_window(
        (canvas_width - 450) / 2 + 20, 
        (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 325, 
        anchor='w', 
        window=text_categories
    )

    # Generate Button
    generate_button = tk.Button(
        frames[2], 
        text="Generate", 
        bg=light_green, 
        fg=off_white, 
        font=('Helvetica', 20), 
        width=button_width
    )
    canvas.create_window(
        canvas_width / 2, 
        (canvas_height + 450) / 2 + button_vertical_offset, 
        window=generate_button
    )
    generate_button.config(command=lambda: generate_meal_plan(
        entry_meals_per_day.get(),
        entry_number_of_days.get(),
        entry_cuisine_preference.get(),
        text_categories.get("1.0", tk.END).strip()
    ))

    ###############
    # Right Frame #
    ###############

    canvas = tk.Canvas(frames[3], width=canvas_width, height=canvas_height, bg=off_white, highlightthickness=0)
    canvas.pack(expand=True)

    # Rectangle for the Recipes section
    create_rounded_rectangle(
        canvas,
        (canvas_width - 450) / 2,  # x1
        (canvas_height - body_height) / 2 - body_vertical_offset,  # y1
        (canvas_width + 450) / 2,  # x2
        (canvas_height + body_height) / 2 - body_vertical_offset,  # y2
        radius=20,
        fill=light_green, 
        outline=''
    )

    # Draw the title bar
    create_rounded_rectangle(
        canvas,
        (canvas_width - 450) / 2, 
        (canvas_height - body_height) / 2 - body_vertical_offset, 
        (canvas_width + 450) / 2, 
        (canvas_height - (body_height - title_height)) / 2 - body_vertical_offset, 
        radius=20,
        fill=dark_green, 
        outline=''
    )

    # Add the title text
    canvas.create_text(
        canvas_width / 2, 
        (canvas_height - body_height) / 2 - body_vertical_offset + title_height / 2 - 55, 
        text="Recipes", 
        fill=off_white, 
        font=('Helvetica', 30)
    )

    # Create a Frame to hold the Canvas and Scrollbar
    recipe_frame = tk.Frame(frames[3], bg=light_green)
    recipe_frame.place(
        x=(canvas_width - 450) / 2 + 20,  # x1 + padding
        y=(canvas_height - body_height) / 2 - body_vertical_offset + title_height - 80,  # y1 + offset
        width=410,  # Width of the box minus padding
        height=500  # Height of the box minus padding
    )

    # Create a Canvas inside the Frame
    recipe_canvas = tk.Canvas(recipe_frame, bg=light_green, highlightthickness=0)
    recipe_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a Scrollbar to the Frame
    scrollbar = tk.Scrollbar(recipe_frame, orient=tk.VERTICAL, command=recipe_canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the Canvas to work with the Scrollbar
    recipe_canvas.configure(yscrollcommand=scrollbar.set)
    recipe_canvas.bind(
        '<Configure>',
        lambda e: recipe_canvas.configure(scrollregion=recipe_canvas.bbox('all'))
    )

    # Create a Frame inside the Canvas to hold the Text widget
    text_frame = tk.Frame(recipe_canvas, bg=off_white)
    recipe_canvas.create_window((0, 0), window=text_frame, anchor='nw')

    # Display recipes
    recipes_text = display_recipe_list(recipes)  # Get the formatted recipe list

    # Create a Text widget to display the recipes
    recipes_text_widget = tk.Text(text_frame, font=('Helvetica', 16), wrap=tk.NONE, bg=off_white, fg=dark_green)
    recipes_text_widget.insert(tk.END, recipes_text)  # Insert the formatted recipe list
    recipes_text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
    recipes_text_widget.pack(fill=tk.BOTH, expand=True)

    # Buttons
    button_width = 28
    button_vertical_offset = 110

    button = tk.Button(frames[3], text="Find Recipes", bg=light_green, fg=off_white, font=('Helvetica', 20), width=button_width)
    button_find = canvas.create_window(canvas_width / 2, (canvas_height + 450) / 2 + button_vertical_offset, window=button)
    button.config(command=lambda: find_button(recipes, recipes_text_widget, must_include_text_widget, must_exclude_text_widget))
    
    ##############
    # Left Frame #
    ##############

    canvas = tk.Canvas(frames[0], width=canvas_width, height=canvas_height, highlightthickness=0, bg=off_white)
    canvas.pack(expand=True)

    # Body Rectangle
    create_rounded_rectangle(
        canvas,
        (canvas_width - 450) / 2, 
        (canvas_height - 450) / 2, 
        (canvas_width + 450) / 2, 
        (canvas_height + 450) / 2, 
        radius=20,
        fill=light_green, 
        outline=''
    )

    if os.path.exists(temp_image_path):
        image = Image.open(temp_image_path)
    else:
        image = Image.open("fridge.jpg")
    image = image.resize((400, 400))
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(canvas_width / 2, canvas_height / 2, image=photo)
    canvas.image = photo

    button = tk.Button(frames[0], text="Upload Image", bg=light_green, fg=off_white, font=('Helvetica', 20))
    button_upload = canvas.create_window(canvas_width / 2, (canvas_height + 450) / 2 + 30, window=button)
    button.config(command=lambda: upload_button(canvas, canvas_width, canvas_height))

    #why does this even work?
    root.mainloop()

def upload_button(canvas, canvas_width, canvas_height):
    global temp_image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;")])
    if file_path:
        img = Image.open(file_path)
        img = img.resize((400, 400))  # Resize the image
        img.save(temp_image_path)  # Save a temporary local copy
        photo = ImageTk.PhotoImage(img)
        canvas.create_image(canvas_width / 2, canvas_height / 2, image=photo)
        canvas.image = photo  # Keep reference to avoid garbage collection


def open_popup(action, ingredients_text_widget):
    # Create a new popup window
    popup = tk.Toplevel()
    popup.title(f"{action.capitalize()} Ingredient")
    popup.geometry("400x200")
    popup.configure(bg=off_white)

    # Add a label
    label = tk.Label(popup, text=f"Enter ingredient to {action}:", bg=off_white, fg=dark_green, font=('Helvetica', 14))
    label.pack(pady=10)

    # Add a text widget for user input
    input_text = tk.Text(popup, font=('Helvetica', 14), wrap=tk.WORD, bg=off_white, fg=dark_green, height=3, width=30)
    input_text.pack(pady=10)

    # Add a submit button
    submit_button = tk.Button(
        popup, 
        text="Submit", 
        bg=light_green, 
        fg=off_white, 
        font=('Helvetica', 14), 
        command=lambda: handle_popup_submit(action, input_text, popup, ingredients_text_widget)
    )
    submit_button.pack(pady=10)

def handle_popup_submit(action, input_text, popup, ingredients_text_widget):
    # Retrieve the user input
    user_input = input_text.get("1.0", tk.END).strip()
    items = [item.strip() for item in user_input.split(',') if item.strip()]  # Split and strip whitespace
    
    if items:  # Check if there are any items to process
        if action == "add":
            # Add each ingredient to common_ingredients
            for item in items:
                common_ingredients[item] = "infinite"  # Default to infinite quantity
        elif action == "remove":
            # Remove each ingredient from common_ingredients
            for item in items:
                if item in common_ingredients:
                    del common_ingredients[item]
        
        # Refresh the ingredients_text_widget
        refresh_ingredients_text_widget(ingredients_text_widget)
    
    # Close the popup
    popup.destroy()

def refresh_ingredients_text_widget(ingredients_text_widget):
    # Clear the current content
    ingredients_text_widget.delete("1.0", tk.END)
    # Add the updated ingredients list
    ingredients_text = "\n".join([f"{ingredient} - {quantity}" if quantity != "infinite" else f"{ingredient}" for ingredient, quantity in common_ingredients.items()])
    ingredients_text_widget.insert(tk.END, ingredients_text)

def find_button(recipes, recipes_text_widget, must_include_text_widget, must_exclude_text_widget):
    print("Find Button Pressed")
    
    # Retrieve text from the "Must Include" and "Must Exclude" text boxes
    must_include_text = must_include_text_widget.get("1.0", tk.END).strip()
    must_exclude_text = must_exclude_text_widget.get("1.0", tk.END).strip()
    
    # Parse the text into lists of ingredients
    must_include = [ingredient.strip() for ingredient in must_include_text.split(",") if ingredient.strip()]
    must_exclude = [ingredient.strip() for ingredient in must_exclude_text.split(",") if ingredient.strip()]
    print("include exclude", must_include, must_exclude)
    # Find the new recipes based on the current ingredients and constraints
    new_recipes = find_recipes(recipes, common_ingredients, must_include, must_exclude)
    print("new recipes: ", new_recipes)
    # Format the new recipe list for display
    new_recipes_text = display_recipe_list(new_recipes)
    print("new recipe text: ", new_recipes_text)
    display_recipe_list_console(new_recipes)
    
    # Update the recipes_text_widget using the helper function
    update_text_widget(recipes_text_widget, new_recipes_text)

def generate_meal_plan(meals_per_day, number_of_days, cuisine_preference, categories):
    print("Generate Button Pressed")
    
    # Convert inputs to appropriate types
    try:
        meals_per_day = int(meals_per_day) if meals_per_day else 3  # Default to 3 meals per day
        number_of_days = int(number_of_days) if number_of_days else 7  # Default to 7 days
    except ValueError:
        print("Invalid input for meals per day or number of days. Using default values.")
        meals_per_day = 3
        number_of_days = 7
    
    # Split categories and cuisine preference into lists
    categories_list = [cat.strip() for cat in categories.split(",") if cat.strip()]
    cuisines_list = [cuisine.strip() for cuisine in cuisine_preference.split(",") if cuisine.strip()]
    
    # Create a state for HTN planning
    state = State(recipes, common_ingredients)
    state.matched_recipes = find_recipes(recipes, common_ingredients)  # Find matching recipes
    
    # Generate the meal plan using the HTN
    meal_plan_found = pyhop.pyhop(state, [('plan_meals', meals_per_day, number_of_days, cuisines_list)], verbose=0)
    
    # Display the meal plan in a pop-up window
    if meal_plan_found is not False:
        meal_plan_text = display_meal_plan(state.meal_plan)
        show_meal_plan_popup(meal_plan_text)
    else:
        show_meal_plan_popup("No valid meal plan could be generated.")

def show_meal_plan_popup(meal_plan_text):
    # Create a new popup window
    popup = tk.Toplevel()
    popup.title("Meal Plan")
    popup.geometry("600x400")
    popup.configure(bg=off_white)

    # Add a label for the meal plan
    label = tk.Label(popup, text="Your Meal Plan", bg=off_white, fg=dark_green, font=('Helvetica', 20))
    label.pack(pady=10)

    # Add a text widget to display the meal plan
    meal_plan_text_widget = tk.Text(
        popup, 
        font=('Helvetica', 14), 
        wrap=tk.WORD, 
        bg=off_white, 
        fg=dark_green, 
        height=15, 
        width=70
    )
    meal_plan_text_widget.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    meal_plan_text_widget.insert(tk.END, meal_plan_text)
    meal_plan_text_widget.config(state=tk.DISABLED)  # Make the text widget read-only

    # Add a close button
    close_button = tk.Button(
        popup, 
        text="Close", 
        bg=light_green, 
        fg=off_white, 
        font=('Helvetica', 14), 
        command=popup.destroy
    )
    close_button.pack(pady=10)

def update_text_widget(text_widget, new_content, readonly=True):
    text_widget.config(state=tk.NORMAL)  # Enable editing
    text_widget.delete(1.0, tk.END)      # Clear current content
    text_widget.insert(tk.END, new_content)  # Insert new content
    if readonly:
        text_widget.config(state=tk.DISABLED)  # Make it read-only

if __name__ == "__main__":
    main()