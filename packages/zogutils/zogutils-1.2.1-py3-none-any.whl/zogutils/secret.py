import secrets
import string


def unique_id(length: int = 8, prefix: str = "Z"):
    alphabet = string.digits + string.ascii_letters
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return prefix + password
