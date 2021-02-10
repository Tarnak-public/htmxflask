import os
import time
import traceback

import flask
import flask_sijax
from flask import request, render_template, g
from werkzeug.utils import secure_filename

import FRServiceConnector

gallery_name_krzys = 'krzys'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS_IMAGES = {'jpeg', 'jpg', 'png'}

path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

app = flask.Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 1024 * 1000
app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)


def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_IMAGES


def upload_directory(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)


def upload_static_directory(filename):
    return "static/uploads/" + filename


# @app.route('/', methods=['GET', 'POST'])
# @app.route('/index.html', methods=['GET', 'POST'])
@flask_sijax.route(app, '/')
@flask_sijax.route(app, '/index.html')
def index():
    def say_hi(obj_response):
        obj_response.alert('Hi there!')

    if g.sijax.is_sijax_request:
        # Sijax request detected - let Sijax handle it
        g.sijax.register_callback('say_hi', say_hi)
        return g.sijax.process_request()

    option_faces = FRServiceConnector.get_gallery_faces(gallery_name_krzys)
    main_page = render_template('index.html', gallery_options=option_faces)
    return main_page


@app.route('/loadImageToCompare', methods=['GET', 'POST'])
def pressed_load_image_to_compare():
    print("loadImageToCompare")
    return '', 204


@app.route('/galleryFaceSelected', methods=['GET', 'POST'])
def selected_gallery_item():
    print("galleryFaceSelected")
    face_guid = request.form['ComboboxKnownFaces']
    print("selected face: " + face_guid)
    file_path = FRServiceConnector.get_faces_image(gallery_name_krzys, face_guid)
    return '<img src="' + file_path + "?empty=" + str(time.time_ns()) + '" id="Image3" alt="" class="resize">'


@app.route('/galleryComboBox', methods=['GET', 'POST'])
def pressed_gallery_combobox():
    print("galleryComboBox")
    return '', 204


@app.route('/selectedImageForGallery', methods=['GET', 'POST'])
def pressed_file_selector_gallery():
    print("selectedImageForGallery: ", request.form['file'])
    file_path, filename = os.path.split(request.form['file'])
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
