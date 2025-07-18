import os
from deepface import DeepFace

def verify_multiple_people(reference_img_folder: str, group_img_path: str, model_name: str = "ArcFace") -> list:
    """
    Verifies which known people from a folder are present in the group image.

    Args:
        reference_img_folder (str): Folder path containing images of known individuals.
        group_img_path (str): Path to the group image to verify against.
        model_name (str): DeepFace model to use for verification (default is 'ArcFace').

    Returns:
        list: A list of strings describing the friends found, e.g., ['رحاب - صديق مبصر', ...]
    """
    friends_found = []

    for filename in os.listdir(reference_img_folder):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            person_path = os.path.join(reference_img_folder, filename)
            name = os.path.splitext(filename)[0]
            label = {name}
            try:
                result = DeepFace.verify(
                    img1_path=person_path,
                    img2_path=group_img_path,
                    model_name=model_name,
                    enforce_detection=False
                )
                is_present = result.get("verified", False)

                if is_present:
                    friends_found.append(label)

            except Exception as e:
                print(f"⚠️ حصل خطأ مع {name}: {e}")

    return friends_found




if __name__ == "__main__":
    known_people_folder = "family" ## family folder path
    group_photo_path = "group.jpg"  ## a group of people to test the model
    friends = verify_multiple_people(known_people_folder, group_photo_path)

    print("\nالأصدقاء اللي موجودين فعلاً:")
    for f in friends:
        print(f"{f}")
