import numpy as np
import pickle
import io
import logging

from PIL import Image
from io import BytesIO
from flask import Flask, request, jsonify, json

app = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@app.route('/')
def index():
    return 'Index'

# TODO
@app.route('/predict', methods=['POST'])
def predict_recipe():
    data = {"success": False}

    if request.method == "POST":
        data["success"] = True
        logging.info('POST')
        if request.files.get("image"):
            logging.info('Image')
            image = request.files["image"].read()
            image = Image.open(BytesIO(image))

    return jsonify(data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
