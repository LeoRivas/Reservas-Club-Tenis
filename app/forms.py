from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, TimeField, DecimalField, TextAreaField, IntegerField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange, Optional, Length
from datetime import time
from app.models import User, Court, Reservation
from app.utils import get_available_times
from flask_login import current_user




class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    is_member = BooleanField('¿Eres socio?', default=False)
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
            self.start_time.choices = [(time.strftime("%H:%M"), time.strftime("%H:%M")) for time in get_available_times(self.date.data, self.court_id.data, self.use_type.data)]

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
    player1 = StringField('Jugador 1', render_kw={'readonly': True})
    player1_is_member = BooleanField('Jugador 1 es socio', default=False, render_kw={'readonly': True}) 
    player2 = StringField('Jugador 2')
    player3 = StringField('Jugador 3')
    player4 = StringField('Jugador 4')
    player2_is_member = BooleanField('¿Es socio?')
    player3_is_member = BooleanField('¿Es socio?')
    player4_is_member = BooleanField('¿Es socio?')
    trainer = StringField('Entrenador')
    elite_category = SelectField('Categoría Elite', choices=[
        ('cancha_naranja', 'Cancha Naranja'),
        ('cancha_roja', 'Cancha Roja'),
        ('cancha_verde', 'Cancha Verde'),
        ('proyeccion', 'Proyección')
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

