import numpy as np
import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return 'Index'

# TODO
@app.route('/predict', methods=['POST'])
def predict_recipe():
    data = {"success": False}
    data = request.get_json(force=True)

    if request.method == "POST":
        pass

    return 'Predict recipe'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
