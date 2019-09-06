import numpy as np
import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return 'Index'

# TODO
@app.route('/predict', methods=['POST'])
def predict_receipt():
    data = request.get_json(force=True)
    return 'Predict'


if __name__ == '__main__':
    app.run(port=5000, debug=True)