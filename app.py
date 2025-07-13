from flask import Flask, render_template, jsonify, request, session, make_response
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates',
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

            raw_choices = [c.strip() for c in choices_str.split(';') if c.strip()]
            choices = []
            for c in raw_choices:
                cleaned = re.sub(r'^\s*(\d+[\.\)]|[-*•])\s*', '', c)
                if cleaned:
                    choices.append(cleaned.strip())

            for c in choices:
                if c.lower() in ['end the story', 'the end', 'end', 'finish the story']:
                    is_ending = True
                    choices = []
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

        if 'Choices:' in ai_response:
            story_text, choices_str = ai_response.split('Choices:', 1)
            if story_text.strip().lower().startswith('story:'):
                story_text = story_text.strip()[6:].strip()

            raw_choices = [c.strip() for c in choices_str.split(';') if c.strip()]
            choices = []
            for c in raw_choices:
                cleaned = re.sub(r'^\s*(\d+[\.\)]|[-*•])\s*', '', c)
                if cleaned:
                    choices.append(cleaned.strip())

            if any(c.lower() in ['end', 'the end', 'finish the story'] for c in choices):
                is_ending = True
                choices = []
        else:
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
        # Clean up the story text and ensure proper formatting
        story = re.sub(r'\s*\n\s*', '\n', story.strip())
        story = re.sub(r'\n(?!\n)', '\n\n', story)
        story = re.sub(r'\n{3,}', '\n\n', story)
        
        # Split into paragraphs and format
        paragraphs = story.split('\n\n')
        formatted_paragraphs = []
        for para in paragraphs:
            if para.strip():
                formatted_paragraphs.append(para.strip())
        
        # Rejoin with proper spacing
        story = '\n\n'.join(formatted_paragraphs)
        
        # Store in session for reloads
        session['final_story'] = story
        
        # Create response with proper headers
        response = make_response(render_template('ending.html', story=story))
        response.headers.update({
            'Content-Type': 'text/html; charset=utf-8',
            'Cache-Control': 'no-cache, no-store, must-revalidate, max-age=0',
            'Content-Security-Policy': "default-src 'self'; style-src 'self' https://fonts.googleapis.com 'unsafe-inline'; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:;",
            'X-Content-Type-Options': 'nosniff',
            'Pragma': 'no-cache'
        })
        return response
    except Exception as e:
        return f"Error rendering ending: {e}", 500

@app.route('/ending/<story_id>')
def show_ending(story_id):
    try:
        from flask import session
        story = session.get('final_story', '')
        if not story:
            return "Story not found", 404
        return render_template('ending.html', story=story)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax'
    )
    app.debug = True
    try:
        app.run(host='0.0.0.0', port=5001)
    except OSError as e:
        print(f"Error: {e}")
        print("Try using a different port or killing existing Flask processes")
