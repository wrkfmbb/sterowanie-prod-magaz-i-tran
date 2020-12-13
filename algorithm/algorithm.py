from algorithm_utils import init_queue, preview_queue, check_distance
from controllers.RestaurantController import RestaurantController

user_reservation_queue = init_queue()
preview_queue(user_reservation_queue)

# Example of calculating distance from queue location and available restaurants location
_, order = user_reservation_queue.get()
restaurants = RestaurantController.get_matched_by_kitchen_type_id(order.kitchen_type_id)

for restaurant in restaurants:
    print(check_distance(order.user_location, restaurant.location))
# end of example :)

