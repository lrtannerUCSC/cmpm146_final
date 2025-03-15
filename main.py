import tkinter as tk
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL
from HTN import load_recipes_from_csv, display_recipe_list, display_recipe_list_console, find_recipes, State, pyhop, display_meal_plan, common_ingredients


off_white = '#fbffe4'
light_green = '#3d8d7a'
dark_green = '#2B5B50'

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

    # Load and resize the image using PIL
    image = Image.open("fridge.jpg")
    image = image.resize((400, 400))  # Resize the image to fit within the rectangle
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(canvas_width / 2, canvas_height / 2, image=photo)
    canvas.image = photo  # Keep a reference to avoid garbage collection

    # Add Upload Image Button
    button = tk.Button(frames[0], text="Upload Image", bg=light_green, fg=off_white, font=('Helvetica', 20))
    button_upload = canvas.create_window(canvas_width / 2, (canvas_height + 450) / 2 + 30, window=button)
    button.config(command=upload_button)

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
        width=30
    )
    ingredients_text_widget.place(
        x=(canvas_width - 450) / 2 + 20, 
        y=(canvas_height - body_height) / 2 - body_vertical_offset + title_height - 80, 
        width=410, 
        height=200
    )
    ingredients_text = "\n".join([f"{ingredient[0]} {ingredient[1] if ingredient[1] != 'infinite' else ''}" for ingredient in common_ingredients.items()])
    ingredients_text_widget.insert(tk.END, ingredients_text)

    # Must Include Text Box
    canvas.create_text(
        (canvas_width - 450) / 2 + 20, 
        (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 140, 
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
        y=(canvas_height - body_height) / 2 - body_vertical_offset + title_height + 170, 
        width=410, 
        height=60
    )

    # Must Exclude Text Box
    canvas.create_text(
        (canvas_width - 450) / 2 + 20, 
        (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 240, 
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
        y=(canvas_height - body_height) / 2 - body_vertical_offset + title_height + 270, 
        width=410, 
        height=60
    )

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
    root.mainloop()

def upload_button():
    print("Upload Button Pressed")

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

def update_text_widget(text_widget, new_content, readonly=True):
    text_widget.config(state=tk.NORMAL)  # Enable editing
    text_widget.delete(1.0, tk.END)      # Clear current content
    text_widget.insert(tk.END, new_content)  # Insert new content
    if readonly:
        text_widget.config(state=tk.DISABLED)  # Make it read-only

if __name__ == "__main__":
    main()