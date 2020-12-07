from controllers.db_connection import get_engine
from sqlalchemy.orm import sessionmaker
from db_objects.objects import Location

engine = get_engine()

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

locations = session.query(Location).order_by(Location.id).all()
print(locations)
