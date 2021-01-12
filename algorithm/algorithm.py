from math import exp
import random
from queue import PriorityQueue

from prodict import Prodict

from algorithm_utils import init_queue, preview_queue, check_distance, copy_queue, get_indexes_to_swap, \
    swap_elements, convert_restaurants_to_dict, convert_reservations_to_dict, print_reservations

from controllers.db_connection import get_session
from db_objects.objects import ReservedTables


class Algorithm:
    def __init__(self):
        self.user_orders_queue = init_queue()
        self.loss = 0
        self.isOptimal = True
        self.__session = get_session()
        self.__restaurants = convert_restaurants_to_dict()
        self.reservations = convert_reservations_to_dict()

    def __get_restaurants_by_kitchen_type_id(self, kitchen_type_id: int) -> list:
        return [restaurant for restaurant in self.__restaurants if restaurant.kitchen_type.id == kitchen_type_id]

    def assign_restaurants(self, queue: PriorityQueue):
        distances = []
        i = 0
        for _, order in queue.queue:
            i += 1
            restaurants = self.__get_restaurants_by_kitchen_type_id(order.kitchen_type_id)
            min_distance, nearest_restaurant_index = self.__find_nearest_restaurant(order, restaurants)

            self.__reserve_table(restaurants[nearest_restaurant_index])
            distances.append(min_distance)

        self.loss = sum(distances)

    def __find_nearest_restaurant(self, order: Prodict, restaurants: list) -> (int, int):
        nearest_restaurant_index = 0
        min_distance = 99999999999
        for i, rest in enumerate(restaurants):
            distance = check_distance(order.user_location, rest.location)

            if distance < min_distance:
                nr_of_available_tables = self.__check_available_tables(rest)[1]

                if not nr_of_available_tables:
                    self.isOptimal = False
                else:
                    nearest_restaurant_index = i
                    min_distance = distance

        return min_distance, nearest_restaurant_index

    def __check_available_tables(self, rest: Prodict) -> tuple:
        key, reserved_tables = self.__match_reservation_by_restaurant_id(rest.id)
        nr_of_all_tables = rest.nr_of_tables
        nr_of_reserved_tables = reserved_tables.total_nr_of_reservations
        nr_of_available_tables = nr_of_all_tables - nr_of_reserved_tables
        return key, nr_of_available_tables

    def __match_reservation_by_restaurant_id(self, restaurant_id: int) -> tuple:
        for key, reservation in enumerate(self.reservations):
            if reservation.restaurant_id == restaurant_id:
                return key, reservation

    def __reserve_table(self, restaurant: Prodict):
        key, reserved_tables = self.__match_reservation_by_restaurant_id(restaurant.id)
        nr_of_all_tables = restaurant.nr_of_tables
        nr_of_reserved_tables = reserved_tables.total_nr_of_reservations
        # TODO: if there will be posibility to reserve more than 1 table then change condition and increment value
        if nr_of_all_tables - nr_of_reserved_tables > 0:
            reserved_tables.total_nr_of_reservations += 1
            # print(f"reserving with id {reserved_tables.id}")
            self.reservations[key] = reserved_tables

    def start(self, start_temp=5000, cooling_factor=0.9, iterations=300):
        if self.isOptimal:
            print("Queue is optimal there's no need to run algorithm")
            return self.loss

        temp = start_temp
        queue = copy_queue(self.user_orders_queue)
        queue_length = len(queue.queue)
        self.__reset_reservations()

        for i in range(iterations):
            i1, i2 = get_indexes_to_swap(queue_length)
            prevoius_queue = copy_queue(queue)
            queue = swap_elements(queue, i1, i2)

            previous_loss = self.loss
            self.assign_restaurants(queue)
            if previous_loss < self.loss:
                accept_probability = exp((previous_loss - self.loss) / temp)
                if random.random() < accept_probability:
                    queue = prevoius_queue

            temp *= cooling_factor
            self.__reset_reservations()
        self.user_orders_queue = queue
        return self.loss

    def __reset_reservations(self):
        self.reservations = convert_reservations_to_dict()

    def get_queue_by_user_id(self):
        return [order[1].user_id for order in self.user_orders_queue.queue]


if __name__ == '__main__':
    from pprint import pprint
    alg = Algorithm()
    alg.assign_restaurants(alg.user_orders_queue)
    # print_reservations(alg.reservations)
    print(f"Initial loss: {alg.loss}, is optimal: {alg.isOptimal}")
    print(f"order {alg.get_queue_by_user_id()}")
    alg.start()
    print(f"end loss: {alg.loss}")
    print(f"order {alg.get_queue_by_user_id()}")
