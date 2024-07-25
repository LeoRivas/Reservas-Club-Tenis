def get_available_times(date, court_id, use_type=None):
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

    # Filtrar horarios ya reservados
    reservations = Reservation.query.filter_by(date=date, court_id=court_id).all()
    reserved_times = [(datetime.combine(date, r.start_time), datetime.combine(date, r.end_time)) for r in reservations]
    available_times = [t for t in times if all(not (start <= datetime.combine(date, t) < end) for start, end in reserved_times)]

    return available_times
