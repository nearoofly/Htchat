import speech_recognition as sr
from gtts import gTTS
import os

# Initialiser le moteur de reconnaissance vocale
recognizer = sr.Recognizer()

def ecouter():
    with sr.Microphone() as source:
        print("Dites quelque chose...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Vous avez dit : " + recognizer.recognize_google(audio))
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition n'a pas pu comprendre l'audio.")
    except sr.RequestError as e:
        print(f"Impossible de demander des résultats à Google Speech Recognition service; {e}")

# Fonction pour faire parler le robot
def parler(texte):
    tts = gTTS(text=texte, lang='fr')
    tts.save("robot_parle.mp3")
    os.system("mpg321 robot_parle.mp3")

# Exemple d'utilisation
while True:
    texte = ecouter()
    if "arrêt" in texte:
        break
    parler("Vous avez dit : " + texte)
