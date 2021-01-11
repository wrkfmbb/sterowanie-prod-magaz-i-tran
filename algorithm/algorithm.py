from math import exp
from queue import PriorityQueue
import random

from algorithm_utils import init_queue, preview_queue, check_distance, reserve_table, copy_queue, get_indexes_to_swap, \
    swap_elements
from controllers.RestaurantController import RestaurantController

# user_reservation_queue = init_queue()
# preview_queue(user_reservation_queue)
#
# # Example of calculating distance from queue location and available restaurants location
# _, order = user_reservation_queue.get()
# # Temp controller instead static methods for auto closing session - i'm not sure is necessary but it's safer
# restaurants = RestaurantController().get_matched_by_kitchen_type_id(order.kitchen_type_id)
#
# for restaurant in restaurants:
#     print(check_distance(order.user_location, restaurant.location))
# # end of example :)
from controllers.db_connection import get_session
from db_objects.objects import Restaurant, ReservedTables


class Algorithm:
    def __init__(self):
        self.user_orders_queue = init_queue()
        self.loss = 0
        self.isOptimal = True
        self.__session = get_session()

    def assign_restaurants(self, queue):
        restaurant_controller = RestaurantController()
        distances = []

        for _, order in queue.queue:
            restaurants = restaurant_controller.get_matched_by_kitchen_type_id(order.kitchen_type_id)
            min_distance, nearest_restaurant_index = self.__find_nearest_restaurant(order, restaurants)

            reserve_table(restaurants[nearest_restaurant_index], self.__session)
            distances.append(min_distance)

        self.loss = sum(distances)

    def __find_nearest_restaurant(self, order, restaurants):
        nearest_restaurant_index = 0
        min_distance = 99999999999
        for i, rest in enumerate(restaurants):
            distance = check_distance(order.user_location, rest.location)

            if distance < min_distance:
                nr_of_available_tables = self.__check_available_tables(rest)

                if not nr_of_available_tables:
                    self.isOptimal = False
                else:
                    nearest_restaurant_index = i
                    min_distance = distance

        return min_distance, nearest_restaurant_index

    def __check_available_tables(self, rest):
        reserved_tables = self.__session.query(ReservedTables).filter(
            ReservedTables.restaurant.has(name=rest.name)).one()
        nr_of_all_tables = rest.nr_of_tables
        nr_of_reserved_tables = reserved_tables.total_nr_of_reservations
        nr_of_available_tables = nr_of_all_tables - nr_of_reserved_tables
        return nr_of_available_tables

    def start(self, start_temp=5000, cooling_factor=0.9, iterations=3):
        if self.isOptimal:
            print("Queue is optimal there's no need to run algorithm")
            return self.loss

        # rollback leastest reservations
        self.__session.rollback()
        temp = start_temp
        queue = copy_queue(self.user_orders_queue)
        queue_length = len(queue.queue)

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
            self.__session.rollback()
        self.__session.commit()
        return self.loss


if __name__ == '__main__':
    alg = Algorithm()
    alg.assign_restaurants(alg.user_orders_queue)
    print(f"Initial loss: {alg.loss}, is optimal: {alg.isOptimal}")
    alg.start()
    print(alg.loss)
