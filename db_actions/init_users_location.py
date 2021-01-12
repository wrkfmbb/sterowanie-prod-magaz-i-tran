import random
from controllers.db_connection import get_session
from db_objects.objects import Location, User

session = get_session()

# wziąłem romb z google tak aby pokrywał dużą część wrocławia
upper_left = 51.12494279251575, 17.011988909212764
bottom_right = 51.090951, 17.068490
upper_right = 51.121032728830166, 17.097620980657062
bottom_left = 51.101113224995665, 16.99674451866926

# żeby wiedzieć ile lokalizacji mam wylosować
users = session.query(User).order_by(User.id).all()
iterations = len(users)

for i in range(iterations):
    # losuję lokalizację z wybranego obszaru
    lat = random.uniform(bottom_right[0], upper_left[0])
    lng = random.uniform(bottom_left[1], upper_right[1])
    loc = Location(latitude=lat, longitude=lng)
    session.add(loc)

session.commit()


