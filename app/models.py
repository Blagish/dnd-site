from datetime import datetime
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

#    histories = db.relationship('History', backref='author', lazy=True)
#    characters = db.relationship('Character', backref ='author', lazy=True)
#    posts = db.relationship('Post', backref='author', lazy=True)
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.about}')"
