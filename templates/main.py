import tkinter as tk
from gtts import gTTS
from pygame import mixer
from threading import Thread
from flask import Flask, render_template, jsonify
import pyttsx3

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

    def speak(self, text):
        tts = gTTS(text=text, lang='fr')
        tts.save("robot_parle.mp3")
        mixer.init()
        mixer.music.load("robot_parle.mp3")
        mixer.music.play()

    def listen(self):
        # Ajoutez votre logique d'écoute ici
        pass

    def start_listening(self):
        self.add_message("Robot: En écoute...")
        listening_thread = Thread(target=self.listen)
        listening_thread.start()

    def send_message(self):
        message = self.entry.get()
        if message:
            self.add_message(f"Utilisateur: {message}")
            # Intégrer ici la logique pour générer la réponse du robot en fonction du message de l'utilisateur
            self.speak(f"Ok : {message}")
            self.entry.delete(0, tk.END)

    def add_message(self, message):
        self.listbox.insert(tk.END, message)
        self.listbox.see(tk.END)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speak/<text>')
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    return jsonify({"status": "success"})

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotInterface(root)
    root.mainloop()
