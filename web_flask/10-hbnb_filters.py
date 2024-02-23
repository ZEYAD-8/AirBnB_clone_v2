#!/usr/bin/python3
"""
A script that starts a Flask web application
listening on 0.0.0.0, port 5000
"""
from models import storage
from models.state import State
from models.amenity import Amenity
from flask import Flask, render_template

app = Flask(__name__)



@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters(id=None):
    """"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)

    amenities = storage.all(Amenity).values()
    amenities = states = sorted(amenities, key=lambda k: k.name)

    return render_template("10-hbnb_filters.html", states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(self):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
