import logging

from flask import Flask, request, jsonify, json

app = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@app.route('/bbq-sticks', methods=['POST'])
def get_bbq_info():
    return 'BBQ INFO'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
