import os
import traceback

import flask
import jyserver.Flask as jsf
from flask import request, render_template
from werkzeug.utils import secure_filename

import FRServiceConnector

gallery_name_krzys = 'krzys'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS_IMAGES = {'jpeg', 'jpg', 'png'}

app = flask.Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 1024 * 1000


# https://dev.to/ftrias/access-js-dom-from-flask-app-using-jyserver-23h9
@jsf.use(app)
class App:

    @jsf.task
    def main(self):
        print("main() started")
        self.js.document.getElementById("count").innerHTML = 5
        pass

    def get_selected_face(self):
        self.js.document.getElementById("ImagesInGalleryCombobox")
        pass

    @jsf.task
    def update_preview_image(self, download_path):
        # self.js.document.getElementById("Image3").outerHTML = '<img src="' + download_path + '" id="Image3" alt="">'
        # self.js.document.getElementById( "Image3").innerHtml = '<img src="{{ url_for("static", filename="' + download_path + '") }}" id="Image3" alt="">'
        # self.js.document.getElementById("Image3").src = download_path
        # self.js.document.getElementById("OutputTextArea").value = "dupa"
        print("update_preview_image() started")
        self.js.document.getElementById("count").innerHTML = 10
        print("update_preview_image() finished")

    def faces_gallery(self, gallery_list):
        self.js.document.getElementById("ImagesInGalleryCombobox").innerHTML = '<option value="audi">Audi</option>'


def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_IMAGES


def upload_directory(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)


def update_preview_image_own():

    pass


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    App.main()

    option_faces = FRServiceConnector.get_gallery_faces(gallery_name_krzys)
    main_page = App.render(render_template('index.html', gallery_options=option_faces))
    # App.update_preview_image("")
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
    FRServiceConnector.get_faces_image(gallery_name_krzys, face_guid)
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
