from flask import Blueprint
from flask_login import current_user
from app import db
from datetime import datetime

main = Blueprint('main', __name__)


