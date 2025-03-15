import tkinter as tk
from HTN import load_recipes_from_csv, display_recipe_list, find_recipes, State, pyhop, display_meal_plan
import math
off_white = '#fbffe4'
light_green = '#3d8d7a'
dark_green = '#2B5B50'

def main():
    

    root = tk.Tk()
    root.title("Simple Tkinter Window")
    root.geometry("1920x1080")
    root.configure(bg=off_white)

    canvas = tk.Canvas(root, width=1920, height=138)
    canvas.pack()

    ##############
    # Header bar #
    ##############

    # Add Header Background
    canvas.create_rectangle(0, 0, 1920, 138, fill=light_green)

    # Add Header Text
    canvas.create_text(230, 69, text="Fridge Friend", fill=off_white, font=('Helvetica', 50))
    canvas.create_text(1820, 110, text="V0.01 Demo", fill=off_white, font=('Helvetica', 20))


    ###############
    # Frame Setup #
    ###############
    
    frame_width = 0.25  # Each frame will take up 25% of the width

    frames = []
    for i in range(4):
        frame = tk.Frame(root, bg='blue')
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
    canvas.create_rectangle(
        (canvas_width - 450) / 2, 
        (canvas_height - 450) / 2, 
        (canvas_width + 450) / 2, 
        (canvas_height + 450) / 2, 
        fill=light_green, 
        outline=''
    )

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
    canvas.create_rectangle(
        (canvas_width - 450) / 2, 
        (canvas_height - body_height) / 2 - body_vertical_offset, 
        (canvas_width + 450) / 2, 
        (canvas_height + body_height) / 2 - body_vertical_offset, 
        fill=light_green, 
        outline=''
    )
    
    # Title Bar
    canvas.create_rectangle(
        (canvas_width - 450) / 2, 
        (canvas_height - body_height) / 2 - body_vertical_offset, 
        (canvas_width + 450) / 2, 
        (canvas_height - (body_height - title_height)) / 2 - body_vertical_offset, 
        fill=dark_green, 
        outline=''
    )

    # Title Text
    canvas.create_text(canvas_width / 2, (canvas_height - body_height) / 2 - body_vertical_offset + title_height / 2 - 55, text="Ingredients", fill=off_white, font=('Helvetica', 30))

    # Body Text
    ingredients = []
    ingredients_text = "Ingredients not implemented yet"
    canvas.create_text((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height - 80, text=ingredients_text, anchor='w', fill=off_white, font=('Helvetica', 20))
    
    # Buttons
    button_spread = 114
    button_width = 12
    button_vertical_offset = 110

    button = tk.Button(frames[1], text="Add", bg=light_green, fg=off_white, font=('Helvetica', 20), width=button_width)
    button_add = canvas.create_window(canvas_width / 2 - button_spread, (canvas_height + 450) / 2 + button_vertical_offset, window=button)
    button.config(command=add_button)

    button = tk.Button(frames[1], text="Remove", bg=light_green, fg=off_white, font=('Helvetica', 20), width=button_width)
    button_remove = canvas.create_window(canvas_width / 2 + button_spread, (canvas_height + 450) / 2 + button_vertical_offset, window=button)
    button.config(command=remove_button)

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
    canvas.create_rectangle(
        (canvas_width - 450) / 2, 
        (canvas_height - body_height) / 2 - body_vertical_offset, 
        (canvas_width + 450) / 2, 
        (canvas_height + body_height) / 2 - body_vertical_offset, 
        fill=light_green, 
        outline=''
    )
    
    # Title Bar
    canvas.create_rectangle(
        (canvas_width - 450) / 2, 
        (canvas_height - body_height) / 2 - body_vertical_offset, 
        (canvas_width + 450) / 2, 
        (canvas_height - (body_height - title_height)) / 2 - body_vertical_offset, 
        fill=dark_green, 
        outline=''
    )

    # Title Text
    canvas.create_text(canvas_width / 2, (canvas_height - body_height) / 2 - body_vertical_offset + title_height / 2 - 55, text="Meal Plan Settings", fill=off_white, font=('Helvetica', 30))

    # Body Text and Input
    canvas.create_text((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height - 80, text="Meals per day", anchor='w', fill=off_white, font=('Helvetica', 20))
    entry_meals_per_day = tk.Entry(frames[2], font=('Helvetica', 20), width=27, bg=off_white)
    entry_meals_per_day_window = canvas.create_window((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height - 40, anchor='w', window=entry_meals_per_day)

    canvas.create_text((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height, text="Number of days", anchor='w', fill=off_white, font=('Helvetica', 20))
    entry_number_of_days = tk.Entry(frames[2], font=('Helvetica', 20), width=27, bg=off_white)
    entry_number_of_days_window = canvas.create_window((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 40, anchor='w', window=entry_number_of_days)

    canvas.create_text((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 80, text="Cuisine preference", anchor='w', fill=off_white, font=('Helvetica', 20))
    entry_cuisine_preference = tk.Entry(frames[2], font=('Helvetica', 20), width=27, bg=off_white)
    entry_cuisine_preference_window = canvas.create_window((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 120, anchor='w', window=entry_cuisine_preference)

    canvas.create_text((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 160, text="Categories", anchor='w', fill=off_white, font=('Helvetica', 20))
    text_categories = tk.Text(frames[2], font=('Helvetica', 20), height=9, width=27, bg=off_white)
    text_categories_window = canvas.create_window((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 325, anchor='w', window=text_categories)

    ###############
    # Right Frame #
    ###############

    canvas = tk.Canvas(frames[3], width=canvas_width, height=canvas_height, bg=off_white, highlightthickness=0)
    canvas.pack(expand=True)

    # Draw the rectangle for the Recipes section
    canvas.create_rectangle(
        (canvas_width - 450) / 2,  # x1
        (canvas_height - body_height) / 2 - body_vertical_offset,  # y1
        (canvas_width + 450) / 2,  # x2
        (canvas_height + body_height) / 2 - body_vertical_offset,  # y2
        fill=light_green, 
        outline=''
    )

    # Draw the title bar
    canvas.create_rectangle(
        (canvas_width - 450) / 2, 
        (canvas_height - body_height) / 2 - body_vertical_offset, 
        (canvas_width + 450) / 2, 
        (canvas_height - (body_height - title_height)) / 2 - body_vertical_offset, 
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

    # Load and display recipes
    recipes = load_recipes_from_csv('recipes.csv')
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
    button.config(command=find_button)

    root.mainloop()

def upload_button():
    print("Upload Button Pressed")

def add_button():
    print("Add Button Pressed")

def remove_button():
    print("Remove Button Pressed")

def find_button():
    print("Find Button Pressed")



if __name__ == "__main__":
    main()