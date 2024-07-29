from datetime import datetime, time, timedelta
from app.models import Court, Reservation
from app import app, db
from sqlalchemy import and_

def get_available_times(date):
    app.logger.info(f"Obteniendo tiempos disponibles para: date={date}")
    
    weekday_hours = (8, 30), (23, 0)
    saturday_hours = (8, 30), (18, 0)
    sunday_hours = (8, 30), (13, 0)

    if date.weekday() < 5:  # Monday to Friday
        opening_hour, closing_hour = weekday_hours
    elif date.weekday() == 5:  # Saturday
        opening_hour, closing_hour = saturday_hours
    else:  # Sunday
        opening_hour, closing_hour = sunday_hours

    current_time = datetime.combine(date, time(hour=opening_hour[0], minute=opening_hour[1]))
    closing_time = datetime.combine(date, time(hour=closing_hour[0], minute=closing_hour[1]))

    times = []
    while current_time + timedelta(minutes=60) <= closing_time:
        times.append(current_time.time())
        current_time += timedelta(minutes=15)  # Increment by 15 minutes

    app.logger.info(f"Tiempos disponibles encontrados: {len(times)}")
    return times

def get_available_courts(date, start_time, use_type):
    app.logger.info(f"Buscando canchas disponibles para: date={date}, start_time={start_time}, use_type={use_type}")

    duration = 90 if use_type in ['amistoso', 'liga'] else 60
    end_time = (datetime.combine(date, start_time) + timedelta(minutes=duration)).time()

    # Obtener las canchas ocupadas
    occupied_courts = db.session.query(Reservation.court_id).filter(
        Reservation.date == date,
        ~((Reservation.end_time <= start_time) | (Reservation.start_time >= end_time))
    ).distinct()

    # Obtener solo las canchas disponibles
    available_courts = Court.query.filter(~Court.id.in_(occupied_courts)).all()

    app.logger.info(f"Canchas disponibles: {[c.id for c in available_courts]}")

    return available_courts