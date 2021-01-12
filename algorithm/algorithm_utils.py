from queue import PriorityQueue
from math import sqrt, pi, cos
from random import randrange

from prodict import Prodict

from controllers.OrderController import OrderController
from controllers.RestaurantController import RestaurantController
from controllers.db_connection import get_session
from db_objects.objects import ReservedTables


def init_queue() -> PriorityQueue:
    user_reservation_queue = PriorityQueue()

    orders = []
    for i, order in enumerate(OrderController().get_all()):
        light_order = order.__dict__
        light_order['user_location'] = order.user_location.__dict__
        light_order['kitchen_type'] = order.kitchen_type.__dict__
        light_order['user'] = order.user.__dict__
        light_order = Prodict().from_dict(light_order)
        orders.append(light_order)

    for i, order in enumerate(orders):
        # Adding orders instead users for more complex information (orders include users)
        user_reservation_queue.put((i, order))
    return user_reservation_queue


# TODO: it's only example. Choose desired information
def preview_queue(queue: PriorityQueue):
    for priority, order in queue.queue:
        print(priority, order.user.username)


def copy_queue(q: PriorityQueue) -> PriorityQueue:
    queue = PriorityQueue()
    for element in q.queue:
        queue.put(element)
    return queue


def check_distance(user_location: Prodict, restaurant_location: Prodict) -> float:
    restaurant_lat = restaurant_location.latitude
    restaurant_lng = restaurant_location.longitude
    user_lat = user_location.latitude
    user_lng = user_location.longitude

    return sqrt((restaurant_lat - user_lat) ** 2 + (cos((user_lat * pi) / 180) * (restaurant_lng - user_lng)) ** 2) * \
           (40075.704 / 360)


def get_indexes_to_swap(queue_length: int) -> (int, int):
    i1, i2 = 0, 0
    while i1 == i2:
        i1 = randrange(queue_length)
        i2 = randrange(queue_length)
    return i1, i2


def swap_elements(queue: PriorityQueue, i1: int, i2: int) -> PriorityQueue:
    list_q = [list(element) for element in queue.queue]
    list_q[i1], list_q[i2] = list_q[i2], list_q[i1]
    list_q[i1][0], list_q[i2][0] = i1, i2
    list_q = [tuple(element) for element in list_q]
    queue = PriorityQueue()
    for element in list_q:
        queue.put(element)
    return queue


def convert_restaurants_to_dict() -> list:
    restaurants = []
    for restaurant in RestaurantController().get_all():
        rest = restaurant.__dict__
        rest['location'] = restaurant.location.__dict__
        rest['kitchen_type'] = restaurant.kitchen_type.__dict__
        rest = Prodict().from_dict(rest)
        restaurants.append(rest)
    return restaurants


def convert_reservations_to_dict() -> list:
    reservations = []
    session = get_session()
    reserved_tables = session.query(ReservedTables).all()
    for reservation in reserved_tables:
        res = reservation.__dict__
        res = Prodict().from_dict(res)
        reservations.append(res)
    return reservations


def print_reservations(reservations: list):
    for i, reservation in enumerate(reservations):
        print(i, reservation.total_nr_of_reservations)


if __name__ == "__main__":
    # print(get_indexes_to_swap(10))
    # q = PriorityQueue()
    # q.put((0, 'a'))
    # q.put((1, 'b'))
    # q.put((2, 'c'))
    # for i, j in q.queue:
    #     print(f"({i}, {j})", end=", ")
    # print('')
    # q = swap_elements(q, 0, 2)
    # for i, j in q.queue:
    #     print(f"({i}, {j})", end=", ")

    import pprint
    q = init_queue()
    pprint.pprint(q.queue[0])
    preview_queue(q)