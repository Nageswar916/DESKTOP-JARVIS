import pyttsx3  # Make sure to install this package if you haven't already
import speech_recognition as sr  # Make sure to install this package if you haven't already

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')  # Corrected from 'getproperty' to 'getProperty'
    engine.setProperty('voice', voices[1].id)  # Corrected from 'setproperty' to 'setProperty'
    rate = engine.getProperty('rate')  # Corrected from 'getproperty' to 'getProperty'
    engine.setProperty('rate', rate - 50)  # Corrected from 'setproperty' to 'setProperty'
    volume = engine.getProperty('volume')  # Corrected from 'getproperty' to 'getProperty'
    engine.setProperty('volume', volume + 0.25)  # Corrected from 'setproperty' to 'setProperty'
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

# Call the speak function
speak("Hello, I am Nageswar")