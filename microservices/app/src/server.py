from src import app
import numpy as np
from keras.models import model_from_json
from flask import jsonify
import os


def load_model():
	print os.getcwd()
    global loaded_model1, loaded_model2, loaded_model3
    json_file = open('microservices/app/src/model1.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model1 = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model1.load_weights("microservices/app/src/model1.h5")

    json_file = open('microservices/app/src/model2.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model2 = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model2.load_weights("microservices/app/src/model2.h5")

    json_file = open('microservices/app/src/model3.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model3 = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model3.load_weights("microservices/app/src/model3.h5")


@app.route("/")
def home():
    return "Hasura Hello World"


@app.route("/predict", methods=["GET"])
def json_message():
    rdata = flask.request.args.to_dict()

    # conversion

    x_in = np.random.randn(1, 5)
    x_in[0][0] = 1
    x_in[0][1] = 3
    x_in[0][2] = 1
    x_in[0][3] = 4
    x_in[0][4] = 5

    pred1 = loaded_model1.predict(x_in)
    pred2 = loaded_model2.predict(x_in)
    pred3 = loaded_model3.predict(x_in)

    pred = (pred1 + pred2 + pred3) / 3

    i = iter(pred)
    pred_dict = {pred[0][i]: i for i in range(0, 85)}

    pred_dict = sorted(pred_dict.items())

    prefs = []

    for _, value in pred_dict:
        prefs.append(value)

    prefs.reverse()
    data = {}

    with open('CountryDB.txt') as f:
        cnt = 1
        line = f.readline()
        while line:
            data[cnt] = line.strip()
            line = f.readline()
            cnt += 1

    for i in range(num_queries):
        print(data[prefs[i]])

    return flask.jsonify(data)

load_model()
