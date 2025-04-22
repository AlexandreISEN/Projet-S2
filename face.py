import cv2
import numpy as np
from deepface import DeepFace


def detect_faces(image_path):
    """
    Détecte tous les visages dans une image et renvoie leurs coordonnées ainsi que l'image chargée.
    Utilise Haar cascades (rapide mais basique).
    """
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Image introuvable ou format non pris en charge.")
    except Exception as e:
        print(f"Erreur de chargement de l'image: {e}")
        return None, None

    # Redimensionner l'image si elle est trop grande pour optimiser la détection
    max_dim = 800
    height, width = img.shape[:2]
    if max(height, width) > max_dim:
        scaling_factor = max_dim / float(max(height, width))
        img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Détection des visages
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(faces) == 0:
        print("Aucun visage détecté.")
        return None, None

    return faces, img


def analyze_face(image_path, face_coords, margin=10):

    results = []
    img = cv2.imread(image_path)
    height, width, _ = img.shape


    if face_coords is None or len(face_coords) == 0:
        print("Aucun visage détecté.")
        return []

    # Zone englobante des visages avec marge réduite
    x_min = max(min([x for (x, y, w, h) in face_coords]) - margin, 0)
    y_min = max(min([y for (x, y, w, h) in face_coords]) - margin, 0)
    x_max = min(max([x + w for (x, y, w, h) in face_coords]) + margin, width)
    y_max = min(max([y + h for (x, y, w, h) in face_coords]) + margin, height)

    cropped_img = img[y_min:y_max, x_min:x_max].copy()

    for (x, y, w, h) in face_coords:
        face = img[y:y+h, x:x+w]

        try:
            analysis = DeepFace.analyze(img_path=face, actions=['gender'], enforce_detection=False)
            gender = analysis[0]['dominant_gender']
        except Exception as e:
            print(f"Erreur d'analyse DeepFace : {e}")
            age = "Inconnu"

        skin_color = detect_skin_color(face)

        results.append({
            "genre": gender,
            "couleur de peau": skin_color,

        })

        # Ellipse étroite et haute (style œuf)
        x_rel, y_rel = x - x_min, y - y_min
        center = (x_rel + w // 2, y_rel + h // 2)
        axes = (int(w * 0.4), int(h * 0.65))  # Moins large, plus haut
        cv2.ellipse(cropped_img, center, axes, angle=0, startAngle=0, endAngle=360, color=(0, 255, 0), thickness=2)

    return results

def detect_skin_color(face):
    """
    Estime le teint de peau basé sur la teinte moyenne (Hue) dans l'espace HSV.
    """
    hsv = cv2.cvtColor(face, cv2.COLOR_BGR2HSV)

    # Masque pour ne garder que les zones plausibles de peau (valeurs ajustées)
    mask = cv2.inRange(hsv, (0, 30, 60), (50, 255, 255))

    h, s, v = cv2.split(hsv)
    v_values = v[mask > 0]

    if len(v_values) == 0:
        return "Indéterminée"

    avg_v = np.mean(v_values)

    # Classification basée sur la luminosité (canal V)
    if avg_v > 200:
        return "Peau très claire"
    elif avg_v > 170:
        return "Peau claire"
    elif avg_v > 130:
        return "Peau métissée"
    elif avg_v > 90:
        return "Peau foncée"
    else:
        return "Peau très foncée"


def main(image_path):
    """
    Fonction principale : détecte les visages, les analyse, affiche et imprime les résultats.
    """
    faces, img = detect_faces(image_path)

    if faces is None:
        return

    results = analyze_face(image_path,faces)

    for i, res in enumerate(results):
        print(f"  Genre : {res['genre']}")
        print(f"  Couleur de peau : {res['couleur de peau']}")


def deepface (img_path):
    try:
        result = DeepFace.analyze(img_path, actions=['gender','race'])
    except Exception as e:
        print(f"Erreur détectée lors de l'analyse DeepFace : {e}")
        return None, None, None, None
    proba_gender = result[0]['gender']
    proba_race = result[0]['race']
    label_gender = max(proba_gender, key=proba_gender.get)
    label_race = 'white' if proba_race['white'] > proba_race['black'] else 'black'
    return label_gender, proba_gender[label_gender],label_race , proba_race[label_race]


# Exemple d'utilisation
if __name__ == "__main__":
    image_path = 'photo_selection/Man_black.jpg'  # Remplacer par ton chemin
    main(image_path)
    print(deepface(image_path))