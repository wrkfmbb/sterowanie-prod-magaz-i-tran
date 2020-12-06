import requests
import json
import pprint



api_key='TVNUTyNaJe4xhgPiXCklyrOafio22opGozY4I7gJVP0jih5_YxysmZd-x3i1SU8zP2d3dyKugVTHOhEQxbeWlAOQvMKIKHqEMEtdXAFTkBKAoOrDog0Gt5ZLcCaGX3Yx'
headers = {'Authorization': 'Bearer %s' % api_key}


url='https://api.yelp.com/v3/businesses/search'
#params={'term':'restaurants', 'location':'Wrocław', 'limit':50}
params={'latitude':51,'longitude':17,'radius':20000, 'limit':50}


req = requests.get(url, params=params, headers=headers)


parsed = json.loads(req.text)
print(json.dumps(parsed, indent=4))
businesses=parsed["businesses"]
Name={}
NameL={}

for business in businesses:
    LOCATION=business["coordinates"]
    NameL[business["name"]]={'Rating':business.setdefault('rating','0'),'Price':business.setdefault('price','0'),'Adress': " ".join(business["location"]["display_address"]),
                 'Latitude':LOCATION.setdefault('latitude','0'),'Longitude':LOCATION.setdefault('longitude','0'),'Phone':business.setdefault('display_phone','0')}
    Name['Name']=NameL

with open('listOfRestaurants', 'w', encoding='utf8') as json_file:
    json.dump(Name, json_file, ensure_ascii=False,indent=4)


pprint.pprint(Name)
