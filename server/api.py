from io import BytesIO

import matplotlib.pyplot as plt
import base64
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from reflection_remover import ReflectionSuppressor

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Hi comp graphics!"


@app.route("/upload", methods=["POST"])
def process_image():
    if "file" not in request.files:
        return "No file part in the request", 400
    
    file = request.files["file"]
    if file.filename == "":
        return "No file selected for uploading", 400

    try:
        h = float(request.form.get("h", 0.03))  # Default h is 0.03 if not provided
    except ValueError:
        return "Invalid value for parameter 'h'", 400

    # Read the image file
    img = plt.imread(file) / 255  # Normalize the image into [0, 1]

    # Remove Reflections
    reflection_remover = ReflectionSuppressor(h_param=h)
    result_img = reflection_remover.remove_reflections(img)

    # return base64 encoded image
    buf = BytesIO()
    plt.imsave(buf, result_img, format="png")
    buf.seek(0)
    # Encode the buffer to a Base64 string
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Return the Base64 string
    return jsonify({
        'message': 'Image processed successfully',
        'image': img_base64
    })


if __name__ == "__main__":
    PORT = os.environ.get('PORT', 4000)
    app.run(port=PORT)
