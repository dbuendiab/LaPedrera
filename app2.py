import os
from flask import Flask, render_template
from flask_scss import Scss

import db, controls

app = Flask(__name__)
app.debug =True
Scss(app, static_dir='static', asset_dir='assets')

import db, controls

@app.route('/') 
def inici():
    name = "prototip dissenyat per Diego Buendía"
    return render_template('inici.html', name=name)

@app.route('/llista_espais_simples')
def llista_espais_simples():
    return render_template('lista_es.html', lista_es=db.get_es())

@app.route('/llista_espais_complexos')
def llista_espais_complexos():
    return render_template('lista_ec.html', lista_es=db.get_ec())
    
@app.route('/creacio_activitats')
def creacio_activitats():
    return render_template('activitats.html', select=controls.espais_complexos('select'))
    
@app.route('/pba')
def pba():
    return(render_template('pba.html'))

if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)
    
