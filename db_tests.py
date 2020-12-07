from controllers.db_connection import get_session

from db_objects.objects import Location, Restaurant

session = get_session()
locations = session.query(Location).order_by(Location.id).all()
print(locations[0].id)

restaurants = session.query(Restaurant).order_by(Restaurant.id).all()
print(restaurants[0].name)