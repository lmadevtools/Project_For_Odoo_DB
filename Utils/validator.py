import re

#check if mail is valid
def is_valid_email(email: str) -> bool:
    if not isinstance(email, str):
        return False
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None