from controllers.db_connection import get_session
from db_objects.objects import Order, Location, Restaurant


class OrderController:
    def __init__(self):
        self.__session = get_session()

    def get_all(self):
        orders = self.__session.query(Order).all()
        return orders

    # TODO: if there will be possibility to reserve more than one change this
    def add(self, user_id: int, location: Location, restaurant: Restaurant):
        order = Order(nr_of_reservations=1, user_id=user_id, user_location_id=location.id,
                      kitchen_type_id=restaurant.kitchen_type.id)
        self.__session.add(order)
        self.__session.commit()
