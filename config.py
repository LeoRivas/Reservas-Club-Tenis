import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Club.Curico'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # Asegúrate de que este sea el path correcto a tu base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
