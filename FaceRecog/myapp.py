import os
import traceback

import flask
from flask import request
from werkzeug.utils import secure_filename

# File extension checking
import FRServiceConnector

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS_IMAGES = {'jpeg', 'jpg', 'png'}

app = flask.Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 1024 * 1000


def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_IMAGES


def upload_directory(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)


@app.route('/')
@app.route('/index.html')
def index():
    FRServiceConnector.setup_api_server()
    return flask.render_template('index.html')


@app.route('/loadImageToCompare', methods=['GET', 'POST'])
def pressed_load_image_to_compare():
    print("loadImageToCompare")
    return '', 204


@app.route('/galleryComboBox', methods=['GET', 'POST'])
def pressed_gallery_combobox():
    print("galleryComboBox")
    return '', 204


@app.route('/selectedImageForGallery', methods=['GET', 'POST'])
def pressed_file_selector_gallery():
    print("selectedImageForGallery: ", request.form['file'])
    path, filename = os.path.split(request.form['file'])
    print("selectedImageForGallery: ", filename)
    return '<input class="form-control" type="text" readonly="" id="addToGalleryTextbox" value = "' + filename + '">'


@app.route('/submitAddToGallery', methods=['GET', 'POST'])
def pressed_submit_to_gallery():
    print("submitAddToGallery: ", request)
    if request.method == 'POST':
        try:
            filename = request.form['addToGalleryTextbox']  # search by name="" of dom element
            new_face_name = request.form['NewFaceNameEditbox']
        except KeyError:
            print(traceback.format_exc())
            print("skip submitAddToGallery as no parameters in form")
            return '', 204

        if new_face_name is None or filename is None:
            print("skip submitAddToGallery as one or more parameters are empty")
            return '', 204

        f = request.files['file']
        print("submitAddToGallery: fileName=", filename)
        print("submitAddToGallery: faceName=", new_face_name)
        f.save(upload_directory(secure_filename(f.filename)))

    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
