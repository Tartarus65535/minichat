# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, Blueprint
from flask_login import current_user, login_required

from minichat.extensions import db
from minichat.forms import ProfileForm
from minichat.models import Message, User
from minichat.utils import flash_errors

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/')
def home():
    messages = Message.query.order_by(Message.timestamp.asc())
    user_amount = User.query.count()
    return render_template('chat/home.html', messages=messages, user_amount=user_amount)


@chat_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.github = form.github.data
        current_user.bio = form.bio.data
        db.session.commit()
        return redirect(url_for('.home'))
    flash_errors(form)
    return render_template('chat/profile.html', form=form)


@chat_bp.route('/profile/<user_id>')
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('chat/_profile_card.html', user=user)

@socketio.on('new message')
def new_message(message_body):
    message= Message(author=current_user._get_current_object(),body=message_body)
    db.session.add(message)
    db.session.commit()
    emit('new message',
        {'mes s age html': render_template('chat/_message.html',message=message)}
        broadcast=True )