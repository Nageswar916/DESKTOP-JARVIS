import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import openai
import os
from moviepy.editor import ImageSequenceClip
from PIL import Image
import requests
from io import BytesIO

# Initialize recognizer, text-to-speech engine, and translator
recognizer = sr.Recognizer()
engine = pyttsx3.init()
translator = Translator()

# Set OpenAI API key
openai.api_key = "your_openai_api_key_here"

# Set properties for the TTS engine
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

# Function to speak text
def speak(text, language='en'):
    """
    Convert text to speech in the specified language.
    """
    if language == 'hi':
        # Translate text to Hindi
        translated_text = translator.translate(text, src='en', dest='hi').text
        print(f"AI (Hindi): {translated_text}")
        engine.say(translated_text)
    else:
        print(f"AI (English): {text}")
        engine.say(text)
    engine.runAndWait()

# Function to listen to user input
def listen():
    """
    Listen to the user's voice command and convert it to text.
    """
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='hi')  # Default to Hindi
            print(f"User (Hindi): {query}")
            return query, 'hi'  # Return query and language
        except sr.UnknownValueError:
            try:
                print("Recognizing in English...")
                query = recognizer.recognize_google(audio, language='en')  # Fallback to English
                print(f"User (English): {query}")
                return query, 'en'
            except sr.UnknownValueError:
                speak("Sorry, I could not understand. Please repeat.", language='en')
                return None, None
        except sr.RequestError:
            speak("Sorry, my speech service is down. Please try again later.", language='en')
            return None, None

# Function to generate an image using OpenAI's DALL·E
def generate_image(prompt):
    """
    Generate an image using OpenAI's DALL·E API.
    """
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,  # Number of images to generate
            size="1024x1024"  # Image size
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

# Function to generate a video from images
def generate_video(image_urls, output_file="output_video.mp4"):
    """
    Generate a video from a list of image URLs.
    """
    try:
        images = []
        for url in image_urls:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            images.append(img)

        # Save images temporarily
        temp_files = []
        for i, img in enumerate(images):
            temp_file = f"temp_image_{i}.jpg"
            img.save(temp_file)
            temp_files.append(temp_file)

        # Create video from images
        clip = ImageSequenceClip(temp_files, fps=1)
        clip.write_videofile(output_file, codec="libx264")

        # Clean up temporary files
        for file in temp_files:
            os.remove(file)

        return output_file
    except Exception as e:
        print(f"Error generating video: {e}")
        return None

# Function to process the query
def process_query(query, language):
    """
    Process the user's query and generate a response.
    """
    if language == 'hi':
        if 'नमस्ते' in query:
            speak("नमस्ते! मैं आपकी कैसे मदद कर सकता हूँ?", language='hi')
        elif 'तुम्हारा नाम क्या है' in query:
            speak("मेरा नाम जार्विस है।", language='hi')
        elif 'चित्र बनाओ' in query:
            speak("कृपया चित्र के लिए विवरण दें।", language='hi')
            prompt, _ = listen()
            if prompt:
                speak("चित्र बनाया जा रहा है...", language='hi')
                image_url = generate_image(prompt)
                if image_url:
                    speak("चित्र बन गया है। इसे देखने के लिए कृपया अपनी फ़ाइल प्रबंधक खोलें।", language='hi')
                    print(f"Generated Image URL: {image_url}")
        elif 'वीडियो बनाओ' in query:
            speak("कृपया वीडियो के लिए विवरण दें।", language='hi')
            prompt, _ = listen()
            if prompt:
                speak("वीडियो बनाया जा रहा है...", language='hi')
                image_urls = [generate_image(prompt) for _ in range(3)]  # Generate 3 images for the video
                video_file = generate_video(image_urls)
                if video_file:
                    speak("वीडियो बन गया है। इसे देखने के लिए कृपया अपनी फ़ाइल प्रबंधक खोलें।", language='hi')
                    print(f"Generated Video File: {video_file}")
        else:
            speak("मैं इस प्रश्न का उत्तर नहीं जानता। कृपया कुछ और पूछें।", language='hi')
    else:
        if 'hello' in query.lower():
            speak("Hello! How can I assist you today?", language='en')
        elif 'what is your name' in query.lower():
            speak("My name is JARVIS.", language='en')
        elif 'generate image' in query.lower():
            speak("Please describe the image you want to generate.", language='en')
            prompt, _ = listen()
            if prompt:
                speak("Generating the image...", language='en')
                image_url = generate_image(prompt)
                if image_url:
                    speak("The image has been generated. Please check your file manager.", language='en')
                    print(f"Generated Image URL: {image_url}")
        elif 'generate video' in query.lower():
            speak("Please describe the video you want to generate.", language='en')
            prompt, _ = listen()
            if prompt:
                speak("Generating the video...", language='en')
                image_urls = [generate_image(prompt) for _ in range(3)]  # Generate 3 images for the video
                video_file = generate_video(image_urls)
                if video_file:
                    speak("The video has been generated. Please check your file manager.", language='en')
                    print(f"Generated Video File: {video_file}")
        else:
            speak("I don't know the answer to that. Please ask something else.", language='en')

# Main loop
if _name_ == "_main_":
    speak("नमस्ते! मैं आपकी सेवा के लिए तैयार हूँ।", language='hi')
    speak("Hello! I am ready to assist you.", language='en')

    while True:
        query, language = listen()
        if query:
            process_query(query, language)