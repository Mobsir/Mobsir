import asyncio
import cv2
import time
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import edge_tts
import os
import pygame
import unicodedata
from datetime import datetime


FAMILY_FOLDER = "family"
CAPTURE_FOLDER = "captured_images"
for folder in [FAMILY_FOLDER, CAPTURE_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Initialize pygame mixer for playing TTS audio
pygame.mixer.init()

def normalize_text(text):
    """
    Normalize Arabic text by removing diacritics and converting to lowercase.

    This function uses Unicode normalization to strip combining characters (harakat)
    and then returns the clean, lowercased text.

    Args:
        text (str): Arabic text to normalize.

    Returns:
        str: Normalized text without diacritics and in lowercase.
    """
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return text.lower().strip()

# List of recognized voice commands (normalized)
START_COMMANDS = [normalize_text(cmd) for cmd in ["أَهْلًا مُبْصِر", "مَرْحَبًا مُبْصِر", "السَّلَامُ عَلَيْك"]]
EXPLORE_COMMANDS = [normalize_text(cmd) for cmd in ["اِسْتَكْشِفْ المَكَان", "اِسْتَكْشَاف المَكَان", "اِسْتِكْشَاف"]]
PHOTO_COMMANDS = [normalize_text(cmd) for cmd in ["اِلْتَقِطْ صُورَة", "صَوِّرْ", "أَخَذْ صُورَة"]]
EXIT_COMMANDS = [normalize_text(cmd) for cmd in ["شُكْرًا مُبْصِر", "إِنْهَاء", "خُرُوج"]]

# Text-to-Speech using Edge TTS
async def edge_speak(text):
    """
    Convert Arabic text to speech using Edge TTS and play it.

    This function creates an MP3 file using Edge TTS with an Arabic voice,
    plays it using pygame, and then deletes the file after playback.

    Args:
        text (str): Arabic text to speak.
    """
    voice = "ar-EG-SalmaNeural"
    filename = "temp.mp3"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        pygame.mixer.music.unload()
        if os.path.exists(filename):
            os.remove(filename)

# Speech recognition
def listen_once(duration=3, fs=16000):
    """
    Record a short audio clip from the microphone and transcribe it to text.

    Uses Google Speech Recognition (with Arabic language) to convert speech to text.
    Normalizes the result before returning.

    Args:
        duration (int, optional): Recording duration in seconds. Default is 3.
        fs (int, optional): Sample rate in Hz. Default is 16000.

    Returns:
        str: Normalized recognized text, or an empty string if recognition fails.
    """
    print("🎤 يَسْتَمِعُ...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    filename = "temp.wav"
    write(filename, fs, recording)

    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="ar-EG")
        print(f" قُلْتَ: {text}")
        return normalize_text(text)
    except sr.UnknownValueError:
        print("لَمْ أَفْهَمِ الكَلَامَ")
        return ""
    except sr.RequestError as e:
        print(f"خَطَأٌ فِي خِدْمَةِ التَّعَرُّفِ: {e}")
        return ""
    finally:
        if os.path.exists(filename):
            os.remove(filename)

# Image capture functions

def capture_Family_image():
    """
    Capture an image and save it to the 'family' folder with a custom name.

    Prompts the user to enter a filename, checks for duplicates, and saves
    the captured photo using OpenCV.

    Returns:
        str or None: File path of the saved image if successful, or None if failed.
    """
    print("سَيَتِمُّ التَّصْوِيرُ بَعْدَ ٣ ثَوَانٍ... اِبْتَسِمْ ")
    time.sleep(3)

    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            raise Exception("📷 لَمْ أَتَمَكَّنْ مِنْ فَتْحِ الكَامِيرَا")

        ret, frame = cam.read()
        cam.release()

        if not ret:
            raise Exception("لَمْ أَتَمَكَّنْ مِنْ التَّقَاطِ الصُّورَة")

        while True:
            img_name_input = input("أَدْخِلِ اسْمَ الصُّورَةِ (بدون امتداد): ").strip()

            if img_name_input:
                img_name_clean = "".join(c for c in img_name_input if c.isalnum())
                if not img_name_clean:
                    print("هَذَا الاِسْمُ غَيْرُ صَالِحٍ، جَرِّبِ اسْمًا آخَرَ.")
                    continue

                img_path = os.path.join(FAMILY_FOLDER, f"{img_name_clean}.png")

                if os.path.exists(img_path):
                    print("الصُّورَةُ مَوْجُودَةٌ بِالفِعْلِ. اِخْتَرِ اسْمًا آخَرَ.")
                else:
                    break
            else:
                print("لَمْ تُدْخِلِ أَيَّ اسْمٍ، جَرِّبْ مَرَّةً أُخْرَى.")

        cv2.imwrite(img_path, frame)
        print("تَمَّ التَّقَاطُ الصُّورَةِ.")
        return img_path

    except Exception as e:
        print(f" خَطَأٌ: {e}")
        return None

def capture_image():
    """
    Capture an image and save it to the 'captured_images' folder using a unique timestamp.

    Uses OpenCV to take the photo, waits for 3 seconds before capturing, and
    saves the image file with a timestamp-based name.

    Returns:
        str or None: File path of the saved image if successful, or None if failed.
    """
    print(" سَيَتِمُّ التَّصْوِيرُ بَعْدَ ٣ ثَوَانٍ... اِبْتَسِمْ ")
    time.sleep(3)

    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            raise Exception("📷 لَمْ أَتَمَكَّنْ مِنْ فَتْحِ الكَامِيرَا")

        ret, frame = cam.read()
        cam.release()

        if not ret:
            raise Exception("📷 لَمْ أَتَمَكَّنْ مِنْ التَّقَاطِ الصُّورَة")


        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_filename = f"image_{timestamp}.png"
        img_path = os.path.join(CAPTURE_FOLDER, img_filename)

        cv2.imwrite(img_path, frame)

        print(f" تَمَّ التَّقَاطُ الصُّورَةِ وَتَخْزِينُهَا: {img_path}")
        return img_path

    except Exception as e:
        print(f"خَطَأٌ: {e}")
        return None
