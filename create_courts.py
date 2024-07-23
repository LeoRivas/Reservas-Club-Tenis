from app import create_app, db
from app.models import Court

app = create_app()

with app.app_context():
    courts = ["Court 1", "Court 2", "Court 3", "Court 4", "Court 5", "Court 6", "Court 7", "Court 8"]
    for court_name in courts:
        court = Court(name=court_name)
        db.session.add(court)
    db.session.commit()
