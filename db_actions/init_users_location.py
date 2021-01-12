import random

from controllers.db_connection import get_session
from db_objects.objects import Location, User
import requests
import json


def get_location(city: str, street: str):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + street + ',' + city + \
          '+PL&key=AIzaSyCWdxt26U61v0z6X_1oRMoRO_42Fxz3hFo'
    req = requests.get(url)
    parsed = json.loads(req.text)
    results = parsed["results"]
    geometry = results[0]['geometry']
    location = geometry['location']
    lat, lng = location.values()
    return Location(latitude=lat, longitude=lng)


streets = """Adama Mickiewicza Wrocław
Al. Lipowa Wrocław
Al. Prezydenta Ryszarda Kaczorowskiego Wrocław
Alojzego Majchra Wrocław
Andrzeja Kmicica Wrocław
Bednarska Wrocław
Białogardzka Wrocław
Bierdzańska Wrocław
Bohdana Zaleskiego Wrocław
Bolesławiecka Wrocław
Brzezińska Wrocław
Bydgoska Wrocław
Bytomska Wrocław
Chojnowska Wrocław
Chorzowska Wrocław
Ciechanowska Wrocław
Gerberowa Wrocław
Głośna Wrocław
Ignacego Chrzanowskiego Wrocław
Jagniątkowska Wrocław
Jana Kilińskiego Wrocław
Januszowicka Wrocław
Jerzego Kukuczki Wrocław
Józefa Gielniaka Wrocław
Kamiennogórska Wrocław
kard. Augusta Hlonda Wrocław
Kolendrowa Wrocław
Kontradmirała Stefana Frankowskiego Wrocław
Korzeńska Wrocław
Kozia Wrocław
Kręta Wrocław
Krótka Wrocław
Krzyżanowicka Wrocław
ks. Piotra Wawrzyniaka Wrocław
Kukułcza Wrocław
Las Kuźnicki Wrocław
Las Pilczycki Wrocław
Lawendowa Wrocław
Limanowska Wrocław
Ludwika Rydygiera Wrocław
Macieja Rataja Wrocław
Mączna Wrocław
Malborska Wrocław
Mariana Haisiga Wrocław
Marsowa Wrocław
Mazowiecka Wrocław
Mewia Wrocław
Miodowa Wrocław
Modrzewiowa Wrocław
Monopolowa Wrocław
Most Partynicki Wrocław
Most Sołtysowicki Wrocław
Mosty Średzkie Wrocław
Nefrytowa Wrocław
Niepierzyńska Wrocław
Pakosławska Wrocław
Papiernicza Wrocław
Park Kleciński Wrocław
Plac Tadeusza Kościuszki Wrocław
Plac Westerplatte Wrocław
"""
# streets = streets.split('\n')
# streets = [name.split() for name in streets]
# streets = [street[:-1] for street in streets if len(street) == 2]
# streets = streets[:30]

session = get_session()

# for street_list in streets:
#     street_name = street_list[0]
#     location = get_location('wrocław', street_name)
#     session.add(location)

upper_left = 51.12494279251575, 17.011988909212764
bottom_right = 51.090951, 17.068490
upper_right = 51.121032728830166, 17.097620980657062
bottom_left = 51.101113224995665, 16.99674451866926

users = session.query(User).order_by(User.id).all()
iterations = len(users)

for i in range(iterations):
    lat = random.uniform(bottom_right[0], upper_left[0])
    lng = random.uniform(bottom_left[1], upper_right[1])
    loc = Location(latitude=lat, longitude=lng)
    session.add(loc)

session.commit()


