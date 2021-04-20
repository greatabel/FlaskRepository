#!/usr/bin/python
# -- coding: utf-8 --
import cv2
import numpy as np
import base64

def basetoimg(base64_data):
    imgData = base64.b64decode(base64_data)
    nparr = np.fromiter(imgData, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img
