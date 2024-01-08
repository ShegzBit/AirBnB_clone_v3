#!/usr/bin/python3
"""flask RESTful API definition for AirBnB clone
"""
import os
from flask import Flask, jsonify, make_response
from flask_cors import CORS

from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exception=None):
    """Remove the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def error_handler(err):
    """ Return 404 error response
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port)
