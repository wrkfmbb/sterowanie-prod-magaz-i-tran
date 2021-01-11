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
        light_order = Prodict().from_dict(light_order)
        orders.append(light_order)

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
    print('\n')
    for priority, order in queue_backup:
        queue.put((priority, order))


def copy_queue(q):
    queue = PriorityQueue()
    for element in q.queue:
        queue.put(element)
    return queue


def check_distance(user_location, restaurant_location) -> float:
    restaurant_lat = restaurant_location.latitude
    restaurant_lng = restaurant_location.longitude
    user_lat = user_location.latitude
    user_lng = user_location.longitude

    return sqrt((restaurant_lat - user_lat) ** 2 + (cos((user_lat * pi) / 180) * (restaurant_lng - user_lng)) ** 2) * \
           (40075.704 / 360)


def reserve_table(restaurant, session):
    # session = get_session()
    reserved_tables = session.query(ReservedTables) \
        .filter(ReservedTables.restaurant.has(name=restaurant.name)).one()
    nr_of_all_tables = restaurant.nr_of_tables
    nr_of_reserved_tables = reserved_tables.total_nr_of_reservations
    # TODO: if there will be posibility to reserve more than 1 table then change condition and increment value
    if nr_of_all_tables - nr_of_reserved_tables > 0:
        reserved_tables.total_nr_of_reservations += 1
        session.commit()


def get_indexes_to_swap(queue_length: int):
    i1, i2 = 0, 0
    while i1 == i2:
        i1 = randrange(queue_length)
        i2 = randrange(queue_length)
    return i1, i2


def swap_elements(queue: PriorityQueue, i1: int, i2: int):
    list_q = [list(element) for element in queue.queue]
    list_q[i1], list_q[i2] = list_q[i2], list_q[i1]
    list_q[i1][0], list_q[i2][0] = i1, i2
    list_q = [tuple(element) for element in list_q]
    queue = PriorityQueue()
    for element in list_q:
        queue.put(element)
    return queue


def convert_restaurants_to_dict():
    restaurants = []
    for restaurant in RestaurantController().get_all():
        rest = restaurant.__dict__
        rest['location'] = restaurant.location.__dict__
        rest['kitchen_type'] = restaurant.kitchen_type.__dict__
        rest = Prodict().from_dict(rest)
        restaurants.append(rest)
    return restaurants


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
