from controllers.db_connection import get_session
from db_objects.objects import Order, User, Location

session = get_session()

# TODO: restaurant location is the same as user location -> generate some new locations for users
users = session.query(User).order_by(User.id).all()
users_id = [user.id for user in users]

locations = session.query(Location).order_by(Location.id.desc()).limit(len(users_id))
locations_id = [location.id for location in locations]

for i, (user_id, location_id) in enumerate(zip(users_id, locations_id)):
    order = Order(nr_of_reservations=1, user_id=user_id, user_location_id=location_id, kitchen_type_id=((i % 9) + 1))
    session.add(order)
session.commit()
