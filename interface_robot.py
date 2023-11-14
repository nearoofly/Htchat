import tkinter as tk
from gtts import gTTS
from pygame import mixer
import speech_recognition as sr
from threading import Thread
from flask import Flask, render_template

app = Flask(__name__)

class RobotInterface:
    def __init__(self, master):
        self.master = master
        master.title("Robot Interface")

        self.listbox = tk.Listbox(master, selectbackground="lightblue", selectmode=tk.SINGLE, width=40, height=10)
        self.listbox.pack(pady=10)

        self.entry = tk.Entry(master, width=40)
        self.entry.pack(pady=10)

        self.send_button = tk.Button(master, text="Envoyer", command=self.send_message)
        self.send_button.pack(pady=10)

        self.talk_button = tk.Button(master, text="Parler", command=self.start_listening)
        self.talk_button.pack(pady=10)

        mixer.init()

        self.recognizer = sr.Recognizer()

    def speak(self, text):
        tts = gTTS(text=text, lang='fr')
        tts.save("robot_parle.mp3")
        mixer.music.load("robot_parle.mp3")
        mixer.music.play()

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio, language="fr-FR")
            self.add_message(f"Utilisateur: {text}")
            self.speak(f"Vous avez dit : {text}")
            # Ajouter l'appel à la fonction JavaScript pour ajouter le message sur la page web
            self.add_message_from_python_js(text)
        except sr.UnknownValueError:
            self.speak("Désolé, je n'ai pas compris.")
        except sr.RequestError as e:
            print(f"Impossible de demander des résultats à Google Speech Recognition service; {e}")

    def start_listening(self):
        self.add_message("Robot: En écoute...")
        listening_thread = Thread(target=self.listen)
        listening_thread.start()

    def send_message(self):
        message = self.entry.get()
        if message:
            self.add_message(f"Utilisateur: {message}")
            self.speak(f"Ok : {message}")
            # Ajouter l'appel à la fonction JavaScript pour ajouter le message sur la page web
            self.add_message_from_python_js(f"Robot: {message}")
            self.entry.delete(0, tk.END)

    def add_message(self, message):
        self.listbox.insert(tk.END, message)
        self.listbox.see(tk.END)

if __name__ == "__main__":
    # Lancer le serveur Flask dans un thread
    flask_thread = Thread(target=app.run, kwargs={'debug': True, 'use_reloader': False})
    flask_thread.start()

    # Ouvrir la page web dans le navigateur
    import webbrowser
    webbrowser.open('http://127.0.0.1:5000/')
