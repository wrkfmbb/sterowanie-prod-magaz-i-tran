import json

with open('restaurants.json', 'r', encoding='utf-8') as json_data_file:
    data = json_data_file.read()

restaurants_dirty_info = json.loads(data)
restaurants_clean_info = []

for restaurant in restaurants_dirty_info:
    restaurant_clean = {}
    restaurant_clean['restaurant_name'] = restaurant['restaurant_name']
    restaurant_clean['kitchens'] = restaurant['kitchens']
    menu = restaurant['menu']
    clean_menu = []
    for dish in menu:
        if not dish.lower().startswith('każda '):
            clean_menu.append(dish)
    restaurant_clean['menu'] = clean_menu
    restaurants_clean_info.append(restaurant_clean)
    
with open('restaurants.json', 'w', encoding='utf-8') as json_file:
    json.dump(restaurants_clean_info, json_file, indent=4, sort_keys=True, ensure_ascii=False)
