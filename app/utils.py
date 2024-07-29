from datetime import datetime, time, timedelta
from app.models import Reservation, Court

def get_available_courts(date_str, start_time_str, use_type):
    print(f"Buscando canchas disponibles para: date={date_str}, start_time={start_time_str}, use_type={use_type}")

    # Convertir la fecha y la hora a objetos datetime
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    start_time = datetime.strptime(start_time_str, '%H:%M').time()

    # Calcular la hora de término basada en el tipo de uso
    if use_type in ['amistoso', 'liga']:
        end_time = (datetime.combine(date, start_time) + timedelta(minutes=90)).time()
    else:
        end_time = (datetime.combine(date, start_time) + timedelta(minutes=60)).time()

    # Obtener todas las reservas en la fecha y hora seleccionada
    reservations = Reservation.query.filter_by(date=date).all()

    # Filtrar las canchas ocupadas en ese horario
    occupied_courts = set()
    for reservation in reservations:
        if not (reservation.end_time <= start_time or reservation.start_time >= end_time):
            occupied_courts.add(reservation.court_id)

    # Obtener todas las canchas
    all_courts = Court.query.all()

    # Filtrar las canchas disponibles
    available_courts = [court for court in all_courts if court.id not in occupied_courts]
    print(f"Canchas ocupadas: {occupied_courts}")
    print(f"Canchas disponibles: {available_courts}")

    return available_courts

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
