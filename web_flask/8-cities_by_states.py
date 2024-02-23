#!/usr/bin/python3
"""
A script that starts a Flask web application
listening on 0.0.0.0, port 5000
"""
from models import storage
from models.state import State
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Function that displays all state objects sorted by name"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    return render_template("7-states_list.html", states=states)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Displays an HTML page with a list of all states and related cities.

    States/cities are sorted by name.
    """
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    states_cities = []
    for state in states:
        states_cities.append([state,
                              sorted(state.cities, key=lambda k: k.name)])
    return render_template("8-cities_by_states.html", st_ci=states_cities)


@app.teardown_appcontext
def teardown(self):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
