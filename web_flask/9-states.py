#!/usr/bin/python3
"""
A script that starts a Flask web application
listening on 0.0.0.0, port 5000
"""
from models import storage
from models.state import State
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/states/', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_list(id=None):
    """Function that displays all state objects sorted by name"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    arg = False
    found = None
    if id is not None:
        arg = True
        for state in states:
            if state.id == id:
                found = state

    return render_template("9-states.html",
                           states=states,
                           arg=arg,
                           found=found)


@app.teardown_appcontext
def teardown(self):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
