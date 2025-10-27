import random
import secrets
import string
from typing import Literal


def get_random_string(symbols: Literal['digits', 'letters', 'both'] = 'digits', n=8):
    """Return a random string."""
    match symbols:
        case 'digits':
            return ''.join(random.choices(string.digits, k=n))
        case 'letters':
            return ''.join(random.choices(string.ascii_letters, k=n))
        case 'both':
            return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(n))
        case _:
            raise ValueError("Unsupported 'symbols' value")
