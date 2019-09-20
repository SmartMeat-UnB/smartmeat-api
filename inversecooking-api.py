import os
import numpy as np
import pickle
import logging
import torch
import torch.nn as nn

from PIL import Image
from io import BytesIO
from torchvision import transforms
from utils.output_utils import prepare_output
from flask import Flask, request, jsonify, json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Input params
DATA_DIR = ''
ingrs_vocab = pickle.load(open(os.path.join(DATA_DIR, 'ingr_vocab.pkl'), 'rb'))
vocab = pickle.load(open(os.path.join(DATA_DIR, 'instr_vocab.pkl'), 'rb'))

ingr_vocab_size = len(ingrs_vocab)
instrs_vocab_size = len(vocab)
output_dim = instrs_vocab_size

# Model params
MODEL_PATH = ''
device = None
greedy = [True, False, False, False]
beam = [-1, -1, -1, -1]
temperature = 1.0
numgens = len(greedy)
model = None

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_model(model_path):
    global model


def preprocess_image(image):

    transf_list_batch = []
    transf_list_batch.append(transforms.ToTensor())
    transf_list_batch.append(transforms.Normalize((0.485, 0.456, 0.406),
                                                  (0.229, 0.224, 0.225)))
    to_input_transf = transforms.Compose(transf_list_batch)

    transf_list = []
    transf_list.append(transforms.Resize(256))
    transf_list.append(transforms.CenterCrop(224))
    transform = transforms.Compose(transf_list)

    image_transf = transform(image)
    image_tensor = to_input_transf(image_transf).unsqueeze(0).to(device)

    return image_tensor


@app.route('/predict', methods=['POST'])
def predict_recipe():
    data = {"success": False}

    if request.method == "POST":
        logging.info('POST')
        if request.files.get("image"):
            logging.info('Image received')
            image = request.files["image"].read()
            image = Image.open(BytesIO(image))

            image_tensor = preprocess_image(image)

        num_valid = 1
        for i in range(numgens):
            with torch.no_grad():
                outputs = model.sample(image_tensor, greedy=greedy[i],
                                       temperature=temperature, beam=beam[i],
                                       true_ingrs=None)
            ingr_ids = outputs['ingr_ids'].cpu().numpy()
            recipe_ids = outputs['recipe_ids'].cpu().numpy()

            outs, valid = prepare_output(recipe_ids[0], ingr_ids[0],
                                         ingrs_vocab, vocab)

            if valid['is_valid']:
                logging.debug('Recipe succesfully generated!')
                num_valid += 1
                # outs['title'], outs['ingrs'], outs['recipe']
                return outs
            else:
                logging.error('Recipe error!')
        else:
            raise TypeError("File must be a image.")

    return jsonify(data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
