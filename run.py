from face import *

import pygame
import random
from PIL import Image
import subprocess
import threading
import cv2
import numpy as np
import time
import os
import sys


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

# Initialize global roop variables
global roop_execution
roop_execution = None

def wrap_text(font, text, max_width):
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph.split(' ')
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
    return lines

def resource_path(relative_path):
    """Donne le chemin absolu vers un fichier ressource, même après PyInstaller"""
    try:
        base_path = sys._MEIPASS  # quand c'est packagé avec PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_exe_dir():
    if getattr(sys, 'frozen', False):
        # Exécutable PyInstaller
        return os.path.dirname(sys.executable)
    else:
        # Exécution normale
        return os.path.dirname(os.path.abspath(__file__))


# 1.1 Start screen
def start_screen(face_detected):
    start_running = True

    while start_running:
        background_image = pygame.image.load(resource_path("background.jpg"))  # Charger l'image de fond
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Redimensionner l'image
        screen.blit(background_image, (0, 0))  # Afficher l'image de fond

        # Dessin du bouton Let's Go
        button_width = 300
        button_height = 80
        button_x = (SCREEN_WIDTH - button_width) // 2
        button_y = SCREEN_HEIGHT // 2
        go_button = pygame.draw.rect(screen, (199, 255, 250), (button_x, button_y, button_width, button_height), border_radius=15)

        go_font = pygame.font.SysFont(None, 50)
        go_text = go_font.render("Let's Go*", True, (30, 34, 56))
        screen.blit(go_text, (button_x + (button_width - go_text.get_width()) // 2,
                              button_y + (button_height - go_text.get_height()) // 2))

        # Texte avec astérisque en bas
        footnote_font = pygame.font.SysFont(None, 24)
        footnote_text = footnote_font.render("*Voir conditions auprès de personnel présent", True, (199, 255, 250))
        screen.blit(footnote_text, ((SCREEN_WIDTH - footnote_text.get_width()) // 2, SCREEN_HEIGHT - 40))

        # Afficher un message d'erreur si aucun visage détecté
        if not face_detected:
            error_font = pygame.font.SysFont(None, 36)
            error_text = error_font.render("Aucun visage trouvé, veuillez vous rapprocher et réessayer.", True, (255, 100, 100))
            screen.blit(error_text, ((SCREEN_WIDTH - error_text.get_width()) // 2, button_y - 60))

        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # clic gauche
                    if go_button.collidepoint(event.pos):
                        start_running = False  # Sort de la boucle et lance le jeu

# 1.2 Take a picture
def take_picture(face_detected):

    start_screen(face_detected)

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
    flash_start_time = None
    running = True

    while running:
        pygame.display.flip()
        background_image = pygame.image.load(resource_path("background.jpg"))  # Charger l'image de fond
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Redimensionner l'image
        screen.blit(background_image, (0, 0))  # Afficher l'image de fond

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

        # Effet de flash (non-bloquant)
        if flash_start_time:
            elapsed = pygame.time.get_ticks() - flash_start_time
            if elapsed < 300:  # Durée du flash
                flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                flash_surface.fill(WHITE)
                flash_surface.set_alpha(flash_alpha)
                screen.blit(flash_surface, (0, 0))
                flash_alpha = max(0, flash_alpha - 25)
            else:
                flash_start_time = None  # Fin du flash
                cap.release()
                running = False  # Quitte la boucle principale proprement

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
                        save_path = os.path.join(get_exe_dir(), "_internal/capture.png")
                        cv2.imwrite(save_path, photo)
                        print("Photo prise et enregistrée sous 'capture.png'.")

                    # Déclenchement du flash
                    flash_alpha = 255
                    flash_start_time = pygame.time.get_ticks()
                    taking_photo = False




# 2. Preprocess the image
def preprocess_image(image_path):
    global game_state

    label_gender, proba_gender ,label_race , proba_race = deepface(image_path)
    print(label_gender, proba_gender ,label_race , proba_race)

    if label_gender == None:
        return None, None

    selected_photo = f"photo_selection\{label_gender}_{label_race}.jpg"
    selected_video = f"video_selection\{label_gender}_{label_race}.mp4"

    print(selected_photo, selected_video)
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
    print(command)
    if keep_fps:
        command.append("--keep-fps")
    if skip_audio:
        command.append("--skip-audio")
    
    try:
        process = subprocess.Popen(command)
        process.wait()
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de Roop: {e}")
    except FileNotFoundError:
        print("Erreur: Assurez-vous que Roop est installé et accessible.")

# 3.2 Background thread for Roop
def background(select_photo, select_video):
    global roop_execution
    roop_execution = True
    roop(resource_path("capture.png"), select_photo, resource_path("output_photo.png"))
    roop(resource_path("capture.png"), select_video, resource_path("output_video.mp4"))
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

# 4.2 Display the tutorial screen
def tutorial():
    # Load and display the background image
    background_image = pygame.image.load(resource_path("explanation.jpg"))
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background_image, (0, 0))

    # Define the button dimensions and position
    button_width, button_height = 300, 80
    button_x = (SCREEN_WIDTH - button_width) // 2
    button_y = SCREEN_HEIGHT - 150
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    running = True
    while running:
        # Draw the button
        pygame.draw.rect(screen, (199, 255, 250), button_rect, border_radius=15)
        button_font = pygame.font.SysFont(None, 50)
        button_text = button_font.render("C'est parti !", True, BLACK)
        screen.blit(button_text, (button_x + (button_width - button_text.get_width()) // 2,
                                  button_y + (button_height - button_text.get_height()) // 2))

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos):
                    running = False  # Exit the loop when the button is clicked


# 4.3 Display the GAME
def display_game():
    start_time = pygame.time.get_ticks()
    real_images = [
        {"url": "Real/anne_hathaway.jpg", "real": True, "explanation": "Le visage d'Anne Hathaway est très détaillé, la peau n'est pas lisse comme sur les images générées par IA."},
        {"url": "Real/Bryan_Cranston.jpg", "real": True, "explanation": "C'est une vraie photo prise pour la série 'Breaking Bad'."},
        {"url": "Real/Forest_Image.jpg", "real": True, "explanation": "Cette image d'une forêt est très détaillée, les couleurs sont cohérentes et il n'y a pas d'éléments flous ou déformés."},
        {"url": "Real/Girl_Portrait_Lake.png", "real": True, "explanation": "Rien d'incohérent à signaler sur cette photo."},
        {"url": "Real/Girl_Portrait_Smile.png", "real": True, "explanation": "Bien que certaines zones soient floues et adoucies, c'est une vraie photographie."},
        {"url": "Real/Guy_Portrait.jpg", "real": True, "explanation": "Le regard est naturel, la barbe est bien dessinée et il n'y a pas d'éléments flous."},
        {"url": "Real/Henry_Cavill_Jason_Momoa.jpg", "real": True, "explanation": "Sur cette image de Henry Cavill et Jason Momoa, les éléments et les personnes en arrière-plan ne sont pas illogiques ou déformés."},
        {"url": "Real/Modern_House.png", "real": True, "explanation": "C'est une vraie photographie d'une maison moderne."},
        {"url": "Real/Robin Williams.jpg", "real": True, "explanation": "Sur cette photo, l'acteur Robin Williams a une peau détaillée ; rien n'est hors de l'ordinaire."},
        {"url": "Real/Willem_Dafoe.jpg", "real": True, "explanation": "Sur cette photo de Willem Dafoe, il y a de nombreux éléments d'arrière-plan très détaillés. Il est possible de retrouver cette image sur internet avec une recherche inversé ssur Google."},
        {"url": "Real/Person_exist.jpg", "real": True, "explanation": "C'est une vraie photographie d'une personne."},
    ]

    ai_images = [
        {"url": "AI/Beach_Selfie_AI.jpeg", "real": False, "explanation": "On peut voir le téléphone censé prendre la photo... sur la photo !"},
        {"url": "AI/Cola_Bottle_AI.jpg", "real": False, "explanation": "Le texte ici ne veut rien dire."},
        {"url": "AI/Deepfake1_AI.jpeg", "real": False, "explanation": "Ce deepfake de Tom Cruise est très bien réalisé et trompe de nombreux internautes sur TikTok."},
        {"url": "AI/Deepfake2_AI.png", "real": False, "explanation": "M. Macron ne se laisserait probablement pas pousser la barbe de cette façon et la liaison entre le visage et la barbe est ratée, c'est un deepfake."},
        {"url": "AI/Guy_Portrait_Sunny_AI.jpg", "real": False, "explanation": "Impressionnant, mais le regard et les yeux sont étranges."},
        {"url": "AI/Img_AI_Superman.jpeg", "real": False, "explanation": "Le fond est flou, la peau est trop lisse et on voit des imperfections de couleur sur l'avant du bras droit."},
        {"url": "AI/Modern_House_AI.jpg", "real": False, "explanation": "Bien que l'image soit très bien faite, il faut zoomer pour voir des incohérences (l'ombre de la chaise gauche et les plantes)."},
        {"url": "AI/Pope_Drip_2_AI.jpg", "real": False, "explanation": "Le pape François ne s'habillerait jamais de cette manière."},
        {"url": "AI/Rainy_Fence_Plants_AI.jpeg", "real": False, "explanation": "Il y a beaucoup trop de pots de fleurs et la facade est trop parfaite."},
        {"url": "AI/Squirrel_Picture_AI.jpg", "real": False, "explanation": "C'est un très beau fond d'écran inspiré de photographies mais généré par IA."},
        {"url": "AI/Trump_Arrest_AI.jpg", "real": False, "explanation": "Les visages des policiers sont flous et il y a de sérieux problèmes au niveau des jambes."},
        {"url": "AI/Will_Smith_Slap_AI.jpg", "real": False, "explanation": "L'IA a mal généré les doigts de Will Smith."},
        {"url": "AI/Woman_Fence_AI.jpg", "real": False, "explanation": "Très belle image, mais généré par IA. Cette image représente bien le niveau de l'IA générative aujourd'hui."},
        {"url": "AI/Woman_nature_AI.png", "real": False, "explanation": "Les yeux ne sont pas alignés avec le regard."},
        {"url": "AI/Woman_neon_AI.jpg", "real": False, "explanation": "Très belle image, mais généré par IA. Cette image représente bien le niveau de l'IA générative aujourd'hui."},
        {"url": "AI/Woman_Portrait_Plants_AI.jpg", "real": False, "explanation": "La plante en bas à droite n'est pas naturelle et ressemble à un amas de branches vertes sans réelle lien."},
        {"url": "AI/Person_dont_exist.jpg", "real": False, "explanation": "Cette image a été générée par une IA. Trouvez-en d'autres sur le site https://thispersondoesnotexist.com ."},
    ]


    # Combine and shuffle images
    images = real_images + ai_images
    random.shuffle(images)
    
    global current_image_index, score, show_explanation, explanation_text, game_state, roop_execution

    running = True  # Boucle interne pour gérer l'état "game"
    # Game state variables
    current_image_index = 0
    score = 0
    show_buttons = True
    max_possible_score = 0

    # Ajuster dynamiquement la taille de la police en fonction de la hauteur de l'écran
    dynamic_font_size = max(20, SCREEN_HEIGHT // 30)  # Taille minimale de 20
    dynamic_font = pygame.font.Font(None, dynamic_font_size)

    while running:
        explanation_alpha = 0
        background_image = pygame.image.load(resource_path("background2.jpg")) 
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)) 
        screen.blit(background_image, (0, 0))
        elapsed_time = pygame.time.get_ticks() - start_time

        if roop_execution == False and elapsed_time > 60000 and current_image_index >= 5 :  # 60 000 ms = 1 minute
            new_image = [images[current_image_index]]
            current_image_index = 0
            new_image.append( {
                "url": "output_photo.png",
                "real": False,
                "explanation": "Cette image est une Deepfake de vous ! Réalisée en 10sec, imaginée ce qu'il est possible de faire avec plus de temps et d'image de vous..."
            } )
            images = new_image
            roop_execution = None

            if current_image_index >= len(images):
                current_image_index = len(images) - 1

        if current_image_index < len(images):
            image_data = images[current_image_index]
            image_path = resource_path(image_data["url"])

            # Définir le rectangle pour l'image
            image_rect_width = SCREEN_WIDTH * 0.8  # 80% de la largeur de l'écran
            image_rect_height = SCREEN_HEIGHT * 0.6  # 60% de la hauteur de l'écran
            image_rect_x = (SCREEN_WIDTH - image_rect_width) // 2
            image_rect_y = (SCREEN_HEIGHT - image_rect_height) // 2 - 50

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
            button_width = SCREEN_WIDTH // 8  # 12.5% de la largeur de l'écran
            button_height = SCREEN_HEIGHT // 15  # 6.67% de la hauteur de l'écran
            button_spacing = SCREEN_WIDTH // 50  # Espacement entre les boutons

            # Calculer les positions des boutons
            true_button_x = (SCREEN_WIDTH // 2) - button_width - (button_spacing // 2)
            false_button_x = (SCREEN_WIDTH // 2) + (button_spacing // 2)
            button_y = image_rect_y + image_rect_height + 20

            # Dessiner les boutons
            if show_buttons:
                true_button = pygame.draw.rect(screen, GREEN, (true_button_x, button_y, button_width, button_height))
                false_button = pygame.draw.rect(screen, RED, (false_button_x, button_y, button_width, button_height))

                # Texte des boutons
                true_text = dynamic_font.render("Vrai", True, (30, 34, 56))
                false_text = dynamic_font.render("Faux", True, (30, 34, 56))
                screen.blit(true_text, (true_button_x + (button_width - true_text.get_width()) // 2,
                                        button_y + (button_height - true_text.get_height()) // 2))
                screen.blit(false_text, (false_button_x + (button_width - false_text.get_width()) // 2,
                                        button_y + (button_height - false_text.get_height()) // 2))
            elif show_explanation :
                if explanation_alpha < 180:
                    explanation_alpha += 10

                box_width = SCREEN_WIDTH * 0.4  # Largeur de la boîte
                box_height = SCREEN_HEIGHT // 5.5  # Hauteur de la boîte
                box_x = (SCREEN_WIDTH - box_width) // 2
                box_y = button_y  # Garde la position Y d'origine ou modifie-la si nécessaire

                # Affichage de la boîte colorée contenant l'explication
                explanation_box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
                pygame.draw.rect(screen, (199, 255, 250), explanation_box_rect, border_radius=15)

                # Affichage du texte d'explication
                wrapped_text = wrap_text(dynamic_font, explanation_text, explanation_box_rect.width - 20)

                for i, line in enumerate(wrapped_text):
                    line_surface = dynamic_font.render(line, True, (30, 34, 56))
                    # Centrage horizontal
                    line_x = explanation_box_rect.x + (explanation_box_rect.width - line_surface.get_width()) // 2
                    line_y = explanation_box_rect.y + 10 + i * (dynamic_font.get_height() + 5)
                    screen.blit(line_surface, (line_x, line_y))

                # Taille et position du bouton "Next"
                next_button_width = int(SCREEN_WIDTH * 0.2)
                next_button_height = 40

                # Utiliser les coordonnées de la boîte d'explication pour positionner le bouton
                next_button_x = int(explanation_box_rect.x + (explanation_box_rect.width - next_button_width) // 2)
                next_button_y = int(explanation_box_rect.y + explanation_box_rect.height - next_button_height - 10)

                # Dessiner le bouton sur l'écran
                next_button = pygame.draw.rect(
                    screen,
                    (7,12,34), 
                    (next_button_x, next_button_y, next_button_width, next_button_height),
                    border_radius=8
                )

                # Afficher le texte sur le bouton (facultatif)
                font = pygame.font.SysFont(None, 24)
                text_surface = font.render("Suivant", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(next_button_x + next_button_width // 2, next_button_y + next_button_height // 2))
                screen.blit(text_surface, text_rect)

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
                                    explanation_text = f"Bien joué, c'est une vraie image ! \n {images[current_image_index]['explanation']}"
                                else:
                                    explanation_text = f"Dommage, c'est fake ! \n {images[current_image_index]['explanation']}"
                                show_explanation = True
                                show_buttons = False
                            elif false_button.collidepoint(event.pos):
                                if not images[current_image_index]["real"]:
                                    score += 1
                                    explanation_text = f"Bien joué, l'image est fake ! \n {images[current_image_index]['explanation']}"
                                else:
                                    explanation_text = f"Dommage, c'est une vraie image ! \n {images[current_image_index]['explanation']}"
                                show_explanation = True
                                show_buttons = False
                        elif next_button and next_button.collidepoint(event.pos):
                            current_image_index += 1
                            max_possible_score += 1
                            show_explanation = False
                            show_buttons = True
                            if current_image_index >= len(images):
                                print("Fin du jeu !")

                                background_image = pygame.image.load(resource_path("background2.jpg"))
                                background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                                screen.blit(background_image, (0, 0))

                                game_over_text = dynamic_font.render(f"Fin du jeu ! Votre score: {score}/{max_possible_score}", True, WHITE)
                                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                                            SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
                                pygame.display.flip()
                                pygame.time.wait(3000)

                                running = False
                                game_state = "game_over"

        pygame.display.flip()



# 5. Game Over function
def game_over():
    global game_state
    running = True
    video_path = resource_path("output_video.mp4")
    cap = cv2.VideoCapture(video_path)

    # Dimensions fixes pour la vidéo
    video_display_width = 800
    video_display_height = 450

    clock = pygame.time.Clock()
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or np.isnan(fps):
        fps = 30  # fallback de secours


    while running:
        # Charger et afficher l'image de fond
        background_image = pygame.image.load(resource_path("background2.jpg"))
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background_image, (0, 0))

        # Lire la vidéo
        ret, frame = cap.read()
        if ret:
            # Convertir la frame pour Pygame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (video_display_width, video_display_height))
            frame = cv2.flip(frame, 1)
            frame = np.rot90(frame, k=1) 
            frame = pygame.surfarray.make_surface(frame)

            # Calculer les coordonnées pour centrer la vidéo
            video_x = (SCREEN_WIDTH - video_display_width) // 2
            video_y = (SCREEN_HEIGHT - video_display_height) // 2 - 50 
            screen.blit(frame, (video_x, video_y))

        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Redémarrer la vidéo si elle est terminée


        # Ajouter un message sous la vidéo avec gestion des sauts de ligne
        message_text = "Merci d'avoir participé à notre expérience immersive !\nSi vous avez des questions, n'hésitez pas à nous en faire part.\n \n /!\ \nTous les outils utilisés ici sont libres et accessibles gratuitement.\nCela montre à quel point il est facile et rapide aujourd’hui de manipuler des images.\nRestez vigilants face aux contenus que vous voyez en ligne.\nVérifiez toujours la source et faite une recherche inversée sur l'image pour comparer !\n"
        lines = message_text.split("\n")
        line_height = font.get_height() 

        # Afficher chaque ligne de texte
        for i, line in enumerate(lines):
            message_surface = font.render(line, True, WHITE)  # Utiliser une couleur blanche
            message_x = (SCREEN_WIDTH - message_surface.get_width()) // 2
            message_y = video_y + video_display_height + 20 + i * line_height  # Décalage vertical pour chaque ligne
            screen.blit(message_surface, (message_x, message_y))


        # Dessiner le bouton "Finir"
        button_width, button_height = 200, 60
        margin = 30  # marge du bord de l'écran
        button_x = SCREEN_WIDTH - button_width - margin
        button_y = SCREEN_HEIGHT - button_height - margin

        finish_button = pygame.draw.rect(screen, RED, (button_x, button_y, button_width, button_height), border_radius=10)

        finish_text = font.render("Fin", True, WHITE)
        screen.blit(finish_text, (button_x + (button_width - finish_text.get_width()) // 2,
                                  button_y + (button_height - finish_text.get_height()) // 2))

        clock.tick(fps)
        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_state = "take_picture"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if finish_button.collidepoint(event.pos):
                    running = False
                    game_state = "take_picture"

    game_state = "take_picture"
    cap.release()



if __name__ == "__main__":
    running = True
    show_explanation = False
    roop_execution = False
    explanation_text = ""
    face_detected = True
    game_state = "take_picture"

    while running:
        if game_state == "take_picture":
            take_picture(face_detected)
            select_photo, select_video = preprocess_image(resource_path("capture.png"))
            
            if select_photo is None:
                face_detected = False
                continue

            face_detected = True
            roop_thread = threading.Thread(target=background, args=(select_photo, select_video))
            roop_thread.start()

            game_state = "game"

        elif game_state == "game":
            tutorial()
            display_game()

        elif game_state == "game_over":
            game_over()
            game_state = "take_picture"

    pygame.quit()