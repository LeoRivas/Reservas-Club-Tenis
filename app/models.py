from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))  # Aumentado de 128 a 256
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Court(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    reservations = db.relationship('Reservation', backref='court', lazy=True)


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    court_id = db.Column(db.Integer, db.ForeignKey('court.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    use_type = db.Column(db.String(50), nullable=False)
    game_type = db.Column(db.String(50), nullable=True)
    league_category = db.Column(db.String(50), nullable=True)
    player1 = db.Column(db.String(50), nullable=True)
    player1_is_member = db.Column(db.Boolean, default=False)
    player2 = db.Column(db.String(50), nullable=True)
    player2_is_member = db.Column(db.Boolean, default=False)
    player3 = db.Column(db.String(50), nullable=True)
    player3_is_member = db.Column(db.Boolean, default=False)
    player4 = db.Column(db.String(50), nullable=True)
    player4_is_member = db.Column(db.Boolean, default=False)
    trainer = db.Column(db.String(50), nullable=True)
    elite_category = db.Column(db.String(50), nullable=True)
    academy_category = db.Column(db.String(50), nullable=True)
    is_paid = db.Column(db.Boolean, default=False)
    payment_amount = db.Column(db.Integer, default=0)
    comments = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('reservations', lazy=True))
    
    def __repr__(self):
        return f'<Reservation {self.id} {self.court.name}>'
