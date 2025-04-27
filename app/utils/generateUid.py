import random
import string

def generate_custom_id(length=6):
    """Generate a random ID with letters and numbers."""
    characters = string.ascii_lowercase + string.digits  # abc...xyz + 0-9
    custom_id = ''.join(random.choices(characters, k=length))
    return custom_id