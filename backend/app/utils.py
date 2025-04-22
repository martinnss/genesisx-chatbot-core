import os
import requests
from .models import Message, db
from sqlalchemy import asc
import anthropic
import json
import time
from datetime import datetime

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
MODEL_NAME = "claude-3-opus-20240229"

# JSON file to store API call timestamps
API_CALLS_FILE = "api_calls.json"

def format_history(conversation_id):
    messages = Message.query.filter_by(conversation_id=conversation_id)\
                    .order_by(asc(Message.timestamp)).all()
    history = []
    for msg in messages:
        role = "user" if msg.sender == "user" else "assistant"
        history.append({"role": role, "content": msg.content})
    return history


def call_anthropic_api(messages):
    # Record the timestamp of this API call
    timestamp = datetime.now().isoformat()
    
    # Load existing API calls
    api_calls = []
    if os.path.exists(API_CALLS_FILE):
        try:
            with open(API_CALLS_FILE, 'r') as f:
                api_calls = json.load(f)
        except json.JSONDecodeError:
            api_calls = []
    
    # Add new timestamp
    api_calls.append(timestamp)
    
    # Save updated API calls
    with open(API_CALLS_FILE, 'w') as f:
        json.dump(api_calls, f)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)


    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            system="Eres un asistente que trabaja para GenesisX, que responde preguntas y ayuda con tareas según ciertos perfiles, puedes ser un CEO, Analista de datos o un expero en operaciones",
            messages=messages
        )
        print(response)
    except Exception as e:
        return str(e)

    return response.content[0].text



def get_api_call_count():
    """Returns the number of distinct API calls made to Anthropic in this session."""
    if not os.path.exists(API_CALLS_FILE):
        return 0
    
    try:
        with open(API_CALLS_FILE, 'r') as f:
            api_calls = json.load(f)
        return len(api_calls)
    except (json.JSONDecodeError, FileNotFoundError):
        return 0