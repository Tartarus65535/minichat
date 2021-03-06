# -*- coding: utf-8 -*-
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO

socketio = SocketIO()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
moment = Moment()


@login_manager.user_loader
def load_user(user_id):
    from minichat.models import User
    return User.query.get(int(user_id))


login_manager.login_view = 'auth.login'
