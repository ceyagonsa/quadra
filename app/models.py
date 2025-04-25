from . import db

# Modelo para usuarios
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    # Relación con los puestos de comida (un usuario puede tener varios puestos)
    food_stalls = db.relationship('FoodStall', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'

# Modelo para puestos de comida
class FoodStall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(300), nullable=False)  # Geolocalización como texto (latitud/longitud)
    review = db.Column(db.Text, nullable=False)  # Breve reseña
    image_url = db.Column(db.String(300), nullable=True)  # URL de la imagen
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Referencia al creador del puesto
    
    def __repr__(self):
        return f'<FoodStall {self.name}>'
