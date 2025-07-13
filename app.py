from flask import Flask, render_template, jsonify, request, send_from_directory, session
import os
import re

# get OpenAI API key
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Load variables from .env
openai_api_key = os.getenv("OPENAI_API_KEY")

# Use OpenAI client for v1+
client = OpenAI(api_key=openai_api_key)

# Initialize Flask with explicit folder paths
app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates',
    static_url_path='/static'
)

app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_secret")

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
    session['goal'] = goal

    prompt = (
        f"You are a creative storyteller. Write the opening paragraph of an interactive story. "
        f"Setting: {setting}. Main character: {character}. Goal: {goal}. "
        f"End the paragraph with three choices for what the character can do next. "
        f"Format the response as:\nStory: <paragraph>\nChoices: <choice1>; <choice2>; <choice3>\n"
        f"Only include the story paragraph after 'Story:' and the choices after 'Choices:'."
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
            if story_text.strip().lower().startswith('story:'):
                story_text = story_text.strip()[6:].strip()

            # Try robust splitting
            choices = [c.strip() for c in choices_str.split(';') if c.strip()]
            if len(choices) <= 1:
                choices = re.findall(r'(?:\d+\.\s*|-|\*|•)\s*([^;\n\r]+)', choices_str)
                choices = [c.strip() for c in choices if c.strip()]
            choices = list(dict.fromkeys(choices))

            for c in choices:
                if c.lower() in ['end the story', 'the end', 'end', 'finish the story']:
                    is_ending = True
                    choices = [c for c in choices if c.lower() not in ['end the story', 'the end', 'end', 'finish the story']]
                    break
        else:
            if ai_response.strip().lower().startswith('story:'):
                story_text = ai_response.strip()[6:].strip()

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
    goal = data.get('goal') or session.get('goal', 'solve a mystery')

    prompt = (
    f"You are a creative AI storyteller continuing an interactive story, one paragraph at a time. "
    f"The main character has a goal: '{goal}'. When this goal is achieved — even partially — the story should end. "
    f"Do NOT repeat or summarize earlier parts of the story. Only continue directly from the last event based on the user's last choice.\n\n"
    f"Provide your output in this exact format:\n"
    f"Story: <next paragraph>\nChoices: <choice1>; <choice2>; <choice3>\n"
    f"If the story is complete, format it as:\nStory: <final paragraph>\nChoices: END\n\n"
    f"---\nSTORY SO FAR:\n{story_so_far}\n"
    f"USER'S LAST CHOICE: {last_choice}\n"
    f"MAIN GOAL: {goal}\n"
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

        # Parse response
        if 'Choices:' in ai_response:
            story_text, choices_str = ai_response.split('Choices:', 1)

            if story_text.strip().lower().startswith('story:'):
                story_text = story_text.strip()[6:].strip()

            choices = [c.strip() for c in choices_str.split(';') if c.strip()]
            # Normalize and check for ending
            normalized = [c.lower() for c in choices]
            if any(c in ['end', 'the end', 'finish the story'] for c in normalized):
                is_ending = True
                choices = []
        else:
            # If no choices given, assume story ended
            is_ending = True
            choices = []

        response = {
            'text': story_text.strip(),
            'choices': choices if choices else ([] if is_ending else ["Continue"]),
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
    data = request.json
    story = data.get('story', '')
    try:
        return render_template('ending.html', story=story)
    except Exception as e:
        return f"Error rendering ending: {e}", 500

if __name__ == '__main__':
    app.debug = True
    try:
        app.run(host='0.0.0.0', port=5001)
    except OSError as e:
        print(f"Error: {e}")
        print("Try using a different port or killing existing Flask processes")
