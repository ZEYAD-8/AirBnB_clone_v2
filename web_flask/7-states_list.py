#!/usr/bin/python3
"""
A script that starts a Flask web application
listening on 0.0.0.0, port 5000
"""
from flask import Flask, render_template
from models.state import State
from models import storage

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def hbnb():
    """Function that displays all state objects sorted by name"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(self):
    """Function to remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
