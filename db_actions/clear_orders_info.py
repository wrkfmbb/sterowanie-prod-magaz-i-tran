from sqlalchemy import desc
from controllers.db_connection import get_session
from db_objects.objects import Location, Restaurant, Order, ReservedTables

session = get_session()

# delete orders
session.query(Order).delete()
session.commit()

# reset tables reservations
reserved_tables = session.query(ReservedTables).all()
for tables in reserved_tables:
    tables.total_nr_of_reservations = 0
session.commit()

# # delete users locations
# restaurant = session.query(Restaurant).order_by(desc(Restaurant.id)).first()
# session.query(Location).filter(Location.id > restaurant.id).delete()
# session.commit()
