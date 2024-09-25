from flask import Flask, render_template, jsonify, request
import subprocess
import requests

app = Flask(__name__)

outputs = []
result = None  # Global variable to store the last generated result

@app.route('/')
def index():
    return render_template('index.html', result=result)  # Pass the result to the template

@app.route('/get_outputs')
def get_outputs():
    return jsonify(outputs)

@app.route('/run_test', methods=['POST'])
def run_test():
    global result  # Use the global variable
    outputs.clear()  # Clear previous outputs
    subprocess.run(['python', 'test.py'])  # Run test.py
    
    response_string = " ".join(outputs)  # Combine outputs into a single string
    gemini_response = requests.post('http://localhost:5001/gemini', json={'response_string': response_string})
    
    if gemini_response.status_code == 200:
        result = gemini_response.json().get('result')  # Store the result
        return jsonify(result=result)  # Return the response from gemini.py
    else:
        return jsonify(error="Error occurred in gemini service"), 500

@app.route('/store_output', methods=['POST'])
def store_output():
    data = request.json
    outputs.append(data['output'])
    return 'OK'

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Running on port 5000
