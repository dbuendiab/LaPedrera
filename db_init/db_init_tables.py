import sys
import pymongo

cli = pymongo.MongoClient()
db = cli.pedrera
c_es = db.espais_simples
c_ec = db.espais_complexos



if c_es.count() > 0:
    yn = input("N'hi ha files en col·leccions espais_simples/espais_complexos. Vols esborrar-la? (s/n): ")
    if yn != 's':
        print('Operació cancel·lada')
        sys.exit()
    c_es.drop()
    c_ec.drop()
        
print("Omplint col·lecció 'espais_simples'...")

espais_simples =[
    {'id': 1, 'pis': 7, 'nom': 'Pati C', 'observacions': ''},
    {'id': 2, 'pis': 7, 'nom': 'Pati D', 'observacions': ''},
    {'id': 3, 'pis': 7, 'nom': 'Pati E', 'observacions': ''},
    {'id': 4, 'pis': 7, 'nom': 'Pati F', 'observacions': ''},
    {'id': 5, 'pis': 6, 'nom': 'Terrat', 'observacions': ''},
    {'id': 6, 'pis': 5, 'nom': 'Golfes', 'observacions': ''},
    {'id': 7, 'pis': 4, 'nom': 'Pis golfes', 'observacions': ''},
    {'id': 8, 'pis': 3, 'nom': '2on.pis (CER)', 'observacions': ''},
    {'id': 9, 'pis': 2, 'nom': 'Sala Exposició', 'observacions': ''},
    {'id': 10, 'pis': 1, 'nom': 'Aules Entresòl', 'observacions': ''},
    {'id': 11, 'pis': 1, 'nom': '4 Gats', 'observacions': ''},
    {'id': 12, 'pis': 1, 'nom': 'Aula 3', 'observacions': ''},
    {'id': 13, 'pis': 0, 'nom': 'Pati Provença', 'observacions': ''},
    {'id': 14, 'pis': 0, 'nom': 'Pati Passeig Gràcia', 'observacions': ''},
    {'id': 15, 'pis': -1, 'nom': 'Auditori', 'observacions': ''},
    {'id': 16, 'pis': -1, 'nom': 'Sala Gaudí', 'observacions': ''}
]
 
resultat = c_es.insert_many(espais_simples)

print("%s espais simples insertats" % len(resultat.inserted_ids))

print("Omplint col·lecció 'espais_complexos'...")

espais_complexos = [
    {'id': 1, 'nom': 'Patis C-D i E-F', 'color': '#FFFFFF', 'espais': [1, 2, 3, 4], 'observacions': ''},
    {'id': 2, 'nom': 'Terrat', 'color': '#FFCC00', 'espais': [5], 'observacions': ''},
    {'id': 3, 'nom': 'Golfes i pis', 'color': '#FFCC00', 'espais': [6, 7], 'observacions': ''},
    {'id': 4, 'nom': '2on.pis (CER)', 'color': '#00B050', 'espais': [8], 'observacions': ''},
    {'id': 5, 'nom': 'Sala Exposició', 'color': '#339966', 'espais': [9], 'observacions': ''},
    {'id': 6, 'nom': 'Aules Entresòl', 'color': '#9999FF', 'espais': [10], 'observacions': ''},
    {'id': 7, 'nom': '4 Gats', 'color': '#FFFFFF', 'espais': [11], 'observacions': ''},
    {'id': 8, 'nom': 'Aules Entresòl i 4 Gats', 'color': '#FF8585', 'espais': [10, 11], 'observacions': ''},
    {'id': 9, 'nom': '4 Gats i Aula 3', 'color': '#FFFFFF', 'espais': [11, 12], 'observacions': ''},
    {'id': 10, 'nom': 'Pati Provença', 'color': '#FFCC00', 'espais': [13], 'observacions': ''},
    {'id': 11, 'nom': 'Pati Passeig Gràcia', 'color': '#FFCC00', 'espais': [14], 'observacions': ''},
    {'id': 12, 'nom': 'Auditori', 'color': '#FFFFFF', 'espais': [15], 'observacions': ''},
    {'id': 13, 'nom': 'Sala Gaudí', 'color': '#FFFFFF', 'espais': [16], 'observacions': ''}
]

resultat = c_ec.insert_many(espais_complexos)

print("%s espais complexos insertats" % len(resultat.inserted_ids))
