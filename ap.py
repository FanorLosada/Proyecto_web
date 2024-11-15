import matplotlib
matplotlib.use('Agg')  # Configura Matplotlib para no usar Tkinter

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import os

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Puede cambiarla por MySQL, PostgreSQL, etc.
db = SQLAlchemy(app)

# Modelo de la base de datos para los mensajes
class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)

# Ruta para la página principal (index)
@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/apartamentos')
def apartamentos():
    return render_template('apartamentos.html')

@app.route('/ejecutiva')
def ejecutiva():
    return render_template('ejecutiva.html')

@app.route('/habitaciones')
def habitaciones():
    return render_template('habitaciones.html')

@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/mision')
def mision():
    return render_template('mision.html')

@app.route('/multiple')
def multiple():
    return render_template('multiple.html')

@app.route('/oficina')
def oficina():
    return render_template('oficina.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')  

@app.route('/restaurante')
def restaurante():
    return render_template('restaurante.html')  

@app.route('/suit')
def suit():
    return render_template('suit.html')  

@app.route('/vision')
def vision():
    return render_template('vision.html')                

@app.route('/micuenta', methods=['GET', 'POST'])
def micuenta():
    if request.method == 'POST':
        # Recibir datos del formulario
        nombre = request.form['nombre']
        mensaje = request.form['mensaje']

        # Guardar el mensaje en la base de datos
        nuevo_mensaje = Mensaje(nombre=nombre, mensaje=mensaje)
        db.session.add(nuevo_mensaje)
        db.session.commit()

        return redirect(url_for('micuenta'))
    return render_template('micuenta.html')

# Ejecutar la creación de la tabla dentro del contexto de la aplicación
if __name__ == '__main__':
    with app.app_context():  # Crear el contexto de la aplicación
        db.create_all()      # Crear todas las tablas
    app.run(debug=True)
