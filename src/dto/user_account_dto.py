from dataclasses import dataclass, field

from config import EMAIL
from src.utils import utils


@dataclass
class UserAccountDto:
    mobile_number: str = ''
    email: str = field(default_factory=lambda: EMAIL.replace("test", utils.get_random_string('digits', 8)))
    password: str = field(default_factory=lambda: utils.get_random_string('both', 12))
    full_name: str = field(default_factory=lambda: f"TestUser {utils.get_random_string('digits', 8)}")
    username: str = field(default_factory=lambda: utils.get_random_string('letters', 12))
