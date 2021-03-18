from flask import render_template, flash, redirect, url_for, request, Blueprint, current_app
from app.users.forms import (LoginForm, RegistrationForm,
						EditProfileForm, RequestResetForm, ResetPasswordForm)
from app.posts.forms import EmptyForm
from app import db
from flask_login import current_user, login_user
from app.models import User, Post
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from app.users.utils import send_reset_email
import secrets
import os
from PIL import Image
from flask_babel import _, lazy_gettext as _l

users = Blueprint('users', __name__)


# Login page
@users.route('/login', methods=['GET', 'POST'])
def login():

	if current_user.is_authenticated:

		return redirect(url_for('posts.view'))

	form = LoginForm()

	if form.validate_on_submit():
		
		user = User.query.filter_by(username=form.username.data).first()


		if user is None or not user.check_password(form.password.data):

			flash(_('Invalid username or password'))

			return redirect(url_for('users.login'))

		login_user(user, remember=form.remember_me.data)

		next_page = request.args.get('next')


		if not next_page or url_parse(next_page).netloc != '':	# checks whether url is relative or abslute. In relative, netloc=''

			next_page = url_for('posts.view')

		return redirect(next_page)

	return render_template('login.html', title='Sign In', form=form)



@users.route('/logout')
def logout():

	logout_user()

	return redirect(url_for('users.login'))



@users.route('/register', methods=['GET', 'POST'])
def register():

	if current_user.is_authenticated:

		return redirect(url_for('posts.view'))

	form = RegistrationForm()

	if form.validate_on_submit():

		user = User(username=form.username.data, email=form.email.data)

		

		user.set_password(form.password.data)

		db.session.add(user)

		db.session.commit()

		flash(_('Congratulations, you are now a registered user!'))

		return redirect(url_for('users.login'))

	return render_template('register.html', title='Register', form=form)

@users.route('/reset_password', methods=['POST', 'GET'])
def reset_request():

	if current_user.is_authenticated:

		return redirect(url_for('posts.view'))

	form = RequestResetForm()

	if form.validate_on_submit():

		user = User.query.filter_by(email=form.email.data).first()

		send_reset_email(user)

		flash(_('An email has been sent with instructions to reset your password.'))

		return redirect(url_for('users.login'))

	return render_template('reset_request.html', title='Reset Password' , form=form)


@users.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):

	if current_user.is_authenticated:

		return redirect(url_for('posts.view'))

	user = User.verify_token(token)

	if user is None:

		flash(_('This is an invalid or expired token'), 'warning')
		return redirect(url_for('users.reset_request'))

	form = ResetPasswordForm()

	if form.validate_on_submit():

		user.set_password(form.password.data)

		db.session.commit()

		flash(_('your password as been updated. You are now able to login.'))

		return redirect(url_for('users.login'))

	return render_template('reset_token.html', title='Reset Password', form=form)


def save_picture(form_picture):

	random_hex = secrets.token_hex(8)

	_, f_ext = os.path.splitext(form_picture.filename)

	picture_fn = random_hex + f_ext

	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

	output_size = (125, 125)

	img = Image.open(form_picture)

	img.thumbnail(output_size)

	img.save(picture_path)

	return picture_fn

@users.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():

	form = EditProfileForm(current_user.username)

	if form.validate_on_submit():

		if form.picture.data:

			current_user.image_file = save_picture(form.picture.data);

		current_user.username = form.username.data

		current_user.about_me = form.about_me.data

		db.session.commit()

		flash(_('Your changes have been saved.'))

		return redirect(url_for('users.edit_profile'))

	elif request.method == 'GET':

		form.username.data = current_user.username

		form.about_me.data = current_user.about_me

	return render_template('edit_profile.html', title='Edit Profile', form=form)


@users.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):

	form = EmptyForm()

	if form.validate_on_submit():

		user = User.query.filter_by(username=username).first()

		if user is None:

			flash(_l('User %(username)s not found', username=username))

			return redirect(url_for('posts.view'))

		if user == current_user:

			flash(_('You can not follow yourself'))

			return redirect(url_for('posts.user', username=username))

		current_user.follow(user)

		db.session.commit()

		flash('You are following {}'.format(username))

		return redirect(url_for('posts.user', username=username))

	else:

		return redirect(url_for('posts.view'))


@users.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):

	form = EmptyForm()

	if form.validate_on_submit():


		user = User.query.filter_by(username=username).first()


		if user is None:

			flash('User {} not found'.format(username))

			return redirect(url_for('posts.view'))

		if user == current_user:

			flash(_l('You can not unfollow yourself'))

			return redirect(url_for('posts.user', username=username))


		current_user.unfollow(user)
		db.session.commit()

		flash(_l('You are not following %(username)s', username=username))

		return redirect(url_for('posts.user', username=username))

	else:

		return redirect(url_for('posts.view'))


@users.route('/explore')
@login_required
def explore():

	page = request.args.get('page', 1, type=int)

	posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

	next_url = None

	prev_url = None

	if posts.has_next:
		next_url = url_for('users.explore', page=posts.next_num)

	if posts.has_prev:
		prev_url = url_for('users.explore', page=posts.prev_num)

	return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)


