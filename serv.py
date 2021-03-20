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
app = Flask(__name__)


def predict():
    return True


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method != 'POST':
        return

    data = request.json['img']
    buf_decode = base64.b64decode(data)

    if predict():
        return True
    else:
        return False


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
