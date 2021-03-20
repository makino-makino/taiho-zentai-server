import os
import io
import time
import json
import numpy as np
import cv2
import base64
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
# from werkzeug import secure_filename
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from saas.input_client.service.input_client_pb2_grpc import InputClientStub
from saas.input_client.service.input_client_pb2 import NoParam, Tensor
from saas.model_client.service.model_client_pb2_grpc import ModelClientStub
from saas.model_client.service.model_client_pb2 import ModelInfo, ModelBinaryKeras
import grpc
from keras.preprocessing.image import img_to_array, load_img

import pickle

app = Flask(__name__)


def predict():
    host = "yahoo-hackathon-gateai-1.japaneast.cloudapp.azure.com"
    input_client_port = 5001

    channel_input_client = grpc.insecure_channel(
        f'{host}:{str(input_client_port)}', options=[])
    api_input_client = InputClientStub(channel_input_client)

    # call inpuot_client to generate keys
    print("call gen_key")
    # ここはうごく
    api_input_client.gen_key(NoParam())

    img = img_to_array(load_img('hoge.jpg', target_size=(50, 50)))

    img_nad = img_to_array(img)/255
    img_nad = img_nad[None, ...]
    client_test_data = img_nad

    data_for_cf = client_test_data.tolist()
    input_data = Tensor()
    input_data.data = pickle.dumps(data_for_cf)

    # call prediction
    # ここも止まる
    pred = api_input_client.predict(input_data)
    pred = pickle.loads(pred.data)

    result = np.argmax(pred[0])
    return bool(result)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method != 'POST':
        return

    data = request.json['img']
    buf_decode = base64.b64decode(data)

    with open('hoge.jpg', 'wb') as f:
        f.write(buf_decode)

    if predict():
        return 'true'
    else:
        return 'false'


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
