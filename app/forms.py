from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange, Optional, Length
from app.models import User, Court, Reservation
from app.utils import get_available_times
from flask_login import current_user
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    is_member = BooleanField('¿Eres socio?', default=False)
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email(), Length(min=1, max=120)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=1, max=128)])
    password2 = PasswordField('Repetir Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import app, db
from app.forms import ReservationForm
from app.models import Reservation
from app.utils import get_available_times, get_available_courts

@app.route('/reserve', methods=['GET', 'POST'])
@login_required
def reserve():
    form = ReservationForm()
    if form.validate_on_submit():
        start_time = form.start_time.data
        date = form.date.data
        court_id = form.court_id.data

        # Obtener canchas disponibles
        available_courts = get_available_courts(start_time)
        available_court_names = ', '.join([court.name for court in available_courts])

        if court_id not in [court.id for court in available_courts]:
            flash(f'La cancha seleccionada no está disponible en el horario seleccionado. Sin embargo, las siguientes canchas están disponibles: {available_court_names}. Por favor, seleccione una cancha disponible.', 'danger')
        else:
            # Manejo de la lógica de la reserva
            end_time = (datetime.combine(date, datetime.strptime(start_time, "%H:%M").time()) + timedelta(hours=1)).time()
            reservation = Reservation(
                court_id=court_id,
                date=date,
                start_time=start_time,
                end_time=end_time,
                use_type=form.use_type.data,
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
            flash(f'Hola {current_user.username}, ya hemos actualizado tu reserva en la cancha {reservation.court.name} con Hora de Inicio {reservation.start_time} y Hora de Termino {reservation.end_time}, recuerda llegar 10 minutos antes para que puedas comenzar a la hora, te esperamos!', 'success')
            return redirect(url_for('calendar'))

    else:
        # Si no hay fecha proporcionada, usa la fecha actual
        date = form.date.data or datetime.today().date()
        court_id = form.court_id.data
        use_type = form.use_type.data
        form.start_time.choices = [(time.strftime("%H:%M"), time.strftime("%H:%M")) for time in get_available_times(date, court_id, use_type)]

    # Actualizar las opciones del campo de selección de canchas
    if form.start_time.data:
        form.court_id.choices = [(court.id, court.name) for court in get_available_courts(form.start_time.data)]
    else:
        form.court_id.choices = [(court.id, court.name) for court in get_available_courts(datetime.now())]

    return render_template('reservation.html', title='Reservar', form=form)

class EditReservationForm(FlaskForm):
    date = DateField('Fecha', validators=[DataRequired()])
    start_time = SelectField('Hora de Inicio', choices=[])
    court_id = SelectField('Cancha', choices=[])
    use_type = SelectField('Tipo de uso', choices=[
        ('amistoso', 'Amistoso'),
        ('liga', 'Liga'),
        ('entrenamiento_individual', 'Entrenamiento Individual'),
        ('entrenamiento_grupal', 'Entrenamiento Grupal'),
        ('elite', 'Elite'),
        ('academia_interna', 'Academia Interna')
    ], validators=[DataRequired()])
    game_type = SelectField('Tipo de juego', choices=[
        ('singles', 'Singles'),
        ('doubles', 'Dobles')
    ], validators=[Optional()])
    league_category = SelectField('Categoría de liga', choices=[
        ('primera', 'Primera'),
        ('segunda', 'Segunda'),
        ('tercera', 'Tercera'),
        ('cuarta', 'Cuarta'),
        ('a', 'A'),
        ('b', 'B')
    ], validators=[Optional()])
    player1 = StringField('Jugador 1', render_kw={'readonly': True})
    player1_is_member = BooleanField('Jugador 1 es socio', default=False, render_kw={'readonly': True})
    player2 = StringField('Jugador 2', validators=[Optional()])
    player2_is_member = BooleanField('¿Es socio?', validators=[Optional()])
    player3 = StringField('Jugador 3', validators=[Optional()])
    player3_is_member = BooleanField('¿Es socio?', validators=[Optional()])
    player4 = StringField('Jugador 4', validators=[Optional()])
    player4_is_member = BooleanField('¿Es socio?', validators=[Optional()])
    trainer = StringField('Entrenador', validators=[Optional()])
    elite_category = SelectField('Categoría Elite', choices=[
        ('cancha_naranja', 'Cancha Naranja'),
        ('cancha_roja', 'Cancha Roja'),
        ('cancha_verde', 'Cancha Verde'),
        ('proyeccion', 'Proyección')
    ], validators=[Optional()])
    academy_category = SelectField('Categoría de Academia', choices=[
        ('inicio', 'Inicio'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado')
    ], validators=[Optional()])
    is_paid = BooleanField('Pagado')
    payment_amount = IntegerField('Monto de Pago', validators=[Optional(), NumberRange(min=0)])
    comments = TextAreaField('Comentarios')
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(EditReservationForm, self).__init__(*args, **kwargs)
        self.court_id.choices = [(court.id, court.name) for court in Court.query.all()]
        self.start_time.choices = [(time.strftime("%H:%M"), time.strftime("%H:%M")) for time in get_available_times(self.date.data, self.court_id.data, self.use_type.data)]

class DateRangeForm(FlaskForm):
    start_date = DateField('Fecha de Inicio', validators=[DataRequired()])
    end_date = DateField('Fecha de Término', validators=[DataRequired()])
    submit = SubmitField('Buscar')

class FormGeneral(FlaskForm):
    date = DateField('Fecha', validators=[DataRequired()])
    submit = SubmitField('Guardar')

class FormIngresos(FlaskForm):
    start_date = DateField('Fecha de Inicio', validators=[DataRequired()])
    end_date = DateField('Fecha de Término', validators=[DataRequired()])
    submit = SubmitField('Buscar')

class FormNoPagadas(FlaskForm):
    date = DateField('Fecha', validators=[DataRequired()])
    submit = SubmitField('Guardar')
