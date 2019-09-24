import os
import pickle
import logging
import torch

from PIL import Image
from io import BytesIO
from args import get_parser
from torchvision import transforms
from model import get_model
from utils.output_utils import prepare_output
from flask import Flask, request, jsonify, json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.warning("Working on %s" % os.getcwd())
logger.warning("The cwd contains: %s" % os.listdir(os.getcwd()))

# Input params
DATA_DIR = 'data/'
WORKING_DIR = 'src/'
ingrs_vocab = pickle.load(open(os.path.join(DATA_DIR, 'ingr_vocab.pkl'), 'rb'))
vocab = pickle.load(open(os.path.join(DATA_DIR, 'instr_vocab.pkl'), 'rb'))

ingr_vocab_size = len(ingrs_vocab)
instrs_vocab_size = len(vocab)
output_dim = instrs_vocab_size

# Model params
MODEL_PATH = os.path.join(DATA_DIR, 'modelbest.ckpt')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
map_loc = None if torch.cuda.is_available() else 'cpu'
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


def load_model():
    global model
    args = get_parser()
    args.maxseqlen = 15
    args.ingrs_only = False
    model = get_model(args, ingr_vocab_size, instrs_vocab_size)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=map_loc))
    model.to(device)
    model.eval()
    model.ingrs_only = False
    model.recipe_only = False
    logger.debug('Loaded model')


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
        logger.info('POST')
        if request.files.get("image"):
            logger.info('Image received')
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
                logger.debug('Recipe succesfully generated!')
                num_valid += 1
                # outs['title'], outs['ingrs'], outs['recipe']
                return outs
            else:
                logger.error('Recipe error!')
        else:
            raise TypeError("File must be a image.")

    return jsonify(data)


if __name__ == '__main__':
    load_model()
    app.run(host="0.0.0.0", port=3000, debug=True)
