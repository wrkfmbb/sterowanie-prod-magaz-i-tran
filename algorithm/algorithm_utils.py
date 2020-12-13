from queue import PriorityQueue
from math import sqrt, pi, cos

from controllers.db_connection import get_session
from db_objects.objects import Order, Location


def init_queue() -> PriorityQueue:
    user_reservation_queue = PriorityQueue()
    session = get_session()
    orders = session.query(Order).order_by(Order.id).all()
    for i, order in enumerate(orders):
        # Adding orders instead users for more complex information (orders include users)
        user_reservation_queue.put((i, order))
    return user_reservation_queue


# TODO: it's only example. Choose desired information
def preview_queue(queue):
    queue_backup = []
    while not queue.empty():
        priority, order = queue.get()
        queue_backup.append((priority, order))
        print(priority, order.user.username)
    for priority, order in queue_backup:
        queue.put((priority, order))


def check_distance(user_location, restaurant_location) -> float:
    restaurant_lat = restaurant_location.latitude
    restaurant_lng = restaurant_location.longitude
    user_lat = user_location.latitude
    user_lng = user_location.longitude

    return sqrt((restaurant_lat - user_lat) ** 2 + (cos((user_lat * pi) / 180) * (restaurant_lng - user_lng)) ** 2) * \
           (40075.704 / 360)
