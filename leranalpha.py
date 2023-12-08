import os
import tkinter as tk
from tkinter import PhotoImage, Entry, Button, Toplevel, Canvas
from PIL import Image, ImageTk
import random
#Hit
# Define root as a global variable
root = None

# Global variables for canvas items and images
champion_canvas = None
lane_canvas = None
mythics_canvas = None
cover_canvas = None  # New canvas item for covering the second window
champion_image = None
lane_image = None
mythics_image = None
cover_image = None  # New PhotoImage for covering the second window
last_champion_index = -1
last_lane_index = -1
last_mythics_index = -1

# Global variable for user input
user_input_text = None

# Global variable for shuffling counter
shuffle_counter = 0
total_shuffles = 5  # Adjust the total number of shuffles as needed

def load_images():
    global champion_image, lane_image, mythics_image, last_champion_index, last_lane_index, last_mythics_index

    # Use the global keyword to access the global variables
    global champion_images, lane_images, mythics_images

    # List of image file paths
    champion_folder = 'images/Champions'
    lane_folder = 'images/Lanes'
    mythics_folder = 'images/Mythics'

    # Check if any image paths are available
    if not os.path.exists(champion_folder) or not os.path.exists(lane_folder) or not os.path.exists(mythics_folder):
        print("Error: Image directories not found.")
        return

    champion_images = os.listdir(champion_folder)
    lane_images = os.listdir(lane_folder)
    mythics_images = os.listdir(mythics_folder)

    # Check if any image paths are available
    if not champion_images or not lane_images or not mythics_images:
        print("Error: No image paths found.")
        return

    # Randomly select an image path for each category
    last_champion_index = random.randint(0, len(champion_images) - 1)
    last_lane_index = random.randint(0, len(lane_images) - 1)
    last_mythics_index = random.randint(0, len(mythics_images) - 1)

    random_champion_path = os.path.join(champion_folder, champion_images[last_champion_index])
    random_lane_path = os.path.join(lane_folder, lane_images[last_lane_index])
    random_mythics_path = os.path.join(mythics_folder, mythics_images[last_mythics_index])

    # Load new images with a brief delay
    update_images(random_champion_path, random_lane_path, random_mythics_path)

# Rest of your code remains unchanged

def update_images(champion_path, lane_path, mythics_path):
    global champion_image, lane_image, mythics_image

    # Load new images
    champion_image = ImageTk.PhotoImage(file=champion_path)
    lane_image = ImageTk.PhotoImage(file=lane_path)
    mythics_image = ImageTk.PhotoImage(file=mythics_path)

    # Update the images on the canvas in the second window
    my_canvas.itemconfig(champion_canvas, image=champion_image)
    my_canvas.itemconfig(lane_canvas, image=lane_image)
    my_canvas.itemconfig(mythics_canvas, image=mythics_image)

    # Add borders around the images
    add_border(champion_canvas)
    add_border(lane_canvas)
    add_border(mythics_canvas)

def add_border(canvas_item):
    bbox = my_canvas.bbox(canvas_item)
    border_width = 3  # Adjust the border width as needed
    my_canvas.create_rectangle(bbox, outline="black", width=border_width)

def add_label_with_image(canvas):
    # Load the background image for the label
    label_bg = PhotoImage(file='images/Banners/textentrybanw2.png')

    # Create a label with the image
    label = canvas.create_image(480, 50, image=label_bg, anchor='center')

    # To prevent garbage collection
    canvas.itemconfig(label, image=label_bg)
    canvas.itemconfig(label, anchor='center')
    canvas.itemconfig(label, tags=('label',))  # Add a tag to the label

    # Create a border around the label
    bbox = canvas.bbox(label)
    border_width = 3  # Adjust the border width as needed
    canvas.create_rectangle(bbox, outline="#C2C6C6", width=border_width)

    return label

def destroy_root_window():
    global user_input_text

    # Withdraw (hide) the main window
    root.withdraw()

    # Get the user input text
    user_input_text = user_name.get()

    # Display the entered text on the second window canvas
    display_text = f"Hello {user_input_text}! It is time to lose your next game!"
    text_item = my_canvas.create_text(480, 50, text=display_text, font=('Helvetica', 16, ), fill='#F8EAA0')

    # Add label with image
    label = add_label_with_image(my_canvas)

    # Load images for the second window
    load_images()

    # Raise the text item to overlay other canvas items
    my_canvas.tag_raise(text_item)

    # Raise the label to be above the text item
    my_canvas.tag_raise(label)

    # Deiconify (restore) the second window immediately
    new_window.deiconify()

    return text_item

def randomize_images():
    # Reset shuffle counter
    global shuffle_counter
    shuffle_counter = 0
    
    # Schedule the image update after a brief delay
    root.after(100, shuffle_images)

def shuffle_images():
    global shuffle_counter

    # Check if we still need to shuffle
    if shuffle_counter < total_shuffles:
        load_images()
        # Schedule the next shuffle after a brief delay
        root.after(100, shuffle_images)
        shuffle_counter += 1
    else:
        # After shuffling 5 times, pick a result
        pick_result()

def pick_result():
    # Update the images one last time to show the final result
    load_images()

    # Add label with image
    final_label = add_label_with_image(my_canvas)

    # Raise the label to be above the text item
    my_canvas.tag_raise(final_label)

# Create main window
root = tk.Tk()
root.title("Lightz League Tools")
root.geometry("900x500")

# Create canvas for the main window
my_canvas = Canvas(root, width=900, height=500)
my_canvas.pack(fill='both', expand=True)

# Background image for the main window
bg1 = PhotoImage(file='images\Backgrounds\league1.png')
my_canvas.create_image(0, 0, image=bg1, anchor='nw')

# Text label on the main window
my_canvas.create_text(450, 40, text='Lightz League Randomizer', font=('Helvetica', 40), fill='orange')

# Create "continue" button on the main window
photo = PhotoImage(file=r"images/Buttons/continue2.png")
photo_image = photo.subsample(1, 1)

def continue_button_click():
    destroy_root_window()
con_button2 = Button(root, image=photo_image,
                     height=25,
                     width=85,
                     fg='#37d3ff',
                     bg='#001d26',
                     bd=10, relief=tk.RAISED,
                     highlightthickness=4,
                     highlightcolor="#37d3ff",
                     highlightbackground="#37d3ff",
                     borderwidth=4,
                     command=continue_button_click)
con_b2window = my_canvas.create_window(440, 280, anchor='center', window=con_button2)

# Text box for user input
user_name = Entry(root, font=('Helvetica', 9), bd=2)
user_name.insert(0, " Summoner Name: ")
user_name.place(x=350, y=220, width=180, height=30)

# Define entry bind
def entry_clear(e):
    user_name.delete(0, tk.END)

# Bind the text box to the screen with a placeholder 'clear' after a button press
user_name.bind('<Button-1>', entry_clear)

# Create a second window
new_window = Toplevel(root)
new_window.title('Randomized Results!')
new_window.geometry('900x500')
new_window.withdraw()

# Canvas for the second window
my_canvas = Canvas(new_window, width=900, height=500)
my_canvas.pack(fill='both', expand=True)

# Background image for the second window
bg2 = PhotoImage(file='images\Backgrounds\league2origtan1.png')
my_canvas.create_image(0, 0, image=bg2, anchor='nw')

# Load the image for covering the second window
#cover_image = PhotoImage(file='')  ## Place Image border here (must be transparent and at least 900x900? maybe 1kx1k)

# Create canvas item for the new image covering the second window
cover_canvas = my_canvas.create_image(0, 0, image=cover_image, anchor='nw')

# Set the coordinates and size to cover the desired area
my_canvas.coords(cover_canvas, 530, 260)
my_canvas.itemconfig(cover_canvas, anchor='center', tags=('cover_image',))  # Add tags if needed

# Create canvas items for images in the second window
champion_canvas = my_canvas.create_image(100, 160, anchor='nw')
lane_canvas = my_canvas.create_image(330, 160, anchor='nw')
mythics_canvas = my_canvas.create_image(640, 160, anchor='nw')

# Create "randomize" button on the second window
photo_randomize = PhotoImage(file=r"images/Buttons/randomize.png")
photo_close = PhotoImage(file=r"images/Buttons/close.png")

ran_button2 = Button(new_window, image=photo_randomize,
                    height=25, width=85,
                    fg='#37d3ff',
                    bg='#001d26',
                    bd=4,
                    relief=tk.RAISED,
                    highlightthickness=4,
                    highlightcolor="#37d3ff",
                    highlightbackground="#37d3ff",
                    command=randomize_images)
ran_b2window = my_canvas.create_window(450, 400, anchor='center', window=ran_button2)

# Create "close" button on the second window
close_button3 = Button(new_window, image=photo_close,
                       height=20,
                       width=80,
                       fg='#37d3ff',
                       bg='#001d26',
                       bd=4,
                       relief=tk.RAISED,
                       highlightthickness=4,
                       highlightcolor="#37d3ff",
                       highlightbackground="#37d3ff",
                       command=new_window.withdraw)
cls_b3window = my_canvas.create_window(70, 470, anchor='center', window=close_button3)

# Load the background image for the text entry box
text_entry_bg = PhotoImage(file='images/Banners/textentrybanw2.png')
my_canvas.create_image(480, 50, image=text_entry_bg)  # Adjust coordinates as needed

# Start the main event loop
root.mainloop()
