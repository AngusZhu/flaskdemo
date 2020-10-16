# coding=utf-8
import face_recognition
import re
import base64
import json
from flask import Flask, render_template
from flask import request
from io import BytesIO



app = Flask(__name__)

def read_file_from_base64(base64img):
    base64_data = re.sub('^data:image/.+;base64,', '', base64img)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    return image_data

@app.route('/', methods=['get'])
def lambda_handler():
    return render_template('upload.html')


@app.route('/upload', methods=['post'])
def upload():
    files = request.form.get('data')  # 获取上传的文件
    filejson = json.loads(files)
    pic1 = filejson["first"]
    pic2 = filejson['second']

    file1 = read_file_from_base64(pic1)
    file2 = read_file_from_base64(pic2)

    # # 加载图片
    img1 = face_recognition.load_image_file(file1)
    img2 = face_recognition.load_image_file(file2)

    pic1_face_encoding = face_recognition.face_encodings(img1)[0]
    pic2_face_encoding = face_recognition.face_encodings(img2)[0]
    known_encodings = [
       pic1_face_encoding
    ]

    face_distances = face_recognition.face_distance(known_encodings, pic2_face_encoding)
    for i, face_distance in enumerate(face_distances):
        result1 ="-差距值为普通的 0.6, 他们为同一人的对比结果是： {}".format(face_distance < 0.6)
        result2 ="-更严格的差距设置为0.5 ,  他们为同一人的对比结果是：{}".format(face_distance < 0.5)
        print(result1)
        print(result2)

    resultdata = {"result1": result1, "result2": result2}
    resp = {"data": resultdata}
    return resp


if __name__ == "__main__":
    app.run()
