import streamlit as st
from PIL import Image
import asyncio
import os
import re
import threading
import sys

# Import your modules with error handling
try:
    from NLP.Voice_Assistant import *
    from NLP.Translation import *
    from Computer_Vision.Image_Caption import *
    from Computer_Vision.face_recognition import check_family_in_image
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Safe favicon loading
try:
    if os.path.exists("assets/favicon.jpg"):
        favicon = Image.open("assets/favicon.jpg")
        st.set_page_config(page_title="Mobsir", page_icon=favicon, layout="centered")
    else:
        st.set_page_config(page_title="Mobsir", layout="centered")
except Exception as e:
    st.set_page_config(page_title="Mobsir", layout="centered")

# CSS styles
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

def contains_person_keywords(text):
    """Check if the caption contains person-related keywords."""
    english_keywords = [
        'person', 'people', 'man', 'woman', 'men', 'women', 
        'boy', 'girl', 'child', 'children', 'baby', 'adult',
        'guy', 'lady', 'gentleman', 'individual', 'human',
        'someone', 'somebody', 'figure', 'character'
    ]
    
    arabic_keywords = [
        'شخص', 'أشخاص', 'رجل', 'امرأة', 'رجال', 'نساء',
        'ولد', 'بنت', 'طفل', 'أطفال', 'طفلة', 'بالغ',
        'شاب', 'فتاة', 'سيدة', 'أحد', 'شخصية', 'فرد'
    ]
    
    all_keywords = english_keywords + arabic_keywords
    text_lower = text.lower()
    
    for keyword in all_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
            return True
    return False

def run_async_function(coro):
    """Helper function to run async functions in Streamlit."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    except Exception as e:
        print(f"Async execution error: {e}")
        return None

async def enhance_caption_with_family(original_caption, img_path):
    """Enhance the caption with family member names if they are detected."""
    try:
        family_members = await check_family_in_image(img_path)
        
        if family_members:
            valid_names = [name for name in family_members if name and name.strip()]
            
            if valid_names:
                names_text = "، ".join(valid_names)
                enhanced_caption = f"{original_caption} كما يوجد في الصورة: {names_text}."
                return enhanced_caption, valid_names
    
    except Exception as e:
        print(f"Warning: Family recognition failed: {e}")
    
    return original_caption, []

def run_voice_assistant():
    """Main function to run the voice assistant."""
    
    async def start_point():
        try:
            await edge_speak("أهلاً بك! أنا مُبصر. قل: أهلا مبصر لنبدأ.")
            
            # Initial greeting loop
            while True:
                command = listen_once(duration=3)
                if any(word in command for word in START_COMMANDS):
                    await edge_speak("تمام! يمكنك قول استكشف المكان، التقط صورة، أو شكرًا مبصر.")
                    break
                elif command:
                    await edge_speak("لم أسمع أهلا مبصر، حاول مرة أخرى.")
            
            # Main command loop
            while True:
                command = listen_once(duration=3)
                
                if any(word in command for word in PHOTO_COMMANDS):
                    img_path = capture_Family_image()
                    if img_path:
                        await edge_speak("تم التقاط الصورة وحفظها.")
                        try:
                            family = await check_family_in_image(img_path)
                            if family:
                                names = "، ".join(family)
                                await edge_speak(f"الأشخاص الموجودين في الصورة: {names}")
                            else:
                                await edge_speak("لا يوجد أحد من أفراد العائلة في الصورة.")
                        except Exception as e:
                            print(f"❌ خطأ في التعرف على الوجوه: {e}")
                            await edge_speak("لم أتمكن من التعرف على الأشخاص في الصورة.")
                    else:
                        await edge_speak("وقعت مشكلة أثناء التصوير.")
                
                elif any(word in command for word in EXPLORE_COMMANDS):
                    img_path = capture_image()
                    if img_path:
                        await edge_speak("تم التقاط الصورة، جاري إنشاء الوصف...")
                        try:
                            # Generate caption
                            caption = get_caption(model, image_processor, tokenizer, img_path)
                            print(f"Original caption: {caption}")
                            
                            # Check for person and enhance with family recognition
                            if contains_person_keywords(caption):
                                print("Person detected in caption. Running family recognition...")
                                enhanced_caption, family_members = await enhance_caption_with_family(caption, img_path)
                                translated_caption = translate_text(enhanced_caption)
                                await edge_speak(f"وصف الصورة: {translated_caption}")
                                
                                if family_members:
                                    names = "، ".join(family_members)
                                    await edge_speak(f"كما يوجد من أفراد العائلة: {names}")
                            else:
                                print("No person mentioned in caption. Skipping family recognition.")
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
                    
        except Exception as e:
            print(f"Error in voice assistant: {e}")
            await edge_speak("حدث خطأ في النظام.")
    
    # Run the async function
    return run_async_function(start_point())

# Run the application
if __name__ == "__main__":
    try:
        run_voice_assistant()
    except Exception as e:
        st.error(f"Application error: {e}")
        print(f"Error: {e}")