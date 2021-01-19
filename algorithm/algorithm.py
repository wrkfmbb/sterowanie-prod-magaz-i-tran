from math import exp
import random
from queue import PriorityQueue
from prodict import Prodict
from algorithm_utils import init_queue, check_distance, copy_queue, get_indexes_to_swap, \
    swap_elements, convert_restaurants_to_dict, convert_reservations_to_dict


class Algorithm:
    def __init__(self):
        self.user_orders_queue = init_queue()
        self.loss = 0
        self.minimal_loss = 99999999999
        self.best_queue = copy_queue(self.user_orders_queue)
        self.isOptimal = True
        self.__restaurants = convert_restaurants_to_dict()
        self.__reservations = convert_reservations_to_dict()
        self.__backup_reservations = convert_reservations_to_dict()

    def __get_restaurants_by_kitchen_type_id(self, kitchen_type_id: int) -> list:
        return [restaurant for restaurant in self.__restaurants if restaurant.kitchen_type.id == kitchen_type_id]

    def assign_restaurants(self, queue: PriorityQueue):
        distances = [] # wszystkie odległości do restauracji do funkcji straty

        for _, order in queue.queue:
            # wybór restauracji które serwują dania wybranego typu
            restaurants = self.__get_restaurants_by_kitchen_type_id(order.kitchen_type_id)
            # odległość i indeks dla najbliższej restauracji
            distance, nearest_restaurant_index = self.__find_nearest_restaurant(order, restaurants)
            distances.append(distance)
            self.__reserve_table(restaurants[nearest_restaurant_index])  # rezerwacja miejsca

        self.loss = sum(distances)  # funkcja straty to po prostu suma odległości

    def __find_nearest_restaurant(self, order: Prodict, restaurants: list) -> (int, int):
        nearest_restaurant_index = 0
        min_distance = 99999999999 # duża wartość aby można wejść do ifa za pierwszym razem
        for i, rest in enumerate(restaurants):
            distance = check_distance(order.user_location, rest.location)

            if distance < min_distance:
                _, nr_of_available_tables = self.__check_available_tables(rest)

                # jeśli nie ma wolnych miejsc w najbliższej to znaczy że rozwiązanie nie będzie optymalne i trzeba
                # odpalić algorytm
                if not nr_of_available_tables:
                    self.isOptimal = False
                else:
                    nearest_restaurant_index = i
                    min_distance = distance

        return min_distance, nearest_restaurant_index

    def __check_available_tables(self, rest: Prodict) -> tuple:
        # potrzebujemy klucza do słownika aby potem go modyfikować
        key, reserved_tables = self.__match_reservation_by_restaurant_id(rest.id)
        nr_of_all_tables = rest.nr_of_tables
        nr_of_reserved_tables = reserved_tables.total_nr_of_reservations
        nr_of_available_tables = nr_of_all_tables - nr_of_reserved_tables
        return key, nr_of_available_tables

    # wybieramy restauracje po id ze słownika
    def __match_reservation_by_restaurant_id(self, restaurant_id: int) -> tuple:
        # potrzebujemy klucza do słownika aby potem go modyfikować
        for key, reservation in enumerate(self.__reservations):
            if reservation.restaurant_id == restaurant_id:
                return key, reservation

    def __reserve_table(self, restaurant: Prodict):
        key, reserved_tables = self.__match_reservation_by_restaurant_id(restaurant.id)
        # TODO: if there will be posibility to reserve more than 1 table then change condition and increment value
        reserved_tables.total_nr_of_reservations += 1
        self.__reservations[key] = reserved_tables  # update miejsc w słowniku

    def start(self, start_temp=5000, cooling_factor=0.85, iterations=200):
        if self.isOptimal:
            print("Queue is optimal there's no need to run algorithm")
            return self.loss

        temp = start_temp
        queue = copy_queue(self.user_orders_queue)
        queue_length = len(queue.queue)
        # wycofujemy wcześniejsze rezerwacje z inita bo będziemy zmieniać kolejność
        self.__reset_reservations()

        for i in range(iterations):
            prevoius_queue = copy_queue(queue)
            previous_loss = self.loss

            i1, i2 = get_indexes_to_swap(queue_length)  # wybór elementów do zamiany
            queue = swap_elements(queue, i1, i2)

            self.assign_restaurants(queue)  # przypisanie według nowej kolejki

            # algorytm - losowanie prawdopodobieństa odrzucenia wyniku gdy ten jest gorszy - odwrócona logika algorytmu
            # efekt ten sam
            if self.loss < self.minimal_loss:
                self.minimal_loss = self.loss
                self.best_queue = copy_queue(queue)

            if previous_loss < self.loss:
                accept_probability = exp((previous_loss - self.loss) / temp)
                if random.random() < accept_probability:
                    queue = prevoius_queue

            temp *= cooling_factor
            self.__reset_reservations()  # zerowanie rezerwacji po działanu algorytmu
        self.user_orders_queue = queue  # kolejka optymalizowana
        return self.loss

    def __reset_reservations(self):
        # reset polega na ponownym zaczytaniu kolejki z bazy.
        self.__reservations = convert_reservations_to_dict()

    def get_queue_by_user_id(self):
        return [order.user_id for _, order in self.user_orders_queue.queue]

    def get_best_solution_by_user_id(self):
        return [order.user_id for _, order in self.best_queue.queue]


if __name__ == '__main__':
    from pprint import pprint
    alg = Algorithm()
    alg.assign_restaurants(alg.user_orders_queue)
    # print_reservations(alg.__reservations)
    print(f"Initial loss: {alg.loss}, is optimal: {alg.isOptimal}")
    print(f"order {alg.get_queue_by_user_id()}")
    alg.start()
    print(f"end loss: {alg.loss}, minimal_loss {alg.minimal_loss}")
    print(f"end order {alg.get_queue_by_user_id()}")
    print(f"best order {alg.get_best_solution_by_user_id()}")
