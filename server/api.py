from io import BytesIO

import matplotlib.pyplot as plt
from flask import Flask, request, send_file
from flask_cors import CORS

from reflection_remover import ReflectionSuppressor

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Hi comp graphics!"


@app.route("/process_image", methods=["POST"])
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

    buf = BytesIO()
    plt.imsave(buf, result_img, format="png")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


if __name__ == "__main__":
    app.run(port=8000)
