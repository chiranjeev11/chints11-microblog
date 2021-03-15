from flask import Flask, request, current_app
from flask_cors import CORS
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging								# To send logs by mail.
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_mail import Mail
import os
from flask_babel import Babel




db = SQLAlchemy()

migrate = Migrate(db)

login = LoginManager()

login.login_view = 'users.login'					#login is the function name used for url_for


mail = Mail()

babel = Babel()

@babel.localeselector
def get_locale():

	#request object called accept_languages. This object provides a high-level interface to work with the Accept-Language header that clients send with a request.
	#To select the best language, you need to compare the list of languages requested by the client against the languages the application supports, and using the 
	#client provided weights, find the best language. The logic to do this is somewhat complicated, but it is all encapsulated in the best_match() method, which 
	#takes the list of languages offered by the application as an argument and returns the best choice.
	return request.accept_languages.best_match(current_app.config['LANGUAGES'])
	# return 'es'


def create_app(config_class=Config):

	app = Flask(__name__)
	app.config.from_object(config_class)

	CORS(app, resources = {'/':{'origins': '*'}})
	db.init_app(app)
	migrate.init_app(app, db)
	login.init_app(app)
	mail.init_app(app)
	babel.init_app(app)



	from app.users.routes import users		# import of the blueprint right above the app.register_blueprint() to avoid circular dependencies.
	app.register_blueprint(users)			# When a blueprint is registered, any view functions, templates, static files, error handlers, etc. are connected to the application.

	from app.posts.routes import posts
	app.register_blueprint(posts)

	from app.main.routes import main
	app.register_blueprint(main)

	if not app.debug and not app.testing:

		if app.config['MAIL_SERVER']:

			auth = None

			if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:

				auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

			secure = None

			if app.config['MAIL_USE_TLS']:

				secure = ()

			mail_handler = SMTPHandler(

				mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
				fromaddr = 'no-reply@' + app.config['MAIL_SERVER'],
				toaddrs = app.config['ADMINS'],
				subject = 'Microblog Failure',
				credentials = auth, secure = secure)

			mail_handler.setLevel(logging.ERROR)

			app.logger.addHandler(mail_handler)

		if not os.path.exists('logs'):

			os.mkdir('logs')

			# Rotate file ensures that log file do not grow too large.
			# log file size will be 10kb and for backup 10 log files will be there.
			file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)

			# format that includes the timestamp, the logging level, the message and the source file and line number from where the log entry originated.
			file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s in [in %(pathname)s : %(lineno)d]'))

			file_handler.setLevel(logging.INFO)

			app.logger.addHandler(file_handler)

			app.logger.setLevel(logging.INFO)

			app.logger.info('Microblog startup')

		if app.config['LOG_TO_STDOUT']:

			stream_handler = logging.StreamHandler()
			stream_handler.setlevel(logging.INFO)
			app.logger.addHandler(stream_handler)

		else:

			if not os.path.exists('logs'):

				os.mkdir('logs')
			file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
			file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s in [in %(pathname)s:%(lineno)d]'))
			file_handler.setLevel(logging.INFO)
			app.logger.addHandler(file_handler)

		app.logger.setLevel(logging.INFO)
		app.logger.info('Microblog startup')



	return app


