import tkinter as tk
from gtts import gTTS
from pygame import mixer
import speech_recognition as sr
from threading import Thread

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
            # Intégrer ici la logique pour générer la réponse du robot en fonction du message de l'utilisateur
            self.speak(f"Ok : {message}")
            self.entry.delete(0, tk.END)

    def add_message(self, message):
        self.listbox.insert(tk.END, message)
        self.listbox.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotInterface(root)
    root.mainloop()
