from notes_app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)




class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    notes = db.relationship('Note', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    
    def __repr__(self):
        return f"Username {self.username}"



class Note(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    # 'users.id' comes from the __tablename__ 'users'
    # and id is the attribute of that table.
    # nullable means every blog post must have a user id associated with it
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    
    
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    


    # to make an instance of a posted note
    # they need to provide the title, the text, user_id
    def __init__(self, title, text, user_id):
        self.title = title 
        self.text = text 
        self.user_id = user_id
    

    def __repr__(self):
        # up to you.
        return f"Post ID: {self.id} -- Date: {self.date} == Title: {self.title} -- Text: {self.text}"