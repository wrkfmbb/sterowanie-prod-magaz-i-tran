from controllers.db_connection import get_session
from db_objects.objects import Order

session = get_session()

# TODO: restaurant location is the same as user location -> generate some new locations for users
for i in range(20):
    order = Order(nr_of_reservations=1, user_id=(i+12), user_location_id=(i+1), kitchen_type_id=((i % 9) + 1))
    session.add(order)
session.commit()
