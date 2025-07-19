import os
import cv2
import json
import numpy as np
from numpy.linalg import norm
from insightface.app import FaceAnalysis

def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))


def check_family_in_image(family_folder,image_path, labels_path="labels.json", threshold=0.5):
    """
    Verifies which known people from a folder are present in the group image.

    Args:
        reference_img_folder (str): Folder path containing images of known individuals.
        group_img_path (str): Path to the group image to verify against.
        model_name (str): DeepFace model to use for verification (default is 'ArcFace').

    Returns:
        list: A list of strings describing the friends found, e.g., ['رحاب - صديق مبصر', ...]
    """
    app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"]) ## using CPU
    # app = FaceAnalysis(name="buffalo_l", providers=["CUDAExecutionProvider"]) ## using GPU
    app.prepare(ctx_id=0)


    img = cv2.imread(image_path)
    if img is None:
        print(f"تعذر تحميل الصورة من المسار: {image_path}")
        return []
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detected_faces = app.get(img)

    if not detected_faces:
        print("❌مفيش وجوه واضحة في الصورة.")
        return []

    known_embeddings = []
    known_names = []

    for filename in os.listdir(family_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(family_folder, filename)
            known_img = cv2.imread(img_path)
            if known_img is None:
                 print(f"❌ تعذر تحميل الصورة من المسار: {img_path}")
                 continue
            known_img = cv2.cvtColor(known_img, cv2.COLOR_BGR2RGB)
            faces = app.get(known_img)
            if not faces:
                print(f"⚠ مفيش وجه واضح في {filename}")
                continue
            known_embeddings.append(faces[0].embedding)
            known_names.append(os.path.splitext(filename)[0])

  
    if os.path.exists(labels_path):
        with open(labels_path, "r", encoding="utf-8") as f:
            label_map = json.load(f)
    else:
        label_map = {}

    found_people = set()
    for detected_face in detected_faces:
        for known_name, known_emb in zip(known_names, known_embeddings):
            sim = cosine_similarity(detected_face.embedding, known_emb)
            if sim > threshold:
                label = label_map.get(known_name, known_name)
                found_people.add(label)

    return list(found_people)


if __name__ == "__main__":
    known_people_folder = "family" ## family folder path
    group_photo_path = ".\group.jpg"  ## a group of people to test the model
    friends = check_family_in_image(known_people_folder, group_photo_path)

    print("\nالأصدقاء اللي موجودين فعلاً:")
    for f in friends:
        print(f"{f}")
