from app import app, db
from app.models import User, Court

# Crear el contexto de la aplicación
with app.app_context():
    # Eliminar usuarios duplicados por correo y nombre de usuario
    users_to_delete = User.query.filter(
        (User.email.in_(['leopoldo.rivasurzua@gmail.com', 'cramirez@centralconsultores.cl', 'tenisclubcurico@gmail.com'])) |
        (User.username.in_(['Leopoldo Rivas', 'Claudio Ramirez', 'Carolina Reyes']))
    ).all()
    for user in users_to_delete:
        db.session.delete(user)
    db.session.commit()

    # Crear usuarios administradores
    admin1 = User(username='Leopoldo Rivas', email='leopoldo.rivasurzua@gmail.com', is_admin=True)
    admin1.set_password('Club.Curico')
    admin2 = User(username='Claudio Ramirez', email='cramirez@centralconsultores.cl', is_admin=True)
    admin2.set_password('Club.Curico')
    admin3 = User(username='Carolina Reyes', email='tenisclubcurico@gmail.com', is_admin=True)
    admin3.set_password('Club.Curico')

    # Verificar y agregar usuarios a la sesión
    for admin in [admin1, admin2, admin3]:
        existing_user = User.query.filter_by(email=admin.email).first()
        if not existing_user:
            db.session.add(admin)
    db.session.commit()

    # Crear canchas
    court_names = ['Cancha 1', 'Cancha 2', 'Cancha 3', 'Cancha 4', 'Cancha 5', 'Cancha 6', 'Cancha 7', 'Cancha 8']
    for name in court_names:
        existing_court = Court.query.filter_by(name=name).first()
        if not existing_court:
            court = Court(name=name)
            db.session.add(court)
    db.session.commit()

    # Verificar las entradas
    users = User.query.all()
    courts = Court.query.all()
    print("Usuarios:")
    for user in users:
        print(user.username, user.email)

    print("\nCanchas:")
    for court in courts:
        print(court.name)
