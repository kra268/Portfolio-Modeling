from ..utils.file_utils import read_json, write_json
from ..config import USER_DATA_PATH
from ..models import User

def get_user(username):
    """
    Retrieve user data by username.
    """
    users = read_json(USER_DATA_PATH)
    return users.get(username)

def create_user(username):
    """
    Create a new user.
    """
    users = read_json(USER_DATA_PATH)
    if username in users:
        raise ValueError("User already exists!")
    users[username] = User(username=username).__dict__
    write_json(USER_DATA_PATH, users)
    return users[username]