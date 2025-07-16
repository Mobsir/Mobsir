import streamlit as st
import asyncio
from NLP.Voice_Assistant import *
from NLP.Translation import *
from Computer_Vision.Image_Caption import *
from PIL import Image



favicon = Image.open("assets/favicon.jpg")
st.set_page_config(page_title="Mobsir", 
                   page_icon=favicon, 
                   layout="centered")

st.markdown(
    """
    <style>
    html, body, .stApp {
        background-color: black;
        color: white;
        height: 100%;
        margin: 0;
        padding: 0;
    }
    .container {
        display: flex;
        justify-content: center;        
        align-items: flex-start;        
        height: 100vh;                 
        padding-top: 150px;             
    }

    .mic {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background: radial-gradient(circle, #ffffff, #ffffff);
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% {box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.7);}
        70% {box-shadow: 0 0 0 40px rgba(255, 255, 255, 0);}
        100% {box-shadow: 0 0 0 0 rgba(255, 255, 255, 0);}
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="container">
        <div class="mic"></div>
    </div>
    """,
    unsafe_allow_html=True
)


async def start_point():
    await edge_speak("أهلاً بك! أنا مُبصر. قل: أهلا مبصر لنبدأ.")

    while True:
        command = listen_once(duration=3)
        if any(word in command for word in START_COMMANDS):
            await edge_speak("تمام! يمكنك قول استكشف المكان، التقط صورة، أو شكرًا مبصر.")
            break
        elif command:
            await edge_speak("لم أسمع أهلا مبصر، حاول مرة أخرى.")

    while True:
        command = listen_once(duration=3)

        if any(word in command for word in PHOTO_COMMANDS):
            img_path = capture_Family_image()
            if img_path:
                await edge_speak("تم التقاط الصورة وحفظها.")
            else:
                await edge_speak("وقعت مشكلة أثناء التصوير.")

        elif any(word in command for word in EXPLORE_COMMANDS):
            img_path = capture_image()
            if img_path:
                await edge_speak("تم التقاط الصورة، جاري إنشاء الوصف...")
                try:
                    caption = get_caption(model, image_processor, tokenizer, img_path)
                    translated_caption = translate_text(caption)
                    await edge_speak(f"وصف الصورة: {translated_caption}")
                except Exception as e:
                    print(f"❌ خطأ في مولد الوصف: {e}")
                    await edge_speak("لم أتمكن من إنشاء وصف للصورة.")
            else:
                await edge_speak("وقعت مشكلة أثناء التصوير.")

        elif any(word in command for word in EXIT_COMMANDS):
            await edge_speak("إلى اللقاء!")
            break

        elif command:
            await edge_speak("لم أفهم الطلب، أعد المحاولة.")


asyncio.run(start_point())
