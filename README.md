# (عندما يُصبح الصوت بصيرة)


 # Mobsir 👀🔉: Voice-Controlled Assistive System for the Blind

**Mobsir** is a low-cost, voice-driven assistive system designed to help blind or visually impaired individuals explore their surroundings through image captioning, facial recognition, and natural Arabic speech output.

---

## 🚀 Features

- 🎤 **Arabic Voice Assistant** to initiate interaction and receive commands
- 📸 **Capture and Describe Environment** with Transformer-based image captioning
- 🧑‍🦱 **Family Member Detection** via facial recognition
- 🌍 **Arabic Translation** for generated image descriptions
- 🔈 **Edge TTS Voice Output** for smooth, fast speech generation
- 🖼️ **Streamlit UI** with animated microphone interface
- 🧠 Fully asynchronous execution with fallback error handling

---

## 📁 Project Structure

mobsir/
├── NLP/
│ ├── Voice_Assistant.py # Audio input and TTS logic
│ └── Translation.py # English → Arabic translation
├── Computer_Vision/
│ ├── Image_Caption.py # Transformer image captioning
│ └── face_recognition.py # Face recognition and matching with family DB
├── assets/
│ └── favicon.jpg # App icon
├── main.py # Streamlit UI + Assistant control loop
├── requirements.txt
└── README.md


## Install dependencies:

pip install -r requirements.txt


## Run the app:

streamlit run main.py

