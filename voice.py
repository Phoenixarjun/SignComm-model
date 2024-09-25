from flask import Flask, request, jsonify
import pyttsx3
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    text = data.get('text', '')

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Choose a voice if needed

    engine.say(text)
    engine.runAndWait()

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(port=5002, debug=True)  # Running on port 5002
