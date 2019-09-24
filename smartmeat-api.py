import logging

from flask import Flask, request, jsonify, json, Response

app = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# TODO Data sync with web socket
on = True
sticks = {
    "stick1": {
        "active": True,
        "time_active": "12:45"
    },
    "stick2": {
        "active": True,
        "time_active": "10:10"
    },
    "stick3": {
        "active": False,
        "time_active": "00:00"
    },
    "stick4": {
        "active": False,
        "time_active": "00:00"
    }
}
temperature = 175


def sync_data():
    global on
    global sticks
    global temperature

    return on, sticks, temperature


def build_json():
    logger.debug('Building JSON')
    data = {}
    on, sticks, temperature = sync_data()
    data = {
        'on': on,
        'sticks': sticks,
        'temperature': temperature,
    }
    with app.app_context():
        result = jsonify(data)

        return result


@app.route('/get_info', methods=['GET'])
def get_info():
    data = build_json()
    return data


# @app.route('/get_temperature', methods=['GET'])
# def get_temperature():
#     data = build_json()
#     return data['temperature']


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
