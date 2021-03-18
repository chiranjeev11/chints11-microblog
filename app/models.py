from flask import current_app
from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import time
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from datetime import datetime

# This is auxiliary table  that has no data other than the foreign keys.
followers = db.Table('followers', 
				db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
				db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))

class User(UserMixin, db.Model):

	id = db.Column(db.Integer, primary_key = True)

	username = db.Column(db.String(64), index = True, unique = True)		# index speeds up the query performance

	email = db.Column(db.String(120), index = True, unique = True)

	password_hash = db.Column(db.String(128))

	# any post.author spcifies the user who's post is. A mode of dynamic sets up the query to not run until specifically requested
	post = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')

	about_me = db.Column(db.String(140))

	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

	last_seen = db.Column(db.Integer, default=int(time.time()))

	# secondary specifies association table.
	# primaryjoin specifies left side entity ie. follower_id.
	# secondaryjoin specifies right side entity ie. followed_id.
	followed = db.relationship('User', secondary=followers,
								primaryjoin=(followers.c.follower_id == id),
								secondaryjoin=(followers.c.followed_id == id),
								backref=db.backref('followers',lazy='dynamic'), lazy='dynamic')

	def __repr__(self):

		return '<User {}>'.format(self.username)

	def set_password(self, password):

		self.password_hash = generate_password_hash(password)

	def check_password(self, password):

		return check_password_hash(self.password_hash, password)

	def avatar(self, size):

		digest = md5(self.email.lower().encode('utf-8')).hexdigest()


		x='https://www.gravtar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

		return x

	def follow(self, user):

		if not self.is_following(user):

			self.followed.append(user)


	def unfollow(self, user):

		if self.is_following(user):

			self.followed.remove(user)

	def is_following(self, user):		

		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def followed_post(self):

		followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

		own = Post.query.filter(Post.user_id == self.id)

		return followed.union(own).order_by(Post.timestamp.desc())

	def get_reset_token(self):

		s = Serializer(current_app.config['SECRET_KEY'], 1800)

		token = s.dumps({'user_id': self.id}).decode('utf-8')

		return token

	@staticmethod
	def verify_token(token):

		s = Serializer(current_app.config['SECRET_KEY'], 1800)

		try:

			user_id = s.loads(token)['user_id']

		except:

			return None

		return User.query.get(user_id)



class Post(db.Model):

	id = db.Column(db.Integer, primary_key = True)

	body = db.Column(db.String(140))

	timestamp = db.Column(db.DateTime, 	index=True, default=datetime.utcnow)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	language = db.Column(db.String(5))


	def __repr__(self):

		return '<Post {}>'.format(self.body)


#To load user sesion from database
@login.user_loader
def load_user(id):

	return User.query.get(int(id))