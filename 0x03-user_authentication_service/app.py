#!/usr/bin/env python3
"""App model
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    """GET /
        the home route
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
