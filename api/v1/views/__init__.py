from .amenities import *
from .cities import *
from .states import *
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
