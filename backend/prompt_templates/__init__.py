import os

PROMPT_DIR = os.path.dirname(__file__)

def list_prompts():
    return [f for f in os.listdir(PROMPT_DIR) if f.endswith('.txt')]

def load_prompt(filename):
    with open(os.path.join(PROMPT_DIR, filename), 'r', encoding='utf-8') as f:
        return f.read()

def save_prompt(filename, content):
    with open(os.path.join(PROMPT_DIR, filename), 'w', encoding='utf-8') as f:
        f.write(content)