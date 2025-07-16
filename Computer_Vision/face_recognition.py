import os
import cv2
import numpy as np
import asyncio
from typing import List, Optional

# Try to import DeepFace with error handling
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    print("Warning: DeepFace not available. Face recognition will be disabled.")
    DEEPFACE_AVAILABLE = False

# Path to your family members' reference images
FAMILY_DATABASE_PATH = "family_photos"  # Update this path as needed

async def check_family_in_image(img_path: str) -> List[str]:
    """
    Check if any family members are present in the given image.
    
    Args:
        img_path (str): Path to the image to analyze
        
    Returns:
        List[str]: List of recognized family member names
    """
    if not DEEPFACE_AVAILABLE:
        print("DeepFace not available. Skipping face recognition.")
        return []
    
    try:
        if not os.path.exists(img_path):
            print(f"Error: Image path {img_path} does not exist")
            return []
        
        if not os.path.exists(FAMILY_DATABASE_PATH):
            print(f"Warning: Family database path {FAMILY_DATABASE_PATH} does not exist")
            return []
        
        recognized_family = []
        
        # Get all family member reference images
        family_images = []
        for file in os.listdir(FAMILY_DATABASE_PATH):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                family_images.append(os.path.join(FAMILY_DATABASE_PATH, file))
        
        if not family_images:
            print("No family reference images found")
            return []
        
        print(f"Checking against {len(family_images)} family members...")
        
        # Compare the captured image with each family member
        for family_img_path in family_images:
            try:
                # Use DeepFace to verify if the same person appears in both images
                result = DeepFace.verify(
                    img1_path=img_path,
                    img2_path=family_img_path,
                    model_name='VGG-Face',  # You can change this to 'Facenet', 'OpenFace', etc.
                    distance_metric='cosine',
                    enforce_detection=False  # Set to True if you want stricter face detection
                )
                
                # If faces match (verified as the same person)
                if result['verified']:
                    # Extract family member name from filename
                    family_name = os.path.splitext(os.path.basename(family_img_path))[0]
                    
                    # Clean up the name (remove underscores, numbers, etc.)
                    family_name = family_name.replace('_', ' ').replace('-', ' ')
                    
                    if family_name not in recognized_family:
                        recognized_family.append(family_name)
                        print(f"✅ Recognized: {family_name}")
            
            except Exception as e:
                print(f"Error comparing with {family_img_path}: {e}")
                continue
        
        return recognized_family
    
    except Exception as e:
        print(f"Error in family recognition: {e}")
        return []

def detect_faces_in_image(img_path: str) -> int:
    """
    Count the number of faces detected in an image.
    
    Args:
        img_path (str): Path to the image
        
    Returns:
        int: Number of faces detected
    """
    try:
        # Load the image
        image = cv2.imread(img_path)
        if image is None:
            return 0
        
        # Use OpenCV's face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        return len(faces)
    
    except Exception as e:
        print(f"Error detecting faces: {e}")
        return 0

def setup_family_database():
    """
    Create the family database directory if it doesn't exist.
    """
    if not os.path.exists(FAMILY_DATABASE_PATH):
        os.makedirs(FAMILY_DATABASE_PATH)
        print(f"Created family database directory: {FAMILY_DATABASE_PATH}")
        print("Please add family member photos to this directory.")
        print("Name the files with the person's name (e.g., 'Ahmed.jpg', 'Fatima.png')")

# Initialize the family database on import
setup_family_database()


