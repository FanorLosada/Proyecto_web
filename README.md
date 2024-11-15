# Proyecto_web

# Documentación de la Aplicación Flask

## Descripción General
Esta es una aplicación web desarrollada en Flask que ofrece las siguientes funcionalidades:

- Gestión de usuarios mediante una base de datos SQLite.
- Generación de gráficos de cancelaciones usando Matplotlib y Pandas.
- Navegación a través de varias páginas estáticas (informativas).

## Requisitos Previos
Para ejecutar la aplicación, es necesario tener instalados los siguientes paquetes:

- Flask para manejar el servidor web y el enrutamiento.
- SQLAlchemy para interactuar con la base de datos SQLite.
- Matplotlib para la generación de gráficos.
- Pandas para la manipulación de datos.

Se recomienda instalar estos paquetes mediante pip:

- pip install flask 
- pip install flask_sqlalchemy 
- pip install matplotlib 
- pip install pandas

Flask: Permite manejar el servidor web, el enrutamiento de URL, y las plantillas HTML, entre otras funciones

Flask-SQLAlchemy: Simplifica el uso de bases de datos relacionales mediante SQLAlchemy

Matplotlib: Configura Matplotlib para no utilizar interfaces gráficas (útil en servidores).

Flask: Inicia la aplicación Flask.

Pandas: Proporciona estructuras de datos flexibles y eficientes, como DataFrames, que son fundamentales para trabajar con datos tabulares y series temporales

##Estructura del Código

El código se divide en secciones que configuran la base de datos, definen rutas para las páginas web, y crean gráficos para visualización.


	import matplotlib
	matplotlib.use('Agg')  # Configura Matplotlib para no usar Tkinter

	from flask import Flask, render_template, request, redirect, url_for
	from flask_sqlalchemy import SQLAlchemy
	import matplotlib.pyplot as plt
	import pandas as pd
	import os

	app = Flask(__name__)

	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
	db = SQLAlchemy(app)


##Clase Usuario
Define el modelo de datos para los usuarios registrados en la aplicación.


	class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), nullable=False)
    contrasena = db.Column(db.String(100), nullable=False)

- id: Clave primaria, identificador único para cada usuario.
- usuario: Nombre de usuario del cliente, requerido.
- contrasena: Contraseña del usuario, requerida.

##Ruta Principal 

	@app.route('/')
	def index():
    	imagen_path = grafico()  # Genera el gráfico y obtiene la ruta de la 				imagen
    	return render_template('index.html', imagen_path=imagen_path)

- Ruta: Página principal de la aplicación.
- Función: Llama a grafico() para generar un gráfico y muestra index.html con la ruta del gráfico como parámetro.

##Ruta /grafico

	@app.route('/grafico')
	def grafico_view():
    imagen_path = grafico()
    return render_template('grafico.html', imagen_path=imagen_path)
Ruta: Página que muestra el gráfico de cancelaciones.
Función: Llama a grafico() y pasa la ruta de la imagen a grafico.html.

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

Descripción: Lee los datos del archivo HotelLimpiado.csv, genera un gráfico de torta de cancelaciones y guarda la imagen en la carpeta static/imagenes.
Parámetros: Ninguno.
Retorno: Devuelve la ruta de la imagen guardada.
Rutas Adicionales

	@app.route('/apartamentos')
	def apartamentos():
    return render_template('apartamentos.html')


## Rutas para el ingreso de usuario

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

Método: Permite GET y POST.
POST: Recibe datos del formulario (usuario y contraseña), crea un nuevo Usuario y lo guarda en la base de datos.
GET: Muestra el formulario micuenta.html.

##Inicialización y Ejecución del Servidor

	if __name__ == '__main__':
    with app.app_context():  # Crear el contexto de la aplicación
        db.create_all()      # Crear todas las tablas
    app.run(debug=True)

Descripción: Crea todas las tablas necesarias en la base de datos y ejecuta la aplicación en modo debug.

##Notas Adicionales

- Archivos Estáticos: Las imágenes y archivos CSS estan en la carpeta static.

- Plantillas HTML: Las vistas de la aplicación utilizan render_template para mostrar los archivos HTML ubicados en la carpeta templates.
