import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you_will_never_guess'

	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://chiranjeev:chints11#@localhost:3306/blog_app'

	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_SERVER = 'smtp.googlemail.com' or os.environ.get('MAIL_SERVER')

	MAIL_PORT = int( 587 or os.environ.get('MAIL_PORT'))

	MAIL_USE_TLS = True

	MAIL_USERNAME = 'chiranjeevkhurana11@gmail.com' or os.environ.get('MAIL_USERNAME')

	MAIL_PASSWORD = 'Mamamimi0,' or os.environ.get('MAIL_PASSWORD')

	ADMINS = ['chiranjeevkhurana11@gmail.com', 'ankitkochar456@gmail.com', 'rnavbhardwaj@gmail.com']

	POSTS_PER_PAGE = 3

	LANGUAGES = ['en', 'es']