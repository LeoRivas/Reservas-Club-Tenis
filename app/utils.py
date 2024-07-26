from datetime import datetime, time, timedelta
from app.models import Court, Reservation

def get_available_times(date, court_id, use_type):
    weekday_hours = [(8, 30), (23, 0)]
    saturday_hours = [(8, 30), (18, 0)]
    sunday_hours = [(8, 30), (13, 0)]

    if date.weekday() < 5:  # Lunes a viernes
        opening_hour, closing_hour = weekday_hours
    elif date.weekday() == 5:  # Sábado
        opening_hour, closing_hour = saturday_hours
    else:  # Domingo
        opening_hour, closing_hour = sunday_hours

    times = []
    current_time = datetime.combine(date, time(hour=opening_hour[0], minute=opening_hour[1]))
    closing_time = datetime.combine(date, time(hour=closing_hour[0], minute=closing_hour[1]))

    while current_time + timedelta(minutes=60) <= closing_time:
        times.append(current_time.time())
        current_time += timedelta(minutes=5)

    if court_id:
        reservations = Reservation.query.filter_by(date=date, court_id=court_id).all()
        reserved_times = [(datetime.combine(date, r.start_time), datetime.combine(date, r.end_time)) for r in reservations]
        available_times = [t for t in times if all(not (start <= datetime.combine(date, t) < end) for start, end in reserved_times)]
        return available_times

    return times

def check_availability(date, start_time, end_time):
    reservations = Reservation.query.filter_by(date=date).all()
    available_courts = Court.query.all()
    
    for reservation in reservations:
        if not (start_time >= reservation.end_time or end_time <= reservation.start_time):
            available_courts = [court for court in available_courts if court.id != reservation.court_id]

    return available_courts


