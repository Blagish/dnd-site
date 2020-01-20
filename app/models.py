from app import db, login_manager
from flask_login import UserMixin
from hashlib import md5


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    about = db.Column(db.String(512), default='There is no info yet!')
    is_moderator = db.Column(db.Boolean)
#   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    characters = db.relationship('Character', backref='author', lazy=True)
    rooms = db.relationship('Room', backref='author', lazy=True)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(30))
    lvlclass = db.Column(db.String(20))
    armor = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    race = db.Column(db.String(15))
    stats = db.Column(db.String(20))
    willsave = db.Column(db.String(16))
    skills = db.Column(db.String(40))
    abilities = db.Column(db.String(512))
    inventory = db.Column(db.String(512))
    health = db.Column(db.Integer)
    tokens = db.relation('Token', backref='char', lazy=True)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    link = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    guests = db.Column(db.String(50))
    tokens = db.relation('Token', backref='party', lazy=True)


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(30))
    name = db.Column(db.String(30))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    health = db.Column(db.Integer)
    max_health = db.Column(db.Integer)
    slots = db.Column(db.String(1024))
