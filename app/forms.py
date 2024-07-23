from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, TimeField, DecimalField, TextAreaField, IntegerField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange, Optional, Length
from datetime import time
from app.models import User, Court, Reservation


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=128)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditReservationForm(FlaskForm):
    admin_name = StringField('Admin', render_kw={'readonly': True})
    court_id = SelectField('Cancha', coerce=int, validators=[DataRequired()])
    date = DateField('Fecha', validators=[DataRequired()])
    start_time = TimeField('Hora de Inicio', validators=[DataRequired()])
    end_time = TimeField('Hora de Fin', validators=[DataRequired()])
    is_paid = BooleanField('¿Pagado?')
    payment_amount = DecimalField('Monto del Pago')
    comments = TextAreaField('Comentarios')
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(EditReservationForm, self).__init__(*args, **kwargs)
        self.court_id.choices = [(court.id, court.name) for court in Court.query.all()]


class DateRangeForm(FlaskForm):
    start_date = DateField('Fecha de inicio', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Fecha de fin', format='%Y-%m-%d', validators=[DataRequired()])
    use_type = SelectField('Tipo de uso', choices=[
        ('todos', 'Todos'),
        ('amistoso_singles', 'Amistoso (Singles)'),
        ('amistoso_dobles', 'Amistoso (Dobles)'),
        ('liga_singles', 'Liga (Singles)'),
        ('liga_dobles', 'Liga (Dobles)'),
        ('entrenamiento_particular', 'Entrenamiento Particular'),
        ('entrenamiento_grupal', 'Entrenamiento Grupal')
    ], validators=[DataRequired()])
    submit = SubmitField('Filtrar')

class FormGeneral(FlaskForm):
    start_date = DateField('Fecha de inicio', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Fecha de fin', format='%Y-%m-%d', validators=[DataRequired()])
    use_type = SelectField('Tipo de uso', choices=[
        ('todos', 'Todos'),
        ('amistoso_singles', 'Amistoso (Singles)'),
        ('amistoso_dobles', 'Amistoso (Dobles)'),
        ('liga_singles', 'Liga (Singles)'),
        ('liga_dobles', 'Liga (Dobles)'),
        ('entrenamiento_particular', 'Entrenamiento Particular'),
        ('entrenamiento_grupal', 'Entrenamiento Grupal')
    ], validators=[DataRequired()])
    submit = SubmitField('Filtrar')

class FormIngresos(FlaskForm):
    start_date = DateField('Fecha de inicio', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Fecha de fin', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Filtrar')

class FormNoPagadas(FlaskForm):
    start_date = DateField('Fecha de inicio', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Fecha de fin', format='%Y-%m-%d', validators=[DataRequired()])
    use_type = SelectField('Tipo de uso', choices=[
        ('todos', 'Todos'),
        ('amistoso_singles', 'Amistoso (Singles)'),
        ('amistoso_dobles', 'Amistoso (Dobles)'),
        ('liga_singles', 'Liga (Singles)'),
        ('liga_dobles', 'Liga (Dobles)'),
        ('entrenamiento_particular', 'Entrenamiento Particular'),
        ('entrenamiento_grupal', 'Entrenamiento Grupal')
    ], validators=[DataRequired()])
    submit = SubmitField('Filtrar')

class ReservationForm(FlaskForm):
    court_id = SelectField('Cancha', coerce=int, validators=[DataRequired()])
    date = DateField('Fecha', validators=[DataRequired()])
    start_time = TimeField('Hora de inicio', validators=[DataRequired()])
    end_time = TimeField('Hora de término', validators=[DataRequired()])
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
    ])
    league_category = SelectField('Categoría de liga', choices=[
        ('primera', 'Primera'),
        ('segunda', 'Segunda'),
        ('tercera', 'Tercera'),
        ('cuarta', 'Cuarta'),
        ('a', 'A'),
        ('b', 'B')
    ])
    player1 = StringField('Jugador 1')
    player2 = StringField('Jugador 2')
    player3 = StringField('Jugador 3')
    player4 = StringField('Jugador 4')
    player1_is_member = BooleanField('¿Es socio?')
    player2_is_member = BooleanField('¿Es socio?')
    player3_is_member = BooleanField('¿Es socio?')
    player4_is_member = BooleanField('¿Es socio?')
    trainer = StringField('Entrenador')
    elite_category = SelectField('Categoría Elite', choices=[
        ('cancha_naranja', 'Cancha Naranja'),
        ('cancha_roja', 'Cancha Roja'),
        ('cancha_verde', 'Cancha Verde'),
        ('adultos', 'Adultos')
    ])
    academy_category = SelectField('Categoría de Academia', choices=[
        ('inicio', 'Inicio'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado')
    ])
    is_paid = BooleanField('Pagado')
    payment_amount = IntegerField('Monto de Pago', validators=[Optional(), NumberRange(min=0)])  # Allowing optional values and minimum of 0
    comments = TextAreaField('Comentarios')
    submit = SubmitField('Guardar')


    def validate_start_time(self, field):
        if not (time(8, 30) <= field.data <= time(21, 30)):
            raise ValidationError('La hora de inicio debe estar entre las 08:30 y las 21:30.')

    def validate_end_time(self, field):
        if not (time(8, 30) <= field.data <= time(21, 30)):
            raise ValidationError('La hora de término debe estar entre las 08:30 y las 21:30.')

    def validate_custom(self):
        result = True
        if self.date.data.weekday() >= 5:  # Sábado y Domingo
            if self.date.data.weekday() == 5:  # Sábado
                if not (time(8, 30) <= self.start_time.data <= time(16, 0)):
                    self.start_time.errors.append('Los sábados, la hora de inicio debe estar entre las 08:30 y las 16:00.')
                    result = False
                if not (time(8, 30) <= self.end_time.data <= time(16, 0)):
                    self.end_time.errors.append('Los sábados, la hora de término debe estar entre las 08:30 y las 16:00.')
                    result = False
            if self.date.data.weekday() == 6:  # Domingo
                if not (time(8, 30) <= self.start_time.data <= time(14, 0)):
                    self.start_time.errors.append('Los domingos, la hora de inicio debe estar entre las 08:30 y las 14:00.')
                    result = False
                if not (time(8, 30) <= self.end_time.data <= time(14, 0)):
                    self.end_time.errors.append('Los domingos, la hora de término debe estar entre las 08:30 y las 14:00.')
                    result = False
        return result
