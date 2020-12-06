# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from math import *
import sys
import requests
import json
import random
import sqlite3

con = sqlite3.connect('database/KLIENT_SERW.db')
con.row_factory = sqlite3.Row
cur = con.cursor()

id = 0

with open('data/restaurants.json', 'r', encoding='utf-8') as json_file:
    restaurants = json.load(json_file)

with open('data/listOfRestaurants3.json', 'r', encoding='utf-8') as json_file:
    restaurantsYelp = json.load(json_file)

App = QApplication(sys.argv)
window = QWidget()


def clearMenu():
    combo_box_menu.clear()


def Clicked():
    row = listWidget.item(listWidget.currentRow()).text()
    rowName = row.split("\n")
    rowNameNumber = rowName[0]
    restName = rowNameNumber[7:]

    if restName in listWidget.item(listWidget.currentRow()).text():
        cur.execute('SELECT IloscStol,SzerokoscGeo, DlugoscGeo from REST WHERE Nazwa=?', (restName,))

        varRest = cur.fetchone()
        stolik = varRest[0]
        latRest = varRest[1]

        lngRest = varRest[2]
        newStolik = stolik - 1
        cur.execute('UPDATE REST SET IloscStol=? WHERE NAZWA=?', (int(newStolik), restName))

        cur.execute('SELECT SzerokoscGeo, DlugoscGeo from ZAMOWIENIE WHERE ID=?', (str(1)))
        varUser = cur.fetchone()
        latUser = varUser[0]
        lngUser = varUser[1]

        distance = sqrt((float(latRest) - float(latUser)) ** 2 + (
                    cos((float(latUser) * pi) / 180) * (float(lngRest) - float(lngUser))) ** 2) * (40075.704 / 360)

        con.commit()

        QMessageBox.information(window, "Informacja o rezerwacji", "Zarezerwowano" + "\n" + listWidget.item(
            listWidget.currentRow()).text() + "\n" + "Odległośc do restauracji: " + str(round(distance, 2)) + " km")


def RandRest(tmpList):
    while len(tmpList) < 27:
        NumberR = random.randint(1, 27)
        if NumberR not in tmpList:
            tmpList.append(NumberR)
    return tmpList


def showRest():
    listWidget.clear()
    content = str(combo_box.currentText())
    cur.execute('SELECT NAZWA,Ocena,IloscStol FROM REST WHERE Kuchnia=?', (content,))
    restDatabase = cur.fetchall()
    for rest in restDatabase:
        listWidget.addItem(
            "Nazwa: " + rest['NAZWA'] + "\n" + "Ocena: " + str(rest['Ocena']) + "\n" + "Ilość wolnych stolików: " + str(
                rest['IloscStol']))


def Trigger():
    listOfRandnumber = []
    RandRest(listOfRandnumber)
    for i in range(len(listOfRandnumber)):
        for rest in restaurantsYelp:
            if listOfRandnumber[i] == rest["Number"]:

                if str(rest["Price"]) == "0":
                    price = random.randint(1, 7)
                elif str(rest["Price"]) == "$":
                    price = random.randint(7, 12)
                elif str(rest["Price"]) == "$$":
                    price = random.randint(12, 17)
                elif str(rest["Price"]) == "$$$":
                    price = random.randint(17, 22)

                cur.execute('INSERT INTO REST VALUES(?, ?, ?, ?, ?, ?);', (
                rest["Name"], str(rest["Rating"]), str(rest["Latitude"]), str(rest["Longitude"]), str(price)), "Kebab")
    con.commit()


def find():
    town = window.lineTown.text()
    street = window.lineStreet.text()

    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + street + ',' + town + '+PL&key=AIzaSyCWdxt26U61v0z6X_1oRMoRO_42Fxz3hFo'
    req = requests.get(url)
    parsed = json.loads(req.text)
    results = parsed["results"]

    for par in results:
        geometry = par['geometry']
        location = geometry['location']
        lat = location['lat']
        lng = location['lng']

    global id

    nadawca = window.sender()
    content = str(combo_box.currentText())
    if nadawca.text() == "Show":
        if content == " ":
            combo_box_menu.clear()
            listWidget.clear()

        # contents = ["Kebab", "Chińska", "Polska", "Sushi", "Indyjska", "Pizza", "Burger", "Włoska", "Tajska"]

        # if content in contents:
        for rest in restaurants:
            if content in rest["kitchens"]:
                combo_box_menu.addItems(rest["menu"])

        if content != " ":
            id += 1
            try:
                cur.execute('INSERT INTO ZAMOWIENIE VALUES(?, ?, ?, ?, ?);', (id, content, lat, lng, 1))
            except sqlite3.IntegrityError:
                cur.execute('DELETE FROM ZAMOWIENIE')

            con.commit()

        ukladT.addWidget(label_menu, 6, 0)
        ukladT.addWidget(combo_box_menu, 7, 0)

        combo_box.activated.connect(clearMenu)
        combo_box_menu.activated.connect(showRest)


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

listWidget.itemDoubleClicked.connect(Clicked)
button.clicked.connect(find)

# Only for debug
window.lineTown.setText('Wrocław')
window.lineStreet.setText('Gersona')

window.setLayout(ukladT)
window.setGeometry(30, 30, 600, 400)
window.setWindowTitle("Apka Python")

window.show()
sys.exit(App.exec_())
