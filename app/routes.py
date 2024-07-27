from flask import render_template, redirect, url_for, flash, request, make_response, jsonify
from app import app, db, utils
from app.forms import LoginForm, RegistrationForm, ReservationForm, EditReservationForm, DateRangeForm, FormGeneral, FormIngresos, FormNoPagadas
from app.models import User, Reservation, Court
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from datetime import datetime, timedelta, time
from sqlalchemy import func
import csv
from io import StringIO
from app.utils import get_available_times, check_availability
from app import utils




@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, is_member=form.is_member.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('¡Felicidades, ya estás registrado!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


def check_availability(date, start_time, end_time, selected_court_id):
    selected_court_reservations = Reservation.query.filter_by(date=date, court_id=selected_court_id).all()
    is_selected_court_available = all(
        end_time <= r.start_time or start_time >= r.end_time
        for r in selected_court_reservations
    )

    available_courts = []
    if not is_selected_court_available:
        for court in Court.query.all():
            if court.id != selected_court_id:
                reservations = Reservation.query.filter_by(date=date, court_id=court.id).all()
                is_available = all(
                    end_time <= r.start_time or start_time >= r.end_time
                    for r in reservations
                )
                if is_available:
                    available_courts.append(court)
    
    return is_selected_court_available, available_courts





@app.route('/reserve', methods=['GET', 'POST'])
@login_required
def reserve():
    form = ReservationForm()
    if form.validate_on_submit():
        start_time = datetime.strptime(form.start_time.data, "%H:%M").time()
        use_type = form.use_type.data

        # Calcular la hora de término basada en el tipo de uso
        if use_type in ['amistoso', 'liga']:
            end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=90)).time()
        else:
            end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=60)).time()

        reservation = Reservation(
            court_id=form.court_id.data,
            date=form.date.data,
            start_time=start_time,
            end_time=end_time,
            use_type=use_type,
            game_type=form.game_type.data,
            league_category=form.league_category.data,
            player1=form.player1.data,
            player1_is_member=form.player1_is_member.data,
            player2=form.player2.data,
            player2_is_member=form.player2_is_member.data,
            player3=form.player3.data,
            player3_is_member=form.player3_is_member.data,
            player4=form.player4.data,
            player4_is_member=form.player4_is_member.data,
            trainer=form.trainer.data,
            elite_category=form.elite_category.data,
            academy_category=form.academy_category.data,
            is_paid=form.is_paid.data,
            payment_amount=form.payment_amount.data,
            comments=form.comments.data,
            user_id=current_user.id
        )
        db.session.add(reservation)
        db.session.commit()
        flash('Reserva creada con éxito.')
        return redirect(url_for('index'))
    else:
        form.date.data = datetime.today().date()
        form.start_time.choices = [(time.strftime("%H:%M"), time.strftime("%H:%M")) for time in utils.get_available_times(datetime.today().date(), None, None)]
        form.court_id.choices = [(court.id, court.name) for court in Court.query.all()]
    return render_template('reservation.html', form=form)
    
@app.route('/edit_reservation/<int:reservation_id>', methods=['GET', 'POST'])
@login_required
def edit_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    form = EditReservationForm(obj=reservation)
    if form.validate_on_submit():
        start_time = datetime.strptime(form.start_time.data, "%H:%M").time()
        use_type = form.use_type.data

        # Calcular la hora de término basada en el tipo de uso
        if use_type in ['amistoso', 'liga']:
            end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=90)).time()
        else:
            end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=60)).time()

        reservation.court_id = form.court_id.data
        reservation.date = form.date.data
        reservation.start_time = start_time
        reservation.end_time = end_time
        reservation.use_type = use_type
        reservation.game_type = form.game_type.data
        reservation.league_category = form.league_category.data
        reservation.player1 = form.player1.data
        reservation.player1_is_member = form.player1_is_member.data
        reservation.player2 = form.player2.data
        reservation.player2_is_member = form.player2_is_member.data
        reservation.player3 = form.player3.data
        reservation.player3_is_member = form.player3_is_member.data
        reservation.player4 = form.player4.data
        reservation.player4_is_member = form.player4_is_member.data
        reservation.trainer = form.trainer.data
        reservation.elite_category = form.elite_category.data
        reservation.academy_category = form.academy_category.data
        reservation.is_paid = form.is_paid.data
        reservation.payment_amount = form.payment_amount.data
        reservation.comments = form.comments.data
        db.session.commit()
        flash('Reserva actualizada con éxito.')
        return redirect(url_for('admin_dashboard'))
    else:
        form.date.data = reservation.date
        form.start_time.choices = [(time.strftime("%H:%M"), time.strftime("%H:%M")) for time in get_available_times(reservation.date, None, None)]
    return render_template('edit_reservation.html', form=form, reservation=reservation)

@app.route('/edit_reservation_user/<int:reservation_id>', methods=['GET', 'POST'])
@login_required
def edit_reservation_user(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    form = EditReservationForm(obj=reservation)
    if form.validate_on_submit():
        start_time = datetime.strptime(form.start_time.data, "%H:%M").time()
        use_type = form.use_type.data

        # Calcular la hora de término basada en el tipo de uso
        if use_type in ['amistoso', 'liga']:
            end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=90)).time()
        else:
            end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=60)).time()

        reservation.court_id = form.court_id.data
        reservation.date = form.date.data
        reservation.start_time = start_time
        reservation.end_time = end_time
        reservation.use_type = use_type
        reservation.game_type = form.game_type.data
        reservation.league_category = form.league_category.data
        reservation.player1 = form.player1.data
        reservation.player1_is_member = form.player1_is_member.data
        reservation.player2 = form.player2.data
        reservation.player2_is_member = form.player2_is_member.data
        reservation.player3 = form.player3.data
        reservation.player3_is_member = form.player3_is_member.data
        reservation.player4 = form.player4.data
        reservation.player4_is_member = form.player4_is_member.data
        reservation.trainer = form.trainer.data
        reservation.elite_category = form.elite_category.data
        reservation.academy_category = form.academy_category.data
        reservation.is_paid = form.is_paid.data
        reservation.payment_amount = form.payment_amount.data
        reservation.comments = form.comments.data
        db.session.commit()
        flash('Reserva actualizada con éxito.')
        return redirect(url_for('user_reservations'))
    else:
        form.date.data = reservation.date
        form.start_time.choices = [(time.strftime("%H:%M"), time.strftime("%H:%M")) for time in get_available_times(reservation.date, None, None)]
    return render_template('edit_reservation_user.html', form=form, reservation=reservation)

@app.route('/get_available_courts')
def get_available_courts():
    date_str = request.args.get('date')
    start_time_str = request.args.get('start_time')
    use_type = request.args.get('use_type')

    print(f"Recibidos: date={date_str}, start_time={start_time_str}, use_type={use_type}")

    available_courts = utils.get_available_courts(date_str, start_time_str, use_type)
    
    print(f"Canchas disponibles: {available_courts}")
    
    court_data = [{'id': court.id, 'name': court.name} for court in available_courts]

    return jsonify(court_data)

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    date_str = request.args.get('date')
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date = datetime.today().date()

    courts = Court.query.all()
    times = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00"]
    reservations = Reservation.query.filter_by(date=date).all()

    for reservation in reservations:
        if reservation.use_type == "amistoso":
            reservation.color = "#dff0d8"
        elif reservation.use_type == "liga":
            reservation.color = "#f2dede"
        elif reservation.use_type == "entrenamiento_individual":
            reservation.color = "#d9edf7"
        elif reservation.use_type == "entrenamiento_grupal":
            reservation.color = "#fcf8e3"
        elif reservation.use_type == "elite":
            reservation.color = "#f5f5f5"
        elif reservation.use_type == "academia_interna":
            reservation.color = "#e0e0e0"

        if reservation.game_type == "singles":
            reservation.players = f"{reservation.player1}, {reservation.player2}"
        else:
            reservation.players = f"{reservation.player1}, {reservation.player2}, {reservation.player3}, {reservation.player4}"

    return render_template('calendar.html', 
                           title='Calendario', 
                           courts=courts, 
                           times=times, 
                           reservations=reservations, 
                           date=date.strftime('%Y-%m-%d'))


@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('No tienes permiso para acceder a esta página.')
        return redirect(url_for('index'))

    form_general = FormGeneral()
    form_ingresos = FormIngresos()
    form_no_pagadas = FormNoPagadas()

    reservations = Reservation.query.all()
    total_hours = sum((datetime.combine(reservation.date, reservation.end_time) - datetime.combine(reservation.date, reservation.start_time)).seconds / 3600 for reservation in reservations)
    total_income = sum(reservation.payment_amount for reservation in reservations if reservation.is_paid)
    
    income_by_use_type = {}
    for reservation in reservations:
        if reservation.use_type not in income_by_use_type:
            income_by_use_type[reservation.use_type] = 0
        if reservation.is_paid:
            income_by_use_type[reservation.use_type] += reservation.payment_amount

    unpaid_reservations = Reservation.query.filter_by(is_paid=False).all()

    if form_general.validate_on_submit() or form_ingresos.validate_on_submit() or form_no_pagadas.validate_on_submit():
        start_date = form_general.start_date.data or form_ingresos.start_date.data or form_no_pagadas.start_date.data
        end_date = form_general.end_date.data or form_ingresos.end_date.data or form_no_pagadas.end_date.data
        use_type = form_general.use_type.data or form_no_pagadas.use_type.data

        filtered_reservations = Reservation.query.filter(Reservation.date.between(start_date, end_date))
        if use_type != 'todos':
            filtered_reservations = filtered_reservations.filter_by(use_type=use_type)
        
        total_hours = sum((datetime.combine(reservation.date, reservation.end_time) - datetime.combine(reservation.date, reservation.start_time)).seconds / 3600 for reservation in filtered_reservations)
        total_income = sum(reservation.payment_amount for reservation in filtered_reservations if reservation.is_paid)
        
        income_by_use_type = {}
        for reservation in filtered_reservations:
            if reservation.use_type not in income_by_use_type:
                income_by_use_type[reservation.use_type] = 0
            if reservation.is_paid:
                income_by_use_type[reservation.use_type] += reservation.payment_amount
        
        unpaid_reservations = filtered_reservations.filter_by(is_paid=False).all()
    else:
        filtered_reservations = reservations
    
    return render_template(
        'admin_dashboard.html', 
        title='Panel de Administración', 
        form_general=form_general, 
        form_ingresos=form_ingresos, 
        form_no_pagadas=form_no_pagadas, 
        reservations=filtered_reservations, 
        total_hours=total_hours, 
        total_income=total_income, 
        income_by_use_type=income_by_use_type, 
        unpaid_reservations=unpaid_reservations
    )


@app.route('/export_reservations', methods=['GET'])
@login_required
def export_reservations():
    if not current_user.is_admin:
        flash('No tienes permiso para acceder a esta página.')
        return redirect(url_for('index'))

    si = StringIO()
    cw = csv.writer(si)
    
    reservations = Reservation.query.all()
    cw.writerow(['ID', 'Cancha', 'Usuario', 'Fecha', 'Hora de Inicio', 'Hora de Fin', 'Tipo de Uso', 'Pagado', 'Monto de Pago', 'Comentarios'])
    for reservation in reservations:
        cw.writerow([reservation.id, reservation.court.name, reservation.user.username, reservation.date, reservation.start_time, reservation.end_time, reservation.use_type, reservation.is_paid, reservation.payment_amount, reservation.comments])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=reservas.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/my_reservations', methods=['GET'])
@login_required
def my_reservations():
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template('user_reservations.html', reservations=reservations)



@app.route('/delete_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def delete_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    
    # Verificar que el usuario actual es el propietario de la reserva o un administrador
    if reservation.user_id != current_user.id and not current_user.is_admin:
        flash('No tienes permiso para eliminar esta reserva.')
        return redirect(url_for('index'))
    
    db.session.delete(reservation)
    db.session.commit()
    flash('Reserva eliminada con éxito.')
    return redirect(url_for('index'))


