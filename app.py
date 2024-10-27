import streamlit as st
from translate import translate_arabic_to_english
from langdetect import detect, LangDetectException
from check_similarity import translate_sentence_to_videos
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import speech_recognition as sr

def recognize_speech_from_microphone(language='ar-SA'):
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        st.info("Listening... Please speak something!")
        audio = recognizer.listen(source)
    
    try:
        # Recognize speech using Google Speech Recognition
        recognized_text = recognizer.recognize_google(audio, language=language)
        st.success(f"You said: {recognized_text}")
        return recognized_text
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    
def concatenate_videos(video_sequence):
    clips = []
    
    # Load each video file using moviepy
    for video in video_sequence:
        video_path = f"ESL_Processed/{video}.mp4"
                
        if os.path.exists(video_path):
            clip = VideoFileClip(video_path)
            clips.append(clip)
        else:
            st.error(f"Could not generate due to lack of data.")
    
    if clips:
        # Concatenate the clips
        final_clip = concatenate_videoclips(clips)
        
        # Ensure the output directory exists
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)  # Create 'output' directory if it doesn't exist
        
        # Save the final concatenated video
        output_path = os.path.join(output_dir, "combined_video.mp4")
        final_clip.write_videofile(output_path, codec='libx264', audio=False)
        
        return output_path
    else:
        return None

# UI configurations
st.set_page_config(page_title="Emirati Sign Language Translator", 
                   page_icon=":hand:", 
                   layout="wide")

# CSS styling for consistent fonts and colors
st.markdown("""
    <style>
    /* Consistent font for everything */
    * {
        font-family: 'Arial', sans-serif;
    }
    
    /* Color scheme */
    body {
        background-color: #FFE6A5;
    }
    
    h1, h2, h3 {
        color: #605678;
    }

    .stSidebar {
        background-color: #FFBF61;
    }

    .stButton button {
        background-color: #8ABFA3;
        color: white;
        border-radius: 5px;
        width: 100%;
        height: 40px;
        font-size: 16px;
        font-weight: bold;
        border: none;
    }

    .stButton button:hover {
        background-color: #605678;
        color: #FFE6A5;
            
    }


    .stAlert, .stMarkdown, .stTextArea {
        color: #605678;
        width: 100%;
    }

    .stTextArea textarea {
        border: 1px solid #605678;
        border-radius: 5px;
        color: #605678;
        font-size: 14px;
        width: 100%;
        border-color: #605678;
    }

    
    .stSelectbox > div {
        width: 100%;
        background-color: #8ABFA3;
        color: #605678;
        border-radius: 5px;
        font-size: 14px;
        
    }

    </style>
    """, unsafe_allow_html=True)

st.markdown("# Emirati Sign Language Translator 🙌")


def configure_sidebar():
    with st.sidebar:
        
        if st.button("Home Page"):
            st.session_state['current_option'] = "Home"
        if st.button("Perform Text to Sign Language"):
            st.session_state['current_option'] = "Text to Sign Language"
        if st.button("Perform Speech to Sign Language"):
            st.session_state['current_option'] = "Speech to Sign Language"
        
        if st.button("Examples"):
            st.session_state['current_option'] = "Example Sentences"

        st.markdown("---")

        st.markdown("**Resources**")
        
        st.markdown(
            """
            <a href="https://zho.gov.ae/en/Sign-Language-Dictionary/UAE-Sign-Language-Categories" target="_blank">
                <button style="background-color: #8ABFA3; color: white; border-radius: 5px; width: 100%; height: 40px; font-size: 16px; border: none; font-family: 'Arial', sans-serif; margin-bottom: 15px;">
                    Dataset for ESL
                </button>
            </a>
            <style>
            button:hover {
                background-color: #605678;
                color: #FFE6A5;
            }
            </style>
            """,
            unsafe_allow_html=True
        )



        st.markdown(
            """
            <a href="https://www.youtube.com/@eslzayed6970" target="_blank">
                <button style="background-color: #8ABFA3; color: white; border-radius: 5px; width: 100%; height: 40px; font-size: 16px; border: none; font-family: 'Arial', sans-serif; margin-bottom: 15px;">
                    Youtube Link for ESL
                </button>
            </a>
            <style>
            button:hover {
                background-color: #605678;
                color: #FFE6A5;
            }
            </style>
            """,
            unsafe_allow_html=True
        )


        st.markdown("---")
        st.markdown("Sponsored by Pupilar for Gitex 2024.")

# Main function to handle selected options
def main_page():
    selected_option = st.session_state.get('current_option', None)
    
    if selected_option == "Home":
       
        st.markdown("## Introduction to Emirati Sign Language (ESL) 🌍")
        st.markdown("Emirati Sign Language (ESL) is a unique form of communication created for and by the Deaf community in the UAE. With growing efforts to preserve Emirati culture and heritage, ESL is increasingly recognized as a vital language. It allows for a bridge between the hearing and Deaf communities, encouraging inclusion and accessibility. ESL includes gestures that reflect Emirati traditions and values, making it distinct from other sign languages around the world.")
        st.markdown("## History of Emirati Sign Language 📜")
        st.markdown("The development of ESL dates back to the early 2000s, as more advocacy groups and educational programs focused on Deaf culture emerged in the UAE. With influences from international sign languages, ESL was adapted to better fit Emirati culture and Arabic language nuances. In 2018, the Zayed Higher Organization for People of Determination officially launched the first UAE Sign Language Dictionary, offering Deaf Emiratis a structured language and promoting wider social awareness.")

        st.markdown("## How to Use the Translator App 🛠️")
        st.markdown(""" 
                    - Select Language: Use the drop down to choose between English and Arabic.
                    - Enter Text or Speech: Type text or use the microphone for speech input.
                    - Translation in ESL: The app converts the input to ESL gestures.""")
        
        st.markdown("## How It Works")
        st.markdown("""
                    - 🗣️ Text or Speech Input: The user provides a text or speech input in English or Arabic. The input is first checked for semantic similarity using an AI model to ensure accuracy and relevance to Emirati Sign Language (ESL).
                    - 🧠 Azure OpenAI Processing: Once the semantic similarity is validated, the input is sent to Azure OpenAI services for advanced processing. Here, the system converts the recognized input into a format that can be mapped to ESL gestures.
                    - 🎥 Video Output with MoviePy: After processing the input, the relevant sign language video segments are generated using MoviePy. This tool handles the video editing and assembly to ensure that the output aligns with the corresponding ESL signs, providing smooth transitions between gestures.""")
        
        st.markdown("## Challenges and Considerations")
        st.markdown("""
                    - 📊 Dataset Limitation: If a word or phrase doesn’t exist in the dataset, the app falls back to checking semantic similarity, but in some cases, it may not be able to provide an accurate translation.
                    - 🌍 Language Complexity: Ensuring accurate translation for both English and Arabic while maintaining cultural and linguistic nuances specific to Emirati Sign Language.
                    - 🔇Speech Recognition Limitations: Background noise or unclear speech may result in inaccurate recognition by the speech-to-text component.
                    - ⚙️ Embedding Matching: While cosine similarity helps find similar words, context-sensitive errors may arise, which is why GPT-4 is used to ensure higher accuracy.""")

    elif selected_option == "Text to Sign Language":
        st.markdown("## Text to Sign Language Translation 🖋️➡️👐")
        language = st.selectbox("Select Language", ["English", "Arabic"], key="text_language")
        text_input = st.text_area("Enter your text here:")
        
        if st.button("Translate"):
            if text_input.strip(): 
                
                if language == 'Arabic':
                    text_input = translate_arabic_to_english(text_input)

                st.success(f"Translating...")
                
                video_sequence = translate_sentence_to_videos(text_input) 
                
                if video_sequence:
                    combined_video_path = concatenate_videos(video_sequence)
                    if combined_video_path:
                        st.video(combined_video_path)
                    else:
                        st.error("Error concatenating videos.")
                else:
                    st.error(f"Could not generate due to lack of data.")
                
            else:
                st.error("Please enter some text to translate.")
        

    elif selected_option == "Speech to Sign Language":
        st.markdown("## Speech to Sign Language Translation 🎤➡️👐")
        language = st.selectbox("Select Language", ["English", "Arabic"], key="text_language")


        language_code = 'ar-SA' if language == 'Arabic' else 'en-US'
        recognized_text = None
        
        if st.button("Start Speaking"):
            recognized_text = recognize_speech_from_microphone(language=language_code)
  
            if recognized_text:
                if language_code == 'ar-SA':
                
                    translated_text = translate_arabic_to_english(recognized_text)

                    video_sequence = translate_sentence_to_videos(translated_text) 
                    
                    if video_sequence:
                        combined_video_path = concatenate_videos(video_sequence)
                        if combined_video_path:
                            st.video(combined_video_path)
                        else:
                            st.error("Error concatenating videos.")
                            print("Error in combining videos")
                    else:
                        st.error(f"Could not generate due to lack of data.")
                else:
                
                    video_sequence = translate_sentence_to_videos(recognized_text) 
                    
                    if video_sequence:
                        combined_video_path = concatenate_videos(video_sequence)
                        if combined_video_path:
                            st.video(combined_video_path)
                        else:
                            st.error("Error concatenating videos.")
                            print("Error in combining videos")
                    else:
                        st.error("Could not convert to sign language. Please try again!")
                        
            else:
                st.error("Please try again.")

    elif selected_option == "Example Sentences":
        st.markdown("### Example Sentences for Testing")
        
        # Table of English and Arabic sentences
        st.markdown("""
    <table style="width:100%; border-collapse: collapse; font-family: Arial, sans-serif;">
        <tr>
            <th style="border: 1px solid #605678; padding: 10px; background-color: #FFE6A5;">English</th>
            <th style="border: 1px solid #605678; padding: 10px; direction: rtl; text-align: right; background-color: #FFE6A5;">العربية</th>
        </tr>
        <tr>
            <td style="border: 1px solid #605678; padding: 10px;">Good Morning</td>
            <td style="border: 1px solid #605678; padding: 10px; direction: rtl; text-align: right;">صباح الخير</td>
        </tr>
        <tr>
            <td style="border: 1px solid #605678; padding: 10px;">Good Evening</td>
            <td style="border: 1px solid #605678; padding: 10px; direction: rtl; text-align: right;">مساء الخير</td>
        </tr>
        <tr>
            <td style="border: 1px solid #605678; padding: 10px;">How Are You?</td>
            <td style="border: 1px solid #605678; padding: 10px; direction: rtl; text-align: right;">كيف حالك؟</td>
        </tr>
        <tr>
            <td style="border: 1px solid #605678; padding: 10px;">Beautiful Sunrise</td>
            <td style="border: 1px solid #605678; padding: 10px; direction: rtl; text-align: right;">شروق الشمس الجميل</td>
        </tr>
        <tr>
            <td style="border: 1px solid #605678; padding: 10px;">The teacher gives the student a book.</td>
            <td style="border: 1px solid #605678; padding: 10px; direction: rtl; text-align: right;">المعلم يعطي الطالب كتاباً.</td>
        </tr>
        <tr>
            <td style="border: 1px solid #605678; padding: 10px;">The carpenter is building a house.</td>
            <td style="border: 1px solid #605678; padding: 10px; direction: rtl; text-align: right;">النجار يبني منزلاً.</td>
        </tr>
        <tr>
            <td style="border: 1px solid #605678; padding: 10px;">She is wearing a beautiful dress.</td>
            <td style="border: 1px solid #605678; padding: 10px; direction: rtl; text-align: right;">هي ترتدي فستاناً جميلاً.</td>
        </tr>
        <!-- Add more rows as needed -->
    </table>
        """, unsafe_allow_html=True)

                

    else:
        
        st.markdown("## Introduction to Emirati Sign Language (ESL) 🌍")
        st.markdown("Emirati Sign Language (ESL) is a unique form of communication created for and by the Deaf community in the UAE. With growing efforts to preserve Emirati culture and heritage, ESL is increasingly recognized as a vital language. It allows for a bridge between the hearing and Deaf communities, encouraging inclusion and accessibility. ESL includes gestures that reflect Emirati traditions and values, making it distinct from other sign languages around the world.")
        st.markdown("## History of Emirati Sign Language 📜")
        st.markdown("The development of ESL dates back to the early 2000s, as more advocacy groups and educational programs focused on Deaf culture emerged in the UAE. With influences from international sign languages, ESL was adapted to better fit Emirati culture and Arabic language nuances. In 2018, the Zayed Higher Organization for People of Determination officially launched the first UAE Sign Language Dictionary, offering Deaf Emiratis a structured language and promoting wider social awareness.")

        st.markdown("## How to Use the Translator App 🛠️")
        st.markdown(""" 
                    - Select Language: Use the drop down to choose between English and Arabic.
                    - Enter Text or Speech: Type text or use the microphone for speech input.
                    - Translation in ESL: The app converts the input to ESL gestures.""")
        
        st.markdown("## How It Works")
        st.markdown("""
                    - 🗣️ Text or Speech Input: The user provides a text or speech input in English or Arabic. The input is first checked for semantic similarity using an AI model to ensure accuracy and relevance to Emirati Sign Language (ESL).
                    - 🧠 Azure OpenAI Processing: Once the semantic similarity is validated, the input is sent to Azure OpenAI services for advanced processing. Here, the system converts the recognized input into a format that can be mapped to ESL gestures.
                    - 🎥 Video Output with MoviePy: After processing the input, the relevant sign language video segments are generated using MoviePy. This tool handles the video editing and assembly to ensure that the output aligns with the corresponding ESL signs, providing smooth transitions between gestures.""")
        
        st.markdown("## Challenges and Considerations")
        st.markdown("""
                    - 📊 Dataset Limitation: If a word or phrase doesn’t exist in the dataset, the app falls back to checking semantic similarity, but in some cases, it may not be able to provide an accurate translation.
                    - 🌍 Language Complexity: Ensuring accurate translation for both English and Arabic while maintaining cultural and linguistic nuances specific to Emirati Sign Language.
                    - 🔇Speech Recognition Limitations: Background noise or unclear speech may result in inaccurate recognition by the speech-to-text component.
                    - ⚙️ Embedding Matching: While cosine similarity helps find similar words, context-sensitive errors may arise, which is why GPT-4 is used to ensure higher accuracy.""")




if 'current_option' not in st.session_state:
    st.session_state['current_option'] = None

# Run the app
configure_sidebar()
main_page()



















########################################################################################################
# import streamlit as st
# from translate import translate_arabic_to_english
# from langdetect import detect, LangDetectException
# from check_similarity import translate_sentence_to_videos
# from moviepy.editor import VideoFileClip, concatenate_videoclips
# import os
# import speech_recognition as sr

# # Initialize session state for UI visibility
# if "listening_active" not in st.session_state:
#     st.session_state.listening_active = False
# if "translating_active" not in st.session_state:
#     st.session_state.translating_active = False
# if "translation_output" not in st.session_state:
#     st.session_state.translation_output = None  # Holds the video path or error message

# def recognize_speech_from_microphone(language='ar-SA'):
#     recognizer = sr.Recognizer()
    
#     with sr.Microphone() as source:
#         st.session_state.listening_active = True  # Show "listening..."
#         audio = recognizer.listen(source)
    
#     try:
#         recognized_text = recognizer.recognize_google(audio, language=language)
#         st.session_state.listening_active = False  # Hide "listening..." once done
#         st.success(f"You said: {recognized_text}")
#         return recognized_text
#     except sr.UnknownValueError:
#         st.session_state.listening_active = False
#         st.error("Sorry, I could not understand the audio.")
#         return None
#     except sr.RequestError as e:
#         st.session_state.listening_active = False
#         st.error(f"Could not request results; {e}")
#         return None

# def concatenate_videos(video_sequence):
#     clips = []
#     for video in video_sequence:
#         video_path = f"ESL/{video}.mp4"
#         if os.path.exists(video_path):
#             clip = VideoFileClip(video_path)
#             clips.append(clip)
#         else:
#             st.error(f"Video file {video_path} not found.")
    
#     if clips:
#         final_clip = concatenate_videoclips(clips)
#         output_dir = "output"
#         os.makedirs(output_dir, exist_ok=True)
#         output_path = os.path.join(output_dir, "combined_video.mp4")
#         final_clip.write_videofile(output_path, codec='libx264', audio=False)
#         return output_path
#     else:
#         return None

# def translate_text_and_display_output(text):
#     st.session_state.translating_active = True  # Show "translating..."
#     video_sequence = translate_sentence_to_videos(text)
#     st.session_state.translating_active = False  # Hide "translating..." when done
    
#     if video_sequence:
#         combined_video_path = concatenate_videos(video_sequence)
#         st.session_state.translation_output = combined_video_path if combined_video_path else "Error concatenating videos."
#     else:
#         st.session_state.translation_output = "No corresponding sign language videos found."

# # Sidebar configuration
# def configure_sidebar():
#     with st.sidebar:
#         st.markdown("<h2 style='color: #605678;'>Options</h2>", unsafe_allow_html=True)
        
#         if st.button("Home"):
#             st.session_state['current_option'] = "Home"
#         if st.button("Perform Text to Sign Language"):
#             st.session_state['current_option'] = "Text to Sign Language"
#         if st.button("Perform Speech to Sign Language"):
#             st.session_state['current_option'] = "Speech to Sign Language"

#         st.markdown("---")

#         st.markdown("**Resources**")
#         st.button("[User Guide](https://example.com)")
#         st.button("[Contact Support](https://example.com/contact)")

#         st.markdown("---")
#         st.markdown("Created by Mehnaz Murtuza")

# # UI configurations
# st.set_page_config(page_title="Emirati Sign Language Translator", 
#                    page_icon=":hand:", 
#                    layout="wide")

# # CSS styling for consistent fonts and colors
# st.markdown("""
#     <style>
#     /* Consistent font for everything */
#     * {
#         font-family: 'Arial', sans-serif;
#     }
    
#     /* Color scheme */
#     body {
#         background-color: #FFE6A5;
#     }
    
#     h1, h2, h3 {
#         color: #605678;
#     }

#     .stSidebar {
#         background-color: #FFBF61;
#     }

#     .stButton button {
#         background-color: #8ABFA3;
#         color: white;
#         border-radius: 5px;
#         width: 100%;
#         height: 40px;
#         font-size: 16px;
#         font-weight: bold;
#         border: none;
#     }

#     .stButton button:hover {
#         background-color: #605678;
#         color: #FFE6A5;
#     }

#     .stAlert, .stMarkdown, .stTextArea {
#         color: #605678;
#         width: 100%;
#     }

#     .stTextArea textarea {
#         border: 1px solid #605678;
#         border-radius: 5px;
#         color: #605678;
#         font-size: 14px;
#         width: 100%;
#         border-color: #605678;
#     }

#     .stSelectbox > div {
#         width: 100%;
#         background-color: #8ABFA3;
#         color: #605678;
#         border-radius: 5px;
#         font-size: 14px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Main Page Functionality
# def main_page():
#     selected_option = st.session_state.get('current_option', None)

#     if selected_option == "Home":
#         st.markdown("## Welcome to the Emirati Sign Language Translator! 🌟")
#         # st.markdown("""
#         #     This app helps you translate text or speech into Emirati Sign Language.
#         #     You can either enter text or use the microphone to speak, and the app will
#         #     provide the corresponding sign language videos.
#         #     - Select "Perform Text to Sign Language" to type your text.
#         #     - Select "Perform Speech to Sign Language" to speak directly.
#         #     """)
#         st.write("This app allows you to translate both text and speech into Emirati Sign Language.")
#         st.write("""
#         - Convert **text** into accurate sign language translations 🎯.
#         - Use **speech** input to generate sign language gestures 🎤➡️👐.
#         - Leverage state-of-the-art **Generative AI** models for real-time translation 🚀.
        
#         Whether you're learning sign language or looking to build better communication bridges, this app makes it easy to turn written or spoken language into **Emirati Sign Language**. 
#         """)
        
#     elif selected_option == "Text to Sign Language":
#         st.markdown("## Text to Sign Language Translation 🖋️➡️👐")
#         language = st.selectbox("Select Language", ["English", "Arabic"], key="text_language")
#         text_input = st.text_area("Enter your text here:")
        
#         if st.button("Translate"):
#             if text_input.strip():
#                 if language == 'Arabic':
#                     text_input = translate_arabic_to_english(text_input)
#                 translate_text_and_display_output(text_input)
#             else:
#                 st.error("Please enter some text to translate.")

#     elif selected_option == "Speech to Sign Language":
#         st.markdown("## Speech to Sign Language Translation 🎤➡️👐")
#         language = st.selectbox("Select Language", ["English", "Arabic"], key="text_language")
#         language_code = 'ar-SA' if language == 'Arabic' else 'en-US'
        
#         if st.button("Start Speaking"):
#             st.session_state['translation_output'] = None  # Clear previous translation output
#             recognized_text = recognize_speech_from_microphone(language=language_code)
            
#             if recognized_text:
#                 if language_code == 'ar-SA':
#                     recognized_text = translate_arabic_to_english(recognized_text)
#                 translate_text_and_display_output(recognized_text)
#             else:
#                 st.error("Please try again.")
    
    
#     # Display dynamic elements based on session state
#     if st.session_state.listening_active:
#         st.info("(Listening...)")
#     if st.session_state.translating_active:
#         st.info("(Translating...)")
#     if st.session_state.translation_output:
#         if st.session_state.translation_output.endswith(".mp4"):
#             st.video(st.session_state.translation_output)
#         else:
#             st.error(st.session_state.translation_output)

# if 'current_option' not in st.session_state:
#     st.session_state['current_option'] = None

# # Run the app
# configure_sidebar()
# main_page()
######################################################################################################################
# import streamlit as st
# from translate import translate_arabic_to_english
# from langdetect import detect, LangDetectException
# from check_similarity import translate_sentence_to_videos
# from moviepy.editor import VideoFileClip, concatenate_videoclips
# import os
# import speech_recognition as sr

# def recognize_speech_from_microphone(language='ar-SA'):
#     recognizer = sr.Recognizer()
    
#     with sr.Microphone() as source:
#         st.info("Listening... Please speak something!")
#         audio = recognizer.listen(source)
    
#     try:
#         recognized_text = recognizer.recognize_google(audio, language=language)
#         st.success(f"You said: {recognized_text}")
#         return recognized_text
#     except sr.UnknownValueError:
#         st.error("Sorry, I could not understand the audio.")
#         return None
#     except sr.RequestError as e:
#         st.error(f"Could not request results from Google Speech Recognition service; {e}")
#         return None
    
# def concatenate_videos(video_sequence):
#     clips = []
    
#     for video in video_sequence:
#         video_path = f"ESL/{video}.mp4"
        
#         if os.path.exists(video_path):
#             clip = VideoFileClip(video_path)
#             clips.append(clip)
#         else:
#             st.error(f"Video file {video_path} not found.")
    
#     if clips:
#         final_clip = concatenate_videoclips(clips)
        
#         output_dir = "output"
#         os.makedirs(output_dir, exist_ok=True)
        
#         output_path = os.path.join(output_dir, "combined_video.mp4")
#         final_clip.write_videofile(output_path, codec='libx264', audio=False)
        
#         return output_path
#     else:
#         return None

# # UI configurations
# st.set_page_config(page_title="Emirati Sign Language Translator", 
#                    page_icon=":hand:", 
#                    layout="wide")

# st.markdown("""
#     <style>
#     * {
#         font-family: 'Arial', sans-serif;
#     }
    
#     body {
#         background-color: #FFE6A5;
#     }
    
#     h1, h2, h3 {
#         color: #605678;
#     }

#     .stSidebar {
#         background-color: #FFBF61;
#     }

#     .stButton button {
#         background-color: #8ABFA3;
#         color: white;
#         border-radius: 5px;
#         width: 100%;
#         height: 40px;
#         font-size: 16px;
#         font-weight: bold;
#         border: none;
#     }

#     .stButton button:hover {
#         background-color: #605678;
#         color: #FFE6A5;
#     }

#     .stAlert, .stMarkdown, .stTextArea {
#         color: #605678;
#         width: 100%;
#     }

#     .stTextArea textarea {
#         border: 1px solid #605678;
#         border-radius: 5px;
#         color: #605678;
#         font-size: 14px;
#         width: 100%;
#         border-color: #605678;
#     }

#     .stSelectbox > div {
#         width: 100%;
#         background-color: #8ABFA3;
#         color: #605678;
#         border-radius: 5px;
#         font-size: 14px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Sidebar configuration
# def configure_sidebar():
#     with st.sidebar:
#         st.markdown("<h2 style='color: #605678;'>Options</h2>", unsafe_allow_html=True)
        
#         if st.button("Home "):
#             st.session_state['current_option'] = "Home"
#         if st.button("Perform Text to Sign Language"):
#             st.session_state['current_option'] = "Text to Sign Language"
#         if st.button("Perform Speech to Sign Language"):
#             st.session_state['current_option'] = "Speech to Sign Language"

#         st.markdown("---")
#         st.markdown("**Resources**")
#         st.button("[User Guide](https://example.com)")
#         st.button("[Contact Support](https://example.com/contact)")
#         st.markdown("---")
#         st.markdown("Created by Mehnaz Murtuza")

# # Main function to handle selected options
# def main_page():
#     selected_option = st.session_state.get('current_option', None)
    
#     if selected_option == "Home":
#         st.markdown("## Welcome to the Emirati Sign Language Translator! 🌟")
#         st.markdown("""
#             This app helps you translate text or speech into Emirati Sign Language.
#             You can either enter text or use the microphone to speak, and the app will
#             provide the corresponding sign language videos.
#             - Select "Perform Text to Sign Language" to type your text.
#             - Select "Perform Speech to Sign Language" to speak directly.
#         """)

#     elif selected_option == "Text to Sign Language":
#         st.markdown("## Text to Sign Language Translation 🖋️➡️👐")
#         language = st.selectbox("Select Language", ["English", "Arabic"], key="text_language")
#         text_input = st.text_area("Enter your text here:")
        
#         if st.button("Translate"):
#             if text_input.strip(): 
#                 if language == 'Arabic':
#                     text_input = translate_arabic_to_english(text_input)
                
#                 st.info("Translating...")  # Show translating status
#                 video_sequence = translate_sentence_to_videos(text_input) 
                
#                 if video_sequence:
#                     combined_video_path = concatenate_videos(video_sequence)
#                     if combined_video_path:
#                         st.video(combined_video_path)
#                     else:
#                         st.error("Error concatenating videos.")
#                 else:
#                     st.error("No corresponding sign language videos found.")
                
#             else:
#                 st.error("Please enter some text to translate.")

#     elif selected_option == "Speech to Sign Language":
#         st.markdown("## Speech to Sign Language Translation 🎤➡️👐")
#         language = st.selectbox("Select Language", ["English", "Arabic"], key="text_language")
#         language_code = 'ar-SA' if language == 'Arabic' else 'en-US'
        
#         if st.button("Start Speaking"):
#             st.session_state['listening_active'] = True
#             st.session_state['translating_active'] = False
#             recognized_text = recognize_speech_from_microphone(language=language_code)
#             st.session_state['listening_active'] = False  # Reset listening status
            
#             if recognized_text:
#                 st.session_state['translating_active'] = True
#                 if language_code == 'ar-SA':
#                     recognized_text = translate_arabic_to_english(recognized_text)
                
#                 video_sequence = translate_sentence_to_videos(recognized_text)
                
#                 if video_sequence:
#                     combined_video_path = concatenate_videos(video_sequence)
#                     if combined_video_path:
#                         st.video(combined_video_path)
#                     else:
#                         st.error("Error concatenating videos.")
#                 else:
#                     st.error("Could not convert to sign language. Please try again!")
                
#             else:
#                 st.error("Please try again.")
#         # Show listening or translating status
#         if st.session_state.get('listening_active'):
#             st.info("(Listening...)")
#         if st.session_state.get('translating_active'):
#             st.info("(Translating...)")

# if 'current_option' not in st.session_state:
#     st.session_state['current_option'] = None

# if 'listening_active' not in st.session_state:
#     st.session_state['listening_active'] = False

# if 'translating_active' not in st.session_state:
#     st.session_state['translating_active'] = False

# # Run the app
# configure_sidebar()
# main_page()
