# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QLabel, QLineEdit, QComboBox, QListWidget, QPushButton, \
    QGridLayout
import sys
import requests

from controllers.db_connection import get_session
from db_objects.objects import Restaurant, Meal, ReservedTables


App = QApplication(sys.argv)
window = QWidget()


def clear_menu():
    combo_box_menu.clear()


def make_order():
    row = listWidget.item(listWidget.currentRow()).text()
    rowName = row.split("\n")
    rowNameNumber = rowName[0]
    restaurant_name = rowNameNumber[7:]

    if restaurant_name in listWidget.item(listWidget.currentRow()).text():
        session = get_session()
        restaurant = session.query(Restaurant).filter(Restaurant.name == restaurant_name).one()
        reserved_tables = session.query(ReservedTables)\
                                 .filter(ReservedTables.restaurant.has(name=restaurant_name)).one()

        nr_of_all_tables = restaurant.nr_of_tables
        nr_of_reserved_tables = reserved_tables.total_nr_of_reservations

        if nr_of_all_tables - nr_of_reserved_tables > 0:
            reserved_tables.total_nr_of_reservations += 1
            session.commit()

        # latRest = restaurant.location.latitude
        # lngRest = restaurant.location.longitude
        #
        # cur.execute('SELECT SzerokoscGeo, DlugoscGeo from ZAMOWIENIE WHERE ID=?', (str(1)))
        # varUser = cur.fetchone()
        # latUser = varUser[0]
        # lngUser = varUser[1]
        #
        # distance = sqrt((float(latRest) - float(latUser)) ** 2 + (
        #         cos((float(latUser) * pi) / 180) * (float(lngRest) - float(lngUser))) ** 2) * (40075.704 / 360)
        #
        # con.commit()

        QMessageBox.information(window, "Informacja o rezerwacji", "Zarezerwowano" + "\n" + listWidget.item(
            listWidget.currentRow()).text() + "\n" + "Odległośc do restauracji: " + "ToDo"  # str(round(distance, 2))
                                + " km")


def show_restaurants():
    listWidget.clear()
    content = str(combo_box.currentText())
    session = get_session()

    restaurants = session.query(Restaurant).filter(Restaurant.kitchen_type.has(type=content)).all()
    for rest in restaurants:
        reserved_tables = session.query(ReservedTables).filter(ReservedTables.restaurant.has(name=rest.name)).one()

        nr_of_all_tables = rest.nr_of_tables
        nr_of_reserved_tables = reserved_tables.total_nr_of_reservations

        listWidget.addItem(f'Nazwa: {rest.name}\n' +
                           f'Ocena: {str(rest.rate)}\n' +
                           f'Ilość wolnych stolików: {str(nr_of_all_tables - nr_of_reserved_tables)}')


def find():
    # town = window.lineTown.text()
    # street = window.lineStreet.text()
    #
    # url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + street + ',' + town + '+PL&key=AIzaSyCWdxt26U61v0z6X_1oRMoRO_42Fxz3hFo'
    # req = requests.get(url)
    # parsed = json.loads(req.text)
    # results = parsed["results"]
    #
    # for par in results:
    #     geometry = par['geometry']
    #     location = geometry['location']
    #     lat = location['lat']
    #     lng = location['lng']
    #
    # global id

    nadawca = window.sender()
    content = str(combo_box.currentText())
    if nadawca.text() == "Show":
        if content == " ":
            combo_box_menu.clear()
            listWidget.clear()

        session = get_session()
        menu = session.query(Meal).filter(Meal.kitchen_type.has(type=content)).all()

        for meal in menu:
            # if content in rest["kitchens"]:
            # menu = session.query(Meal).filter_by()
            combo_box_menu.addItem(meal.meal)

        # if content != " ":
        #     id += 1
        #     try:
        #         cur.execute('INSERT INTO ZAMOWIENIE VALUES(?, ?, ?, ?, ?);', (id, content, lat, lng, 1))
        #     except sqlite3.IntegrityError:
        #         cur.execute('DELETE FROM ZAMOWIENIE')
        #
        #     con.commit()

        ukladT.addWidget(label_menu, 6, 0)
        ukladT.addWidget(combo_box_menu, 7, 0)

        combo_box.activated.connect(clear_menu)
        combo_box_menu.activated.connect(show_restaurants)


label_kitchens = QLabel("Kuchnia: ")
label_street = QLabel("Ulica: ")
window.lineStreet = QLineEdit()
label_town = QLabel("Miasto: ")
window.lineTown = QLineEdit()
label_menu = QLabel("Dania: ")
label_rest = QLabel("Restauracje: ")
combo_box = QComboBox()
combo_box_menu = QComboBox()
listWidget = QListWidget()
combo_box.setGeometry(20, 15, 120, 30)
combo_box_menu.setGeometry(20, 15, 120, 30)
geek_list = [" ", "Kebab", "Chińska", "Polska", "Sushi", "Indyjska", "Pizza", "Burger", "Włoska", "Tajska"]
combo_box.addItems(geek_list)
listWidget.resize(30, 12)
button = QPushButton("Show")
button.setStyleSheet("background-color: lightblue")

ukladT = QGridLayout()
ukladT.addWidget(label_town, 0, 0)
ukladT.addWidget(window.lineTown, 1, 0)
ukladT.addWidget(label_street, 2, 0)
ukladT.addWidget(window.lineStreet, 3, 0)
ukladT.addWidget(label_kitchens, 4, 0)
ukladT.addWidget(combo_box, 5, 0)
ukladT.addWidget(button, 5, 5)
ukladT.addWidget(label_rest, 8, 0)
ukladT.addWidget(listWidget, 9, 0)

listWidget.itemDoubleClicked.connect(make_order)
button.clicked.connect(find)

# Only for debug
window.lineTown.setText('Wrocław')
window.lineStreet.setText('Gersona')

window.setLayout(ukladT)
window.setGeometry(30, 30, 600, 400)
window.setWindowTitle("Apka Python")

window.show()
sys.exit(App.exec_())
