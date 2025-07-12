from flask import Flask, render_template, jsonify, request, send_from_directory
import os

# get OpenAI API key
from dotenv import load_dotenv
import os
import openai

load_dotenv()  # Load variables from .env
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely get the key

# Initialize Flask with explicit folder paths
app = Flask(__name__, 
    static_folder='static',
    template_folder='templates',
    static_url_path='/static'
)

# Debug prints to verify paths
print("Current working directory:", os.getcwd())
print("Static folder:", app.static_folder)
print("Template folder:", app.template_folder)

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        return str(e), 500

@app.route('/generate', methods=['POST'])
def generate_story():
    data = request.json
    # Mock response for now
    response = {
        'text': f"In the neon-lit streets of {data.get('setting')}, {data.get('character')} searches for clues to {data.get('goal')}...",
        'choices': [
            "Investigate the mysterious alley",
            "Follow the digital trail",
            "Seek help from local contacts"
        ]
    }
    return jsonify(response)

@app.route('/continue', methods=['POST'])
def continue_story():
    data = request.json
    # Mock response for now
    response = {
        'text': "The story continues...",
        'choices': [
            "Proceed with caution",
            "Take a bold approach",
            "Seek an alternative path"
        ]
    }
    return jsonify(response)

if __name__ == '__main__':
    app.debug = True
    try:
        app.run(host='0.0.0.0', port=5001)  # Changed port to 5001
    except OSError as e:
        print(f"Error: {e}")
        print("Try using a different port or killing existing Flask processes")