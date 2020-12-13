from controllers.db_connection import get_session
from db_objects.objects import Restaurant


class RestaurantController:
    def __init__(self):
        pass

    @staticmethod
    def get_matched_by_kitchen_type_id(kitchen_type_id):
        session = get_session()
        restaurants = session.query(Restaurant).filter_by(kitchen_type_id=kitchen_type_id).all()
        return restaurants
