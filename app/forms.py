from flask_wtf.file import FileField, FileRequired
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User

error =""

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')

    def validate_username(self, username):
        global error
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            error = "yes"

    def validate_password(self, password):
        global error
        user = User.query.filter_by(password_hash=password.data).first()
        if error == "yes":
            error = "no"
            raise ValidationError('Не верный логин или пароль')
        else:
            error = "no"
            if user is None:
                raise ValidationError('Не верный логин или пароль')

class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    login = StringField('Имя', validators=[DataRequired()])
    fullname = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        global error
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пользователь с таким логином уже существует')


    def validate_email(self, email):
        global error
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пользователь с таким email уже существует')

class SettingForm(FlaskForm):
    username = StringField('Логин', validators=[])
    password = PasswordField('Пароль')
    login = StringField('Имя')
    fullname = StringField('Фамилия')
    email = StringField('Email', validators=[])
    file_object = FileField('file')
    commentary = StringField('Комментарий', validators=[Length(max=17)])
    submit = SubmitField('Внести изменения')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        super(SettingForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Пользователь с таким именем уже существует')


    def validate_email(self, email):
        if email.data != "" and email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Пользователь с таким email уже существует')



class FileForm(FlaskForm):
    file_object = FileField('file', validators=[FileRequired()])
    submit = SubmitField('Загрузить')

class TranslateForm(FlaskForm):
    text = TextAreaField('Текст', validators=[Length(max=630)])
    lang = SelectField('Язык', choices=[('en', 'Английский'), ('it', 'Итальянский'), ('zh', 'Китайский'), ('ru', 'Русский'), ('ba', 'Белорусский'), ('ko', 'Корейский'), ('az', 'Азербайджанский'), ('sq', 'Албанский'), ('am', 'Амхарский'), ('ar', 'Арабский')
                                        , ('ar', 'Армянский'), ('hy', 'Африкаанс'), ('af', 'Баскский'), ('eu', 'Башкирский'), ('be', 'Бенгальский'), ('bn', 'Бирманский'), ('my', 'Болгарский')
                                        , ('bg', 'Боснийский'), ('cy', 'Валлийский'), ('hu', 'Венгерский'), ('vi', 'Вьетнамский'), ('ht', 'Гаитянский'), ('gl', 'Галисийский'), ('nl', 'Голландский'), ('mrj', 'Горномарийский')
                                        , ('el', 'Греческий'), ('ka', 'Грузинский'), ('gu', 'Гуджарати'), ('da', 'Датский'), ('he', 'Иврит'), ('yi', 'Идиш'), ('id', 'Индонезийский')
                                        , ('ga', 'Ирландский'), ('is', 'Исландский'), ('es', 'Испанский'), ('kk', 'Казахский'), ('kn', 'Каннада'), ('ca', 'Каталанский')
                                        , ('ky', 'Киргизский'), ('ko', 'Корейский'), ('xh', 'Коса'), ('km', 'Кхмерский'), ('lo', 'Лаосский'), ('la', 'Латынь'), ('lv', 'Латышский'), ('lt', 'Литовский'), ('lb', 'Люксембургский')
                                        , ('mg', 'Малагасийский'), ('ms', 'Малайский')])
    submit = SubmitField('Перевести')

class NasaForm(FlaskForm):
    rover = SelectField('Марсоход', choices=[('https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos', 'Curiosity'),
                                             ('https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos', 'Spirit'),
                                             ('https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos', 'Opportunity')])
    submit = SubmitField('Обновить')

class NasaPlanetForm(FlaskForm):
    YY = StringField('Год')
    MM = StringField('Месяц')
    DD = StringField('День')
    submit = SubmitField('Применить')

class WeatherForm(FlaskForm):
    sity = StringField('Город')
    submit = SubmitField('Посмотреть')