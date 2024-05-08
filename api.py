from flask import Flask, request, send_file
import matplotlib.pyplot as plt

from io import BytesIO
from reflection_remover import ReflectionSuppressor
from data_store import DataStorage
from flask_cors import CORS



app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/process_image', methods=['POST'])
def process_image():
    # Check if the request has the file part
    if 'file' not in request.files:
        return "No file part in the request", 400
    file = request.files['file']
    print(file, request.form)
    if file.filename == '':
        return "No file selected for uploading", 400
    
    try:
        h = float(request.form.get('h', 0.03))  # Default h is 0.03 if not provided
    except ValueError:
        return "Invalid value for parameter 'h'", 400
    
    debug = request.form.get('debug', 'false').lower() == 'true'

    # Read the image file
    img = plt.imread(file) / 255  # Normalize the image into [0, 1]

    debug_writer = None
    if debug:
        debug_writer = DataStorage(directory="logs")

    frr = ReflectionSuppressor(h_param=h, storage=debug_writer)

    # Process the image to remove reflections
    result_img = frr.remove_reflections(img)

    # Save the processed image to a buffer
    buf = BytesIO()
    plt.imsave(buf, result_img, format='png')
    buf.seek(0)

    # Return the processed image
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='processed_image.png')


if __name__ == '__main__':
    app.run(port=8000, debug=True)
