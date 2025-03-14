import tkinter as tk
import math

def main():
    off_white = '#fbffe4'
    light_green = '#3d8d7a'
    dark_green = '#2B5B50'

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
    entry_meals_per_day = tk.Entry(frames[2], font=('Helvetica', 20), width=27)
    entry_meals_per_day_window = canvas.create_window((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height - 40, anchor='w', window=entry_meals_per_day)

    canvas.create_text((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height, text="Number of days", anchor='w', fill=off_white, font=('Helvetica', 20))
    entry_number_of_days = tk.Entry(frames[2], font=('Helvetica', 20), width=27)
    entry_number_of_days_window = canvas.create_window((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 40, anchor='w', window=entry_number_of_days)

    canvas.create_text((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 80, text="Cuisine preference", anchor='w', fill=off_white, font=('Helvetica', 20))
    entry_cuisine_preference = tk.Entry(frames[2], font=('Helvetica', 20), width=27)
    entry_cuisine_preference_window = canvas.create_window((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 120, anchor='w', window=entry_cuisine_preference)

    canvas.create_text((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 160, text="Categories", anchor='w', fill=off_white, font=('Helvetica', 20))
    text_categories = tk.Text(frames[2], font=('Helvetica', 20), height=9, width=27)
    text_categories_window = canvas.create_window((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height + 325, anchor='w', window=text_categories)

    ###############
    # Right Frame #
    ###############

    canvas = tk.Canvas(frames[3], width=canvas_width, height=canvas_height, bg=off_white, highlightthickness=0)
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
    canvas.create_text(canvas_width / 2, (canvas_height - body_height) / 2 - body_vertical_offset + title_height / 2 - 55, text="Recipes", fill=off_white, font=('Helvetica', 30))

    # Body Text
    recipes = []
    recipes_text = "Recipes not implemented yet"
    canvas.create_text((canvas_width - 450) / 2 + 20, (canvas_height - body_height) / 2 - body_vertical_offset + title_height - 80, text=recipes_text, anchor='w', fill=off_white, font=('Helvetica', 20))

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