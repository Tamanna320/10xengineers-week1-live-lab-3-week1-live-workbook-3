import uuid
from datetime import datetime

def gen_id():
    return str(uuid.uuid4())[:8]

def now():
    return datetime.now()

def slugify(text):
    return text.lower().replace(" ", "-")

def truncate(text, length=100):
    if len(text) <= length:
        return text
    return text[:length] + "..."

def word_count(text):
    return len(text.split())

def estimate_read_time(text, wpm=200):
    words = word_count(text)
    mins = words / wpm
    return max(1, round(mins))

