from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, FoodStall
from . import db

# Definimos el blueprint para las rutas
main = Blueprint('main', __name__)

# Ruta para iniciar sesión
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Buscar el usuario en la base de datos
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Guardar user_id en la sesión
            return redirect(url_for('main.stalls'))  # Redirigir a los puestos
        else:
            return "Correo o contraseña incorrectos. Por favor, intenta nuevamente."
    
    return render_template('login.html')

# Ruta para registrar un nuevo usuario
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Verificar si el correo ya está registrado
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Este correo ya está registrado. Por favor, usa otro."

        # Crear hash seguro de la contraseña
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Crear nuevo usuario y agregarlo a la base de datos
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.login'))
    
    return render_template('register.html')

# Ruta para cerrar sesión
@main.route('/logout')
def logout():
    session.pop('user_id', None)  # Eliminar el ID del usuario de la sesión
    return redirect(url_for('main.login'))  # Redirigir al login

# Ruta para agregar un nuevo puesto de comida
@main.route('/add_stall', methods=['GET', 'POST'])
def add_stall():
    if 'user_id' not in session:  # Proteger la ruta para usuarios logueados
        return redirect(url_for('main.login'))  # Redirigir al login si no está logueado

    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')  # Guardar la ubicación (latitud/longitud)
        review = request.form.get('review')      # Breve reseña
        image_url = request.form.get('image_url')  # URL de la imagen

        # Crear el objeto FoodStall y guardarlo en la base de datos
        new_stall = FoodStall(
            name=name,
            location=location,
            review=review,
            image_url=image_url,
            user_id=session['user_id']  # Relacionar con el usuario que lo subió
        )
        db.session.add(new_stall)
        db.session.commit()

        return redirect(url_for('main.stalls'))

    return render_template('add_stall.html')

# Ruta para listar todos los puestos de comida
@main.route('/stalls')
def stalls():
    food_stalls = FoodStall.query.all()  # Obtener todos los puestos de la base de datos

    # Si no hay puestos de comida, pasar una lista vacía
    return render_template('stalls.html', stalls=food_stalls or [])
