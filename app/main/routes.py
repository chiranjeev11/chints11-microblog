from flask import Blueprint
from app import db
from datetime import datetime

main = Blueprint('main', __name__)


@main.before_request
def before_request():

	if current_user.is_authenticated:

		current_user.last_seen = datetime.utcnow()

		db.session.commit()