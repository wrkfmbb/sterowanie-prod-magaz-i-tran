from random_username.generate import generate_username

from controllers.db_connection import get_session
from db_objects.objects import User

usernames = generate_username(29)
session = get_session()

for username in usernames:
    user = User(username=username)
    session.add(user)
session.commit()