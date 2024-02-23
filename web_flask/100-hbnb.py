#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /hbnb: HBnB home page.
"""
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def hbnb_filters():
    """Displays the main HBnB filters HTML page."""
    states = storage.all(State)
    amenities = storage.all(Amenity)
    cities = storage.all(City)
    places = storage.all(Place)

    return render_template("100-hbnb.html",
                           states=states,
                           cities=cities,
                           places=places,
                           amenities=amenities)


@app.teardown_appcontext
def teardown(self):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
