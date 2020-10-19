from nsfw_detector import predict
import os, fcntl
import time
import shutil
import random

import requests
from flask import Flask,render_template,request
import base64

model = predict.load_model('/Imgfit/ImageReview-v3/nsfw_model/nsfw.299x299.h5')
img_root = './images'

def getRandomSet(bits):
    num_set = [chr(i) for i in range(48,58)]
    char_set = [chr(i) for i in range(97,123)]
    total_set = num_set + char_set
    value_set = "".join(random.sample(total_set, bits))
    return value_set

def predict_img(imgpath):
    name_rand = imgpath.split('/')[2].split('.')[0] + '.txt'
    print('outname',name_rand)
    try:
        print('start')
        time.sleep(float(random.randint(0,5)/10))
        res = predict.classify(model, imgpath)
        print(res) # save
        res2 = res[imgpath]
        return res2
    except:
        return None

app = Flask(__name__)

@app.route("/nsfw",methods = ['GET', 'POST'])
def nsfw():
    if request.method == "POST":
        try:
            imgbase64 = request.form.get('imgbase64')
            imgdata = base64.b64decode(imgbase64)
            randname = getRandomSet(15) + '.jpg'
            imgrandpath = os.path.join(img_root, randname)
            file = open(imgrandpath,'wb')
            file.write(imgdata)
            file.close()
            res = predict_img(imgrandpath)
            return res
        except:
            print('>>>nsfw error')
            return {'sign':-1}
    else:
        return "<h1>Updata faces, please use post!</h1>"

if __name__ == '__main__':
    host = '0.0.0.0'
    port = '8082'
    app.run(debug=True, host=host, port=port)
