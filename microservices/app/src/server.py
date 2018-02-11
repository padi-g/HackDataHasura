from src import app
import numpy as np
from keras.models import model_from_json
import flask
from flask import jsonify
import os


def load_model():
	print(os.getcwd())
	global loaded_model1,loaded_model2,loaded_model3
	json_file = open('src/model1.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model1 = model_from_json(loaded_model_json)
	# load weights into new model
	loaded_model1.load_weights("src/model1.h5")

	json_file = open('src/model2.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model2 = model_from_json(loaded_model_json)
	# load weights into new model
	loaded_model2.load_weights("src/model2.h5")

	json_file = open('src/model3.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model3 = model_from_json(loaded_model_json)
	# load weights into new model
	loaded_model3.load_weights("src/model3.h5")

def categorize(data):

	if data['age'] < '15':
		data['age'] = 1
	elif data['age']< '25':
		data['age'] = 2
	elif data['age'] < '35':
		data['age'] = 3
	elif data['age'] < '45':
		data['age'] = 4
	elif data['age'] < '55':
		data['age'] = 5
	elif data['age'] < '65':
		data['age'] = 6
	else:
		data['age'] = 7

	if data['sex'] == "male":
		data['sex'] = 0
	else :
		data['sex'] = 1

	if data['duration'] < '2':
		data['duration'] = 1
	elif data['duration'] < '3':
		data['duration'] = 2
	elif data['duration'] < '6':
		data['duration'] = 3
	elif data['duration'] < '10':
		data['duration'] = 4
	elif data['duration'] < '15':
		data['duration'] = 5
	else:
		data['duration'] = 6

	if data['budget'] < '50000':
		data['budget'] = 1
	elif data['budget'] < '200000':
		data['budget'] = 2
	elif data['budget'] < '500000':
		data['budget'] = 3
	elif data['budget'] < '2000000':
		data['budget'] = 4
	elif data['budget'] < '5000000':
		data['budget'] = 5
	else:
		data['budget'] = 6

@app.route("/")
def home():
    return "Hasura Hello World"


@app.route("/predict", methods=["GET"])
def json_message():
    rdata = flask.request.args.to_dict()
    print(rdata)
    categorize(rdata)
    # conversion

    x_in = np.random.randn(1,5)
    x_in[0][0]=rdata['quarter']
    x_in[0][1]=rdata['age']
    x_in[0][2]=rdata['sex']
    x_in[0][3]=rdata['duration']
    x_in[0][4]=rdata['budget']

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

    with open('src/CountryDB.txt') as f:
        cnt = 1
        line = f.readline()
        while line:
            data[cnt] = line.strip()
            line = f.readline()
            cnt += 1

    for i in range(5):
        print(data[prefs[i]])

    return flask.jsonify((data[prefs[2]],data[prefs[3]],data[prefs[4]]))

load_model()
