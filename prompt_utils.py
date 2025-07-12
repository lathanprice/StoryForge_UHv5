def build_initial_prompt(setting, character, goal):
    return f"""Create the first paragraph of a choose-your-own-adventure story.
Setting: {setting}
Main character: {character}
Goal: {goal}

Write under 100 words. Provide 2–3 numbered choices.
"""

def build_followup_prompt(previous_paragraph, user_choice):
    return f"""Continue this interactive story.

So far: "{previous_paragraph}"

The user chose: "{user_choice}"

Write the next paragraph (under 100 words). Provide 2–3 numbered choices.
"""