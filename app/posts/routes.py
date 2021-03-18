from flask import render_template, flash, redirect, url_for, request, Blueprint, current_app
from app import db
from flask_login import current_user
from app.posts.forms import EmptyForm, PostForm
from app.models import User, Post
from flask_login import login_required
from guess_language import guess_language
from flask_babel import _
import time
from datetime import datetime


posts = Blueprint('posts', __name__)


# Home page
@posts.route('/', methods=['GET', 'POST'])
@posts.route('/index', methods=['GET', 'POST'])
@login_required
def view():

	page = request.args.get('page', 1, type=int)

	# If True, when an out of range page is requested a 404 error will be automatically returned to the client. If False, an empty list will be returned for out of range pages.
	post = current_user.followed_post().paginate(page, current_app.config['POSTS_PER_PAGE'], False)

	next_url = None
	
	prev_url = None

	if post.has_next:
		# Here page is query argument in the url
		next_url = url_for('posts.view', page=post.next_num)
	if post.has_prev:
		prev_url = url_for('posts.view', page=post.prev_num)

	return render_template('index.html',title='Home Page', posts=post.items, next_url=next_url, prev_url=prev_url)

def lastSeen(last):

	current = int(time.time())

	t = current-last

	active = 0

	if t<=4:

		message = 'Active'
		active = 1

	elif t/60<1:

		message = 'Active few seconds ago'

	elif t/3600<1:

		message = 'Active {}mins ago'.format(t//60)

	elif t/86400<1:

		message = 'Active {}h ago'.format(t//3600)

	elif t/604800<1:

		message = 'Active {} days ago'.format(t//86400)

	elif t/2592000<1:

		message = 'Active {} weeks ago'.format(t//604800)

	elif t/31104000<1:

		message = 'Active {} months ago'.format(t//259200)

	else:

		message = 'Active {} years ago'.format(t//31104000)
	
	return (message, active)


@posts.route('/user/<username>')
@login_required
def user(username):

	user = User.query.filter_by(username=username).first_or_404()


	if user.last_seen:

		last_seen, active = lastSeen(int(user.last_seen))
	else:
		last_seen, active = None, None

	form = EmptyForm()

	image_file = url_for('static', filename=f"profile_pics/{current_user.image_file}")


	page = request.args.get('page', 1, type=int)

	posts = user.post.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

	next_url = None

	prev_url = None

	if posts.has_next:
		next_url = url_for('posts.user', username=username, page=posts.next_num)

	if posts.has_prev:
		prev_url = url_for('posts.user', username=username, page=posts.prev_num)


	return render_template('user.html', user=user, form=form, posts=posts.items, next_url=next_url, prev_url=prev_url, image_file=image_file, last_seen=last_seen, active=active)


@posts.route('/post/new_post/', methods=['GET', 'POST'])
@login_required
def new_post():

	form = PostForm()

	if form.validate_on_submit():

		language = guess_language(form.post.data)

		if language == 'UNKNOWN' or len(language) > 5:

			language = ''

		post = Post(body=form.post.data, author=current_user, language=language)

		db.session.add(post)

		db.session.commit()

		flash(_('Your post is now live !'))

		return redirect(url_for('posts.view'))


	return render_template('create_post.html', form=form)


@posts.before_request
def before_request():

	if current_user.is_authenticated:

		current_user.last_seen = (int(time.time()))

		db.session.commit()