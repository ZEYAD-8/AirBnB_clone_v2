#!/usr/bin/python3
"""
A script that starts a Flask web application
listening on 0.0.0.0, port 5000
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """Function that displays Hello HBNB!"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Function that displays HBNB"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def ctext(text):
    """Function that displays the letter c then the text"""
    return "C {}".format(text.replace("_", " "))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """Function that displays the word python then the text"""
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def n_number(n):
    """Function that displays n is a number only if n is an integer"""
    if isinstance(n, int):
        return "{} is a number".format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=None)
