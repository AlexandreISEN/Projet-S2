
import pygame
import random
from PIL import Image
import subprocess
import threading
import cv2
import numpy as np
import time



# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

#Name of the window
pygame.display.set_caption("Real or Fake Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

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


global roop_execution
roop_execution = None

# 1.Take a picture
def take_picture():
    # Display camera
    CAMERA_WIDTH, CAMERA_HEIGHT = 640, 360
    # Open the camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    # Capture a frame
    BUTTON_WIDTH, BUTTON_HEIGHT = 300, 60
    button_rect = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT - 100), (BUTTON_WIDTH, BUTTON_HEIGHT))
    button_color = RED
    flash_alpha = 0 
    taking_photo = False

    running = True
    while running:
        pygame.display.flip()
        screen.fill(WHITE)

        # Capture image webcam
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)  # Rotation pour l'orientation correcte
            frame = pygame.surfarray.make_surface(frame)
            frame = pygame.transform.scale(frame, (CAMERA_WIDTH, CAMERA_HEIGHT))

            # Positionner l'image au centre de l'écran
            screen.blit(frame, (SCREEN_WIDTH // 2 - CAMERA_WIDTH // 2, SCREEN_HEIGHT // 2 - CAMERA_HEIGHT // 2))

        # Dessiner le bouton (changement de couleur lors du clic)
        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
        text = font.render("Prendre la photo", True, WHITE)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        # Effet de flash (animation après capture)
        if flash_alpha > 0:
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surface.fill(WHITE)
            flash_surface.set_alpha(flash_alpha)
            screen.blit(flash_surface, (0, 0))
            flash_alpha -= 10  # Réduction progressive du flash

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Quitter avec Échap
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos) and not taking_photo:
                    taking_photo = True
                    button_color = GREEN  # Le bouton devient vert brièvement
                    pygame.display.flip()
                    time.sleep(1)  # Petit délai pour l'effet de clic
                    button_color = RED

                    # Capture et enregistrement de la photo
                    ret, photo = cap.read()
                    if ret:
                        cv2.imwrite("capture.png", photo)
                        print("Photo prise et enregistrée sous 'capture.png'.")

                    # Déclenchement du flash
                    flash_alpha = 255  
                    taking_photo = False  
                    cap.release()
                    running = False


# 2. Preprocess the image   (A COMPLETER : CODE DE DETECTION DU VISAGE)
def preprocess_image(image_path):

    selected_photo = r"C:\Users\cc2qk\Documents\ISEN4\PROJET_Deepface\selection_photo\man_white.jpg"
    selected_video = r"C:\Users\cc2qk\Documents\ISEN4\PROJET_Deepface\selection_video\man_white.mp4"

    return selected_photo, selected_video

# 3. Function to create a deepfake using Roop
def roop(source_image: str, target_video: str, output_video: str, 
                     keep_fps=True, skip_audio=False, execution_provider="cuda"):
    command = [
        "python", "roop/run.py",
        "-s", source_image,
        "-t", target_video,
        "-o", output_video,
        "--execution-provider", execution_provider
    ]
    
    if keep_fps:
        command.append("--keep-fps")
    if skip_audio:
        command.append("--skip-audio")
    
    try:
        process = subprocess.Popen(command)
        process.wait()
        print("Deepfake généré avec succès!")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de Roop: {e}")
    except FileNotFoundError:
        print("Erreur: Assurez-vous que Roop est installé et accessible.")

# 3.2 Background thread for Roop
def background(select_photo, select_video):
    global roop_execution
    roop_execution = True
    roop("capture.png", select_photo, "output_photo.png")
    #roop("capture.png", select_video, "output_video.mp4") # Uncomment if needed
    print("Roop a été exécuté en arrière-plan.")
    roop_execution = False

# 4.1 Load an image using pygame
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
    
# 4.2 Display the GAME
def display_game():
    global current_image_index, score, show_explanation, explanation_text, game_state, roop_execution

    running = True  # Boucle interne pour gérer l'état "game"

    while running:
        screen.fill(WHITE)

        if roop_execution == False:
            ai_images.append({
                "url": "output_photo.png",
                "real": False,
                "explanation": "Cette image a été capturée et ajoutée automatiquement."
            })
            images.append(ai_images[-1])  # Ajouter également à la liste globale des images
            roop_execution = None  # Éviter de l'ajouter plusieurs fois

            if current_image_index >= len(images):
                current_image_index = len(images) - 1

        if current_image_index < len(images):
            image_data = images[current_image_index]
            image_path = image_data["url"]

            # Définir le rectangle pour l'image
            image_rect_width = 1200  # Largeur du rectangle
            image_rect_height = 800  # Hauteur du rectangle
            image_rect_x = (SCREEN_WIDTH - image_rect_width) // 2
            image_rect_y = (SCREEN_HEIGHT - image_rect_height) // 2 - 50  # Légèrement au-dessus du centre

            # Charger et redimensionner l'image
            image = load_image(image_path)
            if image:
                # Redimensionner l'image pour qu'elle s'adapte au rectangle tout en conservant les proportions
                image_width, image_height = image.get_width(), image.get_height()
                scale_factor = min(image_rect_width / image_width, image_rect_height / image_height)
                scaled_width = int(image_width * scale_factor)
                scaled_height = int(image_height * scale_factor)
                scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))

                # Centrer l'image redimensionnée dans le rectangle
                image_x = image_rect_x + (image_rect_width - scaled_width) // 2
                image_y = image_rect_y + (image_rect_height - scaled_height) // 2
                screen.blit(scaled_image, (image_x, image_y))

            # Dimensions des boutons
            button_width = 150
            button_height = 50
            button_spacing = 20  # Espace entre les boutons

            # Calculer les positions des boutons
            true_button_x = (SCREEN_WIDTH // 2) - button_width - (button_spacing // 2)
            false_button_x = (SCREEN_WIDTH // 2) + (button_spacing // 2)
            button_y = image_rect_y + image_rect_height + 20  # En dessous de l'image

            # Dessiner les boutons
            true_button = pygame.draw.rect(screen, GREEN, (true_button_x, button_y, button_width, button_height))
            false_button = pygame.draw.rect(screen, RED, (false_button_x, button_y, button_width, button_height))

            # Texte des boutons
            true_text = font.render("True", True, WHITE)
            false_text = font.render("False", True, WHITE)
            screen.blit(true_text, (true_button_x + (button_width - true_text.get_width()) // 2,
                                    button_y + (button_height - true_text.get_height()) // 2))
            screen.blit(false_text, (false_button_x + (button_width - false_text.get_width()) // 2,
                                     button_y + (button_height - false_text.get_height()) // 2))

            # Afficher le texte d'explication si nécessaire
            if show_explanation:
                explanation_surface = font.render(explanation_text, True, BLACK)
                explanation_x = (SCREEN_WIDTH - explanation_surface.get_width()) // 2
                explanation_y = button_y + button_height + 20  # En dessous des boutons
                screen.blit(explanation_surface, (explanation_x, explanation_y))

                # Dessiner le bouton "Next"
                next_button_width = 100
                next_button_height = 40
                next_button_x = SCREEN_WIDTH - next_button_width - 20  # Coin inférieur droit
                next_button_y = SCREEN_HEIGHT - next_button_height - 20
                next_button = pygame.draw.rect(screen, BLACK, (next_button_x, next_button_y, next_button_width, next_button_height))

                next_text = font.render("Next", True, WHITE)
                screen.blit(next_text, (next_button_x + (next_button_width - next_text.get_width()) // 2,
                                        next_button_y + (next_button_height - next_text.get_height()) // 2))
            else:
                next_button = None

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    if event.button == 1:  # Clic gauche
                        if not show_explanation:
                            if true_button.collidepoint(event.pos):
                                if images[current_image_index]["real"]:
                                    score += 1
                                    explanation_text = f"Bien joué! {images[current_image_index]['explanation']}"
                                else:
                                    explanation_text = f"Dommage! {images[current_image_index]['explanation']}"
                                show_explanation = True
                            elif false_button.collidepoint(event.pos):
                                if not images[current_image_index]["real"]:
                                    score += 1
                                    explanation_text = f"Bien joué! {images[current_image_index]['explanation']}"
                                else:
                                    explanation_text = f"Dommage! {images[current_image_index]['explanation']}"
                                show_explanation = True
                        elif next_button and next_button.collidepoint(event.pos):
                            current_image_index += 1
                            show_explanation = False
                            print("Next image...", current_image_index, len(images))
                            if current_image_index >= len(images):
                                print("Fin du jeu !")
                                running = False  # Sortir de la boucle interne

        else:
            # Afficher l'écran de fin de jeu
            game_over_text = font.render(f"Game Over ! Your score: {score}/{max_possible_score}", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False  # Sortir de la boucle interne
            game_state = "game_over"

        pygame.display.flip()



if __name__ == "__main__":
    running = True
    show_explanation = False
    roop_execution = False
    explanation_text = ""
    game_state = "take_picture"

    while running:
        if game_state == "take_picture":
            print("Prendre une photo...")
            take_picture()
            select_photo, select_video = preprocess_image("capture.png")
            print("Prétraitement de l'image terminé.")
            
            roop_thread = threading.Thread(target=background, args=(select_photo, select_video))
            roop_thread.start()

            game_state = "game"

        elif game_state == "game":
            display_game()  # Appeler une seule fois, la boucle interne gère tout

        elif game_state == "game_over":
            print(f"Game Over ! Your score: {score}/{max_possible_score}")
            running = False

    pygame.quit()