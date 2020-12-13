from controllers.db_connection import get_session
from db_objects.objects import Order


class OrderController:
    def __init__(self):
        pass

    @staticmethod
    def get_all():
        session = get_session()
        orders = session.query(Order).all()
        return orders
