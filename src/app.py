from flask import Flask, jsonify, request
from users import users
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET'])
def ping():
    return jsonify({"response": "hello world"})

@app.route('/users')
def usersHandler():
    return jsonify({"users": users})

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['image']
        image = Image.open(file)
        image = np.array(image)
        ocr = PaddleOCR(use_angle_cls=True, lang='es')
        result = ocr.ocr(image, cls=True)
        full_text = ""
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                text = line[1][0]
                full_text += text + " "
        return jsonify({'message': 'Ok', 'status': True, 'data': full_text})
    except Exception as e:
        return jsonify({'message': 'Error', 'status': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
