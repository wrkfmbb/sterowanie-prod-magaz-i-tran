from controllers.db_connection import get_session

from db_objects.objects import Location

session = get_session()
locations = session.query(Location).order_by(Location.id).all()
print(locations[0].id)

# restaurants = session.query(Restaurant).order_by(Restaurant.id).all()
# print(restaurants[0].name)
#
# location = Location(latitude=1.0, longitude=2.0)
# session.add(location)
# session.commit()
# print(location.id)
