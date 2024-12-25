import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import google.generativeai as genai
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "API_KEY"   # Replace with your actual API key
def speak_old(text):
    engine.say(text)
    engine.runAndWait()
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

    
def aiProcess(command):
   genai.configure(api_key="API_KEY")  # Replace with your actual API key
   model = genai.GenerativeModel("gemini-1.5-flash")
   response = model.generate_content(f"You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud.  {command}")
   return   response.text

def processCommand(command):
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open spotify" in command.lower():
        webbrowser.open("https://spotify.com")
    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in command.lower():
        webbrowser.open("https://instagram.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://youtube.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ", 1)[-1]
        link = musicLibrary.music[song]
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {song}")
    elif "news" in command.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
      
        output = aiProcess(command)
        speak(output) 


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        print("recognizing...")
        try:
            print("Listening for wake word 'Jarvis'...")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=20)
                word = recognizer.recognize_google(audio).lower()
                if "jarvis" in word:
                    speak("Yes, how can I assist?")
                    with sr.Microphone() as command_source:
                        recognizer.adjust_for_ambient_noise(command_source)
                        command_audio = recognizer.listen(command_source, timeout=10)
                        command = recognizer.recognize_google(command_audio)
                        processCommand(command)
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
