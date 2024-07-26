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


class ReservationForm(FlaskForm):
    date = DateField('Fecha', validators=[DataRequired()])
    start_time = SelectField('Hora de Inicio', choices=[])
    court_id = SelectField('Cancha', choices=[], coerce=int, validators=[DataRequired()])
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
    player1 = StringField('Jugador 1', validators=[Length(max=64)])
    player1_is_member = BooleanField('Jugador 1 es socio', default=False)
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
    submit = SubmitField('Reservar')

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        date = self.date.data or datetime.today().date()
        court_id = self.court_id.data
        use_type = self.use_type.data
        if date and court_id and use_type:
            self.start_time.choices = [(time.strftime("%H:%M"), time.strftime("%H:%M")) for time in get_available_times(date, court_id, use_type)]
        else:
            self.start_time.choices = []

class EditReservationForm(FlaskForm):
    date = DateField('Fecha', validators=[DataRequired()])
    start_time = SelectField('Hora de Inicio', choices=[])
    court_id = SelectField('Cancha', choices=[], coerce=int, validators=[DataRequired()])
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
    player1 = StringField('Jugador 1', validators=[Length(max=64)])
    player1_is_member = BooleanField('Jugador 1 es socio', default=False)
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
