
from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, CharacterForm, RoomForm, TokenForm
from app.models import User, Character, Room, Token
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import json
from hashlib import md5
from time import localtime
from random import randint
import math


def gen_color(seed):
    color = math.floor((abs(math.sin(seed) * 16777215)) % 16777215);
    color = hex(color)
    while len(color) < 6:
        color = '0' + color
    return '#' + color[2:]


@app.route("/")
@app.route("/home")
def home():
    posts=[]
    image_file_small=''
    if current_user.is_authenticated:
        image_file_small = current_user.avatar(32)
    return render_template('home.html', image_file_small=image_file_small)


@app.route("/about")
def about():
    image_file_small=''
    if current_user.is_authenticated:
        image_file_small = current_user.avatar(32)
    return render_template('about.html', title='About', image_file_small=image_file_small)


@app.route("/faq")
def faq():
    image_file_small=''
    if current_user.is_authenticated:
        image_file_small = current_user.avatar(32)
    return render_template('faq.html', title='FAQ', image_file_small=image_file_small)


@app.route("/resmat")
def resmat():
    image_file_small=''
    if current_user.is_authenticated:
        image_file_small = current_user.avatar(32)
    return render_template('resmat.html', title='Справочные материалы', image_file_small=image_file_small)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Неуданчная попытка входа. Проверьте электронную почту и пароль.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/rooms")
def rooms():
    my_rooms = Room.query.filter_by(user_id=current_user.id)
    all_rooms = Room.query.all()
    j_rooms = []
    for room in all_rooms:
        if current_user.id in json.loads(room.guests) and current_user.id != room.user_id:
            j_rooms.append(room)
    return render_template('rooms.html', title='Комнаты', my_rooms=my_rooms,
                           j_rooms=j_rooms, image_file_small=current_user.avatar(32))


@app.route("/chars")
def chars():
    characters = Character.query.filter_by(user_id=current_user.id)
    return render_template('chars.html', title='Персонажи', chars=characters, image_file_small=current_user.avatar(32))


@app.route("/my_profile")
@login_required
def my_profile():
    return redirect(url_for('user', user_id=current_user.id))


@app.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Информация обновлена!', 'success')
        return redirect(url_for('my_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about.data = current_user.about
    return render_template('profile.html', title='Account',
                           image_file=current_user.avatar(125), image_file_small=current_user.avatar(32), form=form)


@app.route("/user/<int:user_id>")
def user(user_id):
    this_user = User.query.get_or_404(user_id)
    image_file = this_user.avatar(200)
    this_chars = Character.query.filter_by(user_id=user_id)
    return render_template('user.html', user=this_user, chars=this_chars, image_file=image_file, image_file_small=current_user.avatar(32), you=current_user)


@app.route("/char/<int:char_id>")
@login_required
def char(char_id):
    this_char = Character.query.get_or_404(char_id)
    if this_char.user_id != current_user.id:
        return redirect(url_for('chars'))
    data = this_char.__dict__
    data.pop('_sa_instance_state')
    return json.dumps(data)#render_template('user.html', user=this_user, image_file=image_file, image_file_small=current_user.avatar(32))


@app.route("/new_character", methods=['GET', 'POST'])
@login_required
def new_character():
    form = CharacterForm()
    if form.validate_on_submit():
        character = Character(name=form.name.data,
                              lvlclass=form.lvlclass.data,
                              armor=int(form.armor.data),
                              speed=int(form.speed.data),
                              race=form.race.data,
                              stats=f'[{int(form.stat1.data)},{int(form.stat2.data)},{int(form.stat3.data)},{int(form.stat4.data)},{int(form.stat5.data)},{int(form.stat6.data)}]',
                              willsave=f'[{int(form.sw1.data)},{int(form.sw2.data)},{int(form.sw3.data)},{int(form.sw4.data)},{int(form.sw5.data)},{int(form.sw6.data)}]',
                              skills=f'[{int(form.sk1.data)},{int(form.sk2.data)},{int(form.sk3.data)},{int(form.sk4.data)},{int(form.sk5.data)},{int(form.sk6.data)},{int(form.sk7.data)},{int(form.sk8.data)},{int(form.sk9.data)},{int(form.sk10.data)},{int(form.sk11.data)},{int(form.sk12.data)},{int(form.sk13.data)},{int(form.sk14.data)},{int(form.sk15.data)},{int(form.sk16.data)},{int(form.sk17.data)},{int(form.sk18.data)}]',
                              abilities=form.abilities.data,
                              inventory=form.inventory.data,
                              health=form.health.data,
                              author=current_user
                              )
        db.session.add(character)
        db.session.commit()
        flash('Персонаж успешно создан!', 'success')
        return redirect(url_for('chars'))
    return render_template('new_character.html', title='Создать персонажа', form=form, image_file_small=current_user.avatar(32))


@app.route("/edit_character/<int:char_id>", methods=['GET', 'POST'])
@login_required
def edit_character(char_id):
    form = CharacterForm()
    current_char = Character.query.get_or_404(char_id)
    if current_char.user_id != current_user.id and not current_user.is_moderator:
        flash('Ошибка доступа', 'danger')
        return redirect(url_for('chars'))
    if form.validate_on_submit():
        current_char.name = form.name.data
        current_char.lvlclass = form.lvlclass.data
        current_char.armor = int(form.armor.data)
        current_char.speed = int(form.speed.data)
        current_char.race = form.race.data
        current_char.stats = f'[{int(form.stat1.data)},{int(form.stat2.data)},{int(form.stat3.data)},{int(form.stat4.data)},{int(form.stat5.data)},{int(form.stat6.data)}]'
        current_char.willsave = f'[{int(form.sw1.data)},{int(form.sw2.data)},{int(form.sw3.data)},{int(form.sw4.data)},{int(form.sw5.data)},{int(form.sw6.data)}]'
        current_char.skills = f'[{int(form.sk1.data)},{int(form.sk2.data)},{int(form.sk3.data)},{int(form.sk4.data)},{int(form.sk5.data)},{int(form.sk6.data)},{int(form.sk7.data)},{int(form.sk8.data)},{int(form.sk9.data)},{int(form.sk10.data)},{int(form.sk11.data)},{int(form.sk12.data)},{int(form.sk13.data)},{int(form.sk14.data)},{int(form.sk15.data)},{int(form.sk16.data)},{int(form.sk17.data)},{int(form.sk18.data)}]'
        current_char.abilities = form.abilities.data
        current_char.inventory = form.inventory.data
        current_char.health = form.health.data
        db.session.commit()
        flash('Информация обновлена!', 'success')
        return redirect(url_for('chars'))
    elif request.method == 'GET':
        form.name.data = current_char.name
        form.lvlclass.data = current_char.lvlclass
        form.armor.data = current_char.armor
        form.speed.data = current_char.speed
        form.race.data = current_char.race
        form.health.data = current_char.health
        form.abilities.data = current_char.abilities
        form.inventory.data = current_char.inventory

        willsave = json.loads(current_char.willsave)
        skills = json.loads(current_char.skills)
        stats = json.loads(current_char.stats)
        for stat in range(len(willsave)):
            exec(f'form.sw{stat+1}.data = bool({willsave[stat]})')
        for stat in range(len(skills)):
            exec(f'form.sk{stat+1}.data = bool({skills[stat]})')
        for stat in range(len(stats)):
            exec(f'form.stat{stat+1}.data = {stats[stat]}')
    return render_template('new_character.html', title='Редактировать персонажа',
                            image_file_small=current_user.avatar(32), form=form)


@app.route('/new_room', methods=['GET', 'POST'])
@login_required
def new_room():
    form = RoomForm()
    if form.validate_on_submit():
        time = ''.join(map(str, localtime()[:]))
        link = md5(time.encode('utf-8')).hexdigest()[:-2]+str(randint(10, 99))
        room = Room(name=form.name.data,
                    author=current_user,
                    guests=str([current_user.id]),
                    link=link)
        db.session.add(room)
        db.session.commit()
        flash('Комната создана!', 'success')
        return redirect(url_for('rooms'))
    return render_template('new_room.html', title='Создать комнату', form=form, image_file_small=current_user.avatar(32))


@app.route('/room/<room_link>')
@login_required
def room(room_link):
    not_joined = False
    this_room = Room.query.filter_by(link=room_link).first()
    gm = User.query.filter_by(id=this_room.user_id).first()
    all_tokens = Token.query.filter_by(room_id=this_room.id)
    try:
        guests = list(map(lambda x: (User.query.get_or_404(x).username, User.query.get_or_404(x).id) if x != gm.id else (None, None), json.loads(this_room.guests)))
    except TypeError:
        guests = []
    is_gm = (current_user.id == gm.id)
    if (current_user.username, current_user.id) not in guests and not is_gm:
        not_joined = True
    color = gen_color(this_room.id)
    return render_template('room.html', title=this_room.name, room=this_room, not_joined=not_joined, color=color,
                           gm=gm, tokens=all_tokens, is_gm=is_gm, guests=guests, image_file_small=current_user.avatar(32))


@app.route("/join_room/<room_link>")
def join_room(room_link):
    this_room = Room.query.filter_by(link=room_link).first()
    try:
        guests = json.loads(this_room.guests)
    except TypeError:
        guests = []
    if current_user.id not in guests:
        guests.append(current_user.id)
        this_room.guests = str(guests)
        db.session.commit()
        flash('Вы стали участником этой комнаты!', 'success')
    else:
        flash('Вы уже состоите в этой комнате.', 'danger')
    return redirect(url_for('room', room_link=room_link))


@app.route('/room/<room_link>/kick_player/<int:user_id>')
def kick_player(room_link, user_id):
    this_room = Room.query.filter_by(link=room_link).first()
    if current_user.id != this_room.user_id:
        flash('Не хватает прав.', 'danger')
        return redirect(url_for('rooms'))
    try:
        guests = json.loads(this_room.guests)
    except TypeError:
        flash('Этого пользователя нет в комнате.', 'danger')
        return redirect(url_for('room', room_link=room_link))
    guests.remove(user_id)
    this_room.guests = str(guests)
    db.session.commit()
    flash('Пользователь исключен.', 'success')
    return redirect(url_for('room', room_link=room_link))


@app.route('/delete_char/<int:char_id>')
def delete_char(char_id):
    this_char = Character.query.get_or_404(char_id)
    if this_char.user_id != current_user.id:
        return redirect(url_for('chars'))
    db.session.delete(this_char)
    db.session.commit()
    flash('Персонаж удален.', 'success')
    return redirect(url_for('chars'))


@app.route('/room/<room_id>/add_token', methods=['GET', 'POST'])
def add_token(room_id):
    form = TokenForm()
    this_room = Room.query.get_or_404(room_id)
    if this_room.user_id != current_user.id:
        flash('Ошибка доступа', 'danger')
        return redirect(url_for('room', room_link=this_room.link))
    my_chars = Character.query.filter_by(user_id=current_user.id)
    form.character.choices = [(char1.id, char1.name) for char1 in my_chars]
    if form.validate_on_submit():
        chosen_char = Character.query.get_or_404(form.character.data)
        token = Token(photo="default.png",
                      name=chosen_char.name,
                      party=this_room,
                      char=chosen_char,
                      health=chosen_char.health,
                      max_health=chosen_char.health,
                      slots=chosen_char.inventory)
        db.session.add(token)
        db.session.commit()
        return redirect(url_for('room', room_link=this_room.link))
    return render_template('new_token.html', title='Создать токен',
                           form=form, image_file_small=current_user.avatar(32))

