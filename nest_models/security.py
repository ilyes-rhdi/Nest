import optuna
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import paho.mqtt.client as mqtt
import pandas as pd
import numpy as np
import json
from datetime import datetime
import mtcnn as MTCNN
import keras_facenet  as Facenet
import torch
from scipy.spatial.distance import cosine
import cv2
from skimage import io
import warnings
warnings.filterwarnings('ignore')
plt.style.use('dark_background')
model= MTCNN.MTCNN()
def detect_and_crop_faces_from_video(video_path, target_size=(224, 224)):
    cap = cv2.VideoCapture(video_path)
    detector = MTCNN()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print(" Fin de la vidéo ou erreur de lecture.")
            break

        faces_data = detector.detect_faces(frame)

        if faces_data:
            print(f" {len(faces_data)} visage(s) détecté(s).")

            cropped_faces = []
            for face in faces_data:
                x, y, w, h = face['box']

                # S'assurer que les coordonnées sont valides
                x, y = max(0, x), max(0, y)
                face_crop = frame[y:y+h, x:x+w]

                if face_crop.size > 0:
                    face_resized = cv2.resize(face_crop, target_size)
                    cropped_faces.append(face_resized)

            cap.release()
            return frame, cropped_faces  # Image d’origine + visages recadrés

        # Affichage facultatif
        cv2.imshow('Lecture vidéo (q = quitter)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None, []

def reading_img(image_path):
  img=cv2.imread(image_path)
  image=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
  return image
def Embadding(image_with_detection):
  model = Facenet.FaceNet()
  embedding = model.embeddings([image_with_detection])[0]
  return embedding
def is_similar(embedding1, embedding2, threshold=0.7):
    distance = cosine(embedding1, embedding2)
    print(f"Distance cosinus : {distance:.4f}")
    return distance < threshold, distance
def compare_faces(img1, img2):
    face1 = img1
    face2 = img2

    if face1 is not None and face2 is not None:
        plt.style.use('dark_background')
        plt.figure(figsize=(15, 7))
        plt.subplot(1, 2, 1)
        plt.imshow(face1)
        plt.title('Face 1')
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.imshow(face2)
        plt.title('Face 2')
        plt.axis('off')
        plt.show()

        embed1 = Embadding(face1)
        embed2 = Embadding(face2)

        similar, distance = is_similar(embed1, embed2)

        return {
            "similar": similar,
            "distance": distance
        }

    else:
        return {
            "error": "One or both faces not detected."
        }
import requests

def get_users_with_photos():
    url = "http://localhost:8090/api/collections/users/records"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(" Erreur lors de la récupération des utilisateurs depuis PocketBase.")
    
    users = response.json().get("items", [])

    result = []
    for user in users:
        if user.get("avatar"):  # si le champ 'photo' n'est pas vide
            photo_url = f"http://localhost:8090/api/files/users/{user['id']}/{user['avatar']}"
            result.append({
                "id": user["id"],
                "name": user.get("name", ""),
                "photo_url": photo_url
            })

    if not result:
        raise ValueError(" Aucun utilisateur avec photo trouvé dans PocketBase.")
    
    return result
def Showing(img1,img2) :
   result = compare_faces(img1, img2)
   if result.get("similar"):
      print("✅ Visages similaires")
   else:
      print("❌ Pas de correspondance")
def download_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(io.BytesIO(response.content)).convert('RGB')
        return np.array(img)
    else:
        print(f"Erreur lors du téléchargement de l'image: {url}")
        return None
try:
    users = get_users_with_photos()
    for user in users:
        print(f"{user['name']} → {user['photo_url']}")
except ValueError as ve:
    print(str(ve))  # Aucun utilisateur avec photo
except Exception as e:
    print(f"Erreur inattendue : {str(e)}")

def verify_faces_against_database(video_path, threshold=0.7):
    original_frame, detected_faces = detect_and_crop_faces_from_video(video_path)
    
    if not detected_faces:
        print("Aucun visage détecté dans la vidéo.")
        return []

    # Étape 2 : Récupérer les utilisateurs avec photo depuis PocketBase
    try:
        users = get_users_with_photos()
    except Exception as e:
        print(f" Erreur PocketBase : {e}")
        return []

    matches = []

    for i, detected_face in enumerate(detected_faces):
        print(f"\nVérification du visage détecté #{i + 1}")
        for user in users:
            db_face = download_image_from_url(user["photo_url"])
            if db_face is None:
                continue

            result = compare_faces(detected_face, db_face)

            if result.get("similar"):
                print(f"Correspondance trouvée avec {user['name']} (Distance : {result['distance']:.4f})")
                matches.append({
                    "face_index": i,
                    "user_id": user["id"],
                    "user_name": user["name"],
                    "distance": result["distance"]
                })
                break  # Optionnel : on arrête à la première correspondance
            else:
                print(f"Pas de correspondance avec {user['name']} (Distance : {result.get('distance', 'N/A')})")

    if not matches:
        print("Aucune correspondance trouvée.")
    return matches
