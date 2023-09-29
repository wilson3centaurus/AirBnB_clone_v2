from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def status():
    data = {
        "status": "OK"
    }
    response = jsonify(data)
    return response
