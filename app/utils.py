from datetime import datetime, time, timedelta
from app.models import Court, Reservation

def get_available_times(date, court_id, use_type):
    from datetime import datetime, time, timedelta

    # Horarios del club
    weekday_hours = [(8, 30), (23, 0)]
    saturday_hours = [(8, 30), (18, 0)]
    sunday_hours = [(8, 30), (13, 0)]

    if date.weekday() < 5:  # Lunes a viernes
        opening_hour, closing_hour = weekday_hours
    elif date.weekday() == 5:  # Sábado
        opening_hour, closing_hour = saturday_hours
    else:  # Domingo
        opening_hour, closing_hour = sunday_hours

    # Generar todos los posibles horarios en intervalos de 5 minutos
    times = []
    current_time = datetime.combine(date, time(hour=opening_hour[0], minute=opening_hour[1]))
    closing_time = datetime.combine(date, time(hour=closing_hour[0], minute=closing_hour[1]))

    while current_time + timedelta(minutes=60) <= closing_time:
        times.append(current_time.time())
        current_time += timedelta(minutes=5)

    # Filtrar horarios ya reservados si court_id está presente
    if court_id:
        reservations = Reservation.query.filter_by(date=date, court_id=court_id).all()
        reserved_times = [(datetime.combine(date, r.start_time), datetime.combine(date, r.end_time)) for r in reservations]
        available_times = [t for t in times if all(not (start <= datetime.combine(date, t) < end) for start, end in reserved_times)]
        return available_times

    return times


def get_available_courts(start_time, end_time):
    reservations = Reservation.query.filter(
        Reservation.start_time < end_time,
        Reservation.end_time > start_time
    ).all()

    reserved_court_ids = [reservation.court_id for reservation in reservations]
    available_courts = Court.query.filter(Court.id.notin_(reserved_court_ids)).all()

    return available_courts
