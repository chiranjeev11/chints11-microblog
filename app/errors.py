from flask import render_template
from app import db, app

@app.errorhandler(404)
def not_found_error(error):

	return render_template('404.html'), 404		# In view function status code is passed along with render_template.
												# By default 200 is passed and we pass 404 or 500 for for specifying the error.
@app.errorhandler(500)
def internal_error(error):

	db.session.rollback()

	return render_template('500.html'), 500