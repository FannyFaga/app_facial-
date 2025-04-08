import json
import os
import numpy as np
from datetime import datetime

FACES_PATH = 'faces.json'
LOGS_PATH = 'logs.json'

if not os.path.exists(FACES_PATH):
    with open(FACES_PATH, 'w') as f:
        json.dump({}, f)

if not os.path.exists(LOGS_PATH):
    with open(LOGS_PATH, 'w') as f:
        json.dump([], f)

def save_face(name, embedding):
    with open(FACES_PATH, 'r+') as f:
        data = json.load(f)
        data[name] = embedding
        f.seek(0)
        json.dump(data, f)
        f.truncate()

def match_face(embedding):
    with open(FACES_PATH, 'r') as f:
        data = json.load(f)
    for name, known_embedding in data.items():
        dist = np.linalg.norm(np.array(known_embedding) - np.array(embedding))
        if dist < 0.6:
            return name
    return "Inconnu"

def log_access(identity):
    with open(LOGS_PATH, 'r+') as f:
        logs = json.load(f)
        logs.append({'identity': identity, 'timestamp': datetime.now().isoformat()})
        f.seek(0)
        json.dump(logs, f)
        f.truncate()

def get_logs():
    with open(LOGS_PATH, 'r') as f:
        return json.load(f)