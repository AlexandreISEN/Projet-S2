import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from io import BytesIO

# List of image URLs from the "Real" and "AI" folders
real_images = [
    {"url": "Real/anne_hathaway.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    {"url": "Real/anne_hathaway.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    {"url": "Real/Bryan_Cranston.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    {"url": "Real/Cat_Image.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    {"url": "Real/Forest_Image.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    {"url": "Real/Girl_Portrait_Lake.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    {"url": "Real/Girl_Portrait_Smile.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    {"url": "Real/Girl_Portrait.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    {"url": "Real/Guy_Portrait.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    {"url": "Real/Henry_Cavill_Jason_Momoa.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    {"url": "Real/Modern_House.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    {"url": "Real/Robin_Williams.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    {"url": "Real/Willem_Dafoe.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."}
]

ai_images = [
    {"url": "AI/Beach_Selfie_AI.jpeg", "real": False, "explanation": "This image was AI-generated using deep learning."},
    {"url": "AI/Cola_Bottle_AI.jpg", "real": False, "explanation": "This image was AI-generated using deep learning."},
    {"url": "AI/Guy_Portrait_Sunny_AI.jpg", "real": False, "explanation": "This image was AI-generated using deep learning."},
    {"url": "AI/Img_AI_Superman.jpeg", "real": False, "explanation": "This image was AI-generated using deep learning."},
    {"url": "AI/Modern_House_AI.jpg", "real": False, "explanation": "This image was AI-generated using deep learning."},
    {"url": "AI/Pope_Drip_1_AI.jpg", "real": False, "explanation": "This image was AI-generated using deep learning."},
    {"url": "AI/Pope_Drip_2_AI.jpg", "real": False, "explanation": "This image was AI-generated using deep learning."},
    {"url": "AI/Rainy_Fence_Plants_AI.jpeg", "real": False, "explanation": "This image was AI-generated using deep learning."},
    {"url": "AI/Squirrel_Picture_AI.jpg", "real": False, "explanation": "This image was AI-generated using deep learning."},
    {"url": "AI/Trump_Arrest_AI.jpg", "real": False, "explanation": "This image was AI-generated using deep learning."},
    {"url": "AI/Will_Smith_Slap_AI.jpg", "real": False, "explanation": "This image was AI-generated using deep learning."}
]

# Combine and shuffle images
images = real_images + ai_images
random.shuffle(images)

# Game state variables
current_image_index = 0
score = 0

# Initialize main window
root = tk.Tk()
root.title("Real or Fake Game")

# Load and display an image
def load_image():
    global current_image_index, img_label, img_display

    if current_image_index < len(images):
        image_data = images[current_image_index]

        # Load and resize the image
        img = Image.open(image_data["url"]).convert("RGB")  # Converts to standard RGB format
        img = img.resize((400, 300))  # Resize image
        img_display = ImageTk.PhotoImage(img)

        # Update the label with the new image
        img_label.config(image=img_display)
        img_label.image = img_display
    else:
        end_game()

# Check user answer
def check_answer(user_choice):
    global score, current_image_index

    if current_image_index < len(images):  
        if images[current_image_index]["real"] == user_choice:
            score += 1

        current_image_index += 1
        load_image()  # Load next image

# Display game over message
def end_game():
    img_label.config(image='', text=f"The game is over!\nYour score: {score}/{len(images)}", font=("Arial", 16))
    img_label.pack()
    btn_true.pack_forget()
    btn_false.pack_forget()

# Create UI elements
img_label = tk.Label(root)
img_label.pack()

btn_true = tk.Button(root, text="True", command=lambda: check_answer(True), font=("Arial", 12))
btn_true.pack(side=tk.LEFT, padx=10)

btn_false = tk.Button(root, text="False", command=lambda: check_answer(False), font=("Arial", 12))
btn_false.pack(side=tk.RIGHT, padx=10)

# Load the first image
load_image()

# Start the GUI loop
root.mainloop()



import os

image_path = "C:\\Users\\alexa\\OneDrive - JUNIA Grande école d'ingénieurs\\Documents\\Cours\\4e année\\Projet\\Real\\Guy_Portrait.jpg"
print("File exists:", os.path.exists(image_path))



from PIL import Image

path = "C:/Users/alexa/OneDrive - JUNIA Grande école d'ingénieurs/Documents/Cours/4e année/Projet/Real/Guy_Portrait.jpg"
img = Image.open(path)
img.show()