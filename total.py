import os
import io
import time
import json
import numpy as np
import cv2
import base64
import hashlib
import glob

import keras
from keras.models import load_model
import numpy as np
import grpc
from keras.preprocessing.image import img_to_array, load_img
import pickle
from keras.utils import to_categorical, np_utils

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

from saas.input_client.service.input_client_pb2_grpc import InputClientStub
from saas.input_client.service.input_client_pb2 import NoParam, Tensor
from saas.model_client.service.model_client_pb2_grpc import ModelClientStub
from saas.model_client.service.model_client_pb2 import ModelInfo, ModelBinaryKeras

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
# from werkzeug import secure_filename
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method != 'POST':
        return

    data = request.json['img']
    ido = request.json['ido']
    keido = request.json['keido']

    buf_decode = base64.b64decode(data)
    md5 = hashlib.md5(buf_decode).hexdigest()

    filename = f'{ido}-{keido}-{md5}.jpg'
    with open(filename, 'wb') as f:
        f.write(buf_decode)

    return 'true'


def setup():
    host = "yahoo-hackathon-gateai-1.japaneast.cloudapp.azure.com"
    model_client_port = 5002

    model_file = './data/model/model.h5'

    model = load_model(model_file)

    channel_model_client = grpc.insecure_channel(
        f'{host}:{str(model_client_port)}', options=[])
    api_model_client = ModelClientStub(channel_model_client)

    # モデルのアップロード+暗号化
    # サーバが落ちてる？
    # call model_client to upload h5 file from modelfiles/h5/{model_name}.h5
    print("call load_and_compile_model_from_local_h5")
    model_info = ModelBinaryKeras()
    model_info.config = pickle.dumps(model.get_config())
    model_info.weights = pickle.dumps(model.get_weights())
    model_info.type_info = 'sequential'
    model_info.intermediate_output = 'none'
    # ここで止まる
    api_model_client.compile_model_from_binary_keras(model_info)


if __name__ == "__main__":
    # setup()

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
