from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from app.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Имя уже занято.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот адрес уже используется.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class UpdateAccountForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    about = StringField('О мне', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Имя уже занято. Выберите другое.')


class CharacterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    lvlclass = StringField('Класс и уровень', validators=[DataRequired()])
    armor = StringField('Показатель брони', validators=[DataRequired()])
    speed = StringField('Показатель скорости', validators=[DataRequired()])
    race = StringField('Раса персонажа', validators=[DataRequired()])
    health = StringField('Здоровье', validators=[DataRequired()])
    stat1 = StringField('Сила', validators=[DataRequired()])
    stat2 = StringField('Ловкость', validators=[DataRequired()])
    stat3 = StringField('Телосложение', validators=[DataRequired()])
    stat4 = StringField('Интеллект', validators=[DataRequired()])
    stat5 = StringField('Мудрость', validators=[DataRequired()])
    stat6 = StringField('Харизма', validators=[DataRequired()])

    sw1 = BooleanField('Сила')
    sw2 = BooleanField('Ловкость')
    sw3 = BooleanField('Телосложение')
    sw4 = BooleanField('Интеллект')
    sw5 = BooleanField('Мудрость')
    sw6 = BooleanField('Харизма')

    sk1 = BooleanField('Акробатика (Лов)')
    sk2 = BooleanField('Атлетика (Сил)')
    sk3 = BooleanField('Магия (Инт)')
    sk4 = BooleanField('Обман (Хар)')
    sk5 = BooleanField('История (Инт)')
    sk6 = BooleanField('Проницательность (Муд)')
    sk7 = BooleanField('Запугивание (Хар)')
    sk8 = BooleanField('Расследование (Инт)')
    sk9 = BooleanField('Медицина (Муд)')
    sk10 = BooleanField('Природа (Муд)')
    sk11 = BooleanField('Восприятие (Муд)')
    sk12 = BooleanField('Выступление (Хар)')
    sk13 = BooleanField('Убеждение (Хар)')
    sk14 = BooleanField('Религия (Инт)')
    sk15 = BooleanField('Ловкость рук (Лов)')
    sk16 = BooleanField('Скрытность (Лов)')
    sk17 = BooleanField('Выживание (Муд)')
    sk18 = BooleanField('Обращение с животными (Муд)')

    abilities = TextAreaField('Умения и способности')
    inventory = TextAreaField('Инвентарь')

    submit = SubmitField('Создать')


class RoomForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    submit = SubmitField('Создать')


class TokenForm(FlaskForm):
    character = SelectField('Выберите персонажа, на котором основывается игрофигурка', coerce=int)
    submit = SubmitField('Создать')




