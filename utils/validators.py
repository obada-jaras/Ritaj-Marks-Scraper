import re


def is_valid_user_id(user_id):
    return True


def is_valid_email(email: str) -> bool:
    # Check if email matches regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
