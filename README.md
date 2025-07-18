# 👁️‍🗨️ مُبصر  (عندما يُصبح الصوت بصيرة)

# **Mobsir 👀🔉: Voice-Controlled Assistive System for the Blind**

**Mobsir** is a low-cost, voice-driven assistive system designed to help blind or visually impaired individuals explore their surroundings using cutting-edge technologies such as image captioning, facial recognition, and natural Arabic speech output.

---

## 🚀 Features

* 🎤 **Arabic Voice Assistant** to initiate interaction and receive spoken commands
* 🖼️ **Image Captioning** to describe the user's surroundings using Transformer models
* 👤 **Facial Recognition** to identify family members
* 🔤 **Arabic Translation** for English image descriptions
* 🔈 **Edge TTS** or `pyttsx3` for fast, natural Arabic voice output
* 🌐 **Streamlit UI** with an interactive, animated microphone interface
* ⚙️ **Asynchronous Execution** for responsive and smooth user experience
* 🛡️ Built-in **fallback and error handling** mechanisms

---

## 📁 Project Structure

```
mobsir/
├── NLP/
│   ├── Voice_Assistant.py         # 🎤 Audio input and Arabic Text-to-Speech (Edge TTS / pyttsx3)
│   └── Translation.py             # 🔤 English → Arabic translation
│
├── Computer_Vision/
│   ├── Image_Caption.py           # 🖼️ Transformer-based image captioning
│   └── face_recognition.py        # 👤 Face recognition & family member identification
│
├── assets/
│   └── favicon.jpg                # 🌐 Streamlit page icon
│
├── main.py                        # 🖥️ Streamlit UI + asynchronous voice assistant control
├── requirements.txt               # 📦 Project dependencies
└── README.md                      # 📄 Project documentation
```

---

## ⚙️ Installation

Make sure you have Python 3.8+ installed. Then install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the App

Launch the app using Streamlit:

```bash
streamlit run main.py
```
