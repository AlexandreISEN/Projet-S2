
import pygame
import random
from PIL import Image
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# Base Screen dimensions (unused)
#SCREEN_WIDTH = 800
#SCREEN_HEIGHT = 600
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Real or Fake Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)


#{"url": "Real/Cat_Image.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    #{"url": "Real/Forest_Image.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    #{"url": "Real/Girl_Portrait_Lake.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    #{"url": "Real/Girl_Portrait_Smile.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    #{"url": "Real/Guy_Portrait.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},
    #{"url": "Real/Modern_House.jpg", "real": True, "explanation": "This is a real photograph taken by a professional."},




# List of image URLs from the "Real" and "AI" folders
real_images = [
    {"url": "Real/anne_hathaway.jpg", "real": True, "explanation": "Le visage de Anne Hathaway est très détaillé, la peau n'est pas 'lisse' comme les images créées par IA."},
    {"url": "Real/Bryan_Cranston.jpg", "real": True, "explanation": "C'est une vraie photo prise pour la série 'Breaking Bad'."},
    {"url": "Real/Henry_Cavill_Jason_Momoa.jpg", "real": True, "explanation": "Sur cette image de Henry Cavill et Jason Momoa, les éléments et gens en fond ne sont pas illogiques ou déformés."},
    {"url": "Real/Robin Williams.jpg", "real": True, "explanation": "Sur cette photo, l'acteur Robin Williams a une peau détaillée, rien n'est hors de l'ordinaire sur l'image."},
    {"url": "Real/Willem_Dafoe.jpg", "real": True, "explanation": "Sur cette photo de Willem Dafoe, il y a beaucoup d'éléments d'arrière plan très détaillés."}
]

ai_images = [
    {"url": "AI/Beach_Selfie_AI.jpeg", "real": False, "explanation": "On peut voir le téléphone qui est censé prendre la photo SUR la photo."},
    {"url": "AI/Cola_Bottle_AI.jpg", "real": False, "explanation": "Le texte ici ne veut rien dire."},
    {"url": "AI/Guy_Portrait_Sunny_AI.jpg", "real": False, "explanation": "Le fond est très flou et ne semble pas 'naturel'."},
    {"url": "AI/Img_AI_Superman.jpeg", "real": False, "explanation": "Le fond est très flou, la peau trop 'lisse' et on peut voir des imperfections au niveau de la cape."},
    {"url": "AI/Modern_House_AI.jpg", "real": False, "explanation": "Bien que l'image soit très bien faite, elle est presque 'trop parfaite'."},
    {"url": "AI/Pope_Drip_1_AI.jpg", "real": False, "explanation": "Le pape ne s'habillerait jamais comme ça."},
    {"url": "AI/Pope_Drip_2_AI.jpg", "real": False, "explanation": "Le pape ne porterait jamais ce manteau."},
    {"url": "AI/Rainy_Fence_Plants_AI.jpeg", "real": False, "explanation": "Il y a beaucoup trop de pots de fleurs."},
    {"url": "AI/Squirrel_Picture_AI.jpg", "real": False, "explanation": "Le fond est flou et l'image a l'air trop 'parfaite'."},
    {"url": "AI/Trump_Arrest_AI.jpg", "real": False, "explanation": "Les visages des policiers sont flous, il y a des problèmes au niveau des jambes."},
    {"url": "AI/Will_Smith_Slap_AI.jpg", "real": False, "explanation": "Ils n'auraient pas pu prendre la photo en se faisant frapper, et l'IA a raté les doigts."}
]

# Combine and shuffle images
images = real_images + ai_images
random.shuffle(images)

# Game state variables
current_image_index = 0
score = 0
max_possible_score = len(images)

# Load an image using pygame
def load_image(image_path):
    try:
        pil_image = Image.open(image_path).convert("RGB")
        #pil_image = pil_image.resize((800, 600))
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        return pygame.image.fromstring(data, size, mode)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None

# Display the current image and buttons
def display_game():
    global current_image_index, score, show_explanation, explanation_text

    screen.fill(WHITE)

    if current_image_index < len(images):
        image_data = images[current_image_index]
        image_path = image_data["url"]

        # Define the rectangle for the image
        image_rect_width = 1200  # Width of the rectangle
        image_rect_height = 800  # Height of the rectangle
        image_rect_x = (SCREEN_WIDTH - image_rect_width) // 2
        image_rect_y = (SCREEN_HEIGHT - image_rect_height) // 2 - 50  # Slightly above center

        # Load and scale the image
        image = load_image(image_path)
        if image:
            # Scale the image to fit within the rectangle while maintaining proportions
            image_width, image_height = image.get_width(), image.get_height()
            scale_factor = min(image_rect_width / image_width, image_rect_height / image_height)
            scaled_width = int(image_width * scale_factor)
            scaled_height = int(image_height * scale_factor)
            scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))

            # Center the scaled image within the rectangle
            image_x = image_rect_x + (image_rect_width - scaled_width) // 2
            image_y = image_rect_y + (image_rect_height - scaled_height) // 2
            screen.blit(scaled_image, (image_x, image_y))

        # Define button dimensions
        button_width = 150
        button_height = 50
        button_spacing = 20  # Space between buttons

        # Calculate button positions
        true_button_x = (SCREEN_WIDTH // 2) - button_width - (button_spacing // 2)
        false_button_x = (SCREEN_WIDTH // 2) + (button_spacing // 2)
        button_y = image_rect_y + image_rect_height + 20  # Below the image

        # Draw buttons
        true_button = pygame.draw.rect(screen, GREEN, (true_button_x, button_y, button_width, button_height))
        false_button = pygame.draw.rect(screen, RED, (false_button_x, button_y, button_width, button_height))

        # Display button text
        true_text = font.render("True", True, WHITE)
        false_text = font.render("False", True, WHITE)
        screen.blit(true_text, (true_button_x + (button_width - true_text.get_width()) // 2,
                                button_y + (button_height - true_text.get_height()) // 2))
        screen.blit(false_text, (false_button_x + (button_width - false_text.get_width()) // 2,
                                 button_y + (button_height - false_text.get_height()) // 2))

        # Show explanation text if the user has answered
        if show_explanation:
            explanation_surface = font.render(explanation_text, True, BLACK)
            explanation_x = (SCREEN_WIDTH - explanation_surface.get_width()) // 2
            explanation_y = button_y + button_height + 20  # Below the buttons
            screen.blit(explanation_surface, (explanation_x, explanation_y))

            # Draw the "Next" button
            next_button_width = 100
            next_button_height = 40
            next_button_x = SCREEN_WIDTH - next_button_width - 20  # Bottom-right corner
            next_button_y = SCREEN_HEIGHT - next_button_height - 20
            next_button = pygame.draw.rect(screen, BLACK, (next_button_x, next_button_y, next_button_width, next_button_height))

            next_text = font.render("Next", True, WHITE)
            screen.blit(next_text, (next_button_x + (next_button_width - next_text.get_width()) // 2,
                                    next_button_y + (next_button_height - next_text.get_height()) // 2))

            return true_button, false_button, next_button

        return true_button, false_button, None
    else:
        # Display game over screen
        game_over_text = font.render(f"Game Over! Your score: {score}/{max_possible_score}", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                     SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        exit()

# Main game loop
running = True
show_explanation = False
explanation_text = ""

while running:
    true_button, false_button, next_button = display_game()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if not show_explanation:  # Only allow answering if explanation is not shown
                    if true_button.collidepoint(event.pos):
                        if images[0]["real"]:
                            score += 1
                            explanation_text = f"Bien joué! {images[0]['explanation']}"
                        else:
                            explanation_text = f"Dommage! {images[0]['explanation']}"
                        show_explanation = True
                    elif false_button.collidepoint(event.pos):
                        if not images[0]["real"]:
                            score += 1
                            explanation_text = f"Success! {images[0]['explanation']}"
                        else:
                            explanation_text = f"Wrong! {images[0]['explanation']}"
                        show_explanation = True
                elif next_button and next_button.collidepoint(event.pos):  # Handle "Next" button
                    images.pop(0)  # Remove the displayed image
                    show_explanation = False  # Reset explanation state

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Allow exiting fullscreen with the Escape key
                running = False

pygame.quit()

# Main game loop
running = True
while running:
    true_button, false_button = display_game()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if true_button.collidepoint(event.pos):
                    if images[0]["real"]:
                        score += 1
                    images.pop(0)  # Remove the displayed image
                elif false_button.collidepoint(event.pos):
                    if not images[0]["real"]:
                        score += 1
                    images.pop(0)  # Remove the displayed image
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Allow exiting fullscreen with the Escape key
                running = False

pygame.quit()