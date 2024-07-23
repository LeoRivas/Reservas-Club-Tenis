from flask import render_template, redirect, url_for, flash, request, make_response
from app import app, db
from app.forms import LoginForm, RegistrationForm, ReservationForm, EditReservationForm, DateRangeForm, FormGeneral, FormIngresos, FormNoPagadas
from app.models import User, Reservation, Court
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from datetime import datetime, timedelta
from sqlalchemy import func
import csv
from io import StringIO


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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reserve', methods=['GET', 'POST'])
@login_required
def reserve():
    form = ReservationForm()
    form.court_id.choices = [(court.id, court.name) for court in Court.query.all()]
    print(form.__dict__)  # Añade esta línea para depuración

    if form.validate_on_submit():
        reservation = Reservation(
            court_id=form.court_id.data,
            user_id=current_user.id,
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            use_type=form.use_type.data,
            game_type=form.game_type.data,
            league_category=form.league_category.data,
            player1=form.player1.data,
            player2=form.player2.data,
            player3=form.player3.data,
            player4=form.player4.data,
            trainer=form.trainer.data,
            player1_is_member=form.player1_is_member.data,
            player2_is_member=form.player2_is_member.data,
            player3_is_member=form.player3_is_member.data,
            player4_is_member=form.player4_is_member.data,
            elite_category=form.elite_category.data,
            academy_category=form.academy_category.data,
            is_paid=form.is_paid.data,
            payment_amount=form.payment_amount.data if form.payment_amount.data else 0,
            comments=form.comments.data
        )
        db.session.add(reservation)
        db.session.commit()
        flash('Tu reserva ha sido realizada!')
        return redirect(url_for('index'))
    return render_template('reservation.html', title='Reserve', form=form)


@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    date_str = request.args.get('date')
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date = datetime.today().date()

    courts = Court.query.all()
    times = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
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
    
    return render_template('admin_dashboard.html', title='Panel de Administración', form_general=form_general, form_ingresos=form_ingresos, form_no_pagadas=form_no_pagadas, reservations=reservations, total_hours=total_hours, total_income=total_income, income_by_use_type=income_by_use_type, unpaid_reservations=unpaid_reservations)

@app.route('/edit_reservation/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    form = EditReservationForm(obj=reservation)
    if request.method == 'GET':
        form.admin_name.data = current_user.username  # Set admin name to current user's username
    if form.validate_on_submit():
        reservation.court_id = form.court_id.data
        reservation.date = form.date.data
        reservation.start_time = form.start_time.data
        reservation.end_time = form.end_time.data
        reservation.is_paid = form.is_paid.data
        reservation.payment_amount = form.payment_amount.data
        reservation.comments = form.comments.data
        db.session.commit()
        flash('Reserva actualizada con éxito')
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_reservation.html', form=form, reservation=reservation)

@app.route('/delete_reservation/<int:id>', methods=['POST'])
@login_required
def delete_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    if not current_user.is_admin:
        flash('No tienes permisos para acceder a esta página.')
        return redirect(url_for('index'))
    db.session.delete(reservation)
    db.session.commit()
    flash('Reserva eliminada correctamente.')
    return redirect(url_for('admin_dashboard'))



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