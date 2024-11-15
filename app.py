import matplotlib
matplotlib.use('Agg')  # Configura Matplotlib para no usar Tkinter

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import pandas as pd
import os

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Modelo de la base de datos para los mensajes
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), nullable=False)
    contrasena = db.Column(db.String(100), nullable=False)

# Ruta para la página principal (index)
@app.route('/')
def index():
    imagen_path = grafico()  # Genera el gráfico y obtiene la ruta de la imagen
    return render_template('index.html', imagen_path=imagen_path)

# Ruta de ejemplo para mostrar el gráfico de cancelaciones
@app.route('/grafico')
def grafico_view():
    imagen_path = grafico()
    return render_template('grafico.html', imagen_path=imagen_path)

# Función para crear el gráfico y devolver la ruta de la imagen
def grafico():
    # Leer los datos desde el archivo CSV
    df = pd.read_csv('HotelLimpiado.csv')

    # Crear el gráfico de torta de cancelaciones
    plt.figure(figsize=(8, 8))
    
    # Verificar si existe la columna 'is_canceled'
    if 'is_canceled' in df.columns:
        cancelaciones = df['is_canceled'].value_counts()
        labels = ['No Canceladas', 'Canceladas']
    else:
        # En caso de no tener 'is_canceled', usar 'no_of_previous_cancellations' > 0 como cancelación
        df['Cancelada'] = df['no_of_previous_cancellations'] > 0
        cancelaciones = df['Cancelada'].value_counts()
        labels = ['No Canceladas', 'Canceladas']
    
    # Crear gráfico de torta
    plt.pie(cancelaciones, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#4169E1', '#DC143C'])
    plt.title('Análisis de Cancelaciones')
    
    # Guardar el gráfico en la carpeta static/imagenes
    imagen_path = os.path.join('static/imagenes', 'grafico_cancelaciones_torta.png')
    plt.savefig(imagen_path)
    plt.close()  # Cierra la figura para liberar memoria

    return url_for('static', filename='imagenes/grafico_cancelaciones_torta.png')

# Rutas adicionales de la aplicación
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
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        # Guardar el nombre de usuario en la base de datos
        nuevo_usuario = Usuario(usuario=usuario, contrasena=contrasena)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for('micuenta'))
    return render_template('micuenta.html')

# Ejecutar la creación de la tabla dentro del contexto de la aplicación
if __name__ == '__main__':
    with app.app_context():  # Crear el contexto de la aplicación
        db.create_all()      # Crear todas las tablas
    app.run(debug=True)
