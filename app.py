from flask import Flask, render_template
from threading import Thread
import webbrowser

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def run_flask():
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    # Lancer le serveur Flask dans un thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Ouvrir la page web dans le navigateur
    webbrowser.open('http://127.0.0.1:5000/')
