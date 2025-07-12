from flask import Flask, render_template, jsonify, request, send_from_directory
import os

# get OpenAI API key
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()  # Load variables from .env
openai_api_key = os.getenv("OPENAI_API_KEY")  # Securely get the key

# Use OpenAI client for v1+
client = OpenAI(api_key=openai_api_key)

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
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.8
        )
        ai_response = completion.choices[0].message.content
        # Parse the AI response
        story_text = ai_response
        choices = []
        is_ending = False
        if 'Choices:' in ai_response:
            story_text, choices_str = ai_response.split('Choices:', 1)
            choices = [c.strip() for c in choices_str.split(';') if c.strip()]
            # Detect ending if AI signals with "End the story" or "END"
            for c in choices:
                if c.lower() in ['end the story', 'the end', 'end', 'finish the story']:
                    is_ending = True
                    choices = [c for c in choices if c.lower() not in ['end the story', 'the end', 'end', 'finish the story']]
                    break
        response = {
            'text': story_text.strip(),
            'choices': choices if choices else (["Continue"] if not is_ending else []),
            'ending': is_ending
        }
    except Exception as e:
        response = {
            'text': f"Error generating story: {e}",
            'choices': ["Try again"],
            'ending': False
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
        f"If the story is at a natural conclusion, write a final paragraph and indicate the end by including 'Choices: END'. "
        f"Otherwise, write the next paragraph and end with three new choices. "
        f"Format the response as: \nStory: <paragraph>\nChoices: <choice1>; <choice2>; <choice3 or END>"
    )
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.8
        )
        ai_response = completion.choices[0].message.content
        story_text = ai_response
        choices = []
        is_ending = False
        if 'Choices:' in ai_response:
            story_text, choices_str = ai_response.split('Choices:', 1)
            choices = [c.strip() for c in choices_str.split(';') if c.strip()]
            # Detect ending if AI signals with "END"
            for c in choices:
                if c.lower() in ['end the story', 'the end', 'end', 'finish the story', 'end']:
                    is_ending = True
                    choices = [c for c in choices if c.lower() not in ['end the story', 'the end', 'end', 'finish the story']]
                    break
        response = {
            'text': story_text.strip(),
            'choices': choices if choices else (["Continue"] if not is_ending else []),
            'ending': is_ending
        }
    except Exception as e:
        response = {
            'text': f"Error continuing story: {e}",
            'choices': ["Try again"],
            'ending': False
        }
    return jsonify(response)

@app.route('/ending', methods=['POST'])
def ending_screen():
    """
    Expects JSON: { "story": "<full story text>" }
    Renders an ending screen with the full story.
    """
    data = request.json
    story = data.get('story', '')
    try:
        return render_template('ending.html', story=story)
    except Exception as e:
        return f"Error rendering ending: {e}", 500

if __name__ == '__main__':
    app.debug = True
    try:
        app.run(host='0.0.0.0', port=5001)  # Changed port to 5001
    except OSError as e:
        print(f"Error: {e}")
        print("Try using a different port or killing existing Flask processes")