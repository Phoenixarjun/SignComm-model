import google.generativeai as genai
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify

load_dotenv()
api_key = os.getenv('MY_API_KEY')

genai.configure(api_key=api_key)

app = Flask(__name__)

@app.route('/gemini', methods=['POST'])
def gemini():
    data = request.json
    response_string = data['response_string']
    
    prompt = f'"{response_string}" + I will provide you with a set of words. Your task is to create a coherent and meaningful sentence using these words, adding appropriate punctuation where necessary. Ensure the sentence is grammatically correct and logically structured. If there are any extraneous or irrelevant words, feel free to exclude them to enhance clarity and readability. The goal is to form a single, well-constructed sentence like add some supporting word to it exampe if there is yes and i love you word then give a sentence as yes i love you too with correct punctuations and if there is no words give a message as kindly do something like that that conveys a clear message or idea.'
    
    response = genai.generate_text(prompt=prompt)
    
    if response.result:
        result = response.result
    else:
        result = "No meaningful sentence could be generated."

    return jsonify(result=result)  # Send back only the generated sentence

if __name__ == '__main__':
    app.run(port=5001, debug=True)  # Running on port 5001
