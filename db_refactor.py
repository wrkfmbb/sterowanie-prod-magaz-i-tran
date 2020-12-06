import sqlite3

con = sqlite3.connect('database/KLIENT_SERW.db')
con.row_factory = sqlite3.Row
cur = con.cursor()

# meals = ['makaron tagliatelle z dorszem, sosem winnym z szalotką i śmietaną, bulionem, Pecorino Romano, natką pietruszki i gremolatą', 'makaron fusilli z wieprzowiną, wołowiną, pomidorami pelati, warzywami korzeniowymi, parmezanem, natką pietruszki i Pecorino Romano', 'makaron linguine z guanciale, pancettą, żółtkiem, Pecorino Romano, Parmigiano Reggiano, czarnym pieprzem i śmietanką', 'makaron linguine z oliwą, czosnkiem, pietruszką, chilli i Grana Padano', 'makaron fusilli z salsiccią, friarielli, pomidorami pelati i czosnkiem', 'makaron fusilli z salami z truflą, gorgonzolą, czosnkiem i śmietaną', 'makaron fusilli z kremem truflowym, pieczarkami, śmietaną i natką pietruszki', 'makaron linguine z krewetkami, białym winem, śmietaną, chilli, czosnkiem, szpinakiem i Pecorino Romano', 'makaron tagliatelle z sosem grzybowym, wołowiną i gremolatą', "makaron fusilli z n'dują, cheddarem, jalapeno, pomidorami pelati i bakłażanem", 'makaron fusilli z kurczakiem, suszonymi pomidorami, pieczarkami, szpinakiem, śmietaną, gorgonzolą i mozzarellą']
#
# for meal in meals:
#     cur.execute('INSERT INTO meals(meal, kitchen_type_id) VALUES(?, ?);', (meal, 9))
# con.commit()
# types = ['Kebab',
# 'Chińska',
# 'Polska',
# 'Sushi',
# 'Tajska',
# 'Indyjska',
# 'Pizza',
# 'Burger',
# 'Włoska',
# ]
# for i, name in enumerate(types):
#     cur.execute('SELECT nazwa, ocena, ilosc_stolikow, location_id from REST WHERE kuchnia=?', (name,))
#     varRest = cur.fetchall()
#     for restaurant in varRest:
#         cur.execute('INSERT INTO restaurants(name, rate, nr_of_tables, kitchen_type_id, location_id) VALUES(?, ?, ?, ?, ?);',
#                 (restaurant[0], restaurant[1], restaurant[2], i+1, restaurant[3]))
# con.commit()