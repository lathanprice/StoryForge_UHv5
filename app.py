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
    setting = data.get('setting', 'a mysterious city')
    character = data.get('character', 'an unknown hero')
    goal = data.get('goal', 'solve a mystery')
    prompt = (
        f"You are a creative AI storyteller. Write the opening paragraph of an interactive story. "
        f"Setting: {setting}. Main character: {character}. Goal: {goal}. "
        f"End the paragraph with three choices for what the character can do next. "
        f"Format the response as: \nStory: <paragraph>\nChoices: <choice1>; <choice2>; <choice3>"
    )
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.8
        )
        ai_response = completion.choices[0].message['content']
        # Parse the AI response
        story_text = ai_response
        choices = []
        if 'Choices:' in ai_response:
            story_text, choices_str = ai_response.split('Choices:', 1)
            choices = [c.strip() for c in choices_str.split(';') if c.strip()]
        response = {
            'text': story_text.strip(),
            'choices': choices if choices else ["Continue"]
        }
    except Exception as e:
        response = {
            'text': f"Error generating story: {e}",
            'choices': ["Try again"]
        }
    return jsonify(response)

@app.route('/continue', methods=['POST'])
def continue_story():
    data = request.json
    story_so_far = data.get('story', '')
    last_choice = data.get('choice', '')
    prompt = (
        f"Continue the following interactive story based on the user's last choice. "
        f"Story so far: {story_so_far}\n"
        f"User's last choice: {last_choice}\n"
        f"Write the next paragraph and end with three new choices. "
        f"Format the response as: \nStory: <paragraph>\nChoices: <choice1>; <choice2>; <choice3>"
    )
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.8
        )
        ai_response = completion.choices[0].message['content']
        story_text = ai_response
        choices = []
        if 'Choices:' in ai_response:
            story_text, choices_str = ai_response.split('Choices:', 1)
            choices = [c.strip() for c in choices_str.split(';') if c.strip()]
        response = {
            'text': story_text.strip(),
            'choices': choices if choices else ["Continue"]
        }
    except Exception as e:
        response = {
            'text': f"Error continuing story: {e}",
            'choices': ["Try again"]
        }
    return jsonify(response)

if __name__ == '__main__':
    app.debug = True
    try:
        app.run(host='0.0.0.0', port=5001)  # Changed port to 5001
    except OSError as e:
        print(f"Error: {e}")
        print("Try using a different port or killing existing Flask processes")