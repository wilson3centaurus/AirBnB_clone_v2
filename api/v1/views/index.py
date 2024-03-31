<<<<<<< HEAD
#!/usr/bin/python3

from . import app_views
from flask import jsonify


=======
from . import app_views
from flask import jsonify

>>>>>>> f75b135 (initial commit)
# Define a route /status on the object app_views
@app_views.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})
