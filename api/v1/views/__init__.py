<<<<<<< HEAD
#!/usr/bin/python3

from . import index
from flask import Blueprint

from api.v1.views.index import app_views

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
=======
from flask import Blueprint

# Create a Blueprint instance with URL prefix /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import of everything in the package api.v1.views.index
from . import index
>>>>>>> f75b135 (initial commit)
