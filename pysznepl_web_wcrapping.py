from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import requests
import time
from pprint import pprint


def get_restaurant_info(restaurant):
    rest = {}
    rest['kitchens'] = restaurant.find('div', class_='kitchens').text.strip()
    restaurant_info = restaurant.find('a', class_='restaurantname')
    rest['dish_name'] = restaurant_info.text.strip()
    restaurant_menu_postlink = restaurant_info['href']
    rest['menu_link']= f'https://www.pyszne.pl{restaurant_menu_postlink}'
    return rest

def get_dishes_list(menu_soup):
    body = menu_soup.find('body')
    section = body.find('section', attrs={"data-qa": "menu-list"})
    dishes_names_html = section.find_all('div', attrs={'data-qa': 'text'})
    dishes_names = []
    for dish_name in dishes_names_html:
        name = dish_name.text.strip()
        if len(name) > 10 and name not in dishes_names:
            dishes_names.append(name)
    return dishes_names

options = Options()
options.binary_location = r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe'
# browser = webdriver.Chrome(options=options, executable_path=r'D:\Inne\Materialy\Programy\AllegroRamChecker\chromedriver'
#                                                             r'\chromedriver.exe')
# browser.get('https://www.pyszne.pl/restauracja-wroclaw-wroclaw-krzyki-52-141')
# html = browser.execute_script('return document.documentElement.outerHTML')
# soup = BeautifulSoup(html, 'lxml')
# with open('pyszne.html', 'w', encoding='utf-8') as file:
#     file.write(str(soup))
with open('pyszne.html', 'r', encoding='utf-8') as file:
    html = file.read()

soup = BeautifulSoup(html, 'lxml')
restaurants_list = soup.find('div', class_='js-restaurant-list-open')
restaurants = []
browser = webdriver.Chrome(options=options, executable_path=r'D:\Inne\Materialy\Programy\AllegroRamChecker\chromedriver'
                                                            r'\chromedriver.exe')
for restaurant in restaurants_list.find_all('div', class_='restaurant'):
    restaurant_info = get_restaurant_info(restaurant)
    browser.get(restaurant_info['menu_link'])
    time.sleep(3)
    menu_html = browser.execute_script('return document.documentElement.outerHTML')
    menu_soup = BeautifulSoup(menu_html, 'lxml')
    # with open('menu.html', 'r', encoding='utf-8') as file:
    #     menu_html = file.read()
    # menu_soup = BeautifulSoup(menu_html, 'lxml')
    try:
        restaurant_info['menu'] = get_dishes_list(menu_soup)
    except AttributeError:
        print('Error')
    restaurants.append(restaurant_info)
    with open("restaurants.json", "w") as outfile:
        json.dump(restaurants, outfile)

# pprint(dishes_names)
# time.sleep(1000)
