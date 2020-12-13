from controllers.db_connection import get_session
from db_objects.objects import Restaurant


class RestaurantController:
    def __init__(self):
        self.__session = get_session()

    def get_matched_by_kitchen_type_id(self, kitchen_type_id):
        restaurants = self.__session.query(Restaurant).filter_by(kitchen_type_id=kitchen_type_id).all()
        return restaurants

    def get_one_by_name(self, restaurant_name):
        restaurant = self.__session.query(Restaurant).filter(Restaurant.name == restaurant_name).one()
        return restaurant
